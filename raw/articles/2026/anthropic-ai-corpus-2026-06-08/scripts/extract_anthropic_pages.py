#!/usr/bin/env python3
"""Extract clean Anthropic research/learn text into an AI-agent-readable corpus."""
import dataclasses
import datetime as dt
import hashlib
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path('/Users/roshansilva/.hermes/knowledge-base/raw/articles/2026/anthropic-ai-corpus-2026-06-08')
SITEMAP = 'https://www.anthropic.com/sitemap.xml'
UA = 'Mozilla/5.0 (Hermes Anthropic AI corpus extractor; research use)'
NOW = dt.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'

AI_INCLUDE = re.compile(r"\b(ai|artificial intelligence|llm|large language|language model|claude|model|models|machine learning|deep learning|neural|transformer|alignment|interpretability|mechanistic|circuit|safety|eval|evaluation|benchmark|red[- ]?team|jailbreak|agent|agentic|tool use|computer use|coding|code|software|cyber|reasoning|constitutional|pretraining|training|fine[- ]?tuning|rlhf|rl|scaling|token|context|prompt|math|mathematical|automated|assistant|capability|capabilities|privacy|frontier|compute|inference|steering|persona|representation|feature|activation|monosemanticity|sparse autoencoder|sae|classifier|policy)\b", re.I)
EXCLUDE_PRIMARY = re.compile(r"\b(economic index|economics|economy|labor|labour|workers|workforce|jobs?|biology|biosecurity|biorisk|chemical|radiological|nuclear|election|policy memo)\b", re.I)
KEEP_IF_DIRECT_AI = re.compile(r"\b(model|claude|ai|llm|alignment|safety|eval|agent|automated|cyber|compute|frontier)\b", re.I)

@dataclasses.dataclass
class Page:
    url: str
    lastmod: str
    path: str
    section: str
    title: str = ''
    description: str = ''
    canonical: str = ''
    text: str = ''
    links: List[Dict[str, str]] = dataclasses.field(default_factory=list)
    status_code: int = 0
    sha256: str = ''
    included: bool = True
    include_reason: str = ''


def slugify(url: str) -> str:
    path = urlparse(url).path.strip('/') or 'index'
    s = re.sub(r'[^A-Za-z0-9]+', '-', path).strip('-').lower()
    return s[:140] or 'index'


def fetch(url: str) -> Tuple[int, str, str]:
    r = requests.get(url, headers={'User-Agent': UA}, timeout=60, allow_redirects=True)
    ctype = r.headers.get('content-type', '')
    return r.status_code, ctype, r.text


def clean_lines(root) -> List[str]:
    for bad in root(['script','style','noscript','svg','nav','footer','header','form','button']):
        bad.decompose()
    lines=[]
    prev=None
    for raw in root.get_text('\n', strip=True).splitlines():
        line = re.sub(r'\s+', ' ', raw).strip()
        if not line:
            continue
        # trim cookie/nav cruft if it survived
        if line in {'English', '日本語', 'All', 'Research', 'News', 'Careers', 'Product'}:
            continue
        if line != prev:
            lines.append(line)
            prev=line
    return lines


def extract(url: str, lastmod: str, section: str) -> Page:
    path = urlparse(url).path
    p = Page(url=url, lastmod=lastmod, path=path, section=section)
    try:
        status, ctype, html = fetch(url)
        p.status_code = status
        p.sha256 = hashlib.sha256(html.encode('utf-8', 'replace')).hexdigest()
        if status != 200 or 'html' not in ctype:
            p.text = f'[fetch status {status}; content-type {ctype}]'
            return p
        soup = BeautifulSoup(html, 'lxml')
        p.title = soup.title.get_text(' ', strip=True) if soup.title else ''
        meta = soup.find('meta', attrs={'name':'description'}) or soup.find('meta', property='og:description')
        p.description = meta.get('content','').strip() if meta else ''
        can = soup.find('link', rel='canonical')
        p.canonical = urljoin(url, can.get('href','')) if can else url
        main = soup.find('main') or soup.body or soup
        # collect links before removal of nested text
        seen=set(); links=[]
        for a in main.find_all('a', href=True):
            text = re.sub(r'\s+', ' ', a.get_text(' ', strip=True)).strip()
            href = urljoin(url, a['href'])
            if not text and href:
                text = href
            key=(text, href)
            if href and key not in seen:
                seen.add(key); links.append({'text': text, 'url': href})
        p.links=links
        lines = clean_lines(main)
        p.text='\n'.join(lines)
        return p
    except Exception as e:
        p.status_code = -1
        p.text = f'[extract error: {type(e).__name__}: {e}]'
        return p


def get_sitemap_urls() -> List[Dict[str,str]]:
    status, ctype, xml = fetch(SITEMAP)
    if status != 200:
        raise RuntimeError(f'sitemap fetch failed: {status}')
    root=ET.fromstring(xml.encode('utf-8'))
    ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    rows=[]
    for u in root.findall('sm:url', ns):
        loc=u.findtext('sm:loc', default='', namespaces=ns)
        last=u.findtext('sm:lastmod', default='', namespaces=ns)
        if loc:
            rows.append({'url':loc,'lastmod':last,'path':urlparse(loc).path})
    return rows


def decide_research(page: Page) -> Tuple[bool, str]:
    hay = ' '.join([page.path, page.title, page.description, page.text[:4000]])
    if page.path.rstrip('/') == '/research':
        return True, 'research index page'
    inc = bool(AI_INCLUDE.search(hay))
    exc = bool(EXCLUDE_PRIMARY.search(hay))
    if inc and not exc:
        return True, 'matches AI/LLM/ML/CS topic keywords'
    if inc and exc and KEEP_IF_DIRECT_AI.search(hay):
        # Keep AI-policy/safety pages if AI is explicit, but exclude obvious economics reports below.
        lower = hay.lower()
        if 'economic index' in lower or 'economics' in page.path.lower() or 'economics' in page.title.lower():
            return False, 'excluded: primarily economics/labor-market page'
        if any(x in lower for x in ['biosecurity', 'biology', 'biorisk']) and not any(x in lower for x in ['model organism', 'model organisms']):
            return False, 'excluded: primarily biology/biosecurity/non-CS science page'
        return True, 'kept despite broad exclusion keyword because it directly concerns AI models/safety'
    if not inc:
        return False, 'excluded: no strong AI/LLM/ML/CS signal in title/description/main text'
    return False, 'excluded by scope filter'


def write_page(page: Page, out_dir: Path):
    fname = slugify(page.url) + '.md'
    fm = {
        'title': page.title,
        'source_url': page.url,
        'canonical_url': page.canonical or page.url,
        'lastmod': page.lastmod,
        'captured_at': NOW,
        'section': page.section,
        'source_kind': 'anthropic_web_page',
        'extraction_method': 'sitemap_requests_bs4_main_text',
        'status_code': page.status_code,
        'sha256_html': page.sha256,
        'include_reason': page.include_reason,
    }
    y=[]
    for k,v in fm.items():
        v = '' if v is None else str(v).replace('"','\\"')
        y.append(f'{k}: "{v}"')
    links = '\n'.join([f'- [{l["text"]}]({l["url"]})' for l in page.links]) or '- None extracted'
    body = f"---\n" + '\n'.join(y) + f"\n---\n\n# {page.title or page.url}\n\nSource: {page.url}\n\n## Description\n\n{page.description or 'No meta description extracted.'}\n\n## Clean Text\n\n{page.text}\n\n## Main Links\n\n{links}\n"
    (out_dir/fname).write_text(body, encoding='utf-8')
    return fname


def main():
    (ROOT/'research/pages').mkdir(parents=True, exist_ok=True)
    (ROOT/'learn/pages').mkdir(parents=True, exist_ok=True)
    (ROOT/'manifests').mkdir(parents=True, exist_ok=True)
    rows=get_sitemap_urls()
    (ROOT/'manifests/sitemap-all.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
    research_rows=[r for r in rows if r['path'].rstrip('/') == '/research' or r['path'].startswith('/research/')]
    learn_rows=[r for r in rows if r['path'].rstrip('/') == '/learn' or r['path'].startswith('/learn/')]

    research_manifest=[]; excluded=[]
    for i,r in enumerate(research_rows,1):
        p=extract(r['url'], r['lastmod'], 'research')
        include, reason = decide_research(p)
        p.included=include; p.include_reason=reason
        rec=dataclasses.asdict(p)
        rec['file']=None
        if include:
            rec['file']=write_page(p, ROOT/'research/pages')
            research_manifest.append(rec)
        else:
            excluded.append(rec)
        time.sleep(0.12)
        if i % 20 == 0:
            print(f'research {i}/{len(research_rows)}', flush=True)

    learn_manifest=[]
    discovered_learn_links=set()
    for r in learn_rows:
        p=extract(r['url'], r['lastmod'], 'learn')
        p.include_reason='sitemap /learn page'
        rec=dataclasses.asdict(p)
        rec['file']=write_page(p, ROOT/'learn/pages')
        learn_manifest.append(rec)
        for l in p.links:
            href=l['url']
            parsed=urlparse(href)
            if parsed.netloc.endswith('anthropic.com') and (parsed.path.rstrip('/') == '/learn' or parsed.path.startswith('/learn/')):
                discovered_learn_links.add(href.split('#')[0])
        time.sleep(0.12)

    # Cross-check whether in-page /learn links are missing from sitemap.
    sitemap_learn={r['url'].rstrip('/') for r in learn_rows}
    missing_learn=sorted(u for u in discovered_learn_links if u.rstrip('/') not in sitemap_learn)

    manifest={
        'corpus': 'anthropic-ai-corpus-2026-06-08',
        'captured_at': NOW,
        'sitemap_url': SITEMAP,
        'sitemap_total_urls': len(rows),
        'research_sitemap_urls': len(research_rows),
        'research_included_pages': len(research_manifest),
        'research_excluded_pages': len(excluded),
        'learn_sitemap_urls': len(learn_rows),
        'learn_pages': len(learn_manifest),
        'missing_learn_links_from_sitemap': missing_learn,
        'scope_filter': 'include AI/LLM/ML/deep-learning/math/CS/alignment/safety/interpretability/agents/evals/coding; exclude primarily economics/biology/non-CS science unless directly model/safety relevant',
    }
    (ROOT/'manifests/anthropic-web-summary.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    (ROOT/'manifests/research-pages.json').write_text(json.dumps(research_manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    (ROOT/'manifests/research-excluded.json').write_text(json.dumps(excluded, indent=2, ensure_ascii=False), encoding='utf-8')
    (ROOT/'manifests/learn-pages.json').write_text(json.dumps(learn_manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(manifest, indent=2))

if __name__ == '__main__':
    main()

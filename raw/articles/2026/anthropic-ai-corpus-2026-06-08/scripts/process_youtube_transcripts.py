#!/usr/bin/env python3
"""Convert downloaded YouTube VTT captions into clean Markdown transcripts and manifests."""
import datetime as dt
import html
import json
import re
from pathlib import Path

ROOT=Path('/Users/roshansilva/.hermes/knowledge-base/raw/articles/2026/anthropic-ai-corpus-2026-06-08')
CAPTURED_AT=dt.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
RAW=ROOT/'youtube/raw'
OUT=ROOT/'youtube/transcripts'
OUT.mkdir(parents=True, exist_ok=True)
MAN=ROOT/'manifests'

TAG_RE=re.compile(r'<[^>]+>')
TS_RE=re.compile(r'^(\d\d:)?\d\d:\d\d\.\d\d\d\s+-->\s+(\d\d:)?\d\d:\d\d\.\d\d\d')

def clean_caption_line(line):
    line=line.strip()
    if not line or line.startswith(('WEBVTT','Kind:','Language:','NOTE')):
        return ''
    if TS_RE.match(line): return ''
    if re.match(r'^\d+$', line): return ''
    line=TAG_RE.sub('', line)
    line=html.unescape(line)
    line=re.sub(r'\s+', ' ', line).strip()
    return line

def vtt_to_text(path):
    lines=[]; prev=None
    for raw in path.read_text(errors='replace').splitlines():
        line=clean_caption_line(raw)
        if not line: continue
        # auto captions often repeat adjacent fragments; collapse exact repeats.
        if line == prev: continue
        lines.append(line); prev=line
    # Build paragraph-ish text while retaining line boundaries enough for search.
    return '\n'.join(lines)

def slug(title, vid):
    s=re.sub(r'[^A-Za-z0-9]+','-', title or vid).strip('-').lower()
    return (s[:90]+'-'+vid+'.md') if s else vid+'.md'

def yaml_scalar(val):
    return str(val if val is not None else '').replace('\r', ' ').replace('\n', ' ').replace('"', '\\"')

videos=[]
for line in (ROOT/'youtube/video_ids_unique.tsv').read_text().splitlines():
    vid,tab,title,url=line.split('\t',3)
    videos.append({'id':vid,'tab':tab,'title':title,'url':url})

manifest=[]
for v in videos:
    d=RAW/v['id']
    info_files=sorted(d.glob('*.info.json')) if d.exists() else []
    info={}
    if info_files:
        try: info=json.loads(info_files[0].read_text(errors='replace'))
        except Exception: info={}
    vtts=sorted(d.glob('*.vtt')) if d.exists() else []
    # Prefer manual English if present, then canonical English, then largest English-ish file.
    def score(p):
        name=p.name
        pri=0
        if '.en.vtt' in name: pri+=100
        if '.en-orig.vtt' in name: pri+=90
        if '.en-' in name or '.en.' in name: pri+=50
        return (pri, p.stat().st_size)
    chosen=max(vtts, key=score) if vtts else None
    text=vtt_to_text(chosen) if chosen else ''
    out_file=None
    if text:
        out_file=slug(v['title'], v['id'])
        meta={
            'title': v['title'], 'video_id': v['id'], 'source_url': v['url'], 'channel_url': 'https://www.youtube.com/@claude',
            'tab': v['tab'], 'captured_at': CAPTURED_AT, 'source_kind': 'youtube_transcript',
            'extraction_method': 'yt-dlp English subtitles/auto-subtitles converted from VTT',
            'chosen_caption_file': str(chosen.relative_to(ROOT)),
            'upload_date': info.get('upload_date',''), 'duration': info.get('duration_string') or info.get('duration') or '',
            'view_count': info.get('view_count',''), 'description': (info.get('description') or '')[:1000],
        }
        y='\n'.join(f'{k}: "{yaml_scalar(val)}"' for k,val in meta.items())
        body=f'---\n{y}\n---\n\n# {v["title"]}\n\nSource: {v["url"]}\n\n## Transcript\n\n{text}\n'
        (OUT/out_file).write_text(body)
    manifest.append({
        **v,
        'info_json': str(info_files[0].relative_to(ROOT)) if info_files else None,
        'caption_files': [str(p.relative_to(ROOT)) for p in vtts],
        'chosen_caption_file': str(chosen.relative_to(ROOT)) if chosen else None,
        'transcript_file': f'youtube/transcripts/{out_file}' if out_file else None,
        'transcript_chars': len(text),
        'transcript_lines': text.count('\n')+1 if text else 0,
        'upload_date': info.get('upload_date',''),
        'duration': info.get('duration_string') or info.get('duration') or '',
    })

summary={
    'channel_url':'https://www.youtube.com/@claude',
    'captured_at': CAPTURED_AT,
    'enumerated_videos': len(videos),
    'videos_with_caption_files': sum(1 for r in manifest if r['caption_files']),
    'videos_with_clean_transcripts': sum(1 for r in manifest if r['transcript_file']),
    'videos_without_transcripts': [r for r in manifest if not r['transcript_file']],
}
(MAN/'youtube-transcripts.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
(MAN/'youtube-summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
print(json.dumps({k:(len(v) if k=='videos_without_transcripts' else v) for k,v in summary.items()},indent=2))

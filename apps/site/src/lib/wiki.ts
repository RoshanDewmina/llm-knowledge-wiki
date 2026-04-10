import "server-only";

import { promises as fs } from "node:fs";
import path from "node:path";
import { cache } from "react";
import matter from "gray-matter";

export type Frontmatter = Record<string, unknown>;

export interface Heading {
  depth: number;
  text: string;
  id: string;
}

export interface LinkItem {
  href: string;
  label: string;
  meta?: string;
}

export interface PreviewItem extends LinkItem {
  excerpt: string;
  type: string;
  updated?: string;
  sourcePath?: string;
}

export interface SidebarSection {
  title: string;
  items: LinkItem[];
}

export interface RailSection {
  title: string;
  items: LinkItem[];
}

export interface WikiPage {
  title: string;
  type: string;
  target: string;
  href: string;
  relativePath: string;
  section: string;
  frontmatter: Frontmatter;
  markdown: string;
  renderedMarkdown: string;
  headings: Heading[];
  excerpt: string;
  outboundTargets: string[];
  sourcePath?: string;
  sourceUrl?: string;
}

export interface RawDocument {
  title: string;
  relativePath: string;
  frontmatter: Frontmatter;
  markdown: string;
  headings: Heading[];
  excerpt: string;
  sourceUrl?: string;
  sourceDomain?: string;
}

export interface SearchResult {
  page: WikiPage;
  score: number;
  snippet: string;
}

export interface SearchOptions {
  limit?: number;
  type?: string;
  section?: string;
  status?: string;
  minConfidence?: number;
  includeSpecial?: boolean;
}

export interface SectionDirectory {
  section: string;
  title: string;
  description: string;
  pages: PreviewItem[];
}

interface WikiGraph {
  pages: WikiPage[];
  byTarget: Map<string, WikiPage>;
  backlinks: Map<string, WikiPage[]>;
  bySection: Map<string, WikiPage[]>;
  rawToSourcePage: Map<string, WikiPage>;
}

interface ManifestPageRecord {
  title: string;
  type: string;
  target: string;
  relative_path: string;
  section: string;
  frontmatter: Frontmatter;
  markdown: string;
  headings: Heading[];
  excerpt: string;
  outbound_targets: string[];
  source_path?: string | null;
  source_url?: string | null;
}

interface ManifestRawDocumentRecord {
  title: string;
  relative_path: string;
  frontmatter: Frontmatter;
  markdown: string;
  headings: Heading[];
  excerpt: string;
  source_url?: string | null;
  source_domain?: string | null;
}

interface ManifestPayload {
  generated_at: string;
  pages: ManifestPageRecord[];
  raw_documents: ManifestRawDocumentRecord[];
}

const REPO_ROOT = path.resolve(process.cwd(), "../..");
const WIKI_ROOT = path.join(REPO_ROOT, "wiki");
const RAW_ROOT = path.join(REPO_ROOT, "raw");
const MANIFEST_PATH = path.join(WIKI_ROOT, ".cache", "site-manifest.json");
const CONTENT_SECTIONS = [
  "sources",
  "concepts",
  "entities",
  "benchmarks",
  "projects",
  "syntheses",
  "outputs",
  "reviews",
] as const;
const CONTENT_SECTION_SET = new Set<string>(CONTENT_SECTIONS);
const SPECIAL_PAGES = new Set(["index", "inbox", "log"]);

function withPosixSeparators(value: string): string {
  return value.split(path.sep).join("/");
}

function safeResolve(root: string, ...segments: string[]): string {
  const resolved = path.resolve(root, ...segments);
  if (resolved !== root && !resolved.startsWith(`${root}${path.sep}`)) {
    throw new Error(`Path escapes root: ${segments.join("/")}`);
  }
  return resolved;
}

async function exists(filePath: string): Promise<boolean> {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function collectMarkdownFiles(root: string): Promise<string[]> {
  const entries = await fs.readdir(root, { withFileTypes: true });
  const files = await Promise.all(
    entries.map(async (entry) => {
      const absolutePath = path.join(root, entry.name);
      if (entry.isDirectory()) {
        return collectMarkdownFiles(absolutePath);
      }
      if (entry.isFile() && entry.name.endsWith(".md")) {
        return [absolutePath];
      }
      return [];
    }),
  );
  return files.flat();
}

export function slugifyHeading(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[`*_~]/g, "")
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-");
}

function stripMarkdownSyntax(markdown: string): string {
  return markdown
    .replace(/^---[\s\S]*?---\s*/m, "")
    .replace(/\[\[([^\]]+)\]\]/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[`*_>#-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function extractTitle(markdown: string, fallback: string): string {
  const match = markdown.match(/^#\s+(.+)$/m);
  return match ? match[1].trim() : fallback;
}

function removeLeadingTitle(markdown: string, title: string): string {
  const normalizedTitle = title.trim().toLowerCase();
  const match = markdown.match(/^#\s+(.+)\n+/);
  if (!match) {
    return markdown.trim();
  }

  if (match[1].trim().toLowerCase() !== normalizedTitle) {
    return markdown.trim();
  }

  return markdown.slice(match[0].length).trim();
}

function extractHeadings(markdown: string): Heading[] {
  return markdown
    .split("\n")
    .map((line) => line.match(/^(#{2,4})\s+(.+)$/))
    .filter((match): match is RegExpMatchArray => Boolean(match))
    .map((match) => ({
      depth: match[1].length,
      text: match[2].trim(),
      id: slugifyHeading(match[2]),
    }));
}

function extractExcerpt(markdown: string): string {
  const lines = markdown
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#") && !line.startsWith("<!--"));
  return stripMarkdownSyntax(lines[0] ?? "");
}

function normalizeWikiTarget(target: string): string {
  const cleaned = target.trim().replace(/^\/+/, "").replace(/^wiki\//, "").replace(/\.md$/, "");
  if (!cleaned || cleaned === "index") {
    return "index";
  }
  return withPosixSeparators(cleaned);
}

function targetToHref(target: string, anchor?: string): string {
  const base = target === "index" ? "/" : `/${target}`;
  return anchor ? `${base}#${slugifyHeading(anchor)}` : base;
}

export function rawPathToHref(rawPath: string): string {
  return `/raw/${rawPath.replace(/^raw\//, "")}`;
}

function parseWikiLink(rawLink: string): { target: string; href: string; label: string } {
  const [targetLabel, explicitLabel] = rawLink.split("|");
  const [targetPath, anchor] = targetLabel.split("#");
  const normalizedTarget = normalizeWikiTarget(targetPath);
  const label =
    explicitLabel?.trim() || targetPath.split("/").pop()?.replace(/\.md$/, "") || normalizedTarget;
  return {
    target: normalizedTarget,
    href: targetToHref(normalizedTarget, anchor),
    label: label.replace(/[-_]/g, " "),
  };
}

function convertWikilinks(markdown: string): string {
  return markdown.replace(/\[\[([^\]]+)\]\]/g, (_full, rawLink: string) => {
    const parsed = parseWikiLink(rawLink.trim());
    return `[${parsed.label}](${parsed.href})`;
  });
}

function extractWikiTargets(markdown: string): string[] {
  const targets = new Set<string>();
  for (const match of markdown.matchAll(/\[\[([^\]]+)\]\]/g)) {
    const [target] = match[1].split("|");
    const [pathOnly] = target.split("#");
    targets.add(normalizeWikiTarget(pathOnly));
  }
  return Array.from(targets);
}

function getFrontmatterTargets(frontmatter: Frontmatter, key: string): string[] {
  const value = frontmatter[key];
  if (!Array.isArray(value)) {
    return [];
  }
  return value
    .filter((entry): entry is string => typeof entry === "string")
    .map((entry) => normalizeWikiTarget(entry));
}

export function formatSectionLabel(section: string): string {
  if (section === "index") {
    return "Vault Home";
  }
  return section.replace(/-/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function getPageSection(target: string): string {
  if (SPECIAL_PAGES.has(target)) {
    return "index";
  }
  return target.split("/")[0] ?? "wiki";
}

function timestampValue(value: unknown): number {
  if (typeof value !== "string") {
    return 0;
  }
  const parsed = Date.parse(value);
  return Number.isNaN(parsed) ? 0 : parsed;
}

function getPageUpdated(page: WikiPage): string | undefined {
  return typeof page.frontmatter.updated === "string"
    ? page.frontmatter.updated
    : typeof page.frontmatter.created === "string"
      ? page.frontmatter.created
      : undefined;
}

function comparePages(left: WikiPage, right: WikiPage): number {
  if (left.section === "sources" || left.section === "outputs") {
    return timestampValue(getPageUpdated(right)) - timestampValue(getPageUpdated(left));
  }
  return left.title.localeCompare(right.title);
}

function toLinkItem(page: WikiPage, metaOverride?: string): LinkItem {
  return {
    href: page.href,
    label: page.title,
    meta: metaOverride ?? formatSectionLabel(page.type),
  };
}

function toPreviewItem(page: WikiPage): PreviewItem {
  const updated = getPageUpdated(page);
  const metaParts = [formatSectionLabel(page.type)];
  if (updated) {
    metaParts.push(updated.slice(0, 10));
  }
  return {
    href: page.href,
    label: page.title,
    meta: metaParts.join(" / "),
    excerpt: page.excerpt,
    type: page.type,
    updated,
    sourcePath: page.sourcePath,
  };
}

function materializeWikiPage(record: ManifestPageRecord): WikiPage {
  const sourcePath = typeof record.source_path === "string" && record.source_path ? record.source_path : undefined;
  const sourceUrl = typeof record.source_url === "string" && record.source_url ? record.source_url : undefined;
  return {
    title: record.title,
    type: record.type,
    target: record.target,
    href: targetToHref(record.target),
    relativePath: record.relative_path,
    section: record.section,
    frontmatter: record.frontmatter,
    markdown: record.markdown,
    renderedMarkdown: convertWikilinks(record.markdown),
    headings: record.headings,
    excerpt: record.excerpt,
    outboundTargets: record.outbound_targets,
    sourcePath,
    sourceUrl,
  };
}

function materializeRawDocument(record: ManifestRawDocumentRecord): RawDocument {
  return {
    title: record.title,
    relativePath: record.relative_path,
    frontmatter: record.frontmatter,
    markdown: convertWikilinks(record.markdown),
    headings: record.headings,
    excerpt: record.excerpt,
    sourceUrl: typeof record.source_url === "string" && record.source_url ? record.source_url : undefined,
    sourceDomain:
      typeof record.source_domain === "string" && record.source_domain ? record.source_domain : undefined,
  };
}

async function parseWikiFile(filePath: string): Promise<WikiPage> {
  const raw = await fs.readFile(filePath, "utf8");
  const parsed = matter(raw);
  const relativePath = withPosixSeparators(path.relative(WIKI_ROOT, filePath));
  const target = relativePath === "index.md" ? "index" : relativePath.replace(/\.md$/, "");
  const fallbackTitle = relativePath.split("/").pop()?.replace(/\.md$/, "") || "Untitled";
  const title =
    typeof parsed.data.title === "string" ? parsed.data.title : extractTitle(parsed.content, fallbackTitle);
  const markdown = removeLeadingTitle(parsed.content, title);
  const type =
    typeof parsed.data.type === "string"
      ? parsed.data.type
      : SPECIAL_PAGES.has(target)
        ? "operational"
        : getPageSection(target).slice(0, -1) || "page";
  const sourcePath = typeof parsed.data.source_path === "string" ? parsed.data.source_path : undefined;
  const sourceUrl = typeof parsed.data.source_url === "string" ? parsed.data.source_url : undefined;
  const outboundTargets = Array.from(
    new Set([
      ...extractWikiTargets(parsed.content),
      ...getFrontmatterTargets(parsed.data, "related"),
      ...getFrontmatterTargets(parsed.data, "source_pages"),
    ]),
  ).sort();

  return {
    title,
    type,
    target,
    href: targetToHref(target),
    relativePath,
    section: getPageSection(target),
    frontmatter: parsed.data,
    markdown,
    renderedMarkdown: convertWikilinks(markdown),
    headings: extractHeadings(markdown),
    excerpt:
      typeof parsed.data.description === "string" ? parsed.data.description : extractExcerpt(markdown),
    outboundTargets,
    sourcePath,
    sourceUrl,
  };
}

const loadManifest = cache(async (): Promise<ManifestPayload | null> => {
  if (!(await exists(MANIFEST_PATH))) {
    return null;
  }

  const raw = await fs.readFile(MANIFEST_PATH, "utf8");
  return JSON.parse(raw) as ManifestPayload;
});

const loadWikiGraph = cache(async (): Promise<WikiGraph> => {
  const manifest = await loadManifest();
  const pages = manifest
    ? manifest.pages.map((page) => materializeWikiPage(page)).sort(comparePages)
    : (await Promise.all((await collectMarkdownFiles(WIKI_ROOT)).map((filePath) => parseWikiFile(filePath)))).sort(comparePages);
  const byTarget = new Map<string, WikiPage>();
  const backlinks = new Map<string, WikiPage[]>();
  const bySection = new Map<string, WikiPage[]>();
  const rawToSourcePage = new Map<string, WikiPage>();

  for (const page of pages) {
    byTarget.set(page.target, page);

    const sectionPages = bySection.get(page.section) ?? [];
    sectionPages.push(page);
    bySection.set(page.section, sectionPages);

    if (page.sourcePath) {
      rawToSourcePage.set(page.sourcePath, page);
    }
  }

  for (const page of pages) {
    for (const outboundTarget of page.outboundTargets) {
      const linkedPages = backlinks.get(outboundTarget) ?? [];
      linkedPages.push(page);
      backlinks.set(outboundTarget, linkedPages);
    }
  }

  for (const [target, linkedPages] of backlinks.entries()) {
    backlinks.set(
      target,
      linkedPages.sort((left, right) => left.title.localeCompare(right.title)),
    );
  }

  return {
    pages,
    byTarget,
    backlinks,
    bySection,
    rawToSourcePage,
  };
});

export async function getAllWikiPages(): Promise<WikiPage[]> {
  return (await loadWikiGraph()).pages;
}

export async function getWikiPageByRoute(slug: string[] = []): Promise<WikiPage | null> {
  const routeTarget = slug.length === 0 ? "index" : withPosixSeparators(slug.join("/"));
  return (await loadWikiGraph()).byTarget.get(routeTarget) ?? null;
}

export async function getSourcePageForRawPath(rawPath: string): Promise<WikiPage | null> {
  return (await loadWikiGraph()).rawToSourcePage.get(rawPath) ?? null;
}

export async function getSidebarSections(): Promise<SidebarSection[]> {
  const graph = await loadWikiGraph();
  const startPages = ["index", "inbox", "log"]
    .map((target) => graph.byTarget.get(target))
    .filter((page): page is WikiPage => Boolean(page))
    .map((page) => toLinkItem(page));

  const sectionLink = (section: string) =>
    graph.bySection.get(section)?.map((page) => toLinkItem(page, section === "sources" ? getPageUpdated(page)?.slice(0, 10) : undefined)) ??
    [];

  const recentSources = [...(graph.bySection.get("sources") ?? [])].slice(0, 8).map((page) =>
    toLinkItem(page, getPageUpdated(page)?.slice(0, 10)),
  );

  return [
    { title: "Start", items: startPages },
    {
      title: "Sections",
      items: CONTENT_SECTIONS.filter((section) => (graph.bySection.get(section) ?? []).length > 0).map((section) => ({
        href: `/${section}`,
        label: formatSectionLabel(section),
        meta: `${graph.bySection.get(section)?.length ?? 0} pages`,
      })),
    },
    { title: "Concepts", items: sectionLink("concepts").slice(0, 8) },
    { title: "Syntheses", items: sectionLink("syntheses").slice(0, 8) },
    { title: "Outputs", items: sectionLink("outputs").slice(0, 8) },
    { title: "Recent Sources", items: recentSources },
  ].filter((section) => section.items.length > 0);
}

export async function getBacklinks(target: string): Promise<LinkItem[]> {
  const normalizedTarget = normalizeWikiTarget(target);
  return ((await loadWikiGraph()).backlinks.get(normalizedTarget) ?? []).map((page) => toLinkItem(page));
}

export async function getBacklinkPreviews(target: string): Promise<PreviewItem[]> {
  const normalizedTarget = normalizeWikiTarget(target);
  return ((await loadWikiGraph()).backlinks.get(normalizedTarget) ?? []).map((page) => toPreviewItem(page));
}

export async function getLinkItemsForTargets(targets: string[]): Promise<LinkItem[]> {
  const normalizedTargets = Array.from(new Set(targets.map((target) => normalizeWikiTarget(target))));
  if (normalizedTargets.length === 0) {
    return [];
  }

  const graph = await loadWikiGraph();
  return normalizedTargets.map((target) => {
    const page = graph.byTarget.get(target);
    if (page) {
      return toLinkItem(page);
    }
    const fallbackLabel = target.split("/").pop()?.replace(/[-_]/g, " ") || target;
    return {
      href: targetToHref(target),
      label: fallbackLabel,
      meta: "Referenced page",
    };
  });
}

export async function getPreviewItemsForTargets(targets: string[]): Promise<PreviewItem[]> {
  const normalizedTargets = Array.from(new Set(targets.map((target) => normalizeWikiTarget(target))));
  if (normalizedTargets.length === 0) {
    return [];
  }

  const graph = await loadWikiGraph();
  return normalizedTargets
    .map((target) => graph.byTarget.get(target))
    .filter((page): page is WikiPage => Boolean(page))
    .map((page) => toPreviewItem(page));
}

export async function getSectionDirectory(section: string): Promise<SectionDirectory | null> {
  if (!CONTENT_SECTION_SET.has(section)) {
    return null;
  }

  const graph = await loadWikiGraph();
  const pages = graph.bySection.get(section) ?? [];
  if (pages.length === 0) {
    return null;
  }

  const descriptionMap: Record<string, string> = {
    sources:
      "Deterministic source pages that bridge raw files into the compiled wiki. Each page should trace directly back to one raw file.",
    concepts:
      "Reusable concept pages that capture durable definitions, evidence, contradictions, and open questions.",
    entities: "Named entities linked across source pages, syntheses, and outputs.",
    benchmarks: "Benchmark-oriented notes, comparisons, and evaluation references.",
    projects: "Project pages that gather local experiments, implementation notes, and related sources.",
    syntheses:
      "Multi-source explanations that combine several source pages into a durable, higher-level view.",
    outputs:
      "Deliverables, saved answers, and slide-ready artifacts written back into the wiki for reuse.",
    reviews: "Structured review pages for contradictions, quality checks, or periodic audits.",
  };

  return {
    section,
    title: formatSectionLabel(section),
    description: descriptionMap[section] ?? "Directory page for this wiki section.",
    pages: pages.map((page) => toPreviewItem(page)),
  };
}

function countOccurrences(text: string, term: string): number {
  if (!term) {
    return 0;
  }
  let count = 0;
  let cursor = 0;
  while (cursor >= 0) {
    cursor = text.indexOf(term, cursor);
    if (cursor === -1) {
      break;
    }
    count += 1;
    cursor += term.length;
  }
  return count;
}

function buildSearchSnippet(markdown: string, query: string): string {
  const stripped = stripMarkdownSyntax(markdown);
  const lower = stripped.toLowerCase();
  const terms = query
    .toLowerCase()
    .split(/\s+/)
    .map((term) => term.trim())
    .filter(Boolean);
  const firstTerm = terms.find((term) => lower.includes(term));

  if (!firstTerm) {
    return stripped.slice(0, 220);
  }

  const index = lower.indexOf(firstTerm);
  const start = Math.max(0, index - 80);
  const end = Math.min(stripped.length, index + 160);
  const prefix = start > 0 ? "..." : "";
  const suffix = end < stripped.length ? "..." : "";
  return `${prefix}${stripped.slice(start, end).trim()}${suffix}`;
}

export async function searchWiki(query: string, limit = 20): Promise<SearchResult[]> {
  return searchWikiWithOptions(query, { limit });
}

export async function searchWikiWithOptions(query: string, options: SearchOptions = {}): Promise<SearchResult[]> {
  const trimmedQuery = query.trim();
  const graph = await loadWikiGraph();
  const effectiveLimit = options.limit ?? 20;
  const typeFilter = options.type?.trim();
  const sectionFilter = options.section?.trim();
  const statusFilter = options.status?.trim();
  const minConfidence = options.minConfidence;
  const includeSpecial = options.includeSpecial ?? false;
  const hasFilters = Boolean(typeFilter || sectionFilter || statusFilter || typeof minConfidence === "number");
  if (!trimmedQuery && !hasFilters) {
    return [];
  }

  const normalizedQuery = trimmedQuery.toLowerCase();
  const terms = normalizedQuery ? normalizedQuery.split(/\s+/).filter(Boolean) : [];

  const results = graph.pages
    .filter((page) => {
      if (!includeSpecial && SPECIAL_PAGES.has(page.target)) {
        return false;
      }
      if (typeFilter && page.type !== typeFilter) {
        return false;
      }
      if (sectionFilter && page.section !== sectionFilter) {
        return false;
      }
      if (statusFilter && page.frontmatter.status !== statusFilter) {
        return false;
      }
      if (typeof minConfidence === "number") {
        const confidence = page.frontmatter.confidence;
        if (typeof confidence !== "number" || confidence < minConfidence) {
          return false;
        }
      }
      return true;
    })
    .map((page) => {
      const title = page.title.toLowerCase();
      const headings = page.headings.map((heading) => heading.text.toLowerCase()).join(" ");
      const body = stripMarkdownSyntax(page.markdown).toLowerCase();
      const meta = JSON.stringify(page.frontmatter).toLowerCase();

      let score = 0;
      if (normalizedQuery) {
        score += countOccurrences(title, normalizedQuery) * 18;
        score += countOccurrences(headings, normalizedQuery) * 12;
        score += countOccurrences(meta, normalizedQuery) * 6;
        score += countOccurrences(body, normalizedQuery) * 2;
      }

      for (const term of terms) {
        score += countOccurrences(title, term) * 8;
        score += countOccurrences(headings, term) * 5;
        score += countOccurrences(meta, term) * 3;
        score += countOccurrences(body, term);
      }

      if (terms.length > 0 && terms.every((term) => body.includes(term) || title.includes(term) || headings.includes(term))) {
        score += 10;
      }

      if (!normalizedQuery) {
        score += 1;
      }

      if (page.relativePath.endsWith(".slides.md")) {
        score -= 6;
      }
      if (SPECIAL_PAGES.has(page.target)) {
        score -= 8;
      }

      return {
        page,
        score,
        snippet: buildSearchSnippet(page.markdown, trimmedQuery),
      };
    })
    .filter((result) => result.score > 0)
    .sort((left, right) => right.score - left.score || left.page.title.localeCompare(right.page.title));

  return results.slice(0, effectiveLimit);
}

const loadRawDocument = cache(async (key: string): Promise<RawDocument | null> => {
  const manifest = await loadManifest();
  const relativeRepoPath = withPosixSeparators(path.join("raw", key));
  const manifestRecord = manifest?.raw_documents.find((record) => record.relative_path === relativeRepoPath);
  if (manifestRecord) {
    return materializeRawDocument(manifestRecord);
  }

  const filePath = safeResolve(RAW_ROOT, ...key.split("/"));
  if (!(await exists(filePath))) {
    return null;
  }

  const raw = await fs.readFile(filePath, "utf8");
  const parsed = matter(raw);
  const relativePath = withPosixSeparators(path.relative(REPO_ROOT, filePath));
  const fallbackTitle = relativePath.split("/").pop()?.replace(/\.md$/, "") || "Raw source";
  const title =
    typeof parsed.data.title === "string" ? parsed.data.title : extractTitle(parsed.content, fallbackTitle);
  const markdown = removeLeadingTitle(parsed.content, title);

  return {
    title,
    relativePath,
    frontmatter: parsed.data,
    markdown: convertWikilinks(markdown),
    headings: extractHeadings(markdown),
    excerpt:
      typeof parsed.data.description === "string" ? parsed.data.description : extractExcerpt(markdown),
    sourceUrl: typeof parsed.data.source_url === "string" ? parsed.data.source_url : undefined,
    sourceDomain: typeof parsed.data.source_domain === "string" ? parsed.data.source_domain : undefined,
  };
});

export async function getRawDocument(slug: string[]): Promise<RawDocument | null> {
  return loadRawDocument(slug.join("/"));
}

export function getBreadcrumbs(target: string): LinkItem[] {
  if (target === "index") {
    return [];
  }

  const breadcrumbs: LinkItem[] = [{ href: "/", label: "Wiki Index" }];
  const segments = target.split("/");
  const lastIndex = segments.length - 1;

  segments.forEach((segment, index) => {
    const href = index === lastIndex ? targetToHref(target) : `/${segments.slice(0, index + 1).join("/")}`;
    breadcrumbs.push({
      href,
      label: formatSectionLabel(segment),
    });
  });

  return breadcrumbs;
}

export function formatValue(value: unknown): string {
  if (typeof value === "string" || typeof value === "number") {
    return String(value);
  }
  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }
  return "";
}

import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { MarkdownContent } from "@/components/markdown-content";
import { PreviewGrid } from "@/components/preview-grid";
import { WikiShell } from "@/components/wiki-shell";
import {
  getBacklinkPreviews,
  formatSectionLabel,
  formatValue,
  getBacklinks,
  getBreadcrumbs,
  getLinkItemsForTargets,
  getPreviewItemsForTargets,
  getSectionDirectory,
  getSidebarSections,
  getWikiPageByRoute,
  rawPathToHref,
} from "@/lib/wiki";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ slug?: string[] }>;
}

async function loadPage(slug: string[]) {
  const page = await getWikiPageByRoute(slug);
  if (!page) {
    const section = slug.length === 1 ? await getSectionDirectory(slug[0]) : null;
    if (!section) {
      notFound();
    }

    const sidebarSections = await getSidebarSections();
    return {
      kind: "section" as const,
      section,
      sidebarSections,
    };
  }

  const sidebarSections = await getSidebarSections();
  const backlinks = await getBacklinks(page.target);
  const backlinkPreviews = await getBacklinkPreviews(page.target);
  const relatedLinks = await getLinkItemsForTargets(
    Array.isArray(page.frontmatter.related)
      ? page.frontmatter.related.filter((value): value is string => typeof value === "string")
      : [],
  );
  const relatedPreviews = await getPreviewItemsForTargets(
    Array.isArray(page.frontmatter.related)
      ? page.frontmatter.related.filter((value): value is string => typeof value === "string")
      : [],
  );
  const sourceLinks = await getLinkItemsForTargets(
    Array.isArray(page.frontmatter.source_pages)
      ? page.frontmatter.source_pages.filter((value): value is string => typeof value === "string")
      : [],
  );

  return {
    kind: "page" as const,
    page,
    sidebarSections,
    backlinks,
    backlinkPreviews,
    relatedLinks,
    relatedPreviews,
    sourceLinks,
  };
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug = [] } = await params;
  const page = await getWikiPageByRoute(slug);

  if (!page) {
    const section = slug.length === 1 ? await getSectionDirectory(slug[0]) : null;
    if (section) {
      return {
        title: section.title,
        description: section.description,
      };
    }

    return {
      title: "Not Found",
    };
  }

  return {
    title: page.title,
    description: page.excerpt || "Filesystem-backed wiki page",
  };
}

export default async function WikiPageRoute({ params }: PageProps) {
  const { slug = [] } = await params;
  const loaded = await loadPage(slug);

  if (loaded.kind === "section") {
    return (
      <WikiShell
        breadcrumbs={slug.length === 1 ? [{ href: "/", label: "Wiki Index" }] : []}
        currentHref={`/${loaded.section.section}`}
        eyebrow="Section Directory"
        metaItems={[
          { label: "Section", value: loaded.section.title },
          { label: "Pages", value: String(loaded.section.pages.length) },
        ]}
        sidebarSections={loaded.sidebarSections}
        summary={loaded.section.description}
        title={loaded.section.title}
        afterContent={<PreviewGrid items={loaded.section.pages} title={`${loaded.section.title} Pages`} />}
      >
        <div className="sectionLead">
          <p className="pageSummary">
            Browse the pages in this section. These cards are rendered directly from the same markdown files that Obsidian and the agents use.
          </p>
        </div>
      </WikiShell>
    );
  }

  const { page, sidebarSections, backlinks, backlinkPreviews, relatedLinks, relatedPreviews, sourceLinks } = loaded;

  const metaItems = [
    { label: "Type", value: formatSectionLabel(page.type) },
    page.frontmatter.status ? { label: "Status", value: formatValue(page.frontmatter.status) } : null,
    page.frontmatter.confidence
      ? { label: "Confidence", value: formatValue(page.frontmatter.confidence) }
      : null,
    { label: "Backlinks", value: String(backlinks.length) },
    { label: "Related", value: String(relatedPreviews.length) },
    page.frontmatter.updated ? { label: "Updated", value: formatValue(page.frontmatter.updated) } : null,
    page.sourcePath
      ? {
          label: "Raw Source",
          value: <Link href={rawPathToHref(page.sourcePath)}>{page.sourcePath}</Link>,
        }
      : null,
    page.sourceUrl
      ? {
          label: "Original URL",
          value: (
            <a href={page.sourceUrl} rel="noreferrer" target="_blank">
              {page.sourceUrl}
            </a>
          ),
        }
      : null,
  ].filter(Boolean) as { label: string; value: React.ReactNode }[];

  const railSections = [
    relatedLinks.length > 0 ? { title: `Related Pages (${relatedLinks.length})`, items: relatedLinks } : null,
    sourceLinks.length > 0 ? { title: "Source Pages", items: sourceLinks } : null,
    backlinks.length > 0 ? { title: `Backlinks (${backlinks.length})`, items: backlinks } : null,
  ].filter(Boolean) as { title: string; items: typeof backlinks }[];

  return (
    <WikiShell
      breadcrumbs={getBreadcrumbs(page.target)}
      currentHref={page.href}
      eyebrow={`${formatSectionLabel(page.section)} / ${formatSectionLabel(page.type)}`}
      headings={page.headings}
      metaItems={metaItems}
      railSections={railSections}
      sidebarSections={sidebarSections}
      summary={page.excerpt}
      title={page.title}
      afterContent={
        <>
          <PreviewGrid
            emptyLabel="No linked related pages yet."
            items={relatedPreviews}
            title="Related Page Previews"
          />
          <PreviewGrid
            emptyLabel="No backlinks point at this page yet."
            items={backlinkPreviews}
            title="Backlink Previews"
          />
        </>
      }
    >
      <MarkdownContent markdown={page.renderedMarkdown} />
    </WikiShell>
  );
}

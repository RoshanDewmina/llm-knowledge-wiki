import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { MarkdownContent } from "@/components/markdown-content";
import { WikiShell } from "@/components/wiki-shell";
import { formatValue, getRawDocument, getSidebarSections, getSourcePageForRawPath } from "@/lib/wiki";

export const dynamic = "force-dynamic";

interface RawPageProps {
  params: Promise<{ slug: string[] }>;
}

async function loadRawPage(slug: string[]) {
  const document = await getRawDocument(slug);
  if (!document) {
    notFound();
  }

  const [sidebarSections, linkedSourcePage] = await Promise.all([
    getSidebarSections(),
    getSourcePageForRawPath(document.relativePath),
  ]);

  return {
    document,
    linkedSourcePage,
    sidebarSections,
  };
}

export async function generateMetadata({ params }: RawPageProps): Promise<Metadata> {
  const { slug } = await params;
  const document = await getRawDocument(slug);

  if (!document) {
    return {
      title: "Raw Source Not Found",
    };
  }

  return {
    title: `${document.title} (Raw)`,
    description: document.excerpt || "Raw source file",
  };
}

export default async function RawPage({ params }: RawPageProps) {
  const { slug } = await params;
  const { document, linkedSourcePage, sidebarSections } = await loadRawPage(slug);

  const metaItems = [
    { label: "Layer", value: "Raw Source" },
    document.frontmatter.captured_at
      ? { label: "Captured", value: formatValue(document.frontmatter.captured_at) }
      : null,
    document.frontmatter.published
      ? { label: "Published", value: formatValue(document.frontmatter.published) }
      : null,
    document.sourceDomain ? { label: "Domain", value: document.sourceDomain } : null,
    linkedSourcePage
      ? {
          label: "Compiled Page",
          value: <Link href={linkedSourcePage.href}>{linkedSourcePage.title}</Link>,
        }
      : null,
    document.sourceUrl
      ? {
          label: "Original URL",
          value: (
            <a href={document.sourceUrl} rel="noreferrer" target="_blank">
              {document.sourceUrl}
            </a>
          ),
        }
      : null,
  ].filter(Boolean) as { label: string; value: React.ReactNode }[];

  const railSections = linkedSourcePage
    ? [{ title: "Compiled Link", items: [{ href: linkedSourcePage.href, label: linkedSourcePage.title, meta: "Wiki source page" }] }]
    : [];

  return (
    <WikiShell
      currentHref={`/raw/${slug.join("/")}`}
      eyebrow="Raw Source"
      headings={document.headings}
      metaItems={metaItems}
      railSections={railSections}
      sidebarSections={sidebarSections}
      summary={document.excerpt}
      title={document.title}
    >
      <MarkdownContent markdown={document.markdown} />
    </WikiShell>
  );
}

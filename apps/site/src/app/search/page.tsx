import type { Metadata } from "next";
import Link from "next/link";

import { SearchForm } from "@/components/search-form";
import { WikiShell } from "@/components/wiki-shell";
import { getSidebarSections, searchWikiWithOptions } from "@/lib/wiki";

export const dynamic = "force-dynamic";

interface SearchPageProps {
  searchParams: Promise<{
    q?: string;
    type?: string;
    section?: string;
    status?: string;
    minConfidence?: string;
  }>;
}

export const metadata: Metadata = {
  title: "Search",
  description: "Search across compiled wiki pages.",
};

export default async function SearchPage({ searchParams }: SearchPageProps) {
  const { q = "", type = "", section = "", status = "", minConfidence = "" } = await searchParams;
  const query = q.trim();
  const minConfidenceValue = minConfidence ? Number.parseFloat(minConfidence) : undefined;
  const filters = [
    type ? { label: "Type", value: type } : null,
    section ? { label: "Section", value: section } : null,
    status ? { label: "Status", value: status } : null,
    typeof minConfidenceValue === "number" && Number.isFinite(minConfidenceValue)
      ? { label: "Min confidence", value: minConfidenceValue.toFixed(2) }
      : null,
  ].filter(Boolean) as { label: string; value: string }[];
  const hasActiveQuery = Boolean(query);
  const hasActiveFilters = filters.length > 0;

  const [sidebarSections, results] = await Promise.all([
    getSidebarSections(),
    searchWikiWithOptions(query, {
      limit: 24,
      type: type || undefined,
      section: section || undefined,
      status: status || undefined,
      minConfidence:
        typeof minConfidenceValue === "number" && Number.isFinite(minConfidenceValue)
          ? minConfidenceValue
          : undefined,
    }),
  ]);

  return (
    <WikiShell
      currentHref="/search"
      eyebrow="Local Search"
      initialQuery={query}
      metaItems={
        query
          ? [{ label: "Results", value: String(results.length) }, ...filters]
          : []
      }
      railSections={
        query
          ? [
              filters.length > 0
                ? {
                    title: "Active Filters",
                    items: filters.map((filter) => ({
                      href: "/search",
                      label: filter.value,
                      meta: filter.label,
                    })),
                  }
                : null,
              {
                title: "Search Tips",
                items: [
                  {
                    href: "/concepts/transformer-architecture",
                    label: "Try concept pages",
                    meta: "High-signal summaries",
                  },
                  {
                    href: "/syntheses/transformer-orientation",
                    label: "Try syntheses",
                    meta: "Multi-source views",
                  },
                ],
              },
            ].filter(Boolean) as {
              title: string;
              items: { href: string; label: string; meta?: string }[];
            }[]
          : []
      }
      sidebarSections={sidebarSections}
      summary="A lightweight lexical search over the compiled wiki, running directly against the same markdown files used by the vault."
      title="Search The Wiki"
    >
      <div className="searchIntro">
        <SearchForm
          initialMinConfidence={minConfidence}
          initialQuery={query}
          initialSection={section}
          initialStatus={status}
          initialType={type}
        />
        <p className="searchSummary">
          {hasActiveQuery
            ? `Showing the strongest local matches for “${query}”.`
            : hasActiveFilters
              ? "Browsing the compiled wiki through local filters, without needing a separate database or service."
              : "Search titles, headings, frontmatter, and page bodies without leaving the local filesystem."}
        </p>
      </div>

      {hasActiveQuery || hasActiveFilters ? (
        results.length > 0 ? (
          <ul className="resultList">
            {results.map((result) => (
              <li className="resultCard" key={result.page.href}>
                <span className="resultType">{result.page.type}</span>
                <Link className="resultLink" href={result.page.href}>
                  <span className="resultLinkLabel">{result.page.title}</span>
                  <span className="resultPath">{result.page.relativePath}</span>
                  <span className="resultMeta">
                    {[
                      result.page.section,
                      typeof result.page.frontmatter.status === "string" ? result.page.frontmatter.status : null,
                      typeof result.page.frontmatter.confidence === "number"
                        ? result.page.frontmatter.confidence.toFixed(2)
                        : null,
                    ]
                      .filter(Boolean)
                      .join(" / ")}
                  </span>
                  <span className="resultSnippet">{result.snippet}</span>
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          <p className="emptyState">No local matches yet. Try a broader concept name or inspect the vault index first.</p>
        )
      ) : (
        <p className="emptyState">
          Start with a concept, source title, or phrase from the compiled wiki. You can also use the filters to browse a slice of the vault without typing a query.
        </p>
      )}
    </WikiShell>
  );
}

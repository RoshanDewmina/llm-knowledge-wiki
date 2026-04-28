import { PreviewGrid } from "@/components/preview-grid";
import { WikiShell } from "@/components/wiki-shell";
import { getAllWikiPages, getSidebarSections } from "@/lib/wiki";

export const dynamic = "force-dynamic";

export default async function StudiesPage() {
  const pages = (await getAllWikiPages())
    .filter((page) => page.section === "studies")
    .sort((left, right) => {
      const leftUpdated = typeof left.frontmatter.updated === "string" ? Date.parse(left.frontmatter.updated) : 0;
      const rightUpdated = typeof right.frontmatter.updated === "string" ? Date.parse(right.frontmatter.updated) : 0;
      return rightUpdated - leftUpdated || left.title.localeCompare(right.title);
    });
  const sidebarSections = await getSidebarSections();
  const groups = ["paper", "anki", "derivation", "implementation"].map((kind) => ({
    kind,
    pages: pages.filter((page) => page.frontmatter.study_kind === kind),
  }));

  return (
    <WikiShell
      breadcrumbs={[{ href: "/", label: "Wiki Index" }]}
      currentHref="/studies"
      eyebrow="Study Directory"
      metaItems={[{ label: "Studies", value: String(pages.length) }]}
      sidebarSections={sidebarSections}
      summary="Private paper-mastery scaffolding grouped by study kind."
      title="Studies"
    >
      <div className="sectionLead">
        <p className="pageSummary">
          Study pages are the workshop layer: paper notes, Anki decks, derivation drills, and toy implementation specs.
        </p>
      </div>
      {groups.map((group) => (
        <PreviewGrid
          key={group.kind}
          emptyLabel={`No ${group.kind} studies yet.`}
          items={group.pages.map((page) => ({
            href: page.href,
            label: page.title,
            meta: `${page.frontmatter.read_status ?? "unknown"} / mastery ${page.frontmatter.mastery_avg ?? "n/a"}`,
            excerpt: page.excerpt,
            type: page.type,
            updated: typeof page.frontmatter.updated === "string" ? page.frontmatter.updated : undefined,
            sourcePath: page.sourcePath,
          }))}
          title={`${group.kind.charAt(0).toUpperCase()}${group.kind.slice(1)} Studies`}
        />
      ))}
    </WikiShell>
  );
}

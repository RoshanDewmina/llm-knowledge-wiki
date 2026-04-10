import Link from "next/link";

import { SearchForm } from "@/components/search-form";
import type { Heading, LinkItem, RailSection, SidebarSection } from "@/lib/wiki";

interface MetaItem {
  label: string;
  value: React.ReactNode;
}

interface WikiShellProps {
  currentHref: string;
  sidebarSections: SidebarSection[];
  title: string;
  eyebrow: string;
  summary?: string;
  breadcrumbs?: LinkItem[];
  metaItems?: MetaItem[];
  headings?: Heading[];
  railSections?: RailSection[];
  initialQuery?: string;
  children: React.ReactNode;
  afterContent?: React.ReactNode;
}

function NavList({
  items,
  currentHref,
  className,
}: {
  items: LinkItem[];
  currentHref: string;
  className: "sidebar" | "rail";
}) {
  return (
    <ul className={className === "rail" ? "railList" : "sidebarList"}>
      {items.map((item) => {
        const linkClass =
          className === "rail"
            ? "railLink"
            : item.href === currentHref
              ? "sidebarLink sidebarLinkCurrent"
              : "sidebarLink";
        const labelClass = className === "rail" ? "railLinkLabel" : "sidebarLinkLabel";
        const metaClass = className === "rail" ? "railLinkMeta" : "sidebarLinkMeta";

        return (
          <li key={`${item.href}:${item.label}`}>
            <Link className={linkClass} href={item.href}>
              <span className={labelClass}>{item.label}</span>
              {item.meta ? <span className={metaClass}>{item.meta}</span> : null}
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

export function WikiShell({
  currentHref,
  sidebarSections,
  title,
  eyebrow,
  summary,
  breadcrumbs = [],
  metaItems = [],
  headings = [],
  railSections = [],
  initialQuery,
  children,
  afterContent,
}: WikiShellProps) {
  const tableOfContents =
    headings.length > 0
      ? [
          {
            title: "On This Page",
            items: headings.map((heading) => ({
              href: `#${heading.id}`,
              label: heading.text,
              meta: `H${heading.depth}`,
            })),
          },
        ]
      : [];

  const combinedRailSections = [...tableOfContents, ...railSections];

  return (
    <div className="siteShell">
      <aside className="siteSidebar">
        <div className="siteSidebarInner">
          <div className="vaultMark">
            <span className="vaultMarkEyebrow">Local-First Vault</span>
            <Link className="vaultMarkTitle" href="/">
              LLM Knowledge Wiki
            </Link>
            <p className="vaultMarkBody">
              The same markdown files rendered for the web, Obsidian, Codex, and Claude Code.
            </p>
          </div>

          <div className="sidebarSection">
            <span className="sidebarSectionTitle">Search</span>
            <SearchForm initialQuery={initialQuery} />
          </div>

          {sidebarSections.map((section) => (
            <section className="sidebarSection" key={section.title}>
              <h2 className="sidebarSectionTitle">{section.title}</h2>
              <NavList className="sidebar" currentHref={currentHref} items={section.items} />
            </section>
          ))}
        </div>
      </aside>

      <main className="contentCanvas">
        <div className="contentFrame">
          <details className="mobileDrawer">
            <summary>Browse the vault</summary>
            <div className="mobileDrawerContent">
              <SearchForm initialQuery={initialQuery} />
              {sidebarSections.map((section) => (
                <section className="sidebarSection" key={section.title}>
                  <h2 className="sidebarSectionTitle">{section.title}</h2>
                  <NavList className="sidebar" currentHref={currentHref} items={section.items} />
                </section>
              ))}
            </div>
          </details>

          <header className="pageHeader">
            <span className="pageEyebrow">{eyebrow}</span>
            <h1 className="pageTitle">{title}</h1>
            {summary ? <p className="pageSummary">{summary}</p> : null}

            {breadcrumbs.length > 0 ? (
              <div className="utilityLinks">
                {breadcrumbs.map((crumb) => (
                  <Link className="utilityLink" href={crumb.href} key={`${crumb.href}:${crumb.label}`}>
                    {crumb.label}
                  </Link>
                ))}
              </div>
            ) : null}

            {metaItems.length > 0 ? (
              <div className="pageMeta">
                {metaItems.map((item) => (
                  <div className="metaCard" key={item.label}>
                    <span className="metaLabel">{item.label}</span>
                    <div className="metaValue">{item.value}</div>
                  </div>
                ))}
              </div>
            ) : null}
          </header>

          <section className="pageBody">
            {children}

            {afterContent ? <div className="pageSupplement">{afterContent}</div> : null}

            {combinedRailSections.length > 0 ? (
              <div className="mobileRail">
                {combinedRailSections.map((section) => (
                  <section className="railSection" key={`mobile-${section.title}`}>
                    <h2 className="railSectionTitle">{section.title}</h2>
                    <NavList className="rail" currentHref={currentHref} items={section.items} />
                  </section>
                ))}
              </div>
            ) : null}
          </section>
        </div>
      </main>

      <aside className="siteRail">
        <div className="siteRailInner">
          {combinedRailSections.map((section) => (
            <section className="railSection" key={section.title}>
              <h2 className="railSectionTitle">{section.title}</h2>
              <NavList className="rail" currentHref={currentHref} items={section.items} />
            </section>
          ))}
        </div>
      </aside>
    </div>
  );
}

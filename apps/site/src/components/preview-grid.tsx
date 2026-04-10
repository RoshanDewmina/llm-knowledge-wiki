import Link from "next/link";

import type { PreviewItem } from "@/lib/wiki";

interface PreviewGridProps {
  title: string;
  items: PreviewItem[];
  emptyLabel?: string;
}

export function PreviewGrid({ title, items, emptyLabel }: PreviewGridProps) {
  if (items.length === 0) {
    return emptyLabel ? (
      <section className="previewSection">
        <h2 className="previewSectionTitle">{title}</h2>
        <p className="emptyState">{emptyLabel}</p>
      </section>
    ) : null;
  }

  return (
    <section className="previewSection">
      <div className="previewSectionHeader">
        <h2 className="previewSectionTitle">{title}</h2>
        <span className="previewCount">{items.length}</span>
      </div>

      <div className="previewGrid">
        {items.map((item) => (
          <Link className="previewCard" href={item.href} key={`${item.href}:${item.label}`}>
            <div className="previewCardTop">
              <span className="previewMeta">{item.meta}</span>
              <span className="previewType">{item.type}</span>
            </div>
            <h3 className="previewTitle">{item.label}</h3>
            <p className="previewExcerpt">{item.excerpt || "No summary excerpt yet."}</p>
            {item.sourcePath ? <span className="previewFoot">{item.sourcePath}</span> : null}
          </Link>
        ))}
      </div>
    </section>
  );
}

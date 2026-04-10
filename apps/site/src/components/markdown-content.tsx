import Link from "next/link";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { slugifyHeading } from "@/lib/wiki";

function flattenChildren(value: React.ReactNode): string {
  if (typeof value === "string" || typeof value === "number") {
    return String(value);
  }
  if (Array.isArray(value)) {
    return value.map((child) => flattenChildren(child)).join("");
  }
  if (value && typeof value === "object" && "props" in value) {
    return flattenChildren((value as { props?: { children?: React.ReactNode } }).props?.children);
  }
  return "";
}

interface MarkdownContentProps {
  markdown: string;
}

export function MarkdownContent({ markdown }: MarkdownContentProps) {
  return (
    <div className="wikiMarkdown">
      <ReactMarkdown
        components={{
          a({ href = "", children, ...props }) {
            if (href.startsWith("/")) {
              return (
                <Link href={href} {...props}>
                  {children}
                </Link>
              );
            }

            return (
              <a href={href} rel="noreferrer" target="_blank" {...props}>
                {children}
              </a>
            );
          },
          h2({ children, ...props }) {
            return (
              <h2 id={slugifyHeading(flattenChildren(children))} {...props}>
                {children}
              </h2>
            );
          },
          h3({ children, ...props }) {
            return (
              <h3 id={slugifyHeading(flattenChildren(children))} {...props}>
                {children}
              </h3>
            );
          },
          h4({ children, ...props }) {
            return (
              <h4 id={slugifyHeading(flattenChildren(children))} {...props}>
                {children}
              </h4>
            );
          },
        }}
        remarkPlugins={[remarkGfm]}
      >
        {markdown}
      </ReactMarkdown>
    </div>
  );
}

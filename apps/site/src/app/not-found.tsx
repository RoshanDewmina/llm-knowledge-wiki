import Link from "next/link";

export default function NotFound() {
  return (
    <main className="contentCanvas">
      <div className="contentFrame">
        <header className="pageHeader">
          <span className="pageEyebrow">Not Found</span>
          <h1 className="pageTitle">This page is not in the vault.</h1>
          <p className="pageSummary">
            The route does not map to a compiled wiki page or raw source file. Start from the index or search the local graph.
          </p>
          <div className="utilityLinks">
            <Link className="utilityLink" href="/">
              Open Wiki Index
            </Link>
            <Link className="utilityLink" href="/search">
              Search The Wiki
            </Link>
          </div>
        </header>
      </div>
    </main>
  );
}

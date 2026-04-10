interface SearchFormProps {
  initialQuery?: string;
  initialType?: string;
  initialSection?: string;
  initialStatus?: string;
  initialMinConfidence?: string;
}

const TYPE_OPTIONS = ["", "source", "concept", "synthesis", "output", "review"];
const SECTION_OPTIONS = ["", "sources", "concepts", "syntheses", "outputs", "reviews"];
const STATUS_OPTIONS = ["", "stub", "draft", "reviewed", "published", "archived"];

export function SearchForm({
  initialQuery = "",
  initialType = "",
  initialSection = "",
  initialStatus = "",
  initialMinConfidence = "",
}: SearchFormProps) {
  return (
    <form action="/search" className="searchForm">
      <div className="searchPrimary">
        <input
          aria-label="Search the compiled wiki"
          className="searchInput"
          defaultValue={initialQuery}
          name="q"
          placeholder="Search the compiled wiki"
          type="search"
        />
        <button className="searchButton" type="submit">
          Search
        </button>
      </div>
      <div className="searchFilters">
        <label className="searchField">
          <span className="searchFieldLabel">Type</span>
          <select className="searchSelect" defaultValue={initialType} name="type">
            {TYPE_OPTIONS.map((option) => (
              <option key={option || "all"} value={option}>
                {option ? option : "All types"}
              </option>
            ))}
          </select>
        </label>
        <label className="searchField">
          <span className="searchFieldLabel">Section</span>
          <select className="searchSelect" defaultValue={initialSection} name="section">
            {SECTION_OPTIONS.map((option) => (
              <option key={option || "all"} value={option}>
                {option ? option : "All sections"}
              </option>
            ))}
          </select>
        </label>
        <label className="searchField">
          <span className="searchFieldLabel">Status</span>
          <select className="searchSelect" defaultValue={initialStatus} name="status">
            {STATUS_OPTIONS.map((option) => (
              <option key={option || "all"} value={option}>
                {option ? option : "All statuses"}
              </option>
            ))}
          </select>
        </label>
        <label className="searchField">
          <span className="searchFieldLabel">Min confidence</span>
          <input
            className="searchInput searchInputCompact"
            defaultValue={initialMinConfidence}
            max="1"
            min="0"
            name="minConfidence"
            placeholder="0.70"
            step="0.05"
            type="number"
          />
        </label>
      </div>
    </form>
  );
}

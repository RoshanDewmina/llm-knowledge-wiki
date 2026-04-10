# Obsidian Web Clipper Templates

These templates are designed for a simple local-first flow:

1. Clip into `raw/articles/YYYY/`
2. Run `python3 tools/ingest.py raw/articles/YYYY/...`
3. Update linked notes in `wiki/`

They use current official Web Clipper variables and filters such as `{{title}}`, `{{url}}`, `{{domain}}`, `{{date}}`, `{{time}}`, `{{content}}`, `{{highlights}}`, `safe_name`, and `replace`.

## Full Article Template

Suggested note location:

```text
raw/articles/{{date|date:"YYYY"}}
```

Suggested note name:

```text
{{date|date:"YYYY-MM-DD"}}-{{domain|replace:"/\./g":"-"|safe_name}}-{{title|safe_name}}
```

Suggested note body:

```md
---
title: "{{title}}"
source_url: "{{url}}"
source_domain: "{{domain}}"
captured_at: "{{time}}"
author: "{{author}}"
published: "{{published|date:"YYYY-MM-DD"}}"
description: "{{description|trim}}"
tags:
  - clipping
  - article
clipper: obsidian-web-clipper
---

# {{title}}

## Source

- URL: {{url}}
- Site: {{site}}
- Domain: {{domain}}
- Author: {{author}}
- Published: {{published|date:"YYYY-MM-DD"}}
- Captured: {{time}}

## Highlights

{{highlights|blockquote}}

## Content

{{content}}
```

## Highlight-First Template

Suggested note location:

```text
raw/articles/{{date|date:"YYYY"}}
```

Suggested note name:

```text
{{date|date:"YYYY-MM-DD"}}-{{domain|replace:"/\./g":"-"|safe_name}}-{{title|safe_name}}-highlights
```

Suggested note body:

```md
---
title: "{{title}}"
source_url: "{{url}}"
source_domain: "{{domain}}"
captured_at: "{{time}}"
author: "{{author}}"
published: "{{published|date:"YYYY-MM-DD"}}"
description: "{{description|trim}}"
tags:
  - clipping
  - highlights
clipper: obsidian-web-clipper
---

# {{title}}

## Source

- URL: {{url}}
- Domain: {{domain}}
- Captured: {{time}}

## Highlights

{{highlights|blockquote}}
```

## Notes

- These templates are intentionally file-first and markdown-first.
- They do not require MCP.
- They keep enough metadata in the raw file for `tools/ingest.py` to normalize a source page without fabricating a summary.


"""Scaffold a toy implementation study and starter experiment directory."""

from __future__ import annotations
import argparse
from pathlib import Path
from scaffold_study import scaffold
from wiki_utils import REPO_ROOT, humanize_slug, slugify, write_text_if_changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("task")
    parser.add_argument("--lang", choices=("numpy", "pytorch"), default="numpy")
    args = parser.parse_args()
    study_slug = slugify(args.slug)
    task_slug = slugify(args.task)
    title = humanize_slug(task_slug)
    scaffold("implementation", task_slug, title, [f"studies/papers/{study_slug}"], [f"studies/papers/{study_slug}"], False, args.lang)
    exp_dir = REPO_ROOT / "experiments" / "papers" / study_slug / task_slug
    exp_dir.mkdir(parents=True, exist_ok=True)
    readme = exp_dir / "README.md"
    if not readme.exists():
        write_text_if_changed(readme, f"# {title}\n\nStudy: `wiki/studies/papers/{study_slug}.md`\n\nRun the starter script and fill in the equivalence check.\n")
    starter = exp_dir / ("main.py" if args.lang in {"numpy", "pytorch"} else "main.txt")
    if not starter.exists():
        imports = "import numpy as np\n" if args.lang == "numpy" else "import torch\n"
        write_text_if_changed(starter, imports + "\n\ndef main():\n    raise NotImplementedError('fill in toy equivalence check')\n\n\nif __name__ == '__main__':\n    main()\n")
    print(f"created: experiments/papers/{study_slug}/{task_slug}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

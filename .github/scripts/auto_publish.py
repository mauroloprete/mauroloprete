"""Auto-publish draft posts whose date has passed."""

import re
import sys
from datetime import date, datetime
from pathlib import Path


def parse_front_matter(text: str) -> tuple[dict, int, int]:
    """Extract YAML front matter as raw key-value pairs."""
    match = re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL)
    if not match:
        return {}, 0, 0
    raw = match.group(1)
    fm = {}
    for line in raw.splitlines():
        m = re.match(r"^(\w[\w\s]*?):\s*(.+)$", line)
        if m:
            fm[m.group(1).strip()] = m.group(2).strip().strip('"').strip("'")
    return fm, match.start(), match.end()


def main() -> int:
    today = date.today()
    posts_dir = Path("blog/posts")
    published = []

    for qmd in sorted(posts_dir.glob("*/index.qmd")):
        text = qmd.read_text(encoding="utf-8")
        fm, _, _ = parse_front_matter(text)

        if fm.get("draft") != "true":
            continue

        date_str = fm.get("date")
        if not date_str:
            continue

        try:
            post_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            continue

        if post_date > today:
            continue

        # Remove the draft line
        new_text = re.sub(r"\ndraft:\s*true\s*\n", "\n", text)
        qmd.write_text(new_text, encoding="utf-8")
        published.append(f"{qmd} (date: {date_str})")
        print(f"Published: {qmd} (date: {date_str})")

    if not published:
        print("No drafts to publish.")

    return len(published)


if __name__ == "__main__":
    count = main()
    sys.exit(0)

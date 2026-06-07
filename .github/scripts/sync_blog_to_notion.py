#!/usr/bin/env python3
"""Sync blog post metadata from Git to Notion database."""

import os
import re
import sys
from glob import glob

import yaml
from notion_client import Client

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
SITE_BASE_URL = os.environ.get(
    "SITE_BASE_URL", "https://mauroloprete.github.io/mauroloprete"
)

NOTION_CATEGORIES = {
    "Databricks Tips",
    "Data Engineering",
    "Data Architecture",
    "MLOps",
    "Delta Lake",
    "Carrera",
    "Podcast",
}

notion = Client(auth=NOTION_API_KEY)


def parse_front_matter(filepath: str) -> dict | None:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\s*\n(.+?)\n---", content, re.DOTALL)
    if not match:
        print(f"  WARN: No front matter in {filepath}")
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        print(f"  WARN: Bad YAML in {filepath}: {e}")
        return None


def slug_from_path(filepath: str) -> str:
    return filepath.split("/")[2]


def find_notion_page(title: str) -> dict | None:
    response = notion.databases.query(
        database_id=NOTION_DATABASE_ID,
        filter={"property": "Título", "title": {"equals": title.strip()}},
    )
    results = response.get("results", [])
    return results[0] if results else None


def build_properties(front_matter: dict, slug: str) -> dict:
    title = front_matter.get("title", "")
    categories = front_matter.get("categories", [])
    description = front_matter.get("description", "")
    date = front_matter.get("date")
    draft = front_matter.get("draft", False)

    estado = "Borrador" if draft else "Publicado"
    tipo = "Podcast" if "Podcast" in categories else "Blog"

    mapped_cats = [
        {"name": c.strip()}
        for c in categories
        if c.strip() in NOTION_CATEGORIES
    ]

    properties = {
        "Título": {"title": [{"text": {"content": title}}]},
        "Estado": {"select": {"name": estado}},
        "Tipo": {"select": {"name": tipo}},
        "Categoría": {"multi_select": mapped_cats},
        "Descripción": {"rich_text": [{"text": {"content": description}}]},
    }

    if not draft:
        properties["Link Publicado"] = {
            "url": f"{SITE_BASE_URL}/blog/posts/{slug}/"
        }

    if date:
        properties["Fecha Planificada"] = {"date": {"start": str(date)}}

    return properties


def sync_post(filepath: str):
    front_matter = parse_front_matter(filepath)
    if front_matter is None:
        return False

    title = front_matter.get("title", "")
    slug = slug_from_path(filepath)
    print(f"  {title}")

    existing = find_notion_page(title)
    properties = build_properties(front_matter, slug)

    if existing:
        notion.pages.update(page_id=existing["id"], properties=properties)
        print(f"    -> Updated")
    else:
        notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties=properties,
        )
        print(f"    -> Created")

    return True


def main():
    posts = sorted(glob("blog/posts/*/index.qmd"))

    if not posts:
        print("No blog posts found.")
        return

    print(f"Found {len(posts)} blog post(s):\n")

    errors = []
    for filepath in posts:
        try:
            if not sync_post(filepath):
                errors.append(filepath)
        except Exception as e:
            print(f"    ERROR: {e}")
            errors.append(filepath)

    if errors:
        print(f"\n{len(errors)} post(s) failed:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\nAll posts synced.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Sincroniza posts QMD publicados del blog a Obsidian como markdown
con wikilinks al knowledge graph.

Uso:
    python scripts/sync-to-obsidian.py
    python scripts/sync-to-obsidian.py --dry-run
    python scripts/sync-to-obsidian.py --post databricks-tips-01
"""

import argparse
import re
from pathlib import Path

# --- Configuración -----------------------------------------------------------

BLOG_DIR = Path(__file__).parent.parent / "blog" / "posts"
VAULT_DIR = Path.home() / "Library" / "CloudStorage" / "OneDrive-Personal" / "obsidian-vault"
PUBLISHED_DIR = VAULT_DIR / "published" / "blog"
KNOWLEDGE_DIR = VAULT_DIR / "knowledge"
SITE_URL = "https://mauroloprete.github.io/mauroloprete/blog/posts"

# Conceptos del knowledge graph para auto-wikilink.
# Clave: texto a buscar (case insensitive), valor: nombre del archivo .md (sin extensión).
CONCEPT_MAP = {}


def load_concept_map():
    """Carga el mapa de conceptos desde los archivos del knowledge graph."""
    for subdir in ["concepts", "tools", "patterns"]:
        kg_dir = KNOWLEDGE_DIR / subdir
        if not kg_dir.exists():
            continue
        for f in kg_dir.glob("*.md"):
            name = f.stem
            display = name.replace("-", " ").title()
            # Nombre principal
            CONCEPT_MAP[display.lower()] = f"{subdir}/{name}"
            # Leer aliases del frontmatter
            try:
                content = f.read_text(encoding="utf-8")
                m = re.search(r"aliases:\s*\[([^\]]*)\]", content)
                if m:
                    aliases = [a.strip().strip("\"'") for a in m.group(1).split(",") if a.strip()]
                    for alias in aliases:
                        CONCEPT_MAP[alias.lower()] = f"{subdir}/{name}"
            except Exception:
                pass


# --- Parseo de QMD -----------------------------------------------------------

def parse_front_matter(text: str) -> tuple[dict, str]:
    """Extrae YAML front matter y devuelve (metadata dict, body)."""
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    yaml_text = parts[1]
    body = parts[2].lstrip("\n")

    meta = {}
    for line in yaml_text.strip().splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            key, _, val = line.partition(":")
            val = val.strip().strip('"').strip("'")
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip("\"'") for v in val[1:-1].split(",") if v.strip()]
            meta[key.strip()] = val

    # Parsear author (puede ser multi-línea)
    author_match = re.search(
        r"author:\s*\n\s*-\s*name:\s*[\"']?(.+?)[\"']?\s*\n",
        yaml_text,
    )
    if author_match:
        meta["author"] = author_match.group(1).strip()

    return meta, body


def is_published(meta: dict) -> bool:
    """Verifica si el post NO es draft."""
    draft = meta.get("draft", "false")
    if isinstance(draft, str):
        return draft.lower() != "true"
    return not draft


# --- Conversión QMD → Obsidian MD --------------------------------------------

def convert_callouts(text: str) -> str:
    """Convierte callouts Quarto a callouts Obsidian.

    Quarto:
        ::: {.callout-tip}
        ## Título
        Contenido
        :::

    Obsidian:
        > [!tip] Título
        > Contenido
    """
    # Regex para capturar callouts (incluyendo collapse="true")
    pattern = re.compile(
        r'^::: \{\.callout-(\w+)(?:\s+collapse="true")?\}\s*\n'
        r'(?:## (.+)\n\n?)?'
        r'(.*?)\n'
        r'^:::',
        re.MULTILINE | re.DOTALL,
    )

    def replace_callout(m):
        callout_type = m.group(1)
        title = m.group(2) or ""
        content = m.group(3).strip()
        header = f"> [!{callout_type}] {title}".rstrip()
        body = "\n".join(f"> {line}" if line else ">" for line in content.splitlines())
        return f"{header}\n{body}"

    return pattern.sub(replace_callout, text)


def convert_font_awesome(text: str) -> str:
    """Remueve shortcodes Font Awesome: {{< fa icon-name >}} → icono texto."""
    fa_map = {
        "lightbulb": "💡",
        "database": "🗄️",
        "layer-group": "📊",
        "table": "📋",
        "user": "👤",
        "link": "🔗",
        "podcast": "🎙️",
        "book": "📖",
        "file-alt": "📄",
        "warning": "⚠️",
        "check": "✅",
        "github": "🐙",
        "code": "💻",
        "cog": "⚙️",
        "rocket": "🚀",
    }
    def replace_fa(m):
        icon = m.group(1).strip()
        return fa_map.get(icon, "")
    return re.sub(r"\{\{<\s*fa\s+([^>]+?)\s*>\}\}", replace_fa, text)


def convert_internal_links(text: str) -> str:
    """Convierte links relativos entre posts a wikilinks."""
    # Pattern: [texto](../slug/) o [texto](../slug/index.html)
    def replace_link(m):
        label = m.group(1)
        slug = m.group(2).strip("/")
        return f"[[{slug}|{label}]]"
    return re.sub(r'\[([^\]]+)\]\(\.\./([^)]+?)(?:/index\.html|/?)?\)', replace_link, text)


def add_wikilinks(text: str) -> str:
    """Auto-linkea menciones de conceptos del knowledge graph.

    Evita linkear dentro de: URLs, code blocks, wikilinks existentes, headers.
    """
    # Separar code blocks para no tocarlos
    code_block_pattern = re.compile(r'(```.*?```|`[^`]+`)', re.DOTALL)
    # Separar URLs markdown y raw
    url_pattern = re.compile(r'(\[[^\]]*\]\([^)]+\)|https?://\S+)')

    # Combinar patrones de zonas protegidas
    protected = re.compile(
        r'(```.*?```|`[^`]+`|\[[^\]]*\]\([^)]+\)|https?://\S+|\[\[[^\]]+\]\])',
        re.DOTALL,
    )

    # Dividir texto en partes protegidas y no protegidas
    parts = protected.split(text)
    already_linked = set()

    for i, part in enumerate(parts):
        # Índices pares son texto libre, impares son zonas protegidas
        if i % 2 == 1:
            continue
        for term, path in sorted(CONCEPT_MAP.items(), key=lambda x: -len(x[0])):
            if term in already_linked:
                continue
            pattern = re.compile(
                r'(?<!\w)(' + re.escape(term) + r')(?!\w)',
                re.IGNORECASE,
            )
            match = pattern.search(part)
            if match:
                display = match.group(1)
                node_name = path.split("/")[-1].replace("-", " ").title()
                replacement = f"[[{node_name}|{display}]]"
                part = part[:match.start()] + replacement + part[match.end():]
                parts[i] = part
                already_linked.add(term)

    return "".join(parts)


def convert_qmd_to_obsidian(meta: dict, body: str, slug: str) -> str:
    """Convierte un post QMD completo a Obsidian markdown."""
    # Conversiones de sintaxis
    body = convert_callouts(body)
    body = convert_font_awesome(body)
    body = convert_internal_links(body)
    body = add_wikilinks(body)

    # Remover bloques R (```{r} ... ```)
    body = re.sub(r'```\{r[^}]*\}.*?```', '', body, flags=re.DOTALL)

    # Header con metadatos
    title = meta.get("title", slug)
    date = meta.get("date", "")
    categories = meta.get("categories", [])
    description = meta.get("description", "")
    if isinstance(categories, str):
        categories = [categories]

    cat_tags = " ".join(f"#{c.replace(' ', '-')}" for c in categories)
    url = f"{SITE_URL}/{slug}/"

    header = f"""---
title: "{title}"
date: {date}
source: blog
url: {url}
tags: [{', '.join(categories)}]
---

# {title}

> {description}

{cat_tags}

---

"""
    return header + body


# --- Generación de MOC -------------------------------------------------------

def generate_moc(posts: list[tuple[str, dict]]) -> str:
    """Genera el Map of Content con tabla de todos los posts."""
    lines = [
        "# Blog — Map of Content",
        "",
        "Todos los posts publicados de **Spark de Ideas**, ordenados por fecha.",
        "",
        "| Fecha | Post | Categorías |",
        "|-------|------|-----------|",
    ]

    sorted_posts = sorted(posts, key=lambda x: x[1].get("date", ""), reverse=True)
    for slug, meta in sorted_posts:
        date = meta.get("date", "")
        title = meta.get("title", slug)
        cats = meta.get("categories", [])
        if isinstance(cats, str):
            cats = [cats]
        cat_str = ", ".join(cats)
        lines.append(f"| {date} | [[{slug}\\|{title}]] | {cat_str} |")

    lines.extend([
        "",
        f"**Total: {len(posts)} posts**",
        "",
        "## Por categoría",
        "",
    ])

    # Agrupar por categoría
    cat_posts: dict[str, list] = {}
    for slug, meta in sorted_posts:
        cats = meta.get("categories", [])
        if isinstance(cats, str):
            cats = [cats]
        for cat in cats:
            cat_posts.setdefault(cat, []).append((slug, meta))

    for cat in sorted(cat_posts.keys()):
        lines.append(f"### {cat}")
        lines.append("")
        for slug, meta in cat_posts[cat]:
            title = meta.get("title", slug)
            lines.append(f"- [[{slug}|{title}]]")
        lines.append("")

    return "\n".join(lines)


# --- Main --------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Sync blog QMD → Obsidian")
    parser.add_argument("--dry-run", action="store_true", help="Mostrar qué se haría sin escribir")
    parser.add_argument("--post", help="Sincronizar solo un post específico (slug)")
    args = parser.parse_args()

    load_concept_map()
    print(f"Knowledge graph: {len(CONCEPT_MAP)} términos cargados")

    PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)

    all_posts = []
    synced = 0

    for post_dir in sorted(BLOG_DIR.iterdir()):
        qmd_file = post_dir / "index.qmd"
        if not qmd_file.exists():
            continue

        slug = post_dir.name
        if args.post and slug != args.post:
            continue

        text = qmd_file.read_text(encoding="utf-8")
        meta, body = parse_front_matter(text)

        if not is_published(meta):
            print(f"  SKIP (draft): {slug}")
            continue

        all_posts.append((slug, meta))
        obsidian_md = convert_qmd_to_obsidian(meta, body, slug)
        out_file = PUBLISHED_DIR / f"{slug}.md"

        if args.dry_run:
            print(f"  DRY: {slug} → {out_file.name}")
        else:
            out_file.write_text(obsidian_md, encoding="utf-8")
            print(f"  SYNC: {slug} → {out_file.name}")
            synced += 1

    # Generar MOC
    if all_posts:
        moc_content = generate_moc(all_posts)
        moc_file = PUBLISHED_DIR / "MOC.md"
        if args.dry_run:
            print(f"\n  DRY: MOC → {moc_file.name} ({len(all_posts)} posts)")
        else:
            moc_file.write_text(moc_content, encoding="utf-8")
            print(f"\n  MOC: {moc_file.name} ({len(all_posts)} posts)")

    print(f"\nResultado: {synced} posts sincronizados, {len(all_posts)} en MOC")


if __name__ == "__main__":
    main()

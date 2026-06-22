"""Generate the Mauro Bot architecture diagram."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("white")

# -- Palette --
NAVY = "#1e293b"
PURPLE = "#593196"
ORANGE = "#FFA166"
TEAL = "#0d9488"
GRAY = "#64748b"
LIGHT_GRAY = "#e2e8f0"
BG_LIGHT = "#f8fafc"
WHITE = "#ffffff"

def box(x, y, w, h, color, label, sub, number=None, text_color="white", fontsize=13):
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.15",
        facecolor=color,
        edgecolor="none",
        zorder=2,
    )
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2 + 0.15, label,
            ha="center", va="center", fontsize=fontsize,
            fontweight="bold", color=text_color, zorder=3)
    ax.text(x + w / 2, y + h / 2 - 0.25, sub,
            ha="center", va="center", fontsize=9,
            color=text_color, alpha=0.8, zorder=3)
    if number is not None:
        badge = plt.Circle((x + w - 0.15, y + h - 0.1), 0.22,
                           color=ORANGE, zorder=4)
        ax.add_patch(badge)
        ax.text(x + w - 0.15, y + h - 0.1, str(number),
                ha="center", va="center", fontsize=10,
                fontweight="bold", color=NAVY, zorder=5)

def arrow(x1, y1, x2, y2, label="", color=LIGHT_GRAY, style="-|>", lw=1.8):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle=style, color=color,
            lw=lw, connectionstyle="arc3,rad=0",
        ),
        zorder=1,
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.18, label, ha="center", va="bottom",
                fontsize=8, color=GRAY, style="italic", zorder=3)


# ── Title ──
ax.text(7, 8.55, "Mauro Bot — 5 recursos, 1 databricks.yml",
        ha="center", va="center", fontsize=16, fontweight="bold",
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=BG_LIGHT,
                  edgecolor=LIGHT_GRAY, linewidth=1.5))

# ── Row 1: Ingestion pipeline ──
box(0.5, 6.3, 2.8, 1.1, NAVY, "Blog + Docs", "20 documentos", text_color=WHITE)
box(5.0, 6.3, 3.0, 1.1, PURPLE, "Load KB Job", "jobs", number=1)
box(10.0, 6.3, 3.2, 1.1, TEAL, "Vector Search", "vector_search_endpoints", number=2)

arrow(3.3, 6.85, 5.0, 6.85, "scraping +\nchunking")
arrow(8.0, 6.85, 10.0, 6.85, "sync index")

# ── Row 2: Runtime (central) ──
box(0.5, 3.6, 2.8, 1.1, NAVY, "Usuario", "Comunidad", text_color=WHITE)
box(4.5, 3.3, 4.3, 1.7, ORANGE, "Databricks App", "FastAPI + chat.html + marked.js",
    number=3, text_color=NAVY, fontsize=14)

arrow(3.3, 4.15, 4.5, 4.15)

# App → Vector Search (retrieval)
arrow(8.8, 4.5, 11.5, 6.3, "retrieval", color="#0d9488", lw=2)

# ── Row 3: Support services ──
box(1.0, 0.8, 3.5, 1.1, NAVY, "MLflow Experiment", "experiments", number=4, text_color=WHITE)
box(8.5, 0.8, 4.5, 1.1, "#1e3a5f", "Lakebase (PostgreSQL 17)", "postgres_projects", number=5, text_color=WHITE)

# App → MLflow (tracing)
arrow(5.5, 3.3, 2.75, 1.9, "tracing", color=GRAY, lw=1.5)

# App → Lakebase (memory)
arrow(7.5, 3.3, 10.5, 1.9, "checkpoints\n(thread_id)", color="#1e3a5f", lw=2)

# ── Annotations ──
ax.text(6.7, 2.45, "Sin Model Serving Endpoint\nSin Registered Model\nEl agente corre directo en la App",
        ha="center", va="center", fontsize=9, color=GRAY,
        style="italic", linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#f1f5f9",
                  edgecolor=LIGHT_GRAY, linewidth=1))

# ── Footer ──
ax.text(7, 0.15, "engine: direct  |  bundle deploy  |  5 recursos declarativos",
        ha="center", va="center", fontsize=11, fontweight="bold",
        color=WHITE,
        bbox=dict(boxstyle="round,pad=0.35", facecolor=NAVY, edgecolor="none"))

plt.tight_layout(pad=0.5)
plt.savefig(
    "/Users/mauroloprete/Documents/mauroloprete/slides/databricks-meetup-dabs-agents/mauro-bot-architecture.png",
    dpi=200, bbox_inches="tight", facecolor="white",
)
print("Diagram saved.")

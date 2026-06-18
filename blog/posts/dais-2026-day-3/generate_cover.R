library(ggplot2)

generate_cover <- function(title, subtitle, icon_char, out_path) {
  navy   <- "#1e293b"
  orange <- "#FFA166"
  bg     <- "#f8fafc"
  gray2  <- "#94a3b8"

  p <- ggplot() +
    annotate("rect", xmin = 0, xmax = 10, ymin = 0, ymax = 5.625,
             fill = bg, color = NA) +
    annotate("rect", xmin = 0, xmax = 0.25, ymin = 0, ymax = 5.625,
             fill = orange, color = NA) +
    annotate("rect", xmin = 0, xmax = 10, ymin = 0, ymax = 0.6,
             fill = navy, color = NA) +
    annotate("text", x = 9.7, y = 0.3, label = "Spark de Ideas",
             hjust = 1, size = 2.8, color = orange, fontface = "italic") +
    annotate("point", x = 8.5, y = 4.2, size = 40, color = orange, alpha = 0.08) +
    annotate("point", x = 9.2, y = 3.5, size = 25, color = navy, alpha = 0.06) +
    annotate("point", x = 7.8, y = 1.8, size = 15, color = orange, alpha = 0.06) +
    annotate("text", x = 1.2, y = 4.3, label = icon_char,
             hjust = 0, size = 14, color = orange, alpha = 0.3) +
    annotate("text", x = 0.8, y = 3.2, label = title,
             hjust = 0, vjust = 1, size = 7, color = navy,
             fontface = "bold", lineheight = 0.9) +
    annotate("text", x = 0.8, y = 1.5, label = subtitle,
             hjust = 0, vjust = 1, size = 3.5, color = gray2,
             lineheight = 1.1) +
    coord_cartesian(xlim = c(0, 10), ylim = c(0, 5.625)) +
    theme_void() +
    theme(
      plot.background = element_rect(fill = bg, color = "#e2e8f0", linewidth = 0.5),
      plot.margin = margin(0, 0, 0, 0)
    )

  ggsave(out_path, p, width = 10, height = 5.625, dpi = 150, bg = bg)
}

generate_cover(
  title = "DAIS 2026 Día 3\nGenie Code for ML y Lakeflow Designer",
  subtitle = "AI Runtime multi-node, Nadella x\nGhodsi y más del Summit",
  icon_char = "\U0001F680",
  out_path = "blog/posts/dais-2026-day-3/cover.png"
)

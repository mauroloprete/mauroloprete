#!/usr/bin/env Rscript
# LinkedIn cards v5 — Pure vector, no emojis, crisp at any resolution
library(ggplot2)

# Palette
cream   <- "#faf7f2"
cream2  <- "#f0ebe3"
navy    <- "#1e293b"
navy2   <- "#0f172a"
orange  <- "#FFA166"
orange2 <- "#FF8533"
orange3 <- "#e8743b"
cyan    <- "#22d3ee"
green   <- "#34d399"
blue    <- "#60a5fa"
purple  <- "#a78bfa"
gold    <- "#fbbf24"
gray1   <- "#64748b"
gray2   <- "#94a3b8"
gray3   <- "#cbd5e1"
white   <- "#ffffff"

# ============================================================
# VECTOR ICON BUILDERS (pure shapes, no emojis)
# ============================================================

# Lightning bolt
icon_lightning <- function(cx = 8, cy = 2.8, s = 1, col = orange) {
  x <- cx + s * c(-0.3, 0.15, -0.05, 0.3, -0.15, 0.05)
  y <- cy + s * c(1.2, 0.15, 0.15, -1.2, -0.15, -0.15)
  list(
    annotate("polygon", x = x, y = y, fill = col, color = NA)
  )
}

# Book (open)
icon_book <- function(cx = 8, cy = 2.8, s = 1, col = blue) {
  list(
    # Left page
    annotate("polygon",
             x = cx + s * c(-1.0, -0.05, -0.05, -1.0),
             y = cy + s * c(-0.7, -0.5, 0.8, 0.6),
             fill = col, alpha = 0.5, color = col, linewidth = 0.5),
    # Right page
    annotate("polygon",
             x = cx + s * c(0.05, 1.0, 1.0, 0.05),
             y = cy + s * c(-0.5, -0.7, 0.6, 0.8),
             fill = col, alpha = 0.35, color = col, linewidth = 0.5),
    # Spine
    annotate("segment", x = cx, xend = cx, y = cy - s*0.5, yend = cy + s*0.8,
             color = col, linewidth = 1.2),
    # Text lines left
    annotate("segment",
             x = cx + s * c(-0.8, -0.75, -0.7),
             xend = cx + s * c(-0.2, -0.2, -0.2),
             y = cy + s * c(0.35, 0.1, -0.15),
             yend = cy + s * c(0.35, 0.1, -0.15),
             color = white, alpha = 0.5, linewidth = 0.4)
  )
}

# Cycle / refresh arrows
icon_cycle <- function(cx = 8, cy = 2.8, s = 1, col = green) {
  a <- seq(0, 5*pi/3, length.out = 50)
  r <- s * 0.8
  list(
    geom_path(data = data.frame(x = cx + r * cos(a), y = cy + r * sin(a)),
              aes(x = x, y = y), color = col, linewidth = 1.5, alpha = 0.7,
              inherit.aes = FALSE),
    # Arrow head at end
    annotate("polygon",
             x = cx + r * cos(5*pi/3) + s * c(0, 0.2, 0.15),
             y = cy + r * sin(5*pi/3) + s * c(0, 0.2, -0.05),
             fill = col, color = NA)
  )
}

# Puzzle piece
icon_puzzle <- function(cx = 8, cy = 2.8, s = 1, col = purple) {
  list(
    # Main square
    annotate("rect", xmin = cx - s*0.6, xmax = cx + s*0.6,
             ymin = cy - s*0.6, ymax = cy + s*0.6,
             fill = col, alpha = 0.4, color = col, linewidth = 0.8),
    # Tab right
    annotate("point", x = cx + s*0.6, y = cy, size = s*5,
             color = col, alpha = 0.6, shape = 16),
    # Tab top
    annotate("point", x = cx, y = cy + s*0.6, size = s*5,
             color = col, alpha = 0.6, shape = 16),
    # Second piece (offset)
    annotate("rect", xmin = cx + s*0.15, xmax = cx + s*1.2,
             ymin = cy - s*1.1, ymax = cy - s*0.1,
             fill = col, alpha = 0.25, color = col, linewidth = 0.6),
    annotate("point", x = cx + s*0.15, y = cy - s*0.6, size = s*5,
             color = col, alpha = 0.4, shape = 16)
  )
}

# Rocket
icon_rocket <- function(cx = 8, cy = 2.8, s = 1, col = orange) {
  list(
    # Body
    annotate("polygon",
             x = cx + s * c(-0.25, 0, 0.25, 0.25, -0.25),
             y = cy + s * c(-0.5, 1.0, -0.5, -0.5, -0.5),
             fill = col, alpha = 0.6, color = col, linewidth = 0.5),
    # Nose cone
    annotate("polygon",
             x = cx + s * c(-0.25, 0, 0.25),
             y = cy + s * c(0.5, 1.2, 0.5),
             fill = col, alpha = 0.8, color = NA),
    # Fins
    annotate("polygon",
             x = cx + s * c(-0.25, -0.55, -0.25),
             y = cy + s * c(-0.3, -0.7, -0.5),
             fill = col, alpha = 0.5, color = NA),
    annotate("polygon",
             x = cx + s * c(0.25, 0.55, 0.25),
             y = cy + s * c(-0.3, -0.7, -0.5),
             fill = col, alpha = 0.5, color = NA),
    # Exhaust
    annotate("polygon",
             x = cx + s * c(-0.15, 0, 0.15),
             y = cy + s * c(-0.5, -0.9, -0.5),
             fill = gold, alpha = 0.6, color = NA),
    # Window
    annotate("point", x = cx, y = cy + s*0.3, size = s*3,
             color = white, alpha = 0.5, shape = 16)
  )
}

# Package / box
icon_box <- function(cx = 8, cy = 2.8, s = 1, col = orange2) {
  list(
    # Front face
    annotate("polygon",
             x = cx + s * c(-0.7, 0.3, 0.3, -0.7),
             y = cy + s * c(-0.5, -0.5, 0.5, 0.5),
             fill = col, alpha = 0.5, color = col, linewidth = 0.5),
    # Top face
    annotate("polygon",
             x = cx + s * c(-0.7, -0.2, 0.8, 0.3),
             y = cy + s * c(0.5, 0.8, 0.8, 0.5),
             fill = col, alpha = 0.35, color = col, linewidth = 0.5),
    # Right face
    annotate("polygon",
             x = cx + s * c(0.3, 0.8, 0.8, 0.3),
             y = cy + s * c(0.5, 0.8, -0.2, -0.5),
             fill = col, alpha = 0.25, color = col, linewidth = 0.5),
    # Tape
    annotate("segment", x = cx - s*0.2, xend = cx - s*0.2,
             y = cy - s*0.5, yend = cy + s*0.65,
             color = white, alpha = 0.4, linewidth = 1)
  )
}

# Triangle / delta
icon_delta <- function(cx = 8, cy = 2.8, s = 1, col = orange3) {
  list(
    annotate("polygon",
             x = cx + s * c(0, -1.0, 1.0),
             y = cy + s * c(1.1, -0.7, -0.7),
             fill = col, alpha = 0.3, color = col, linewidth = 1.5),
    # Layer lines
    annotate("segment",
             x = cx - s*0.67, xend = cx + s*0.67,
             y = cy - s*0.1, yend = cy - s*0.1,
             color = col, alpha = 0.5, linewidth = 0.6),
    annotate("segment",
             x = cx - s*0.33, xend = cx + s*0.33,
             y = cy + s*0.5, yend = cy + s*0.5,
             color = col, alpha = 0.5, linewidth = 0.6)
  )
}

# Shield
icon_shield <- function(cx = 8, cy = 2.8, s = 1, col = orange) {
  sx <- c(0, 0.3, 0.6, 0.8, 1.0, 0.8, 0.6, 0.3, 0,
          -0.3, -0.6, -0.8, -1.0, -0.8, -0.6, -0.3)
  sy <- c(1.2, 1.15, 1.05, 0.9, 0.6,
          0.2, -0.1, -0.35, -0.5,
          -0.35, -0.1, 0.2, 0.6,
          0.9, 1.05, 1.15)
  list(
    annotate("polygon", x = cx + s * sx, y = cy + s * sy,
             fill = col, alpha = 0.2, color = col, linewidth = 1.2),
    # Check mark inside
    annotate("segment",
             x = cx - s*0.3, xend = cx - s*0.05,
             y = cy + s*0.15, yend = cy - s*0.1,
             color = col, linewidth = 1.5),
    annotate("segment",
             x = cx - s*0.05, xend = cx + s*0.35,
             y = cy - s*0.1, yend = cy + s*0.5,
             color = col, linewidth = 1.5)
  )
}

# Building / columns (governance)
icon_columns <- function(cx = 8, cy = 2.8, s = 1, col = purple) {
  pw <- s * 0.15
  list(
    # Roof (triangle)
    annotate("polygon",
             x = cx + s * c(-1.0, 0, 1.0),
             y = cy + s * c(0.5, 1.0, 0.5),
             fill = col, alpha = 0.4, color = col, linewidth = 0.5),
    # Beam
    annotate("rect", xmin = cx - s*1.05, xmax = cx + s*1.05,
             ymin = cy + s*0.4, ymax = cy + s*0.55,
             fill = col, alpha = 0.5, color = NA),
    # Pillars
    annotate("rect", xmin = cx - s*0.8 - pw, xmax = cx - s*0.8 + pw,
             ymin = cy - s*0.6, ymax = cy + s*0.4,
             fill = col, alpha = 0.4, color = NA),
    annotate("rect", xmin = cx - s*0.3 - pw, xmax = cx - s*0.3 + pw,
             ymin = cy - s*0.6, ymax = cy + s*0.4,
             fill = col, alpha = 0.4, color = NA),
    annotate("rect", xmin = cx + s*0.3 - pw, xmax = cx + s*0.3 + pw,
             ymin = cy - s*0.6, ymax = cy + s*0.4,
             fill = col, alpha = 0.4, color = NA),
    annotate("rect", xmin = cx + s*0.8 - pw, xmax = cx + s*0.8 + pw,
             ymin = cy - s*0.6, ymax = cy + s*0.4,
             fill = col, alpha = 0.4, color = NA),
    # Base
    annotate("rect", xmin = cx - s*1.05, xmax = cx + s*1.05,
             ymin = cy - s*0.7, ymax = cy - s*0.6,
             fill = col, alpha = 0.5, color = NA)
  )
}

# Wave (streaming)
icon_wave <- function(cx = 8, cy = 2.8, s = 1, col = cyan) {
  xs <- seq(-1.2, 1.2, length.out = 60) * s
  ys1 <- sin(xs / s * 3) * s * 0.4
  ys2 <- sin(xs / s * 3 + 1) * s * 0.3
  list(
    geom_path(data = data.frame(x = cx + xs, y = cy + ys1 + s*0.3),
              aes(x = x, y = y), color = col, linewidth = 2, alpha = 0.7,
              inherit.aes = FALSE),
    geom_path(data = data.frame(x = cx + xs, y = cy + ys2 - s*0.3),
              aes(x = x, y = y), color = col, linewidth = 1.2, alpha = 0.4,
              inherit.aes = FALSE),
    # Dots on peaks
    annotate("point",
             x = cx + s * c(-0.9, 0, 0.9),
             y = cy + s * c(0.7, 0.7, 0.7),
             size = 2.5, color = col, alpha = 0.6)
  )
}

# Flask / test tube (MLflow)
icon_flask <- function(cx = 8, cy = 2.8, s = 1, col = green) {
  list(
    # Neck
    annotate("rect", xmin = cx - s*0.15, xmax = cx + s*0.15,
             ymin = cy + s*0.2, ymax = cy + s*0.9,
             fill = col, alpha = 0.4, color = col, linewidth = 0.5),
    # Rim
    annotate("rect", xmin = cx - s*0.25, xmax = cx + s*0.25,
             ymin = cy + s*0.85, ymax = cy + s*0.95,
             fill = col, alpha = 0.6, color = NA),
    # Body (trapezoid)
    annotate("polygon",
             x = cx + s * c(-0.15, -0.7, 0.7, 0.15),
             y = cy + s * c(0.2, -0.7, -0.7, 0.2),
             fill = col, alpha = 0.25, color = col, linewidth = 0.5),
    # Liquid
    annotate("polygon",
             x = cx + s * c(-0.5, -0.7, 0.7, 0.5),
             y = cy + s * c(-0.2, -0.7, -0.7, -0.2),
             fill = col, alpha = 0.4, color = NA),
    # Bubbles
    annotate("point", x = cx + s*c(-0.2, 0.15, 0.0),
             y = cy + s*c(-0.4, -0.5, -0.25),
             size = c(1.5, 2, 1), color = white, alpha = 0.5)
  )
}

# DNA / helix (feature engineering)
icon_helix <- function(cx = 8, cy = 2.8, s = 1, col = blue) {
  ys <- seq(-1.0, 1.0, length.out = 50) * s
  xs1 <- sin(ys / s * 3) * s * 0.5
  xs2 <- -xs1
  list(
    geom_path(data = data.frame(x = cx + xs1, y = cy + ys),
              aes(x = x, y = y), color = col, linewidth = 1.8, alpha = 0.6,
              inherit.aes = FALSE),
    geom_path(data = data.frame(x = cx + xs2, y = cy + ys),
              aes(x = x, y = y), color = col, linewidth = 1.8, alpha = 0.4,
              inherit.aes = FALSE),
    # Cross bars
    annotate("segment",
             x = cx + sin(c(-0.6, 0, 0.6) * 3) * s * 0.5,
             xend = cx - sin(c(-0.6, 0, 0.6) * 3) * s * 0.5,
             y = cy + s * c(-0.6, 0, 0.6),
             yend = cy + s * c(-0.6, 0, 0.6),
             color = col, alpha = 0.3, linewidth = 0.5)
  )
}

# Layers (architecture)
icon_layers <- function(cx = 8, cy = 2.8, s = 1, col = purple) {
  list(
    # Layer 3 (top)
    annotate("polygon",
             x = cx + s * c(-1.0, 0, 1.0, 0),
             y = cy + s * c(0.6, 1.0, 0.6, 0.2),
             fill = col, alpha = 0.5, color = col, linewidth = 0.5),
    # Layer 2
    annotate("polygon",
             x = cx + s * c(-1.0, 0, 1.0, 0),
             y = cy + s * c(0.1, 0.5, 0.1, -0.3),
             fill = col, alpha = 0.35, color = col, linewidth = 0.5),
    # Layer 1 (bottom)
    annotate("polygon",
             x = cx + s * c(-1.0, 0, 1.0, 0),
             y = cy + s * c(-0.4, 0.0, -0.4, -0.8),
             fill = col, alpha = 0.2, color = col, linewidth = 0.5)
  )
}

# Contract / handshake
icon_contract <- function(cx = 8, cy = 2.8, s = 1, col = orange3) {
  list(
    # Paper
    annotate("rect", xmin = cx - s*0.6, xmax = cx + s*0.6,
             ymin = cy - s*0.8, ymax = cy + s*0.8,
             fill = white, alpha = 0.8, color = col, linewidth = 0.8),
    # Lines on paper
    annotate("segment",
             x = rep(cx - s*0.4, 4), xend = cx + s * c(0.4, 0.4, 0.3, 0.2),
             y = cy + s * c(0.5, 0.25, 0.0, -0.25),
             yend = cy + s * c(0.5, 0.25, 0.0, -0.25),
             color = col, alpha = 0.3, linewidth = 0.5),
    # Seal / stamp circle
    annotate("point", x = cx + s*0.2, y = cy - s*0.55,
             size = s*6, color = col, alpha = 0.4, shape = 16),
    # Check
    annotate("segment", x = cx + s*0.1, xend = cx + s*0.18,
             y = cy - s*0.58, yend = cy - s*0.65, color = white, linewidth = 0.8),
    annotate("segment", x = cx + s*0.18, xend = cx + s*0.35,
             y = cy - s*0.65, yend = cy - s*0.45, color = white, linewidth = 0.8)
  )
}

# Network / mesh nodes
icon_mesh <- function(cx = 8, cy = 2.8, s = 1, col = green) {
  nodes <- data.frame(
    x = cx + s * c(-0.8, 0.0, 0.8, -0.5, 0.5, 0.0),
    y = cy + s * c(0.5, 0.8, 0.5, -0.3, -0.3, -0.8)
  )
  edges <- data.frame(
    x    = nodes$x[c(1,1,2,2,3,4,4,5)],
    xend = nodes$x[c(2,4,3,5,5,5,6,6)],
    y    = nodes$y[c(1,1,2,2,3,4,4,5)],
    yend = nodes$y[c(2,4,3,5,5,5,6,6)]
  )
  list(
    geom_segment(data = edges, aes(x = x, xend = xend, y = y, yend = yend),
                 color = col, alpha = 0.3, linewidth = 0.6, inherit.aes = FALSE),
    geom_point(data = nodes, aes(x = x, y = y), color = col, size = 4,
               alpha = 0.7, inherit.aes = FALSE)
  )
}

# Container / whale shape
icon_container <- function(cx = 8, cy = 2.8, s = 1, col = blue) {
  bw <- s * 0.3; gap <- s * 0.05
  list(
    # Container body
    annotate("rect", xmin = cx - s*0.9, xmax = cx + s*0.9,
             ymin = cy - s*0.3, ymax = cy + s*0.5,
             fill = col, alpha = 0.3, color = col, linewidth = 0.8),
    # Smaller containers on top (like Docker whale)
    annotate("rect", xmin = cx - s*0.55, xmax = cx - s*0.55 + bw,
             ymin = cy + s*0.55, ymax = cy + s*0.85,
             fill = col, alpha = 0.5, color = col, linewidth = 0.4),
    annotate("rect", xmin = cx - s*0.2, xmax = cx - s*0.2 + bw,
             ymin = cy + s*0.55, ymax = cy + s*0.85,
             fill = col, alpha = 0.5, color = col, linewidth = 0.4),
    annotate("rect", xmin = cx + s*0.15, xmax = cx + s*0.15 + bw,
             ymin = cy + s*0.55, ymax = cy + s*0.85,
             fill = col, alpha = 0.5, color = col, linewidth = 0.4),
    annotate("rect", xmin = cx + s*0.5, xmax = cx + s*0.5 + bw,
             ymin = cy + s*0.55, ymax = cy + s*0.85,
             fill = col, alpha = 0.5, color = col, linewidth = 0.4),
    # Water line
    geom_path(data = data.frame(
      x = cx + seq(-1.2, 1.2, length.out = 30) * s,
      y = cy - s*0.3 + sin(seq(0, 4*pi, length.out = 30)) * s * 0.06),
      aes(x = x, y = y), color = col, alpha = 0.3, linewidth = 0.5,
      inherit.aes = FALSE)
  )
}

# Gear
icon_gear <- function(cx = 8, cy = 2.8, s = 1, col = orange2) {
  n_teeth <- 8
  angles <- seq(0, 2*pi, length.out = n_teeth * 2 + 1)
  r_outer <- s * 0.9
  r_inner <- s * 0.65
  radii <- rep(c(r_outer, r_inner), n_teeth)
  radii <- c(radii, r_outer)
  xs <- cx + radii * cos(angles)
  ys <- cy + radii * sin(angles)
  list(
    annotate("polygon", x = xs, y = ys,
             fill = col, alpha = 0.3, color = col, linewidth = 0.8),
    # Center hole
    annotate("point", x = cx, y = cy, size = s*6,
             color = cream, shape = 16),
    annotate("point", x = cx, y = cy, size = s*3,
             color = col, alpha = 0.4, shape = 16)
  )
}

# Database cylinder
icon_database <- function(cx = 8, cy = 2.8, s = 1, col = cyan) {
  a <- seq(0, 2*pi, length.out = 60)
  rw <- s * 0.8; rh <- s * 0.2
  list(
    # Side walls
    annotate("rect", xmin = cx - rw, xmax = cx + rw,
             ymin = cy - s*0.7, ymax = cy + s*0.7,
             fill = col, alpha = 0.15, color = NA),
    annotate("segment", x = cx - rw, xend = cx - rw,
             y = cy - s*0.7, yend = cy + s*0.7,
             color = col, linewidth = 0.8, alpha = 0.6),
    annotate("segment", x = cx + rw, xend = cx + rw,
             y = cy - s*0.7, yend = cy + s*0.7,
             color = col, linewidth = 0.8, alpha = 0.6),
    # Top ellipse
    geom_path(data = data.frame(x = cx + rw * cos(a), y = cy + s*0.7 + rh * sin(a)),
              aes(x = x, y = y), color = col, linewidth = 0.8, alpha = 0.7,
              inherit.aes = FALSE),
    geom_polygon(data = data.frame(x = cx + rw * cos(a), y = cy + s*0.7 + rh * sin(a)),
                 aes(x = x, y = y), fill = col, alpha = 0.2, inherit.aes = FALSE),
    # Bottom half-ellipse
    geom_path(data = data.frame(x = cx + rw * cos(a[a >= pi]),
                                 y = cy - s*0.7 + rh * sin(a[a >= pi])),
              aes(x = x, y = y), color = col, linewidth = 0.8, alpha = 0.5,
              inherit.aes = FALSE),
    # Mid ring
    geom_path(data = data.frame(x = cx + rw * cos(a), y = cy + rh * sin(a)),
              aes(x = x, y = y), color = col, linewidth = 0.4, alpha = 0.3,
              inherit.aes = FALSE)
  )
}

# Flow / pipeline arrows
icon_flow <- function(cx = 8, cy = 2.8, s = 1, col = green) {
  list(
    # Three horizontal arrows at different heights
    annotate("segment", x = cx - s*1.0, xend = cx + s*0.6,
             y = cy + s*0.5, yend = cy + s*0.5,
             color = col, alpha = 0.6, linewidth = 1.2,
             arrow = arrow(length = unit(0.12, "inches"), type = "closed")),
    annotate("segment", x = cx - s*0.7, xend = cx + s*0.9,
             y = cy, yend = cy,
             color = col, alpha = 0.4, linewidth = 1.2,
             arrow = arrow(length = unit(0.12, "inches"), type = "closed")),
    annotate("segment", x = cx - s*0.4, xend = cx + s*1.2,
             y = cy - s*0.5, yend = cy - s*0.5,
             color = col, alpha = 0.25, linewidth = 1.2,
             arrow = arrow(length = unit(0.12, "inches"), type = "closed")),
    # Source dot
    annotate("point", x = cx - s*1.0, y = cy + s*0.5,
             size = 3, color = col, alpha = 0.7)
  )
}

# Grid / matrix
icon_grid <- function(cx = 8, cy = 2.8, s = 1, col = purple) {
  set.seed(42)
  cells <- expand.grid(r = 1:4, c = 1:4)
  cells$x <- cx + (cells$c - 2.5) * s * 0.42
  cells$y <- cy + (cells$r - 2.5) * s * 0.42
  cells$alpha <- runif(16, 0.15, 0.7)
  anns <- list()
  for (i in 1:nrow(cells)) {
    anns <- c(anns, list(
      annotate("rect",
               xmin = cells$x[i] - s*0.17, xmax = cells$x[i] + s*0.17,
               ymin = cells$y[i] - s*0.17, ymax = cells$y[i] + s*0.17,
               fill = col, alpha = cells$alpha[i], color = cream, linewidth = 0.3)
    ))
  }
  anns
}


# ============================================================
# MAIN CARD GENERATOR
# ============================================================

generate_card <- function(number, title, subtitle, category, date_str,
                          accent_color, icon_fn, out_path) {

  date_fmt <- tryCatch(format(as.Date(date_str), "%d %b %Y"), error = function(e) date_str)

  dots <- expand.grid(x = seq(0.3, 9.7, by = 0.5), y = seq(1.1, 5.0, by = 0.5))

  base <- list(
    annotate("rect", xmin = 0, xmax = 10, ymin = 0, ymax = 5.25,
             fill = cream, color = NA),
    annotate("rect", xmin = 6, xmax = 10, ymin = 0, ymax = 5.25,
             fill = cream2, alpha = 0.6, color = NA),
    geom_point(data = dots, aes(x = x, y = y), color = gray3, alpha = 0.12,
               size = 0.2, inherit.aes = FALSE),
    annotate("rect", xmin = 0, xmax = 10, ymin = 5.15, ymax = 5.25,
             fill = accent_color, color = NA),
    annotate("rect", xmin = 0, xmax = 0.08, ymin = 0, ymax = 5.15,
             fill = accent_color, color = NA),
    # Number badge
    annotate("rect", xmin = 0.4, xmax = 2.0, ymin = 3.9, ymax = 5.0,
             fill = accent_color, color = NA),
    annotate("text", x = 1.2, y = 4.45, label = number,
             color = white, size = 10, fontface = "bold"),
    # Category
    annotate("label", x = 2.3, y = 4.45, label = paste0(" ", category, " "),
             hjust = 0, size = 2.2, color = navy, fill = cream2,
             fontface = "bold", label.size = 0.3, label.padding = unit(0.3, "lines"),
             label.r = unit(0.2, "lines"), label.colour = gray3),
    # Title
    annotate("text", x = 0.5, y = 3.3, label = title,
             hjust = 0, vjust = 1, size = 6.5, color = navy,
             fontface = "bold", lineheight = 0.85),
    # Subtitle
    annotate("text", x = 0.5, y = 1.6, label = subtitle,
             hjust = 0, vjust = 1, size = 3, color = gray1,
             lineheight = 1.0),
    # Accent glow behind icon
    annotate("point", x = 8.0, y = 2.8, size = 55,
             color = accent_color, alpha = 0.06),
    annotate("point", x = 8.0, y = 2.8, size = 35,
             color = accent_color, alpha = 0.04),
    # Bottom bar
    annotate("rect", xmin = 0, xmax = 10, ymin = 0, ymax = 0.85,
             fill = navy, color = NA),
    annotate("text", x = 0.4, y = 0.45,
             label = "Spark de Ideas  \u00b7  mauroloprete.github.io/mauroloprete",
             hjust = 0, size = 2.8, color = orange, fontface = "italic"),
    annotate("text", x = 9.7, y = 0.45, label = date_fmt,
             hjust = 1, size = 2.5, color = gray2),
    annotate("segment", x = 0, xend = 10, y = 0.85, yend = 0.85,
             color = accent_color, linewidth = 0.5)
  )

  icon_elements <- icon_fn()

  p <- ggplot()
  for (el in c(base, icon_elements)) p <- p + el

  p <- p +
    coord_cartesian(xlim = c(0, 10), ylim = c(0, 5.25)) +
    theme_void() +
    theme(plot.background = element_rect(fill = cream, color = gray3, linewidth = 0.5),
          plot.margin = margin(0, 0, 0, 0))

  ggsave(out_path, p, width = 8, height = 4.18, dpi = 300, bg = cream)
  message("Generated: ", out_path)
}


# ============================================================
# POST DATA
# ============================================================
base_dir <- "blog/posts"

posts <- list(
  list("spark-de-ideas-intro", "01",
       "Spark de Ideas: la chispa\nde la ingeniería de datos",
       "Podcast de Data Engineering en español.\nDatabricks \u00b7 Arquitectura \u00b7 MLOps",
       "Podcast", "2025-08-18", orange,
       function() icon_lightning(s = 1.2, col = orange)),
  list("fundamentals-data-engineering", "02",
       "Fundamentals of Data\nEngineering",
       "Review del libro de Joe Reis & Matt Housley.\nCiclo de vida del dato y arquitecturas clave",
       "Book Review", "2025-08-26", blue,
       function() icon_book(s = 1.2, col = blue)),
  list("dataops-pipelines", "03",
       "DataOps: cómo llevar tus\npipelines al siguiente nivel",
       "Automatización, observabilidad, colaboración\ny errores comunes en producción",
       "DataOps", "2025-09-01", green,
       function() icon_cycle(s = 1.2, col = green)),
  list("data-engineering-design-patterns", "04",
       "Data Engineering\nDesign Patterns",
       "Los 8 patrones de ingesta de Konieczny.\nEjemplos en PySpark/SQL + Medallion",
       "Book Review", "2025-09-15", purple,
       function() icon_puzzle(s = 1.2, col = purple)),
  list("si-arrancara-de-cero", "05",
       "Si empezara de cero...\nqué priorizaría en Data Eng",
       "Python \u2192 SQL \u2192 Spark \u2192 dbt \u2192 Databricks.\nEl orden importa",
       "Carrera", "2026-02-17", orange,
       function() icon_rocket(s = 1.2, col = orange)),
  list("databricks-asset-bundles-advanced", "06",
       "Databricks Tips #1:\nAsset Bundles avanzado",
       "Patrones de deployment, variables\ncomplejas y trucos en producción",
       "Databricks Tips", "2026-02-24", orange2,
       function() icon_box(s = 1.2, col = orange2)),
  list("databricks-tips-01-delta-lake", "07",
       "Databricks Tips #2:\n7 cosas de Delta Lake",
       "Liquid clustering, OPTIMIZE, vacuum,\ntime travel y trucos que cambian todo",
       "Delta Lake", "2026-03-03", orange3,
       function() icon_delta(s = 1.2, col = orange3)),
  list("databricks-tips-02-unity-catalog", "08",
       "Databricks Tips #3:\nUnity Catalog",
       "Namespace 3 niveles, GRANTS, linaje\nautomático y row/column security",
       "Governance", "2026-03-10", purple,
       function() icon_columns(s = 1.2, col = purple)),
  list("databricks-tips-03-structured-streaming", "09",
       "Databricks Tips #4:\nStructured Streaming",
       "Watermarks, triggers, foreachBatch\ny las trampas del micro-batch",
       "Streaming", "2026-03-17", cyan,
       function() icon_wave(s = 1.2, col = cyan)),
  list("databricks-tips-04-mlflow-unity-catalog", "10",
       "Databricks Tips #5:\nMLflow + Unity Catalog",
       "Registro en UC, aliases vs stages,\nlinaje dato\u2192modelo y model serving",
       "MLOps", "2026-03-24", green,
       function() icon_flask(s = 1.3, col = green)),
  list("databricks-tips-05-feature-engineering", "11",
       "Databricks Tips #6:\nFeature Engineering",
       "Feature Store, point-in-time lookups,\nonline features y data leakage",
       "Machine Learning", "2026-03-31", blue,
       function() icon_helix(s = 1.2, col = blue)),
  list("data-modeling-medallion-vault-kimball", "12",
       "Medallion vs Data Vault\nvs Kimball",
       "Comparativa práctica de los tres modelos.\nTrade-offs y guía para elegir",
       "Data Architecture", "2026-04-07", purple,
       function() icon_layers(s = 1.3, col = purple)),
  list("data-contracts-framework", "13",
       "Data Contracts: cómo\ndiseñar un framework",
       "Qué son, por qué los necesitás,\ny cómo implementarlos con Databricks",
       "Data Architecture", "2026-04-14", orange3,
       function() icon_contract(s = 1.3, col = orange3)),
  list("data-mesh-practica", "14",
       "Data Mesh en la práctica:\nlo que funciona y lo que no",
       "Los 4 principios, implementación real\ncon Unity Catalog y errores comunes",
       "Data Architecture", "2026-04-21", green,
       function() icon_mesh(s = 1.4, col = green)),
  list("databricks-tips-06-docker-containers", "15",
       "Databricks Tips #7:\nDocker en Databricks",
       "Container Services, imágenes custom,\ngolden containers y CI/CD",
       "Databricks Tips", "2026-05-30", blue,
       function() icon_container(s = 1.3, col = blue)),
  list("databricks-tips-08-jobs-workflows", "16",
       "Databricks Tips #8:\nJobs & Workflows",
       "File arrival triggers, Trigger.AvailableNow,\nJob Clusters y limitaciones reales",
       "Databricks Tips", "2026-06-09", orange2,
       function() icon_gear(s = 1.2, col = orange2)),
  list("databricks-tips-09-sql-warehouses", "17",
       "Databricks Tips #9:\nSQL Warehouses",
       "Classic vs Pro vs Serverless. Photon,\nQuery Federation, AI Functions y costos",
       "Serverless", "2026-06-16", cyan,
       function() icon_database(s = 1.3, col = cyan)),
  list("databricks-tips-10-lakeflow-declarative-pipelines", "18",
       "Databricks Tips #10:\nLakeflow Pipelines",
       "Streaming tables, expectations, CDC\ncon SCD Type 1/2 y serverless",
       "Databricks Tips", "2026-06-23", green,
       function() icon_flow(s = 1.3, col = green)),
  list("databricks-tips-11-ai-gateway", "19",
       "Databricks Tips #11:\nUnity AI Gateway",
       "Rate limiting, guardrails, cost attribution,\nfallbacks y traffic splitting",
       "MLOps", "2026-06-30", orange,
       function() icon_shield(s = 1.2, col = orange))
)

for (p in posts) {
  generate_card(
    number = p[[2]], title = p[[3]], subtitle = p[[4]],
    category = p[[5]], date_str = p[[6]],
    accent_color = p[[7]], icon_fn = p[[8]],
    out_path = file.path(base_dir, p[[1]], "linkedin.png")
  )
}

message("\nDone! Generated ", length(posts), " LinkedIn cards (pure vector, 300 DPI).")

"""Figures for the report: flower field, convergence curve, best tour. """

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from config import BEEHIVE_POSITION

SURFACE = "#FBF6EC"
INK = "#3E2A17"
MUTED = "#8A7256"
GRID = "#E7DCC8"
FLOWER = "#C2456E"
HONEY = "#C97B0A"

def style(ax, title, subtitle):
    """Shared look: honey surface, recessive grid, left-aligned title."""
    ax.set_facecolor(SURFACE)
    ax.figure.set_facecolor(SURFACE)
    ax.grid(color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.set_title(title, color=INK, fontsize=14,
fontweight="bold", loc="left", pad=18)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes,
color=MUTED, fontsize=10, va="bottom")

def draw_hive(ax, label):
    """The beehive marker, identical on every map."""
    ax.scatter(*BEEHIVE_POSITION, s=520, marker="H", color=HONEY,
               edgecolor=INK, linewidth=1.2, label="Beehive", zorder=3)
    ax.annotate(label, BEEHIVE_POSITION, xytext=(14, 14), textcoords="offset points",
                color=INK, fontsize=10, fontweight="bold")

def plot_field(flowers, path="figures/field.png"):
    """Scatter plot of the flower field"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 6.5))

    ax.scatter(flowers[:, 0], flowers[:, 1], s=55, color=FLOWER,
               edgecolors=SURFACE, linewidth=1.0, label="Flowers", zorder=2)
    draw_hive(ax, "Beehive")

    style(ax, "The flower field", f"{len(flowers)} flowers around the hive")
    ax.set_xlabel("x", color=MUTED)
    ax.set_ylabel("y", color=MUTED)
    ax.set_aspect("equal")

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)

def plot_convergence(history, path="figures/convergence.png"):
    """Colony average and best bee, generation by generation"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    averages = np.array([average for average, _ in history])
    bests = np.array([best for _, best in history])
    generations = np.arange(len(history))

    fig,ax = plt.subplots(figsize=(8, 5))
    ax.plot(generations, averages, color=HONEY, linewidth=2.2, label="Colony average")
    ax.plot(generations, bests, color=FLOWER, linewidth=2.2, label="Best bee")
    ax.annotate(f"{averages[-1]:.0f}", (generations[-1], averages[-1]),
                xytext=(8, 2), textcoords="offset points",
                color=HONEY, fontsize=10, fontweight="bold")
    ax.annotate(f"{bests[-1]:.0f}", (generations[-1], bests[-1]),
                xytext=(8, -4), textcoords="offset points",
                color=FLOWER, fontsize=10, fontweight="bold")
    style(ax, "Convergence",
          f"from {averages[0]:.0f} down to {bests[-1]:.0f} in {len(history) - 1} generations")
    ax.set_xlabel("Generation", color=MUTED)
    ax.set_ylabel("Trip length", color=MUTED)
    ax.set_xlim(0, len(history) - 1 + 6)
    ax.legend(frameon=False, labelcolor=INK)

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)

def plot_tour(flowers, order, length, path="figures/tour.png"):
    """The best route found, hive to hive"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    points = np.vstack([BEEHIVE_POSITION, flowers[order], BEEHIVE_POSITION])

    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.plot(points[:, 0], points[:, 1], color=HONEY, linewidth=1.8,
            solid_capstyle="round", zorder=1)
    ax.scatter(flowers[:, 0], flowers[:, 1], s=55, color=FLOWER,
               edgecolor=SURFACE, linewidth=1.0, label="Flowers", zorder=2)
    draw_hive(ax, "start / end")

    style(ax, "Best route found",
          f"{length:.0f} units, {len(order)} flowers, one visit each")
    ax.set_xlabel("x", color=MUTED)
    ax.set_ylabel("y", color=MUTED)
    ax.set_aspect("equal")

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


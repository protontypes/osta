import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from matplotlib.ticker import MaxNLocator
from pathlib import Path

def compute_ages_from_dates(dates, ref_date=None):
    """Compute project ages (years) from creation dates."""
    if ref_date is None:
        ref_date = dt.date.today()
    ages = []
    for d in dates:
        if pd.isna(d):
            continue
        if isinstance(d, str):
            try:
                d = dt.date.fromisoformat(d[:10])
            except Exception:
                continue
        if isinstance(d, dt.datetime):
            d = d.date()
        if isinstance(d, dt.date):
            ages.append((ref_date - d).days / 365.25)
    return np.array(ages)

def plot_project_age_histogram(ages, title="Project age distribution (years)",
                               palette=None, figsize=(10,6), show=True):
    """Draw histogram of project ages with OpenSustain.tech-inspired palette (1-year bins)."""
    if palette is None:
        palette = {
            "primary": "#2b7a4b",   # deep green
            "secondary": "#88c057", # light/leaf green
            "accent": "#0a6b8a",    # teal
            "bg": "#f5f7f6",        # off-white
            "text": "#033141"       # dark teal
        }

    ages = np.asarray(ages, dtype=float)
    max_age = np.ceil(np.max(ages))  # round up to full years
    bins = np.arange(0, max_age + 1, 1)  # 1-year bin size

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(palette["bg"])
    ax.set_facecolor(palette["bg"])

    counts, bins_, patches = ax.hist(ages, bins=bins, edgecolor=palette["text"],
                                     linewidth=0.8, alpha=0.95, zorder=3)

    # Apply gradient bar colors
    n_patches = len(patches)
    for i, p in enumerate(patches):
        t = i / max(1, n_patches - 1)
        r1, g1, b1 = tuple(int(palette["primary"].lstrip("#")[j:j+2], 16) for j in (0,2,4))
        r2, g2, b2 = tuple(int(palette["secondary"].lstrip("#")[j:j+2], 16) for j in (0,2,4))
        r = int(r1*(1-t) + r2*t)
        g = int(g1*(1-t) + g2*t)
        b = int(b1*(1-t) + b2*t)
        p.set_facecolor(f"#{r:02x}{g:02x}{b:02x}")
        p.set_alpha(0.95)

    ax.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.6, zorder=0)
    ax.set_title(title, fontsize=16, fontweight="bold", color=palette["text"], pad=12)
    ax.set_xlabel("Age (years)", fontsize=12, color=palette["text"])
    ax.set_ylabel("Number of projects", fontsize=12, color=palette["text"])
    ax.tick_params(colors=palette["text"])
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlim(left=0)

    mean_age = np.mean(ages)
    median_age = np.median(ages)
    ax.axvline(mean_age, color=palette["accent"], linestyle="-", linewidth=2,
               label=f"mean = {mean_age:.2f} yr", zorder=4)
    ax.axvline(median_age, color=palette["text"], linestyle=":", linewidth=2,
               label=f"median = {median_age:.2f} yr", zorder=4)
    ax.legend(frameon=False, fontsize=11, loc="upper right")

    for spine in ax.spines.values():
        spine.set_visible(False)

    # Annotate top bars
    top_idxs = np.argsort(counts)[-3:][::-1]
    for idx in top_idxs:
        if counts[idx] <= 0:
            continue
        bin_center = 0.5 * (bins_[idx] + bins_[idx + 1])
        ax.annotate(f"{int(counts[idx])}", xy=(bin_center, counts[idx]),
                    xytext=(0, 6), textcoords="offset points",
                    ha="center", va="bottom", fontsize=10,
                    color=palette["text"], fontweight="bold")

    plt.tight_layout()
    if show:
        plt.show()
    return fig


# ------------- MAIN EXECUTION -------------
def main(csv_path):
    """Load CSV, compute ages from project_created_at, and plot histogram."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {csv_path}")

    df = pd.read_csv(path)
    if "project_created_at" not in df.columns:
        raise ValueError("CSV must contain a 'project_created_at' column.")

    ages = compute_ages_from_dates(df["project_created_at"])
    print(f"Loaded {len(df)} projects, {len(ages)} valid creation dates.")
    print(f"Average age: {np.mean(ages):.2f} years")

    plot_project_age_histogram(ages, title="OpenSustain.tech - Project Age - October 2025")

# Example: Uncomment and run
main("projects.csv")

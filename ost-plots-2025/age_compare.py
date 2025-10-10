import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from pathlib import Path

# ---------- HELPER FUNCTIONS ----------

def compute_ages_from_dates(dates, ref_date=None):
    """Compute project ages (years) from creation dates (vectorized, aligned)."""
    if ref_date is None:
        ref_date = dt.date.today()

    parsed_dates = pd.to_datetime(dates, errors="coerce")
    ages = (ref_date - parsed_dates.dt.date).apply(
        lambda d: d.days / 365.25 if pd.notna(d) else np.nan
    )
    return ages


def load_current_data(csv_path):
    """Load the current CSV and compute project ages from project_created_at."""
    df = pd.read_csv(csv_path)
    if "project_created_at" not in df.columns:
        raise ValueError("Current CSV must contain a 'project_created_at' column.")
    df["age_years"] = compute_ages_from_dates(df["project_created_at"])
    df = df.dropna(subset=["age_years"])
    return df


def load_older_data(csv_path, ref_date_current=None, ref_date_old=None):
    """Load the October 2022 CSV and convert project_age_in_days to years, adjusted for age offset."""
    df = pd.read_csv(csv_path)
    if "project_age_in_days" not in df.columns:
        raise ValueError("Older CSV must contain a 'project_age_in_days' column.")
    
    df["age_years"] = df["project_age_in_days"] / 365.25

    # --- Apply offset so 2022 ages reflect how old those projects are today ---
    if ref_date_current is None:
        ref_date_current = dt.date.today()
    if ref_date_old is None:
        ref_date_old = dt.date(2022, 10, 1)  # approximate date of the 2022 dataset

    offset_years = (ref_date_current - ref_date_old).days / 365.25
    df["age_years"] = df["age_years"] + offset_years

    df = df.dropna(subset=["age_years"])
    return df


# ---------- PLOTTING FUNCTION ----------

def plot_age_histogram_comparison(df_current, df_old,
                                  title="Project Age Distribution (2022 vs Current, Age-Adjusted)",
                                  palette=None, figsize=(10,6), show=True):
    """Plot overall project age histogram for current vs old datasets with age offset."""
    if palette is None:
        palette = {
            "current": "#2b7a4a64",   # deep green (current)
            "old": "#e07b7b",       # light red (old)
            "accent": "#0a6b8a",    # teal for mean line
            "bg": "#f5f7f6",        # off-white
            "text": "#033141"       # dark teal
        }

    ages_now = df_current["age_years"].dropna()
    ages_old = df_old["age_years"].dropna()

    max_age = np.ceil(max(ages_now.max(), ages_old.max()))
    bins = np.arange(0, max_age + 1, 1)  # 1-year bins

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(palette["bg"])
    ax.set_facecolor(palette["bg"])

    # Plot older data (age-adjusted)
    ax.hist(ages_old, bins=bins, color=palette["old"], edgecolor=palette["text"],
            alpha=0.5, label="Oct 2022 (age-adjusted)", zorder=2)

    # Plot current data
    ax.hist(ages_now, bins=bins, color=palette["current"], edgecolor=palette["text"],
            alpha=0.5, label="Current", zorder=3)

    # Add mean/median lines for current data
    mean_age = np.mean(ages_now)
    median_age = np.median(ages_now)
    ax.axvline(mean_age, color=palette["accent"], linestyle="-", linewidth=2,
               label=f"mean = {mean_age:.2f} yr", zorder=4)
    ax.axvline(median_age, color=palette["text"], linestyle=":", linewidth=2,
               label=f"median = {median_age:.2f} yr", zorder=4)

    # Style
    ax.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.6, zorder=0)
    ax.set_title(title, fontsize=16, fontweight="bold", color=palette["text"], pad=12)
    ax.set_xlabel("Project Age (years)", fontsize=12, color=palette["text"])
    ax.set_ylabel("Number of Projects", fontsize=12, color=palette["text"])
    ax.tick_params(colors=palette["text"])
    ax.set_xlim(left=0)

    ax.legend(frameon=False, fontsize=11, loc="upper right")
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    if show:
        plt.show()
    return fig


# ---------- MAIN EXECUTION ----------

def main(current_csv, old_csv):
    """Load both datasets and plot overall project age distributions (offset-adjusted)."""
    path_current = Path(current_csv)
    path_old = Path(old_csv)
    if not path_current.exists() or not path_old.exists():
        raise FileNotFoundError("One or both CSV files not found.")

    df_current = load_current_data(path_current)
    df_old = load_older_data(path_old)

    print(f"Loaded {len(df_current)} current projects.")
    print(f"Loaded {len(df_old)} older projects (Oct 2022, adjusted by ~3 years).")

    plot_age_histogram_comparison(df_current, df_old)

# Example usage:
main("projects_2025.csv", "projects_2022.csv")

# ==========================
# TAB 5: Stats Overview
# ==========================
with st.tab("📋 Stats Overview"):
    st.header("Project Statistics Overview")

    # Compute some metrics from CSV
    total_projects = df["project_names"].count()
    total_stars = df["stars"].sum()
    total_contributors = df["contributors"].sum()
    median_commits = df["total_commits"].median()
    median_stars = df["stars"].median()
    median_dds = df["dds"].median()
    median_contributors = df["contributors"].median()
    median_age = round(df["project_age"].median(), 2)
    median_downloads = df["downloads_last_month"].median()

    # Count by platform
    platforms = df["platform"].value_counts()
    github_projects = platforms.get("github", 0)
    gitlab_projects = platforms.get("gitlab", 0)
    other_projects = platforms.get("custom", 0)

    # Prepare table
    stats_labels = [
        "Total number of projects",
        "GitHub projects",
        "GitLab projects",
        "Other platforms",
        "Total stars of all projects",
        "Total contributors",
        "Median number of commits",
        "Median stargazers",
        "Median Development Distribution Score",
        "Median number of contributors",
        "Median downloads last month",
        "Median age in years",
    ]

    stats_values = [
        total_projects,
        github_projects,
        gitlab_projects,
        other_projects,
        total_stars,
        total_contributors,
        median_commits,
        median_stars,
        round(median_dds, 4),
        median_contributors,
        median_downloads,
        median_age,
    ]

    import plotly.graph_objects as go

    fig_stats = go.Figure(
        data=[
            go.Table(
                columnwidth=[300, 100],
                header=dict(
                    values=["Dimension", "Value"],
                    line_color="#000000",
                    fill_color="#ffffff",
                    font_size=18,
                ),
                cells=dict(
                    fill_color="#ffffff",
                    line_color="#ffffff",
                    font_size=16,
                    height=30,
                    values=[stats_labels, stats_values],
                ),
            )
        ]
    )

    fig_stats.update_layout(height=600, margin=dict(l=5, r=5, b=0, t=5), dragmode=False)

    st.plotly_chart(fig_stats, use_container_width=True)

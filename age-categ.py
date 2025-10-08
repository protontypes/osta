import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timezone
import numpy as np

# Load dataset
df = pd.read_csv("projects.csv")

# Convert and calculate project age
df['project_created_at'] = pd.to_datetime(df['project_created_at'], utc=True)
now_utc = datetime.now(timezone.utc)
df['project_age'] = (now_utc - df['project_created_at']).dt.total_seconds() / (365.25 * 24 * 3600)

# Rename and sort
df.rename(columns={'project_sub_category': 'sub_category', 'project_topic': 'category'}, inplace=True)
df['category_sub'] = df['category'] + ": " + df['sub_category']
df = df.sort_values(['category', 'sub_category']).reset_index(drop=True)

df['contributors'] = df['contributors'].fillna(1)  # ensures no zero-size dots
df['contributors_size'] = np.sqrt(df['contributors']) * 20

# OpenSustain palette (one color per category)
category_colors = {
    cat: color for cat, color in zip(
        df['category'].unique(),
        ["#099ec8", "#84bc41", "#f9c416", "#9cd8e9", "#cde4b3",
         "#f7a600", "#00a0a6", "#00689d", "#009639", "#ffcc00",
         "#a3d55d", "#2cb5e8", "#f46f1b", "#c50084", "#004c97"]
    )
}

fig = px.scatter(
    df,
    x="project_age",
    y="category_sub",
    color="category",          # <-- color by category
    color_discrete_map=category_colors,
    size="contributors_size",  # dot size by number of contributors
    size_max=50,               # maximum dot size
    hover_data={
        "project_names": True,
        "project_age": ':.1f',
        "category": True,
        "sub_category": True,
        "git_url": True,
        "description": True,
        "contributors": True
    },
    labels={"project_age": "Project Age (Years)", "category_sub": ""},
    title="Sustainability Projects: Age vs. Sub-Category",
    template="plotly_white"
)

# Background bands per category
shapes = []
categories = df['category'].unique()
for idx, cat in enumerate(categories):
    subcats = df[df['category'] == cat]['category_sub'].unique()
    if len(subcats) > 0:
        shapes.append(dict(
            type="rect",
            xref="paper",
            x0=0, x1=1,
            yref="y",
            y0=subcats[0], y1=subcats[-1],
            fillcolor="grey" if idx % 2 == 0 else "whitesmoke",
            opacity=0.2,
            layer="below",
            line_width=0
        ))

fig.update_layout(shapes=shapes, showlegend=True)

# Style Y-axis labels
fig.update_yaxes(
    tickfont=dict(
        family="Arial Black",
        size=20,
        color="black"
    )
)

# Layout cleanup
fig.update_layout(
    showlegend=False,
    height=1400 + 20 * df['category_sub'].nunique(),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=220, r=50, t=50, b=20),
    title_font=dict(size=30, family="Arial", color="#099ec8"),
    font=dict(size=20, family="Arial")
)
fig.update_yaxes(autorange="reversed")

fig.update_layout(
    hoverlabel=dict(
        font_size=24,
        font_family="Arial",
        bgcolor="white",
        font_color="black"
    )
)

fig.update_layout(
    title=dict(
        x=0.5,
        xanchor='center',
        yanchor='top',
        pad=dict(t=5, b=-60),
        font=dict(size=40, family="Arial", color="#099ec8"),
        text="Open Sustainable Technology: Age vs. Sub-Category"
    )
)

fig.show()

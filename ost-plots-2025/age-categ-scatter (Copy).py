import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timezone

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

# OpenSustain palette
color_palette = [
    "#099ec8", "#84bc41", "#f9c416", "#9cd8e9", "#cde4b3",
    "#f7a600", "#00a0a6", "#00689d", "#009639", "#ffcc00",
    "#a3d55d", "#2cb5e8", "#f46f1b", "#c50084", "#004c97"
]

# Create scatter
fig = px.scatter(
    df,
    x="project_age",
    y="category_sub",
    color="sub_category",
    hover_data={
        "project_names": True,
        "project_age": ':.1f',
        "category": True,
        "sub_category": True,
        "git_url": True
    },
    labels={
        "project_age": "Project Age (Years)",
        "category_sub": "Category: Sub-Category"
    },
    title="Open Sustainable Technology: Age vs. Sub-Category",
    template="plotly_white",
    color_discrete_sequence=color_palette
)

# Larger dots
fig.update_traces(
    marker=dict(size=14, line=dict(width=0)),
    hovertemplate="<b>%{customdata[2]}</b><br>" +
                  "Project: %{customdata[0]}<br>" +
                  "Age: %{x:.1f} years<br>" +
                  "<a href='%{customdata[3]}' target='_blank'>Open Project</a><extra></extra>",
    customdata=df[['project_names', 'category', 'sub_category', 'git_url']].values
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

fig.update_layout(shapes=shapes, showlegend=False)

# Style Y-axis labels to make subcategories stand out
fig.update_yaxes(
    tickfont=dict(
        family="Arial Black",   # bolder font
        size=20,
        color="#099ec8"         # OpenSustain blue
    )
)

# Layout cleanup
fig.update_layout(
    height=1000 + 20 * df['category_sub'].nunique(),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=220, r=50, t=50, b=20),
    title_font=dict(size=30, family="Arial", color="#099ec8"),
    font=dict(size=20, family="Arial")
)
fig.update_yaxes(autorange="reversed")

fig.update_layout(
    title=dict(
        x=0.5,         # center the title
        xanchor='center',
        yanchor='top',  # aligns title to top
        pad=dict(t=5, b=-60),  # reduce padding above and below title
        font=dict(size=40, family="Arial", color="#099ec8")
    )
)


# Show the plot
fig.show()

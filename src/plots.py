"""
Pure Plotly figure builders for the bird seed recommender.
No Streamlit imports here.
"""

from typing import Dict
import plotly.graph_objects as go
import plotly.express as px


def seed_score_bars(scores: Dict[str, float], labels: Dict[str, str]) -> go.Figure:
    """Horizontal bar chart of normalized seed scores (0-100)."""
    items = sorted(scores.items(), key=lambda x: x[1])
    y = [labels.get(k, k) for k, _ in items]
    x = [v for _, v in items]
    colors = ["#4f8ef7" if v >= 70 else "#e06c4a" if v >= 40 else "#8890a8" for v in x]

    fig = go.Figure(
        go.Bar(
            x=x,
            y=y,
            orientation="h",
            marker_color=colors,
            text=[f"{v:.0f}" for v in x],
            textposition="outside",
            hovertemplate="%{y}: %{x:.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Seed Match Score (0-100)",
        xaxis_title="Match %",
        yaxis_title="",
        height=max(320, 28 * len(y)),
        margin=dict(l=10, r=40, t=40, b=10),
        xaxis=dict(range=[0, 105]),
        font=dict(size=12),
    )
    return fig


def simple_coverage_pie(coverage: Dict[str, Dict]) -> go.Figure:
    """Small pie showing how many of your birds are 'well covered' by top recs."""
    covered = sum(1 for c in coverage.values() if c.get("covered"))
    total = len(coverage) or 1
    fig = px.pie(
        values=[covered, total - covered],
        names=["Well matched by top seeds", "May need extra options"],
        hole=0.55,
        title=f"{covered}/{total} of your birds strongly matched",
    )
    fig.update_layout(height=260, margin=dict(t=30, b=10, l=10, r=10))
    return fig
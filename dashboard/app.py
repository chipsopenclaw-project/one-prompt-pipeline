import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="World Happiness Report Dashboard",
    page_icon="🌍",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Load data — path relative to project root (where Streamlit is launched from)
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "gold", "happiness_aggregated.parquet")

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_parquet(DATA_PATH)
    df = df.sort_values("ladder_score", ascending=False).reset_index(drop=True)
    df.insert(0, "rank", range(1, len(df) + 1))
    return df

df = load_data()

# ---------------------------------------------------------------------------
# Category colour mapping
# ---------------------------------------------------------------------------
CATEGORY_COLORS = {
    "Happy": "#2ecc71",
    "Neutral": "#f39c12",
    "Unhappy": "#e74c3c",
}

CATEGORY_EMOJI = {
    "Happy": "🟢 Happy",
    "Neutral": "🟡 Neutral",
    "Unhappy": "🔴 Unhappy",
}

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("Filters")

    all_regions = sorted(df["regional_indicator"].unique().tolist())
    selected_regions = st.multiselect(
        "Region",
        options=all_regions,
        default=all_regions,
    )

    all_categories = ["Happy", "Neutral", "Unhappy"]
    selected_categories = st.multiselect(
        "Category",
        options=all_categories,
        default=all_categories,
    )

    st.markdown("---")
    st.caption("Data source: World Happiness Report 2024")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🌍 World Happiness Report Dashboard")
st.markdown(
    "Explore happiness scores, regional rankings, and well-being categories "
    "across **143 countries** using data from the World Happiness Report 2024."
)
st.markdown("---")

# ---------------------------------------------------------------------------
# Section 1: Top 20 Happiest Countries
# ---------------------------------------------------------------------------
st.subheader("Top 20 Happiest Countries")

top20 = df.nlargest(20, "ladder_score").sort_values("ladder_score", ascending=True)

fig_top20 = px.bar(
    top20,
    x="ladder_score",
    y="country_name",
    orientation="h",
    color="category",
    color_discrete_map=CATEGORY_COLORS,
    hover_data={"regional_indicator": True, "ladder_score": ":.3f"},
    labels={
        "ladder_score": "Happiness Score (Ladder Score)",
        "country_name": "Country",
        "category": "Category",
        "regional_indicator": "Region",
    },
    title="Top 20 Happiest Countries",
)
fig_top20.update_layout(
    height=550,
    xaxis_title="Happiness Score (Ladder Score)",
    yaxis_title="",
    legend_title="Category",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
fig_top20.update_xaxes(gridcolor="rgba(200,200,200,0.3)")

st.plotly_chart(fig_top20, use_container_width=True)

# ---------------------------------------------------------------------------
# Section 2: Average Happiness Score by Region
# ---------------------------------------------------------------------------
st.subheader("Average Happiness Score by Region")

regional_avg = (
    df.groupby("regional_indicator", as_index=False)["ladder_score"]
    .mean()
    .rename(columns={"ladder_score": "avg_ladder_score"})
    .sort_values("avg_ladder_score", ascending=False)
)

fig_region = px.bar(
    regional_avg,
    x="regional_indicator",
    y="avg_ladder_score",
    color="avg_ladder_score",
    color_continuous_scale="RdYlGn",
    labels={
        "regional_indicator": "Region",
        "avg_ladder_score": "Average Happiness Score",
    },
    title="Average Happiness Score by Region",
    text_auto=".2f",
)
fig_region.update_layout(
    height=450,
    xaxis_title="Region",
    yaxis_title="Average Happiness Score",
    xaxis_tickangle=-30,
    coloraxis_showscale=False,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
fig_region.update_xaxes(gridcolor="rgba(0,0,0,0)")
fig_region.update_yaxes(gridcolor="rgba(200,200,200,0.3)")

st.plotly_chart(fig_region, use_container_width=True)

# ---------------------------------------------------------------------------
# Metrics row
# ---------------------------------------------------------------------------
total_countries = len(df)
happiest_country = df.loc[df["ladder_score"].idxmax(), "country_name"]
avg_global_score = round(df["ladder_score"].mean(), 2)

col1, col2, col3 = st.columns(3)
col1.metric("Total Countries", total_countries)
col2.metric("Happiest Country", happiest_country)
col3.metric("Average Global Score", avg_global_score)

st.markdown("---")

# ---------------------------------------------------------------------------
# Section 3: Full Country Table with Filters
# ---------------------------------------------------------------------------
st.subheader("Country Happiness Rankings")

# Apply sidebar filters
mask = df["regional_indicator"].isin(selected_regions) & df["category"].isin(selected_categories)
filtered_df = df[mask].copy()

st.markdown(f"Showing **{len(filtered_df)}** of **{total_countries}** countries")

# Prepare display dataframe
display_df = filtered_df[
    ["rank", "country_name", "regional_indicator", "ladder_score", "regional_rank", "category"]
].copy()
display_df["ladder_score"] = display_df["ladder_score"].round(3)
display_df["category"] = display_df["category"].map(CATEGORY_EMOJI)

display_df = display_df.rename(
    columns={
        "rank": "Rank",
        "country_name": "Country",
        "regional_indicator": "Region",
        "ladder_score": "Happiness Score",
        "regional_rank": "Regional Rank",
        "category": "Category",
    }
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Rank": st.column_config.NumberColumn("Rank", width="small"),
        "Country": st.column_config.TextColumn("Country"),
        "Region": st.column_config.TextColumn("Region"),
        "Happiness Score": st.column_config.NumberColumn(
            "Happiness Score",
            format="%.3f",
        ),
        "Regional Rank": st.column_config.NumberColumn("Regional Rank", width="small"),
        "Category": st.column_config.TextColumn("Category"),
    },
    height=500,
)

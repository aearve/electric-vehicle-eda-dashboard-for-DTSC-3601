import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

DATA_PATH = "Electric_Vehicle_Population_Data.csv"

sns.set_theme(style="whitegrid")
PALETTE = "viridis"
ACCENT = sns.color_palette(PALETTE, 10)

st.set_page_config(
    page_title="WA EV Population EDA",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 Washington State Electric Vehicle Population Dashboard")
st.markdown(
    """
    This app explores the **Washington State Department of Licensing's Electric Vehicle
    Population Data** — a registry of every Battery Electric Vehicle (BEV) and Plug-in
    Hybrid Electric Vehicle (PHEV) registered in the state. Use the sidebar filters to
    narrow down by county and make, then browse the tabs below for an overview of the
    dataset, detailed exploratory statistics, and visualizations of key trends.
    """
)


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


df = load_data(DATA_PATH)

# --- Sidebar filters ---
st.sidebar.header("Filters")

counties = sorted(df["County"].dropna().unique())
selected_counties = st.sidebar.multiselect("County", counties, default=[])

makes = sorted(df["Make"].dropna().unique())
selected_makes = st.sidebar.multiselect("Make", makes, default=[])

filtered_df = df.copy()
if selected_counties:
    filtered_df = filtered_df[filtered_df["County"].isin(selected_counties)]
if selected_makes:
    filtered_df = filtered_df[filtered_df["Make"].isin(selected_makes)]

st.sidebar.markdown(f"**{len(filtered_df):,}** of {len(df):,} rows match the current filters.")

if filtered_df.empty:
    st.warning("No rows match the current filter selection. Adjust the filters in the sidebar.")
    st.stop()

tab_overview, tab_eda, tab_viz = st.tabs(["📌 Overview", "🔍 EDA", "📊 Visualizations"])

# ---------------------------------------------------------------------------
# Overview tab
# ---------------------------------------------------------------------------
with tab_overview:
    st.subheader("Key Metrics")

    total_vehicles = len(filtered_df)
    unique_makes = filtered_df["Make"].nunique()
    avg_range = filtered_df.loc[filtered_df["Electric Range"] > 0, "Electric Range"].mean()
    top_county = filtered_df["County"].value_counts().idxmax() if not filtered_df["County"].empty else "N/A"
    bev_pct = (
        filtered_df["Electric Vehicle Type"].str.contains("Battery", na=False).mean() * 100
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Vehicles", f"{total_vehicles:,}")
    col2.metric("Unique Makes", f"{unique_makes:,}")
    col3.metric("Avg. Electric Range", f"{avg_range:,.0f} mi" if pd.notna(avg_range) else "N/A")
    col4.metric("Top County", top_county)
    col5.metric("% Battery Electric (BEV)", f"{bev_pct:.1f}%")

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Top 5 Makes")
        st.dataframe(
            filtered_df["Make"].value_counts().head(5).rename("Count"),
            use_container_width=True,
        )
    with col_b:
        st.subheader("Top 5 Counties")
        st.dataframe(
            filtered_df["County"].value_counts().head(5).rename("Count"),
            use_container_width=True,
        )

# ---------------------------------------------------------------------------
# EDA tab
# ---------------------------------------------------------------------------
with tab_eda:
    st.subheader("Sample of the Data")
    st.dataframe(filtered_df.head(10), use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Dataset Shape")
        st.write(f"{filtered_df.shape[0]:,} rows × {filtered_df.shape[1]} columns")

        st.subheader("Column Data Types")
        st.dataframe(filtered_df.dtypes.astype(str).rename("dtype"), use_container_width=True)

    with col_b:
        st.subheader("Missing Values per Column")
        missing = filtered_df.isna().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        if missing.empty:
            st.write("No missing values.")
        else:
            missing_pct = (missing / len(filtered_df) * 100).round(2)
            st.dataframe(
                pd.DataFrame({"missing_count": missing, "missing_pct": missing_pct}),
                use_container_width=True,
            )

    st.subheader("Summary Statistics (Numeric Columns)")
    st.dataframe(filtered_df.describe(), use_container_width=True)

# ---------------------------------------------------------------------------
# Visualizations tab
# ---------------------------------------------------------------------------
with tab_viz:
    row1_a, row1_b = st.columns(2)

    with row1_a:
        st.subheader("Top 10 Vehicle Makes by Count")
        top_makes = filtered_df["Make"].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.barplot(
            x=top_makes.values,
            y=top_makes.index,
            hue=top_makes.index,
            palette=PALETTE,
            legend=False,
            ax=ax,
        )
        ax.set_title("Top 10 Vehicle Makes by Count")
        ax.set_xlabel("Number of Vehicles")
        ax.set_ylabel("Make")
        st.pyplot(fig)

    with row1_b:
        st.subheader("Electric Vehicle Type Distribution")
        ev_type_counts = filtered_df["Electric Vehicle Type"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.pie(
            ev_type_counts.values,
            labels=ev_type_counts.index.str.replace(
                r"\s*\(.*\)", "", regex=True
            ),
            autopct="%1.1f%%",
            startangle=90,
            colors=sns.color_palette(PALETTE, len(ev_type_counts)),
        )
        ax.set_title("Electric Vehicle Type Distribution")
        ax.axis("equal")
        st.pyplot(fig)

    row2_a, row2_b = st.columns(2)

    with row2_a:
        st.subheader("Electric Range Distribution")
        range_df = filtered_df[filtered_df["Electric Range"] > 0]
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.histplot(range_df["Electric Range"], bins=40, kde=True, color=ACCENT[4], ax=ax)
        ax.set_title("Electric Range Distribution")
        ax.set_xlabel("Electric Range (miles)")
        ax.set_ylabel("Count")
        st.caption("Vehicles with a reported range of 0 (unknown/unresearched) are excluded.")
        st.pyplot(fig)

    with row2_b:
        st.subheader("Vehicles Registered by Model Year")
        by_year = filtered_df["Model Year"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.barplot(x=by_year.index, y=by_year.values, color=ACCENT[6], ax=ax)
        ax.set_title("Vehicles Registered by Model Year")
        ax.set_xlabel("Model Year")
        ax.set_ylabel("Number of Registrations")
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        st.pyplot(fig)

    st.subheader("Top 10 Counties by EV Count")
    top_counties = filtered_df["County"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=top_counties.index,
        y=top_counties.values,
        hue=top_counties.index,
        palette=PALETTE,
        legend=False,
        ax=ax,
    )
    ax.set_title("Top 10 Counties by EV Count")
    ax.set_xlabel("County")
    ax.set_ylabel("Number of Vehicles")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig)

import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.concat(
    map(
        pd.read_json,
        [
            "../data/endsong_0.json",
            "../data/endsong_1.json",
            "../data/endsong_2.json",
            "../data/endsong_3.json",
            "../data/endsong_4.json",
            "../data/endsong_5.json",
        ],
    )
)

df_top_tracks = df["master_metadata_track_name"].value_counts().to_frame()
df_top_tracks = df_top_tracks.reset_index().rename(
    columns={"master_metadata_track_name": "name", "count": "plays"}
)

st.title("SpotiStats")

st.header("Basics", divider=True)
st.write(
    "For starters, some basic stats to get a feeling and get excited about our data."
)
col1, col2 = st.columns(2)
df_top_tracks = df["master_metadata_track_name"].value_counts().to_frame()
df_top_tracks = df_top_tracks.reset_index().rename(
    columns={"master_metadata_track_name": "name", "count": "plays"}
)

reason_end_count = (
    df["reason_end"]
    .value_counts(normalize=True)
    .to_frame()
    .reset_index()
    .rename({"count": "reason_end"}, axis=1)
)
reason_end_count["proportion"] = reason_end_count["proportion"] * 100

with col1:
    with st.container(border=True):
        st.metric(
            "Most played track",
            df_top_tracks.iloc[df_top_tracks["plays"].idxmax()]["name"],
        )

    perc_skipped = float(
        reason_end_count[reason_end_count["reason_end"] == "fwdbtn"]["proportion"] * 100
    )
    with st.container(border=True):
        st.metric(label="Tracks skipped", value=f"{perc_skipped:.2f} %")

with col2:
    unique_tracks = df["master_metadata_track_name"].unique()
    with st.container(border=True):
        st.metric("Total number of tracks", len(unique_tracks))

    ms_total = df["ms_played"].sum()
    s_total = ms_total / 1000
    m_total = s_total / 60
    h_total = m_total / 60
    d_total = h_total / 24

    hs = (d_total % 1) * 24
    mins = (hs % 1) * 60

    metric = f"{int(d_total)}d {int(hs)}h {int(mins)}m"
    with st.container(border=True):
        st.metric("Time played", metric)


fig = px.bar(
    reason_end_count,
    x="proportion",
    y="reason_end",
    orientation="h",
    color="reason_end",
    color_discrete_sequence=px.colors.sequential.algae_r,
    labels={
        "proportion": "Proportion (%)",
        "reason_end": "",
    },
    title="Reason for ending tracks",
)
fig.update_layout(showlegend=False)
st.write(fig)

df["ts"] = pd.to_datetime(df["ts"])
years_data = pd.DataFrame(df.groupby(df["ts"].dt.year)["ts"].count())
years_data = years_data.rename(columns={"ts": "plays"}).reset_index()
fig = px.bar(years_data, x="ts", y="plays", title="Plays per year")
st.write(fig)

df_top_per_year = (
    df.groupby(df["ts"].dt.year)["master_metadata_track_name"]
    .value_counts()
    .groupby(level=0, group_keys=False)
    .head(5)
).reset_index()

cols = st.columns(2)

for i, year in enumerate(df_top_per_year["ts"].unique()):
    with cols[i % 2]:
        st.subheader(year)
        st.table(
            df_top_per_year[df_top_per_year["ts"] == year][
                ["master_metadata_track_name", "count"]
            ].set_index("master_metadata_track_name")
        )

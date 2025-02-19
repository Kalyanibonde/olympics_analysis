import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Load and preprocess data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)

# Sidebar setup
st.sidebar.title("🏅 Olympics Analysis")
st.sidebar.image("https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png")
user_menu = st.sidebar.radio(
    "Select an Option",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete-wise Analysis")
)

# Medal Tally
if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Title based on selection
    if selected_year == "Overall" and selected_country == "Overall":
        st.title("🏆 Overall Medal Tally")
    elif selected_year != "Overall" and selected_country == "Overall":
        st.title(f"🎖 Medal Tally in {selected_year} Olympics")
    elif selected_year == "Overall" and selected_country != "Overall":
        st.title(f"🌍 {selected_country} Overall Performance")
    else:
        st.title(f"🏅 {selected_country} Performance in {selected_year} Olympics")

    st.table(medal_tally)

# Overall Analysis
if user_menu == "Overall Analysis":
    # Compute statistics
    editions = df["Year"].nunique()
    cities = df["City"].nunique()
    sports = df["Sport"].nunique()
    events = df["Event"].nunique()
    athletes = df["Name"].nunique()
    nations = df["region"].nunique()

    # Display statistics
    st.title("📊 Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    # Plots
    st.title("📈 Participating Nations Over the Years")
    nations_over_time = helper.data_over_time(df, "region")
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.plotly_chart(fig)

    st.title("🏟 Events Over the Years")
    events_over_time = helper.data_over_time(df, "Event")
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.plotly_chart(fig)

    st.title("👥 Athletes Over the Years")
    athlete_over_time = helper.data_over_time(df, "Name")
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.plotly_chart(fig)

    st.title("⚡ Number of Events Over Time (Every Sport)")
    fig, ax = plt.subplots(figsize=(15, 10))
    heatmap_data = df.drop_duplicates(["Year", "Sport", "Event"])
    ax = sns.heatmap(heatmap_data.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype(int),
                      annot=True, cmap="coolwarm")
    st.pyplot(fig)

    st.title("🏅 Most Successful Athletes")
    sport_list = sorted(df["Sport"].unique().tolist())
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Select a Sport", sport_list)
    top_athletes = helper.most_successful(df, selected_sport)
    st.table(top_athletes)

# Country-wise Analysis
if user_menu == "Country-wise Analysis":
    st.sidebar.title("🌍 Country-wise Analysis")

    country_list = sorted(df["region"].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Select a Country", country_list)

    # Medal Tally
    st.title(f"🏆 {selected_country} Medal Tally Over the Years")
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.plotly_chart(fig)

    # Heatmap
    st.title(f"🔥 {selected_country} Excels in These Sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.heatmap(pt, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # Top Athletes
    st.title(f"🏅 Top 10 Athletes of {selected_country}")
    top_athletes = helper.most_successful_countrywise(df, selected_country)
    st.table(top_athletes)

# Athlete-wise Analysis
if user_menu == "Athlete-wise Analysis":
    athlete_df = df.drop_duplicates(subset=["Name", "region"])

    # Age Distribution
    st.title("📊 Distribution of Age")
    age_data = [
        athlete_df["Age"].dropna(),
        athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna(),
        athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna(),
        athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna(),
    ]
    labels = ["Overall Age", "Gold Medalists", "Silver Medalists", "Bronze Medalists"]
    fig = ff.create_distplot(age_data, labels, show_hist=False, show_rug=False)
    st.plotly_chart(fig)

    # Age Distribution in Different Sports
    st.title("🏅 Distribution of Age w.r.t Sports (Gold Medalists)")
    sports = [
        "Basketball", "Judo", "Football", "Athletics", "Swimming", "Gymnastics",
        "Wrestling", "Hockey", "Rowing", "Fencing", "Boxing", "Cycling", "Tennis",
        "Golf", "Archery", "Volleyball", "Table Tennis", "Baseball"
    ]
    age_data = [athlete_df[athlete_df["Sport"] == sport]["Age"].dropna() for sport in sports]
    fig = ff.create_distplot(age_data, sports, show_hist=False, show_rug=False)
    st.plotly_chart(fig)

    # Height vs Weight
    st.title("📏 Height vs Weight of Athletes")
    sport_list = sorted(df["Sport"].unique().tolist())
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Select a Sport", sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    sns.scatterplot(data=temp_df, x="Weight", y="Height", hue="Medal", style="Sex", s=60, ax=ax)
    st.pyplot(fig)

    # Men vs Women Participation
    st.title("👨‍🦰 vs 👩 Participation Over the Years")
    gender_data = helper.men_vs_women(df)
    fig = px.line(gender_data, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)

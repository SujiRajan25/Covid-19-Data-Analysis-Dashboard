import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(
    page_title="COVID-19 Dashboard",
    layout="wide"
)

# Title
st.title("🦠 COVID-19 Data Analysis Dashboard")

# Load Excel File
df = pd.read_excel("covid_data.xlsx")

# Convert date column
df['Date'] = pd.to_datetime(df['Date'])
# Sidebar
st.sidebar.header("Filter Data")

country = st.sidebar.selectbox(
    "Select Country",
    df['Country'].unique()
)

# Filter dataframe
country_df = df[df['Country'] == country]

# Latest Data
latest = country_df.iloc[-1]

# KPI Metrics
st.subheader(f"Latest COVID Statistics - {country}")
col1, col2, col3 = st.columns(3)

col1.metric(
    "Confirmed Cases",
    int(latest['Confirmed'])
)

col2.metric(
    "Deaths",
    int(latest['Deaths'])
)

col3.metric(
    "Recovered",
    int(latest['Recovered'])
)

# Line Chart
st.subheader("Confirmed Cases Over Time")

fig = px.line(
    country_df,
    x='Date',
    y='Confirmed',
    title='Confirmed Cases Trend'
)

st.plotly_chart(fig, use_container_width=True)

# Daily Cases
country_df['Daily_Cases'] = (
    country_df['Confirmed'].diff()
)

# 7-Day Moving Average
country_df['MA7'] = (
    country_df['Daily_Cases']
    .rolling(7)
    .mean()
)

# Daily Cases Chart
st.subheader("Daily Cases")

fig2, ax = plt.subplots(figsize=(10,5))

ax.plot(
    country_df['Date'],
    country_df['Daily_Cases']
)

ax.set_xlabel("Date")
ax.set_ylabel("Cases")
ax.set_title("Daily COVID Cases")

st.pyplot(fig2)

# Moving Average Chart
st.subheader("7-Day Moving Average")

fig3 = px.line(
    country_df,
    x='Date',
    y='MA7',
    title='7-Day Moving Average'
)

st.plotly_chart(fig3, use_container_width=True)

# Raw Data
st.subheader("Dataset")

st.dataframe(country_df)

# Map
st.subheader("Country Location")


map_data=country_df.rename(columns={'Latitude':'lat','Longitude':'lon'})
st.map(map_data)
# Footer
st.markdown("---")
st.write("COVID-19 Dashboard using Streamlit")

import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Complete Diwali Sales Dashboard", layout="wide")

st.title("🪔 Complete Diwali Sales Analytics Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Diwali Sales Data.csv", encoding="unicode_escape")
    df.drop(['Status', 'unnamed1'], axis=1, inplace=True, errors='ignore')
    df.dropna(inplace=True)
    df['Amount'] = df['Amount'].astype(int)
    return df

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🔎 Filters")

state_filter = st.sidebar.multiselect(
    "State",
    df["State"].unique(),
    default=df["State"].unique()
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered_df = df[
    (df["State"].isin(state_filter)) &
    (df["Gender"].isin(gender_filter))
]

# --------------------------------------------------
# KPI Metrics
# --------------------------------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹ {filtered_df['Amount'].sum():,}")
col2.metric("Total Orders", int(filtered_df["Orders"].sum()))
col3.metric("Total Customers", filtered_df.shape[0])
col4.metric("Average Order Value",
            f"₹ {filtered_df['Amount'].mean():,.0f}")

st.markdown("---")

# --------------------------------------------------
# ROW 1
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    fig = px.histogram(filtered_df, x="Gender", color="Gender", text_auto=True)
    st.plotly_chart(fig, width="stretch")

with col2:
    sales_gen = filtered_df.groupby("Gender", as_index=False)["Amount"].sum()
    fig = px.bar(sales_gen, x="Gender", y="Amount", color="Gender", text_auto=True)
    st.plotly_chart(fig, width="stretch")

with col3:
    filtered_df.loc[:, 'Maritail_status'] = filtered_df['Marital_Status'].map({0:"unmarried",1:"married"})
    fig = px.pie(filtered_df, names="Marital_Status", title="Marital Status Distribution")
    st.plotly_chart(fig, width="stretch")

st.markdown("---")

# --------------------------------------------------
# ROW 2
# --------------------------------------------------
col4, col5, col6 = st.columns(3)

with col4:
    fig = px.histogram(filtered_df, x="Age Group", color="Gender", barmode="group")
    st.plotly_chart(fig, width="stretch")

with col5:
    top_states = (
        filtered_df.groupby("State")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig = px.bar(top_states, x="State", y="Amount", text_auto=True)
    st.plotly_chart(fig, width="stretch")

with col6:
    fig = px.histogram(filtered_df, x="Occupation", color="Occupation")
    st.plotly_chart(fig, width="stretch")

st.markdown("---")

# --------------------------------------------------
# ROW 3
# --------------------------------------------------
col7, col8 = st.columns(2)

with col7:
    top_products = (
        filtered_df.groupby("Product_Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig = px.bar(top_products, x="Product_Category", y="Amount", text_auto=True)
    st.plotly_chart(fig, width="stretch")

with col8:
    fig = px.scatter(
        filtered_df,
        x="Orders",
        y="Amount",
        color="Gender",
        title="Orders vs Revenue"
    )
    st.plotly_chart(fig, width="stretch")

st.markdown("---")

if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)

# st.success("🚀 Full Analytics Dashboard Loaded Successfully")
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time

# -------------------------
# ⚙️ Page Config & CSS
# -------------------------
st.set_page_config(page_title="HealthKart Campaign Dashboard", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #000000;
        color: #00FF66;
        font-family: 'Segoe UI', sans-serif;
    }

    div[data-testid="metric-container"] {
        background-color: #111111;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00FF66;
        box-shadow: 0 1px 5px rgba(0, 255, 102, 0.2);
        color: #00FF66 !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #0d0d0d;
        border-right: 1px solid #00FF66;
    }

    h1, h2, h3, h4 {
        color: #00FF66;
    }

    .stDataFrame {
        background-color: #111111;
        border-radius: 10px;
        color: #00FF66;
    }

    .stDownloadButton > button {
        background-color: #00FF66;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 20px;
    }

    .stDownloadButton > button:hover {
        background-color: #00cc55;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# 📂 Load Data
# -------------------------
@st.cache_data
def load_data():
    data_path = 'data'
    influencers = pd.read_csv(os.path.join(data_path, 'influencers.csv'))
    payouts = pd.read_csv(os.path.join(data_path, 'payouts.csv'))
    tracking = pd.read_csv(os.path.join(data_path, 'tracking_data.csv'))

    influencers.rename(columns={"ID": "influencer_id"}, inplace=True)

    summary = tracking.groupby('influencer_id').agg({
        'orders': 'sum',
        'revenue': 'sum'
    }).reset_index()

    merged = pd.merge(summary, payouts, on='influencer_id', how='left')
    merged = pd.merge(merged, influencers, on='influencer_id', how='left')
    merged['ROAS'] = merged['revenue'] / merged['total_payout']

    return merged

df = load_data()

# -------------------------
# 🎯 Header
# -------------------------
st.title("🤖 HealthKart Influencer Campaign Dashboard")
st.markdown("Filter campaign performance by platform, category and ROAS.")

# -------------------------
# 🎛️ Sidebar Filters
# -------------------------
st.sidebar.header("🎯 Filter by")
platforms = df['platform'].dropna().unique()
categories = df['category'].dropna().unique()

selected_platform = st.sidebar.selectbox("Platform", ["All"] + sorted(platforms))
selected_category = st.sidebar.selectbox("Category", ["All"] + sorted(categories))
roas_threshold = st.sidebar.slider("Min ROAS", 0.0, 5.0, step=0.1, value=1.0)

# -------------------------
# 🔍 Apply Filters
# -------------------------
filtered_df = df.copy()
if selected_platform != "All":
    filtered_df = filtered_df[filtered_df['platform'] == selected_platform]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
filtered_df = filtered_df[filtered_df['ROAS'] >= roas_threshold]

# -------------------------
# 🤖 Simulate AI-Style Loading
# -------------------------
with st.spinner("🧠 Analyzing influencer performance..."):
    time.sleep(1.5)

# -------------------------
# 📊 Summary Metrics
# -------------------------
total_rev = filtered_df['revenue'].sum()
total_payout = filtered_df['total_payout'].sum()
avg_roas = total_rev / total_payout if total_payout != 0 else 0

st.markdown("### 📊 Campaign Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹ {total_rev:,.0f}")
col2.metric("Total Payout", f"₹ {total_payout:,.0f}")
col3.metric("Average ROAS", f"{avg_roas:.2f}")

st.markdown("---")

# -------------------------
# 📈 Top Influencer ROAS Chart
# -------------------------
if not filtered_df.empty:
    st.markdown("### 🚀 Top Influencers by ROAS")
    fig1 = px.bar(
        filtered_df.sort_values(by='ROAS', ascending=False).head(10),
        x='name', y='ROAS', color='platform',
        template='plotly_dark',
        title="Top 10 Influencers by ROAS"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # -------------------------
    # 📉 Revenue vs Payout Chart (Line/Scatter)
    # -------------------------
    st.markdown("### 📈 Revenue vs Payout Spread")
    sorted_df = filtered_df.sort_values(by="total_payout")
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=sorted_df['total_payout'],
        y=sorted_df['revenue'],
        mode='markers+lines',
        line=dict(color='#00FF66', width=2),
        marker=dict(size=10, color='#00FF66', line=dict(width=1, color='black')),
        text=sorted_df['name'],
        hovertemplate='Influencer: %{text}<br>Payout: ₹%{x}<br>Revenue: ₹%{y}<extra></extra>'
    ))

    fig2.update_layout(
        title="📈 Revenue vs Payout Spread (Connected)",
        xaxis_title="Total Payout (₹)",
        yaxis_title="Revenue (₹)",
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        font=dict(color="#00FF66"),
        height=400
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------
    # 📋 Data Table
    # -------------------------
    st.markdown("### 📋 Influencer Table")
    st.dataframe(
        filtered_df[['name', 'platform', 'category', 'revenue', 'total_payout', 'ROAS']].sort_values(by='ROAS', ascending=False),
        use_container_width=True,
        height=400
    )

    # -------------------------
    # 📤 Export Data
    # -------------------------
    st.markdown("### 💾 Export Filtered Data")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name='filtered_influencer_data.csv',
        mime='text/csv'
    )
else:
    st.warning("⚠️ No data matches the selected filters.")

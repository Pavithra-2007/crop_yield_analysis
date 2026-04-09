import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Crop Analytics",
    layout="wide",
    page_icon="🌾"
)

# -------------------------------
# CUSTOM CSS (🔥 PREMIUM UI)
# -------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
[data-testid="stSidebar"] {
    background: #111827;
}
.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
h1, h2, h3 {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("crop_yield_data.csv")

# -------------------------------
# 🤖 ML MODEL (TRAIN ONCE)
# -------------------------------
features = ["Rainfall_mm", "Avg_Temp_C", "Fertilizer_kg_per_ha"]
target = "Yield_kg_per_ha"

X = df[features]
y = df[target]

model = LinearRegression()
model.fit(X, y)

# -------------------------------
# TITLE
# -------------------------------
st.title("🌾 Smart Crop Yield Dashboard")
st.markdown("### 🚀 Advanced Agriculture Analytics")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🔍 Filters")

region = st.sidebar.multiselect("Region", df["Region"].unique())
crop = st.sidebar.multiselect("Crop", df["Crop"].unique())

filtered_df = df.copy()

if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]

if crop:
    filtered_df = filtered_df[filtered_df["Crop"].isin(crop)]

# -------------------------------
# KPI CARDS
# -------------------------------
st.markdown("## 📊 Key Insights")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f'<div class="metric-card"><h3>Total Records</h3><h2>{len(filtered_df)}</h2></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-card"><h3>Avg Yield</h3><h2>{round(filtered_df["Yield_kg_per_ha"].mean(),2)}</h2></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-card"><h3>Max Yield</h3><h2>{round(filtered_df["Yield_kg_per_ha"].max(),2)}</h2></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-card"><h3>Avg Rainfall</h3><h2>{round(filtered_df["Rainfall_mm"].mean(),2)}</h2></div>', unsafe_allow_html=True)

# -------------------------------
# CHART ROW 1
# -------------------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Yield Trend")

    fig1 = px.line(
        filtered_df,
        x="Year",
        y="Yield_kg_per_ha",
        color="Crop",
        markers=True,
        template="plotly_dark"
    )
    st.plotly_chart(fig1, width="stretch")   # ✅ fixed warning

with colB:
    st.subheader("🌍 Top Regions")

    top_regions = (
        filtered_df.groupby("Region")["Yield_kg_per_ha"]
        .mean()
        .nlargest(10)
        .reset_index()
    )

    fig2 = px.bar(
        top_regions,
        x="Yield_kg_per_ha",
        y="Region",
        orientation='h',
        color="Yield_kg_per_ha",
        template="plotly_dark"
    )
    st.plotly_chart(fig2, width="stretch")

# -------------------------------
# CHART ROW 2
# -------------------------------
colC, colD = st.columns(2)

with colC:
    st.subheader("🌾 Crop Comparison")

    crop_data = (
        filtered_df.groupby("Crop")["Yield_kg_per_ha"]
        .mean()
        .nlargest(8)
        .reset_index()
    )

    fig3 = px.bar(
        crop_data,
        x="Yield_kg_per_ha",
        y="Crop",
        orientation='h',
        color="Yield_kg_per_ha",
        template="plotly_dark"
    )
    st.plotly_chart(fig3, width="stretch")

with colD:
    st.subheader("🌧 Rainfall Impact")

    fig4 = px.scatter(
        filtered_df,
        x="Rainfall_mm",
        y="Yield_kg_per_ha",
        color="Crop",
        size="Yield_kg_per_ha",
        template="plotly_dark"
    )
    st.plotly_chart(fig4, width="stretch")

# -------------------------------
# 🤖 AI PREDICTION SECTION
# -------------------------------
st.markdown("## 🤖 AI Yield Prediction")

col1, col2, col3 = st.columns(3)

rain = col1.number_input("🌧 Rainfall (mm)", 0.0)
temp = col2.number_input("🌡 Temperature (°C)", 0.0)
fert = col3.number_input("🧪 Fertilizer (kg/ha)", 0.0)

if st.button("🚀 Predict Yield"):
    prediction = model.predict([[rain, temp, fert]])

    st.success(f"🌾 Predicted Yield: {round(prediction[0],2)} kg/ha")

    if prediction[0] > 3000:
        st.info("✅ High Yield Expected")
    elif prediction[0] > 1500:
        st.warning("⚠️ Moderate Yield")
    else:
        st.error("❌ Low Yield - Improve conditions")

# -------------------------------
# DATA TABLE
# -------------------------------
st.markdown("## 📋 Data Table")
st.dataframe(filtered_df, width="stretch")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
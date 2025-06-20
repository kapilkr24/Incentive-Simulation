import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Incentive Simulator", layout="wide")
st.title("🌍 Multi-Region Incentive Payout Simulator")

st.markdown("""
This simulator allows internal C&B teams to simulate incentive payouts across multiple countries or regions by entering hypothetical KPI achievements, multipliers, and weights.
""")

# --- Define Default KPI Table ---
def get_default_kpi_table():
    return pd.DataFrame({
        "Region": ["India", "India", "India"],
        "KPI": ["Revenue", "Pipeline Coverage", "Customer Satisfaction"],
        "Target %": [100, 100, 100],
        "Achieved %": [100, 100, 100],
        "Multiplier": [1.0, 1.0, 1.0],
        "Weight %": [40, 30, 30],
        "Score": [0.0, 0.0, 0.0],
        "Weighted Score": [0.0, 0.0, 0.0],
        "Payout Component": [0.0, 0.0, 0.0]
    })

# --- Target payout per region (optional override) ---
st.sidebar.header("🔧 Global Settings")
regions = st.sidebar.multiselect("Select Regions to Simulate", ["India", "USA", "Europe", "MEA", "APAC"], default=["India"])

region_target_map = {}
for region in regions:
    region_target_map[region] = st.sidebar.number_input(f"Target Incentive (₹) for {region}", min_value=0, value=100000, step=1000)

# --- Editable KPI Table ---
st.subheader("📊 KPI Input Table – Enter Region-Specific Hypothetical Values")
kpi_df = st.data_editor(
    get_default_kpi_table(),
    num_rows="dynamic",
    use_container_width=True,
    key="kpi_table"
)

# --- Filter for selected regions only ---
kpi_df = kpi_df[kpi_df['Region'].isin(regions)]

# --- Compute Payout Logic ---
output = []
for region in kpi_df['Region'].unique():
    sub_df = kpi_df[kpi_df['Region'] == region].copy()
    total_weight = sub_df["Weight %"].sum()

    sub_df["Score"] = (sub_df["Achieved %"] / sub_df["Target %"]) * sub_df["Multiplier"]
    sub_df["Weighted Score"] = sub_df["Score"] * (sub_df["Weight %"] / 100)
    sub_df["Payout Component"] = sub_df["Weighted Score"] * region_target_map[region]
    total_payout = sub_df["Payout Component"].sum()

    output.append((region, sub_df, total_weight, total_payout))

# --- Display Results ---
for region, sub_df, total_weight, total_payout in output:
    st.subheader(f"🌐 {region} – Payout Summary")

    if total_weight != 100:
        st.warning(f"⚠️ Total KPI weight for {region} is {total_weight}%. It should be exactly 100%.")

    st.dataframe(sub_df.style.format({
        "Score": "{:.2f}",
        "Weighted Score": "{:.2f}",
        "Payout Component": "₹{:.2f}"
    }), use_container_width=True)

    st.success(f"✅ Total Projected Payout for {region}: ₹{total_payout:,.2f}")

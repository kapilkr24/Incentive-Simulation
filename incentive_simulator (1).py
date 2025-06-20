import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Incentive Simulator", layout="wide")
st.title("💰 Incentive Payout Simulator")

st.markdown("""
This simulator allows internal C&B teams to simulate incentive payouts by entering hypothetical KPI achievements, multipliers, and weights.
""")

# --- Define Default KPI Table ---
def get_default_kpi_table():
    return pd.DataFrame({
        "KPI": ["Revenue", "Pipeline Coverage", "Customer Satisfaction"],
        "Target %": [100, 100, 100],
        "Achieved %": [100, 100, 100],
        "Multiplier": [1.0, 1.0, 1.0],
        "Weight %": [40, 30, 30],
        "Score": [0.0, 0.0, 0.0],
        "Weighted Score": [0.0, 0.0, 0.0],
        "Payout Component": [0.0, 0.0, 0.0]
    })

# --- Input for Target Payout ---
target_payout = st.number_input("Enter Target Incentive Amount (₹)", value=100000, step=1000)

# --- Editable KPI Table ---
st.subheader("🎯 KPI Table – Enter Hypothetical Values")
kpi_df = st.data_editor(
    get_default_kpi_table(),
    num_rows="dynamic",
    use_container_width=True,
    key="kpi_table"
)

# --- Compute Payout Logic ---
total_weighted_score = 0
kpi_df["Score"] = (kpi_df["Achieved %"] / kpi_df["Target %"]) * kpi_df["Multiplier"]
kpi_df["Weighted Score"] = kpi_df["Score"] * (kpi_df["Weight %"] / 100)
kpi_df["Payout Component"] = kpi_df["Weighted Score"] * target_payout
total_payout = kpi_df["Payout Component"].sum()

total_weight = kpi_df["Weight %"].sum()
if total_weight != 100:
    st.warning(f"⚠️ Total KPI weight is {total_weight}%. It should be exactly 100%.")

# --- Display Results ---
st.subheader("🧾 Projected Payout Summary")
st.dataframe(kpi_df.style.format({
    "Score": "{:.2f}",
    "Weighted Score": "{:.2f}",
    "Payout Component": "₹{:.2f}"
}))

st.success(f"✅ Total Projected Payout: ₹{total_payout:,.2f}")

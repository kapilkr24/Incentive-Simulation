
import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="C&B Payout Simulation", layout="wide")
st.title("💼 Corp C&B Incentive Budget Simulator with Headcount Scaling")

st.markdown("""
Simulate total incentive payouts across different regions, roles, bands, and KPI performance scenarios with employee count projection.
""")

# Sidebar filters
st.sidebar.header("🔧 Global Settings")
regions = st.sidebar.multiselect("Regions", ["India", "USA", "Europe", "APAC"], default=["India"])
roles = st.sidebar.multiselect("Roles", ["Field Sales", "Inside Sales", "Sales Manager"], default=["Field Sales"])
bands = st.sidebar.multiselect("Bands", ["B3", "B4", "B5"], default=["B4"])
scenarios = st.sidebar.selectbox("Performance Scenario", ["Expected", "Optimistic", "Conservative"])
target_incentive = st.sidebar.number_input("Target Incentive Amount (₹)", value=100000, step=10000)

# Generate editable table
rows = []
for region in regions:
    for role in roles:
        for band in bands:
            rows.extend([
                {
                    "Region": region,
                    "Role": role,
                    "Band": band,
                    "KPI": kpi,
                    "Target %": 100,
                    "Achieved %": 100,
                    "Weight %": weight,
                    "Multiplier": 1.0,
                    "Employees": 10 if kpi == "Revenue" else np.nan  # only one row per combo needs employee count
                }
                for kpi, weight in zip(["Revenue", "Pipeline", "CSAT"], [40, 30, 30])
            ])

df = pd.DataFrame(rows)

# Apply scenario adjustments
if scenarios == "Optimistic":
    df["Achieved %"] += 15
    df["Multiplier"] = 1.2
elif scenarios == "Conservative":
    df["Achieved %"] -= 10
    df["Multiplier"] = 0.8

st.subheader("📋 KPI Input Grid")
edited = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="editor")

# Fill missing 'Employees' downward by group
edited["Employees"] = edited.groupby(["Region", "Role", "Band"])["Employees"].transform("first").fillna(0)

# Calculate payouts
edited["Score"] = (edited["Achieved %"] / edited["Target %"]) * edited["Multiplier"]
edited["Weighted Score"] = edited["Score"] * (edited["Weight %"] / 100)
edited["Payout per Employee"] = edited["Weighted Score"] * target_incentive
edited["Total Payout"] = edited["Payout per Employee"] * edited["Employees"]

# Show final results
st.subheader("📊 Simulated Total Payouts by Group")
st.dataframe(edited, use_container_width=True)
total_budget = edited["Total Payout"].sum()
st.success(f"💰 Total Simulated Incentive Budget: ₹{total_budget:,.0f}")

# Download
csv = edited.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Simulation as CSV",
    data=csv,
    file_name="cb_payout_simulation_scaled.csv",
    mime="text/csv"
)

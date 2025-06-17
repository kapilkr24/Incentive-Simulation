# 💻 Streamlit App – KPI-Based Incentive Simulation with Weightages

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Client KPI Incentive Simulator", layout="centered")
st.title("📊 Weighted KPI-Based Incentive Payout Simulator")

st.markdown("""
Simulate projected payouts using **client-specific KPI logic**:
- 4 KPIs displayed in a table format
- Adjustable performance %, multipliers, and weightages
- Payout based on weighted KPI contributions

Useful for C&B teams to test various hypothetical scenarios.
""")

# Input Parameters
total_employees = st.number_input("Total Eligible Employees", min_value=0, max_value=10000, value=100, step=1)
base_incentive = st.number_input("Base Incentive per Employee (₹)", min_value=0.0, value=50000.0, step=1000.0)

# KPI Table Setup
st.subheader("🔢 KPI Performance Table")
kpi_data = pd.DataFrame({
    "KPI": ["KPI 1", "KPI 2", "KPI 3", "KPI 4"],
    "Performance %": [90.0, 85.0, 88.0, 92.0],
    "Multiplier": [1.0, 1.1, 0.9, 1.2],
    "Weightage %": [25, 25, 25, 25],
})

edited_data = st.data_editor(kpi_data, use_container_width=True, num_rows="fixed")

# Run Simulation
if st.button("Run Simulation"):
    kpi_details = []
    total_weight = sum(edited_data["Weightage %"])
    payout_per_employee = 0

    for _, row in edited_data.iterrows():
        kpi_name = row["KPI"]
        perf = row["Performance %"]
        multiplier = row["Multiplier"]
        weight = row["Weightage %"] / total_weight  # Normalize weight

        payout = base_incentive * (perf / 100) * multiplier * weight
        kpi_details.append((kpi_name, payout))
        payout_per_employee += payout

    total_projected_payout = payout_per_employee * total_employees

    # Output
    st.success("✅ Simulation Complete")
    st.metric(label="Total Payout per Employee (₹)", value=f"₹ {payout_per_employee:,.2f}")
    st.metric(label="Total Projected Payout (₹)", value=f"₹ {total_projected_payout:,.2f}")

    st.markdown("---")
    st.subheader("📊 KPI-wise Payout Breakdown")
    for name, payout in kpi_details:
        st.write(f"**{name}:** ₹ {payout:,.2f}")

    st.markdown("""
    ### 🧮 Calculation Logic:
    - **Component Payout** = Base Incentive × KPI % × Multiplier × (Weight ÷ 100)
    - **Total per Employee** = Sum of all KPI payouts
    - **Total Projected** = Total per employee × Eligible employees
    """)

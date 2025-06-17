# 💻 Streamlit App – Client-Specific KPI-Based Incentive Simulation Tool

import streamlit as st

st.set_page_config(page_title="Client KPI Incentive Simulator", layout="centered")
st.title("📊 KPI-Based Incentive Payout Simulator")

st.markdown("""
This enhanced version allows simulation of projected payouts based on **client-specific incentive logic**:
- Four custom KPIs
- Grid-based multipliers applied per KPI
- Total payout calculated as the sum of each KPI's payout

This is ideal for C&B teams to simulate payouts using hypothetical values.
""")

st.header("📥 Input Parameters")
total_employees = st.number_input("Total Eligible Employees", min_value=0, max_value=10000, value=100, step=1)
base_incentive = st.number_input("Base Incentive per Employee (₹)", min_value=0.0, value=50000.0, step=1000.0)

st.subheader("KPI Performance and Multipliers")

kpi_inputs = []
kpi_names = ["KPI 1", "KPI 2", "KPI 3", "KPI 4"]

for i, kpi in enumerate(kpi_names):
    st.markdown(f"### {kpi}")
    perf = st.number_input(f"Average Performance Score for {kpi} (%)", min_value=0.0, max_value=200.0, value=90.0, step=0.5, key=f"perf_{i}")
    multiplier = st.number_input(f"Multiplier for {kpi} (based on client grid)", min_value=0.0, max_value=5.0, value=1.0, step=0.1, key=f"multiplier_{i}")
    kpi_inputs.append({"performance": perf, "multiplier": multiplier})

if st.button("Run Simulation"):
    total_payout_per_employee = 0
    kpi_details = []

    for i, kpi in enumerate(kpi_inputs):
        component_payout = base_incentive * (kpi["performance"] / 100) * kpi["multiplier"] / len(kpi_names)
        total_payout_per_employee += component_payout
        kpi_details.append((kpi_names[i], component_payout))

    total_projected_payout = total_payout_per_employee * total_employees

    st.success("✅ Simulation Complete")
    st.metric(label="Total Payout per Employee (₹)", value=f"₹ {total_payout_per_employee:,.2f}")
    st.metric(label="Total Projected Payout (₹)", value=f"₹ {total_projected_payout:,.2f}")

    st.markdown("---")
    st.subheader("🔍 KPI-wise Breakdown")
    for name, payout in kpi_details:
        st.write(f"**{name}:** ₹ {payout:,.2f}")

    st.markdown("""
    ### 🧮 Calculation Logic per KPI:
    - **Component Payout** = (Base Incentive × KPI % × KPI Multiplier) ÷ 4
    - **Total Payout per Employee** = Sum of all KPI payouts
    - **Total Projected Payout** = Total per employee × Total eligible employees
    """)

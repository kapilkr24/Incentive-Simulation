# 💻 Streamlit App – Incentive Simulation Tool (No Upload Required)

import streamlit as st

st.set_page_config(page_title="Incentive Simulation Tool", layout="centered")
st.title("📊 Incentive Payout Simulator")

st.markdown("""
This tool helps simulate **projected payout** for a group of employees based on:
- Average performance score (%)
- Base incentive value per employee
- Number of eligible employees

No employee-level upload is required.
""")

# Input fields
avg_score = st.number_input("Average Performance Score (%)", min_value=0.0, max_value=200.0, value=85.0, step=0.5)
total_employees = st.number_input("Total Eligible Employees", min_value=0, max_value=10000, value=100, step=1)
base_incentive = st.number_input("Base Incentive per Employee (₹)", min_value=0.0, value=50000.0, step=1000.0)

if st.button("Run Simulation"):
    multiplier = avg_score / 100
    payout_per_employee = base_incentive * multiplier
    total_payout = payout_per_employee * total_employees

    st.success("✅ Simulation Complete")

    st.metric(label="Projected Payout per Employee (₹)", value=f"₹ {payout_per_employee:,.2f}")
    st.metric(label="Total Projected Payout (₹)", value=f"₹ {total_payout:,.2f}")

    st.markdown("""
    ### 🧮 Calculation Logic:
    - **Payout per employee** = Base Incentive × (Avg Score ÷ 100)
    - **Total payout** = Payout per employee × No. of employees
    """)

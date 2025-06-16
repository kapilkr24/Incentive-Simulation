# 💻 Streamlit App – Advanced Incentive Simulation Tool

import streamlit as st

st.set_page_config(page_title="Advanced Incentive Simulator", layout="centered")
st.title("📊 Advanced Incentive Payout Simulator")

st.markdown("""
This tool allows C&B teams to simulate **complex projected payouts** based on average group performance. No employee-level upload is needed.

Includes multiple business rules:
- Revenue-based incentive multipliers
- Bonus tiers for threshold achievements
- Penalty adjustments for underperformance
""")

# Input Fields
st.header("📥 Input Parameters")
avg_score = st.number_input("Average Performance Score (%)", min_value=0.0, max_value=200.0, value=85.0, step=0.5)
total_employees = st.number_input("Total Eligible Employees", min_value=0, max_value=10000, value=100, step=1)
base_incentive = st.number_input("Base Incentive per Employee (₹)", min_value=0.0, value=50000.0, step=1000.0)

# Additional Parameters for Advanced Rules
st.subheader("Advanced Scheme Parameters")
threshold_bonus_score = st.slider("Minimum Score for Bonus Tier (%)", min_value=80, max_value=120, value=90)
bonus_amount = st.number_input("Bonus Amount per Employee (₹)", min_value=0.0, value=10000.0, step=1000.0)
underperformance_penalty = st.number_input("Penalty Deduction for Underperformance (₹)", min_value=0.0, value=5000.0, step=1000.0)
penalty_threshold = st.slider("Penalty Applies Below (%)", min_value=50, max_value=90, value=75)

if st.button("Run Simulation"):
    multiplier = avg_score / 100
    payout_per_employee = base_incentive * multiplier

    # Apply bonus if above bonus threshold
    if avg_score >= threshold_bonus_score:
        payout_per_employee += bonus_amount

    # Apply penalty if below penalty threshold
    if avg_score < penalty_threshold:
        payout_per_employee -= underperformance_penalty
        payout_per_employee = max(0, payout_per_employee)  # No negative payout

    total_payout = payout_per_employee * total_employees

    # Output Results
    st.success("✅ Simulation Complete")
    st.metric(label="Payout per Employee (₹)", value=f"₹ {payout_per_employee:,.2f}")
    st.metric(label="Total Projected Payout (₹)", value=f"₹ {total_payout:,.2f}")

    st.markdown("""
    ### 🧮 Business Logic Applied:
    - **Base Payout** = Base Incentive × (Avg Score ÷ 100)
    - **+ Bonus ₹{bonus_amount:,.0f}** if Avg Score ≥ {threshold_bonus_score}%
    - **− Penalty ₹{underperformance_penalty:,.0f}** if Avg Score < {penalty_threshold}%
    - **Total Payout** = Adjusted Payout per Employee × Total Employees
    """)

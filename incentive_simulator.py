import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Incentive Simulator", layout="wide")
st.title("💰 Incentive Payout Simulator for C&B Teams")

# --- Sidebar for Mode Selection ---
mode = st.sidebar.radio("Choose Input Mode", ["Single Employee Simulation", "Upload for Budgeting (Bulk)"])

# --- Define Slab Function ---
def get_multiplier(achievement):
    if achievement < 90:
        return 0
    elif 90 <= achievement < 100:
        return 1.0
    elif 100 <= achievement < 110:
        return 1.2
    else:
        return 1.5

# --- Define Simulation Function ---
def simulate_payout(row):
    total_weighted_score = 0
    for kpi in row['KPIs']:
        ach = row[f"{kpi}_Achievement"]
        weight = row[f"{kpi}_Weight"]
        multiplier = get_multiplier(ach)
        score = (ach / 100) * weight * multiplier
        total_weighted_score += score
    payout = row['Target Payout'] * total_weighted_score
    return payout

# --- Mode 1: Single Employee Simulation ---
if mode == "Single Employee Simulation":
    st.subheader("🔹 Enter KPI Inputs for One Employee")

    target_payout = st.number_input("Target Incentive Amount (₹)", value=100000)
    kpi_count = st.slider("Number of KPIs", min_value=1, max_value=5, value=2)

    kpi_data = []
    total_weight = 0
    for i in range(kpi_count):
        col1, col2, col3 = st.columns(3)
        with col1:
            kpi_name = st.text_input(f"KPI {i+1} Name", key=f"name_{i}")
        with col2:
            achievement = st.slider(f"Achievement % for {kpi_name}", 0, 200, 100, key=f"ach_{i}")
        with col3:
            weight = st.slider(f"Weight % for {kpi_name}", 0, 100, 50, key=f"weight_{i}") / 100
        total_weight += weight
        kpi_data.append({"KPI": kpi_name, "Achievement": achievement, "Weight": weight})

    if total_weight != 1.0:
        st.warning("⚠️ Total weightage should sum to 100%.")
    else:
        total_score = 0
        for kpi in kpi_data:
            mult = get_multiplier(kpi['Achievement'])
            score = (kpi['Achievement'] / 100) * kpi['Weight'] * mult
            total_score += score
        payout = target_payout * total_score
        st.success(f"💸 Projected Payout: ₹{payout:,.2f}")

        # Chart
        chart_df = pd.DataFrame({
            "KPI": [k['KPI'] for k in kpi_data],
            "Achievement %": [k['Achievement'] for k in kpi_data]
        })
        chart = alt.Chart(chart_df).mark_bar().encode(
            x='KPI',
            y='Achievement %',
            color='KPI'
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

# --- Mode 2: Bulk Upload ---
elif mode == "Upload for Budgeting (Bulk)":
    st.subheader("📤 Upload File for Bulk Simulation")
    sample = pd.DataFrame({
        'Employee': ['John Doe', 'Jane Smith'],
        'Target Payout': [100000, 120000],
        'KPIs': [['Revenue', 'Pipeline'], ['Revenue', 'Pipeline']],
        'Revenue_Achievement': [95, 110],
        'Revenue_Weight': [0.5, 0.6],
        'Pipeline_Achievement': [100, 105],
        'Pipeline_Weight': [0.5, 0.4]
    })
    st.download_button("📄 Download Sample Excel", data=sample.to_csv(index=False), file_name="sample_simulation.csv")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file, converters={"KPIs": eval})
        df['Simulated Payout'] = df.apply(simulate_payout, axis=1)
        st.dataframe(df)

        st.metric("📊 Total Projected Budget", f"₹{df['Simulated Payout'].sum():,.0f}")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results", csv, "simulated_payouts.csv", "text/csv")

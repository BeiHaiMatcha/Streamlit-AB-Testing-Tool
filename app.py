import os
os.system("pip install --no-cache-dir scipy numpy pandas pymc matplotlib")

import streamlit as st
import numpy as np
import scipy.stats as stats
import pandas as pd
import pymc as pm
import matplotlib.pyplot as plt


# Apply Universal Theme Colors and Custom Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        body { background-color: #F9FAFC; font-family: 'Poppins', sans-serif; }
        .title { text-align: center; font-size: 42px; font-weight: 600; color: #2A2A2A; margin-bottom: 10px; }
        .subtitle { text-align: center; font-size: 24px; font-weight: 400; color: #6C63FF; margin-bottom: 20px; }
        .fun-text { font-size: 18px; color: #6C63FF; font-weight: bold; }
        .stButton>button { background-color: #6C63FF; color: white; border-radius: 12px; padding: 10px 18px; font-size: 18px; font-family: 'Poppins', sans-serif; border: none; }
        .stDataFrame { background-color: #F1F3F8; border-radius: 12px; padding: 5px; }
        .stCheckbox>label { color: #2A2A2A; font-size: 16px; font-family: 'Poppins', sans-serif; }
        .info-text { font-size: 18px; color: #2A2A2A; text-align: center; line-height: 1.7; font-family: 'Poppins', sans-serif; }
        .footer { text-align: center; font-size: 16px; color: #6C63FF; margin-top: 40px; padding-top: 20px; border-top: 1px solid #6C63FF; font-family: 'Poppins', sans-serif; }
        .sidebar-text { font-size: 16px; color: #2A2A2A; font-family: 'Poppins', sans-serif; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

# Streamlit App Title with Updated Font
st.markdown("<div class='title'>🎉 Welcome to the A/B Testing Playground! 🎉</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Effortless Statistical Testing for Everyone ✨</div>", unsafe_allow_html=True)

st.markdown("""
<div class='info-text'>
    🚀 Provide your test details in the table below. No need to fill multiple forms! 🎯<br>
    📌 <b>Enter your segments, categories, and relevant data in the table.</b> 📝<br>
    📌 <b>Enter absolute counts only</b> (e.g., 500 clicks, **not** 0.25 for 25%). 📝<br>
    📌 <i><b>Why absolute counts?</b> To ensure consistency across different statistical tests, we require absolute counts rather than rates. Tests like the Chi-Square test work with actual counts, and keeping everything in counts allows for a more universal approach to A/B testing.</i> 📊
</div>
""", unsafe_allow_html=True)
# Add Footer with Creator Info
st.markdown("<div class='footer'>✨ Created by Bei | Product Analytics & Experimentation 👩‍💻 | Powered by Streamlit 🚀</div>", unsafe_allow_html=True)


# Sidebar Guide for Choosing the Right Test
st.sidebar.header("📊 Choosing the Right Test 🧐")
st.sidebar.markdown("<div class='fun-text'>📈 T-Test (For Continuous Data, Two Groups)</div>", unsafe_allow_html=True)
st.sidebar.write("Use this test when comparing the **average** of a continuous metric (e.g., AOV) between **two** groups.")

st.sidebar.markdown("<div class='fun-text'>📊 Chi-Square Test (For Proportions)</div>", unsafe_allow_html=True)
st.sidebar.write("""
Use this test when comparing **proportions** or **conversion rates** (e.g., Click-through Rate, Purchase Rate).  
🔹 **Enter absolute counts only** (e.g., number of conversions, number of clicks).  
🔹 **We do not accept percentages (e.g., 25%) or decimals (e.g., 0.25).**   
🔹 This ensures a **universal approach** across all statistical tests.
""")

st.sidebar.markdown("<div class='fun-text'>📊 ANOVA (For Continuous Data, More Than Two Groups)</div>", unsafe_allow_html=True)
st.sidebar.write("Use this test when comparing the **average** of a continuous metric across **three or more** groups.")

st.sidebar.markdown("<div class='fun-text'>🎲 Bayesian Testing (For Probability-Based Insights)</div>", unsafe_allow_html=True)
st.sidebar.write("Want more than just a yes/no significance? Bayesian testing provides **probability-based insights** into which variant is better!")

st.markdown("""
    <div style="text-align: center; background-color: #FFF3CD; padding: 10px; border-radius: 5px; border-left: 5px solid #FFC107; font-size: 16px;">
        ⚠️ If you started a new row and didn't fill it, please delete it before running the test.
    </div>
""", unsafe_allow_html=True)

# Default Data for the Table
default_data = pd.DataFrame({
    "Segment": ["FI", "NO"],  # Empty row added
    "Category": ["Category A", "Category B"],
    "Sample Size - Control": [2500, 2700],
    "Sample Size - Variant": [2500, 2700],
    "Metric Type": ["Categorical", "Continuous"],  # Dropdown Selection
    "Control Value (Absolute)": [500, 600],  # Absolute counts only
    "Variant Value (Absolute)": [550, 720],  # Absolute counts only
    "Test Type": ["Chi-Square", "T-Test"]
})


# Let users edit the table
st.write("### Fill in your test details 📝")
edited_data = st.data_editor(
    default_data,
    num_rows="dynamic",
    column_config={
        "Metric Type": st.column_config.SelectboxColumn(options=["Categorical", "Continuous"]),
        "Test Type": st.column_config.SelectboxColumn(options=["Chi-Square", "T-Test", "ANOVA"])
    },
    height=275  # Enables scrolling
)


# Function to Interpret P-Value
def interpret_p_value(p_value):
    significance_level = 0.05
    if p_value < significance_level:
        return f"🎉 **Significant Result!** The p-value ({p_value:.4f}) is below {significance_level}, meaning there is strong evidence that the difference is not due to chance."
    else:
        return f"⚠️ **Not Significant.** The p-value ({p_value:.4f}) is above {significance_level}, meaning we do not have strong evidence to reject the null hypothesis."

# Run Statistical Tests
if st.button("Run Analysis 🚀"):
    for _, row in edited_data.iterrows():
        Segment = row["Segment"]
        Category = row["Category"]
        sample_size_control = int(row["Sample Size - Control"])
        sample_size_variant = int(row["Sample Size - Variant"])
        metric_type = row["Metric Type"]
        control_value = row["Control Value (Absolute)"]
        variant_value = row["Variant Value (Absolute)"]
        test_selection = row["Test Type"]

        st.write(f"### Results for {Segment} | {Category}")

        if test_selection == "T-Test":
            t_stat, p_value = stats.ttest_ind_from_stats(
                mean1=control_value, std1=10, nobs1=sample_size_control,
                mean2=variant_value, std2=10, nobs2=sample_size_variant,
                equal_var=False
            )
            st.write(f"📊 **T-Test Results:** t-statistic = {t_stat:.4f}, p-value = {p_value:.4f}")
            st.write(interpret_p_value(p_value))

        elif test_selection == "Chi-Square":
            observed = np.array([[control_value, sample_size_control - control_value],
                                 [variant_value, sample_size_variant - variant_value]])
            chi2, p_value, _, _ = stats.chi2_contingency(observed)
            st.write(f"📊 **Chi-Square Test Results:** Chi2 = {chi2:.4f}, p-value = {p_value:.4f}")
            st.write(interpret_p_value(p_value))

        elif test_selection == "ANOVA":
            f_stat, p_value = stats.f_oneway(
                np.random.normal(control_value, 1, sample_size_control),
                np.random.normal(variant_value, 1, sample_size_variant)
            )
            st.write(f"📊 **ANOVA Results:** F-statistic = {f_stat:.4f}, p-value = {p_value:.4f}")
            st.write(interpret_p_value(p_value))

# Bayesian Analysis Option
st.write("### Optional Bayesian Analysis 🎲")
use_bayesian = st.checkbox("Do you want to see the probability that the variant is better?")

if use_bayesian:
    st.subheader("Bayesian Analysis 🎲")

    for _, row in edited_data.iterrows():
        Segment = row["Segment"]
        Category = row["Category"]
        sample_size_control = int(row["Sample Size - Control"])
        sample_size_variant = int(row["Sample Size - Variant"])
        metric_type = row["Metric Type"]
        control_value = row["Control Value (Absolute)"]
        variant_value = row["Variant Value (Absolute)"]

        st.write(f"### Bayesian Analysis for {Segment} | {Category}")

        with pm.Model() as model:
            if metric_type == "Categorical":
                # Bayesian approach for conversion rates (CR%)
                prior_control = pm.Beta("control", 2, 2)
                prior_variant = pm.Beta("variant", 2, 2)
                observed_control = pm.Binomial("obs_control", p=prior_control, n=sample_size_control, observed=int(control_value))
                observed_variant = pm.Binomial("obs_variant", p=prior_variant, n=sample_size_variant, observed=int(variant_value))
            else:
                # Bayesian approach for AOV (continuous data)
                prior_control = pm.Normal("control", mu=control_value, sigma=10)
                prior_variant = pm.Normal("variant", mu=variant_value, sigma=10)
                observed_control = pm.Normal("obs_control", mu=prior_control, sigma=10, observed=control_value)
                observed_variant = pm.Normal("obs_variant", mu=prior_variant, sigma=10, observed=variant_value)

            trace = pm.sample(2000, return_inferencedata=True, progressbar=False)

        pm.plot_posterior(trace, var_names=["control", "variant"], figsize=(10, 4))
        st.pyplot(plt)

        # Compute probability that variant is better
        prob_variant_better = np.mean(trace.posterior["variant"].values > trace.posterior["control"].values)
        st.write(f"🎯 **Probability that the Variant is better: {prob_variant_better:.2%}**")

        # Compute 95% HDI (Highest Density Interval)
        hdi_low, hdi_high = np.percentile(trace.posterior["variant"].values - trace.posterior["control"].values, [2.5, 97.5])
        st.write(f"📊 **95% HDI:** [{hdi_low:.4f}, {hdi_high:.4f}]")

        # Interpretation of HDI
        if hdi_low > 0:
            st.write(f"🎉 **Strong Evidence of an Effect!** The 95% HDI is [{hdi_low:.4f}, {hdi_high:.4f}], meaning the variant likely has a positive impact.")
        elif hdi_high < 0:
            st.write(f"⚠️ **Strong Evidence of a Negative Effect!** The 95% HDI is [{hdi_low:.4f}, {hdi_high:.4f}], meaning the variant may harm performance.")
        else:
            st.write(f"🤔 **Inconclusive Test.** The 95% HDI is [{hdi_low:.4f}, {hdi_high:.4f}], meaning we cannot rule out no effect. More data may be needed.")
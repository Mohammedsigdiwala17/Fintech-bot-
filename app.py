import streamlit as st
from openai import OpenAI
import io
import pandas as pd
import matplotlib.pyplot as plt

# ---- PAGE SETUP ----
st.set_page_config(page_title="FinBot AI - Virtual Tax Assistant", layout="centered")

st.title("💼 FinBot AI – Smart Tax & Finance Assistant")
st.markdown("### Instantly calculate Income Tax, GST & get AI-based financial insights 🇮🇳")

# ---- OPENAI CLIENT ----
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---- USER INPUTS ----
st.subheader("📋 Enter Your Financial Details")

col1, col2 = st.columns(2)
with col1:
    income = st.number_input("Total Annual Income (₹)", min_value=0)
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    marital_status = st.selectbox("Marital / Family Status", ["Single", "Married", "With Dependents"])
    business_type = st.selectbox("Type of Income", ["Freelance", "Business", "Salary", "Other"])
with col2:
    ded_80C = st.number_input("Deduction under 80C (₹)", min_value=0)
    ded_80D = st.number_input("Deduction under 80D (₹)", min_value=0)
    other_deductions = st.number_input("Other Deductions (₹)", min_value=0)
    tds_paid = st.number_input("TDS Paid (₹)", min_value=0)
    prof_tax = st.number_input("Professional Tax (₹)", min_value=0)

gst_collected = st.number_input("GST Collected (₹)", min_value=0)
gst_paid = st.number_input("GST Paid (₹)", min_value=0)
regime_preference = st.selectbox("Preferred Tax Regime", ["Compare Both", "Old Regime", "New Regime"])

# ---- PROMPT CREATION ----
prompt = f"""
You are FinBot AI, a professional financial assistant for Indian freelancers, salaried individuals, and business owners.

Calculate and summarize the following based on Indian tax rules (FY 2025–26):

Income: ₹{income}
Age: {age}
Marital/Family Status: {marital_status}
Income Type: {business_type}
Deductions: 80C ₹{ded_80C}, 80D ₹{ded_80D}, Other ₹{other_deductions}
TDS Paid: ₹{tds_paid}, Professional Tax: ₹{prof_tax}
GST Collected: ₹{gst_collected}, GST Paid: ₹{gst_paid}
Preferred Regime: {regime_preference}

Return a clear financial summary including:
1. Taxable Income  
2. Tax (Old vs New Regime)  
3. Recommended Regime  
4. Net Income After Tax  
5. GST Payable / Refund  
6. Recommended ITR Form  
7. Tax Saving Tips  
8. A professional summary in bullet points with ₹ formatting.
"""

# ---- ANALYSIS BUTTON ----
if st.button("💡 Generate Tax Summary"):
    if income == 0:
        st.warning("Please enter your income details to calculate.")
    else:
        with st.spinner("🧮 Calculating..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                result = response.choices[0].message.content

                # ---- DISPLAY RESULTS ----
                st.success("✅ Tax Summary Generated Successfully!")
                st.markdown("### 📊 Your Tax Summary")
                st.markdown(result)

                # ---- COPY SUMMARY ----
                st.code(result, language="markdown")
                st.download_button(
                    label="📥 Download Report (PDF)",
                    data=result.encode("utf-8"),
                    file_name="FinBot_AI_Tax_Report.pdf",
                    mime="application/pdf"
                )

                # ---- INCOME VS EXPENSE DASHBOARD ----
                st.markdown("---")
                st.markdown("### 📈 Income vs Expenses Dashboard")

                total_deductions = ded_80C + ded_80D + other_deductions + prof_tax + tds_paid
                gst_payable = max(gst_collected - gst_paid, 0)
                net_income = income - total_deductions - gst_payable

                data = {
                    "Category": ["Total Income", "Deductions", "GST Payable", "Net Income"],
                    "Amount (₹)": [income, total_deductions, gst_payable, net_income]
                }

                df = pd.DataFrame(data)

                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(df["Category"], df["Amount (₹)"])
                ax.set_title("💰 Income vs Expenses Overview")
                ax.set_ylabel("Amount (₹)")
                st.pyplot(fig)

                st.caption("This chart shows how your deductions and GST affect your total net income.")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

# ---- FUTURE FEATURES ----
st.markdown("---")
st.markdown("### 🔮 Coming Soon Features")
st.markdown("""
- 📊 Auto Income vs Expense Tracking Dashboard  
- 🧾 Automated ITR Filing Assistant  
- 💡 Smart Investment Recommendations  
- 📈 Yearly Financial Planner with AI Predictions  
""")

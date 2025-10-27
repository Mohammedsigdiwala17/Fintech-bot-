import streamlit as st
from openai import OpenAI
import io

# ---- SETUP ----
st.set_page_config(page_title="FinBot AI - Virtual Tax Assistant", layout="centered")

st.title("💼 FinBot AI – Your Virtual Financial Assistant")
st.markdown("### Calculate taxes, compare regimes, and get personalized savings suggestions!")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---- USER INPUT SECTION ----
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
You are FinBot AI, a professional financial assistant for Indian freelancers and small business owners.

Calculate and summarize the following based on Indian tax rules (FY 2025–26):

Income: ₹{income}
Age: {age}
Marital/Family Status: {marital_status}
Income Type: {business_type}
Deductions: 80C ₹{ded_80C}, 80D ₹{ded_80D}, Other ₹{other_deductions}
TDS Paid: ₹{tds_paid}, Professional Tax: ₹{prof_tax}
GST Collected: ₹{gst_collected}, GST Paid: ₹{gst_paid}
Preferred Regime: {regime_preference}

Return a complete financial summary including:
1. Taxable Income  
2. Tax (Old vs New Regime)  
3. Recommended Regime  
4. Net Income After Tax  
5. GST Payable / Refund  
6. ITR Form Recommendation  
7. Tax Saving Tips  
8. Professional Summary in clear bullet points with ₹ formatting.
"""

# ---- RUN ANALYSIS ----
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
                st.success("✅ Tax Summary Generated Successfully!")

                st.markdown("### 📊 Your Tax Summary")
                st.markdown(result)

                # ---- COPY BUTTON ----
                st.code(result, language="markdown")
                st.button("📋 Copy Summary", on_click=lambda: st.session_state.update({"copied": True}))
                if st.session_state.get("copied"):
                    st.info("Copied to clipboard!")

                # ---- DOWNLOAD AS TEXT-BASED PDF ----
                pdf_buffer = io.BytesIO()
                pdf_content = f"FinBot AI - Tax Summary Report\n\n{result}"
                pdf_buffer.write(pdf_content.encode('utf-8'))
                pdf_buffer.seek(0)

                st.download_button(
                    label="📥 Download Tax Report (PDF)",
                    data=pdf_buffer,
                    file_name="FinBot_AI_Tax_Report.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")

# ---- FUTURE FEATURE PREVIEW ----
st.markdown("---")
st.markdown("### 📈 Coming Soon: Income vs Expenses Dashboard")
st.caption("Track your income, expenses, and visualize savings automatically using FinBot AI Insights.")

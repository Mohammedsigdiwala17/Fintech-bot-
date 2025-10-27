import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import datetime

# -------------------- Page Setup --------------------
st.set_page_config(page_title="FinBot AI", page_icon="💰", layout="centered")
st.title("💰 FinBot AI – Your Personal Tax & GST Assistant")

# -------------------- Sidebar Premium Info --------------------
st.sidebar.header("FinBot AI Premium")
st.sidebar.info("""
- Download detailed PDF reports
- Personalized tax-saving strategy
- Historical tax comparison
""")

# -------------------- User Inputs --------------------
st.header("Enter Your Financial Details")

income = st.number_input("Total Annual Income (₹)", min_value=0)
ded_80C = st.number_input("Deductions under 80C (₹)", min_value=0)
ded_80D = st.number_input("Deductions under 80D (₹)", min_value=0)
other_deductions = st.number_input("Other Deductions (₹)", min_value=0)
tds_paid = st.number_input("TDS Already Paid (₹)", min_value=0)
prof_tax = st.number_input("Professional Tax (₹)", min_value=0)
gst_collected = st.number_input("GST Collected (₹)", min_value=0)
gst_paid = st.number_input("GST Paid (₹)", min_value=0)

age = st.number_input("Your Age", min_value=18, max_value=120)
marital_status = st.selectbox("Marital Status", ["Single", "Married"])
business_type = st.selectbox("Income Type", ["Salaried", "Freelancer", "Business"])
regime_preference = st.selectbox("Preferred Tax Regime", ["Old", "New", "Auto"])

user_question = st.text_input("Or ask a question to FinBot AI (optional):")

# -------------------- OpenAI API Client --------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------- Generate Tax Summary --------------------
if st.button("Generate Tax Summary") or user_question:
    prompt = f"""
    You are FinBot AI, a professional financial assistant and virtual accountant for Indian freelancers, small business owners, and self-employed professionals. 

    User Input: 
    - Total annual income: ₹{income}  
    - Deductions: 80C ₹{ded_80C}, 80D ₹{ded_80D}, other ₹{other_deductions}  
    - TDS paid: ₹{tds_paid}  
    - Professional tax: ₹{prof_tax}  
    - GST collected: ₹{gst_collected}, GST paid: ₹{gst_paid}  
    - Age: {age}  
    - Marital/family status: {marital_status}  
    - Income type: {business_type}  
    - Preferred tax regime: {regime_preference}  

    Your task: Generate a full tax summary including:
    1. Taxable Income
    2. Total Tax (Old vs New)
    3. Recommended Regime
    4. Net Income After Tax
    5. GST Payable / Refund
    6. Recommended ITR Form
    7. Tax-saving tips

    If the user asked a question: "{user_question}", answer it based on the financial data above.
    Explain calculations step-by-step in ₹. Make it ready for display in Streamlit.
    """

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are FinBot AI, a professional financial assistant for Indian freelancers and small business owners."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    tax_summary = response.choices[0].message.content
    st.subheader("✅ FinBot AI Tax Summary")
    st.write(tax_summary)

    # -------------------- PDF Download --------------------
    if st.button("Download PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 6, txt=f"FinBot AI Tax & GST Report\nGenerated on {datetime.date.today()}\n\n{tax_summary}")
        pdf_file = f"FinBot_Report_{datetime.date.today()}.pdf"
        pdf.output(pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name=pdf_file)
        st.success("✅ PDF report generated successfully!")

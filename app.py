import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import base64
from fpdf import FPDF

# ---------------------- PAGE SETUP ----------------------
st.set_page_config(page_title="FinBot AI 💰", layout="centered")
st.title("💰 FinBot AI — Smart Indian Tax & Finance Assistant 🇮🇳")
st.caption("Your AI-based financial assistant for taxes, GST & finance management")

# ---------------------- OPENAI API ----------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------------------- USER INPUTS ----------------------
st.header("🧾 Enter Your Financial Details")

col1, col2 = st.columns(2)
with col1:
    total_income = st.number_input("Total Annual Income (₹)", min_value=0)
    deductions_80C = st.number_input("Deductions under 80C (₹)", min_value=0, max_value=150000)
    deductions_80D = st.number_input("Deductions under 80D (₹)", min_value=0)
    other_deductions = st.number_input("Other Deductions (₹)", min_value=0)
    age = st.number_input("Age", min_value=18, max_value=100)

with col2:
    tds_paid = st.number_input("TDS Paid (₹)", min_value=0)
    professional_tax = st.number_input("Professional Tax (₹)", min_value=0)
    gst_collected = st.number_input("GST Collected (₹)", min_value=0)
    gst_paid = st.number_input("GST Paid (₹)", min_value=0)
    regime = st.selectbox("Preferred Tax Regime", ["Old", "New"])

income_type = st.selectbox("Income Type", ["Salaried", "Freelancer", "Business"])
family_status = st.selectbox("Family Status", ["Single", "Married", "Senior Citizen"])

st.markdown("---")

# ---------------------- INCOME VS EXPENSES DASHBOARD ----------------------
st.header("📊 Income vs Expenses Dashboard (Future Feature)")

with st.expander("💡 Open Dashboard"):
    st.write("Enter your monthly income and expenses to view your annual savings trend 👇")

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    income_data, expense_data = [], []

    col1, col2 = st.columns(2)
    for month in months:
        with col1:
            income = st.number_input(f"{month} Income (₹)", min_value=0, key=f"in_{month}")
            income_data.append(income)
        with col2:
            expense = st.number_input(f"{month} Expense (₹)", min_value=0, key=f"ex_{month}")
            expense_data.append(expense)

    if st.button("📈 Generate Dashboard"):
        df = pd.DataFrame({"Month": months, "Income": income_data, "Expenses": expense_data})
        df["Net Savings"] = df["Income"] - df["Expenses"]

        st.dataframe(df)
        fig, ax = plt.subplots()
        ax.plot(df["Month"], df["Income"], label="Income", marker="o")
        ax.plot(df["Month"], df["Expenses"], label="Expenses", marker="o")
        ax.plot(df["Month"], df["Net Savings"], label="Net Savings", marker="o")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (₹)")
        ax.legend()
        st.pyplot(fig)

        st.success(f"🎯 Total Annual Savings: ₹{df['Net Savings'].sum():,.0f}")

st.markdown("---")

# ---------------------- TAX REPORT GENERATION ----------------------
if st.button("🤖 Generate AI Tax Report"):
    with st.spinner("Analyzing your data and generating report..."):

        prompt = f"""
        You are FinBot AI, a professional Indian tax consultant.
        Based on this data:
        Income ₹{total_income}, Age {age}, 80C ₹{deductions_80C}, 80D ₹{deductions_80D},
        Other ₹{other_deductions}, TDS ₹{tds_paid}, Professional Tax ₹{professional_tax},
        GST Collected ₹{gst_collected}, GST Paid ₹{gst_paid}, Family: {family_status}, Type: {income_type}, Regime: {regime}.
        Return:
        1. Taxable income
        2. Tax under Old & New regimes
        3. Recommended regime
        4. GST payable/refund
        5. ITR form
        6. Tax-saving tips
        7. Net income after tax
        Explain clearly using rupee symbols and headings.
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        result = response.choices[0].message.content
        st.subheader("📄 AI-Generated Tax Report")
        st.markdown(result)
        st.code(result)

        # PDF Download
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, result)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        st.download_button(
            "📥 Download Report as PDF",
            data=pdf_output,
            file_name="FinBot_Tax_Report.pdf",
            mime="application/pdf"
        )

st.markdown("---")

# ---------------------- VOICE QUERY ASSISTANT ----------------------
st.header("🎙️ FinBot Voice Assistant")
st.caption("Ask FinBot any finance or tax question using your voice (e.g., 'How can I save tax under 80C?').")

if st.button("🎤 Start Listening"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening... Please speak clearly.")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        st.info("Processing your query...")

    try:
        query = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {query}")

        voice_prompt = f"You are FinBot AI, an Indian tax & finance assistant. Answer briefly: {query}"
        voice_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": voice_prompt}],
            temperature=0.4,
        )
        answer = voice_response.choices[0].message.content
        st.write("💬 FinBot says:")
        st.markdown(answer)

        # Text-to-speech response
        tts = gTTS(answer)
        voice_bytes = BytesIO()
        tts.write_to_fp(voice_bytes)
        voice_bytes.seek(0)
        audio_base64 = base64.b64encode(voice_bytes.read()).decode()
        st.audio(f"data:audio/mp3;base64,{audio_base64}", format="audio/mp3")

    except sr.UnknownValueError:
        st.error("⚠️ Sorry, I couldn't understand your voice. Please try again.")
    except sr.RequestError:
        st.error("⚠️ Voice recognition service unavailable. Try again later.")

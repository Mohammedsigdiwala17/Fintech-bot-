# 💰 FinBot AI — Smart Indian Tax & Finance Assistant 🇮🇳

## 🧠 Overview  
**FinBot AI** is an intelligent AI-powered **virtual tax assistant** built for Indian freelancers, salaried individuals, and business owners.  
It helps calculate **Income Tax**, **GST**, and recommends the correct **ITR form** — all instantly and interactively using **AI + Streamlit**.

FinBot uses **OpenAI’s GPT model** to simplify tax calculations and financial guidance in human-friendly language.

---

## ⚙️ Features  

| Feature | Description |
|----------|--------------|
| 💵 **Income Tax Calculator** | Calculates tax under both Old & New regimes (FY 2025–26) |
| 🧾 **ITR Recommendation** | Suggests the correct ITR form (ITR-1, ITR-2, ITR-3, etc.) |
| 🧮 **GST Calculation** | Computes CGST, SGST, and IGST based on your business details |
| 📊 **Regime Comparison** | Shows Old vs New regime comparison with savings |
| 💡 **Tax-Saving Suggestions** | Personalized deductions under 80C, 80D, NPS, etc. |
| 👤 **User Types** | Supports Salaried, Freelancer, and Business Income |
| 📄 **Downloadable Summary** | Option to export your result as a PDF or copy the summary text |

---

## 🧾 Example Input  

| Field | Example Value |
|--------|----------------|
| Total annual income | ₹12,00,000 |
| Deductions under 80C | ₹1,50,000 |
| Deductions under 80D | ₹25,000 |
| Other deductions | ₹20,000 |
| TDS paid | ₹50,000 |
| Professional tax | ₹2,500 |
| GST collected | ₹1,20,000 |
| GST paid | ₹80,000 |
| Age | 29 |
| Marital/family status | Single |
| Income type | Freelancer |
| Preferred tax regime | New |

---

## 🧠 Tech Stack  

- **Frontend:** Streamlit  
- **Backend:** Python  
- **AI Engine:** OpenAI GPT-4o  
- **PDF Generation:** FPDF  
- **Deployment:** Streamlit Cloud  

---

## 🚀 How to Run Locally  

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/finbot-ai.git
cd finbot-ai
🌐 Deploy on Streamlit Cloud
	1.	Go to https://share.streamlit.io
	2.	Connect your GitHub repository
	3.	Choose your repo → branch → select app.py
	4.	Go to Settings → Secrets and add:
🧑‍💻 Developer

Created by: Mohammed Sigdiwala
Purpose: To simplify Indian taxation and finance for everyone using AI 💼🤖
🏦 License

This project is open for educational and personal use.
For commercial or SaaS usage, please provide credit or link back to this repository.

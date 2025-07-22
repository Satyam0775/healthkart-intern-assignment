# 💼 HealthKart Influencer Campaign Dashboard

This project is submitted as part of the **HealthKart Internship Assignment** (Data Science Track). It provides a fully functional dashboard for tracking and analyzing the performance of influencer marketing campaigns across different platforms and brands.

---

## 📌 Objective

Build an open-source tool or dashboard that can:
- 📊 Track campaign performance
- 💸 Measure ROI & ROAS (Return on Ad Spend)
- 👤 Analyze influencer performance and payout structure
- 📈 Identify top/bottom influencers and poor ROAS
- 📤 Export filtered insights

---

## 🗂️ Project Structure

```bash
healthkart_intern_assignment/
├── streamlit_dashboard.py       # ✅ Main Streamlit dashboard app
├── data/
│   ├── influencers.csv          # Influencer metadata
│   ├── payouts.csv              # Payout per influencer
│   ├── tracking_data.csv        # Campaign + conversion data
├── outputs/
│   └── exports/                 # Optional CSV downloads
├── README.md                    # 📘 You are here
├── requirements.txt             # 📦 Required Python libraries


📦 Installation
1. Install Python libraries

pip install -r requirements.txt
2. Run the Streamlit App

streamlit run streamlit_dashboard.py
📊 Features
Filters: Platform, category, and minimum ROAS slider

Summary Metrics: Total Revenue, Total Payout, Average ROAS

Visualizations:

Top 10 Influencers by ROAS (bar chart)

Revenue vs Payout Spread (scatter + line)

Detailed Table: All influencer details with ROAS

Download: Export filtered influencer data as CSV

Dark Theme: Modern black + green visual style

🧠 Sample Insights
Top 5 influencers by ROAS tend to be in the Fitness, Tech, and Travel categories.

Platforms like YouTube and Instagram give better ROI when campaigns are order-based.

Poor ROAS is usually due to high payouts with low order conversion.

✅ Assumptions
ROAS is calculated as:
ROAS = revenue / total_payout

Influencer ID column was standardized across CSVs
Missing or zero payout → ROAS is set to 0
Dummy simulated dataset was used for demonstration

🧾 requirements.txt

streamlit
pandas
plotly
matplotlib
seaborn
✨ Optional Extensions
Export PDF insights report

Incremental ROAS via A/B modeling

Deployment to Streamlit Cloud 

📬 Contact
Satyam Kumar

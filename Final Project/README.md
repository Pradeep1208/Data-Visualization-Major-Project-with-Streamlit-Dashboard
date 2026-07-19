# 💼 Glassdoor Jobs & Salary Analytics Dashboard

An interactive, multi-page Streamlit dashboard (Plotly-only visualizations) analyzing real-world
Glassdoor job postings — industry/company salary drivers, technical skill demand, and a
machine-learning salary predictor.

## Folder Structure

```text
Glassdoor_Salary_Project/
├── data/
│   └── salary_data_cleaned.csv      # cleaned & feature-engineered dataset
├── models/
│   ├── salary_model.pkl             # best trained regression model
│   ├── scaler.pkl                   # StandardScaler used at train time
│   └── encoder.pkl                  # dict of LabelEncoders per categorical column
├── pages/
│   ├── 01_📊_Dashboard.py
│   ├── 02_🏢_Company_Analysis.py
│   ├── 03_💰_Salary_Explorer.py
│   ├── 04_🛠️_Skills_Analysis.py
│   └── 05_🤖_Salary_Predictor.py
├── app.py                           # entry point / Home page / navigation
├── utils.py                         # cached data + model loading, predict_salary()
├── config.py                        # paths, column lists, theme
├── Glassdoor_Salary_Analysis.ipynb  # data cleaning, EDA (12 questions), ML training notebook
├── requirements.txt
└── README.md
```

## How to Run

1. **Generate the data & model artifacts** (if not already present):
   Open `Glassdoor_Salary_Analysis.ipynb` and run all cells. It will produce
   `data/salary_data_cleaned.csv` and `models/salary_model.pkl` / `scaler.pkl` / `encoder.pkl`.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```

4. Open the URL Streamlit prints (usually `http://localhost:8501`).

## Pages

| Page | What it shows |
|---|---|
| 🏠 Home | KPI cards, dataset summary, navigation |
| 📊 Dashboard Overview | Salary distribution, top industries, ratings, top hiring industries |
| 🏢 Company Analysis | Top-paying companies, rating/revenue/size/age vs. salary |
| 💰 Salary Explorer | Salary trends by industry, state, job title, company size |
| 🛠️ Skills Analysis | Skill demand, salary impact per skill, skill correlations, top combos |
| 🤖 Salary Predictor | ML-powered salary estimate for a new job posting |

## Deployment

This app is ready for **Streamlit Community Cloud**: push this folder to a GitHub repo, then
deploy by pointing Streamlit Cloud at `app.py`.

"""
app.py — entry point. Defines the multi-page navigation and the Home / KPI landing page.
Run with:  streamlit run app.py
"""

import streamlit as st
from utils import load_data, kpi_dict
from config import APP_TITLE, APP_ICON

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")


def home():
    """Home / KPI landing page — rendered when 'Home' is selected in the nav."""
    df = load_data()
    kpis = kpi_dict(df)

    st.title(f"{APP_ICON} {APP_TITLE}")
    st.markdown(
        "An interactive analytics dashboard exploring **salary drivers, industry trends, "
        "and technical skill demand** from real-world Glassdoor job postings — "
        "plus a machine-learning salary predictor."
    )

    st.markdown("### Key Metrics")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Jobs", kpis["Total Jobs"])
    c2.metric("Total Companies", kpis["Total Companies"])
    c3.metric("Total Industries", kpis["Total Industries"])
    c4.metric("Avg Salary", f"${kpis['Average Salary ($K)']}K")
    c5.metric("Highest Salary", f"${kpis['Highest Salary ($K)']}K")
    c6.metric("Lowest Salary", f"${kpis['Lowest Salary ($K)']}K")

    st.divider()
    st.markdown("### Explore the Dashboard")
    st.markdown(
        """
- **📊 Dashboard Overview** — salary distribution, top industries, ratings
- **🏢 Company Analysis** — top-paying companies, rating/revenue/age vs. salary
- **💰 Salary Explorer** — salary trends by industry, state, and job title
- **🛠️ Skills Analysis** — which technical skills are in demand and pay the most
- **🤖 Salary Predictor** — predict a salary for a new job posting using ML
        """
    )
    st.caption("Data source: Glassdoor Jobs Dataset (Kaggle) · Model: trained in the companion notebook")


# ── Navigation ──────────────────────────────────────────────────────────
# Home is a Python function (not a file) so app.py doesn't recursively re-run itself.
pg = st.navigation([
    st.Page(home, title="Home", icon="🏠", default=True),
    st.Page("pages/01_📊_Dashboard.py", title="Dashboard Overview", icon="📊"),
    st.Page("pages/02_🏢_Company_Analysis.py", title="Company Analysis", icon="🏢"),
    st.Page("pages/03_💰_Salary_Explorer.py", title="Salary Explorer", icon="💰"),
    st.Page("pages/04_🛠️_Skills_Analysis.py", title="Skills Analysis", icon="🛠️"),
    st.Page("pages/05_🤖_Salary_Predictor.py", title="Salary Predictor", icon="🤖"),
])
pg.run()

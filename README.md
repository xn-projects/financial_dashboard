# Financial Resilience Dashboard 

This project explores how companies balance liquidity and long-term debt to evaluate their financial resilience. The goal is to provide clear, interactive insights into how well different companies can cover debt obligations with liquid assets.

The dashboard was initially prototyped in Tableau for rapid exploration, then rebuilt using Python, Plotly Dash, and FastAPI to support automation, API integration, and scalable deployment.

---

## Live Versions

* **Tableau Prototype:** (first exploratory version)<br>
  [https://public.tableau.com/app/profile/kseniia.chepigina/viz/EvolutionofCCPLTD/Dashboard12](https://public.tableau.com/app/profile/kseniia.chepigina/viz/EvolutionofCCPLTD/Dashboard12)

* **Plotly Dash Application:** (production interactive dashboard)<br>
  [https://financial-dashboard-ep61.onrender.com/dashboard/](https://financial-dashboard-ep61.onrender.com/dashboard/)

---

## Dashboard Preview

The dashboard includes five analytical views:

### 1. CCP & LTD by Company

This view shows how cash reserves and long-term debt evolve over time for each company. A widening gap between CCP and LTD indicates improving liquidity strength, while convergence or crossing patterns may signal rising financial pressure. Trends of liquid assets vs long‑term debt.

![CCP & LTD by Company](images/CCP%20&%20LTD%20by%20Company.png)

### 2. Debt Coverage Ratio

This ratio highlights the company’s ability to cover debt with available liquid assets. Stable or rising values imply stronger resilience. Companies consistently below 0.5 may face higher refinancing or liquidity risks. CCP/LTD ratio over time as an indicator of resilience.

![Debt Coverage Ratio](images/Debt%20Coverage%20Ratio.png)

### 3. Financial Resilience Heatmap

The color gradient helps quickly identify periods of financial stress or stability. Cooler tones (higher CCP/LTD) point to stronger liquidity positions, while warmer tones highlight potentially vulnerable quarters. Quarter-by-quarter comparison across companies.

![Financial Resilience Heatmap](images/Financial%20Resilience%20Heatmap.png)

### 4. Debt vs Liquid Assets (all)

This visualization compares companies’ liquidity (CCP) and long-term debt (LTD), with the option to view either the most recent quarter or any selected reporting period.

It helps evaluate balance sheet positioning:

- **Bottom-right quadrant** → stronger liquidity relative to debt  
- **Top-left quadrant** → higher leverage pressure  

By switching between quarters or aggregated time ranges, you can observe how company positions shift over time:

- **Rightward movement** → growing liquid assets
- **Upward movement** → increasing long-term debt

This allows analysis of both the current financial state and longer-term strategic trends.


![Debt vs Liquid Assets (all)](images/Debt%20vs%20Liquid%20Assets%20\(all\).png)

---

## Interaction

The dashboard supports:

* Selecting one or multiple companies for comparison.
* Choosing any time period from 2019 to 2024.
* Switching between absolute values (CCP & LTD) and ratios (CCP/LTD).
* Exploring both the latest financial positions and long‑term trajectories.

### Why These Metrics?

* **CCP (Cash & Cash Position)** reflects a company’s available liquid resources.
* **LTD (Long‑Term Debt)** represents obligations that require repayment over a longer horizon.
* **CCP/LTD ratio** shows how well a company can cover long‑term debt using available cash.

---

## Repository Structure
```
📦 financial_dashboard/
├── 📁 app/
│   ├── __init__.py
│   └── app.py
│
├── 📁 data/
│   ├── filings_demo_step3.sglite
│   └── financial_data.json
│
├── 📁 docs/
│   └── technical_details.md
│
├── 📁 figures/
│   ├── fig1_CCP_and_LTD_by_Company.json
│   ├── fig2_Ratio_CCP_LTD_by_Companies.json
│   ├── fig3_Financial_Resilience_Heatmap.json 
│   ├── fig4_Debt_vs_Liquid_Assets_Company_Segments.json
│   └── fig5_Debt_vs_Liquid_Assets.json
│
├── 📁 images/
│   ├── CCP & LTD by Company.png
│   ├── Debt Coverage Ratio.png
│   ├── Debt vs Liquid Assets (all).png
│   ├── Debt vs Liquid Assets (lastest).png
│   └── Financial Resilience Heatmap.png
│
├── 📁 tableau/
│   ├── Forms-3.csv
│   ├── Stocks.csv
│   ├── Tableau_dashboard.png
│   ├── Tasks.csv
│   └── export_sqlite_tables.py
│
├── Procfile
├── 📄 README.md
├── render.yaml
└── requirements.txt
```
---

## How to Run Locally

```bash
git clone https://github.com/xn-projects/financial_dashboard.git
cd financial_dashboard
pip install -r requirements.txt

# Default: uses MongoDB if configured, otherwise JSON fallback
uvicorn app.app:api --reload
```

To force JSON mode:

```bash
USE_MONGO=false uvicorn app.app:api --reload
```

---

## Technical Details

For architecture, data workflow, and implementation details (including Tableau-to-Dash transition, API structure, MongoDB integration, and normalization methodology), see:

[Technical Details](docs/technical_details.md)

---

## Summary

This dashboard helps assess financial resilience by comparing liquidity and debt positions across companies and quarters. The current implementation supports automated data loading, flexible API access, and a fully interactive visualization interface suitable for further analysis and expansion.

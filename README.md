# Financial Resilience Dashboard 

This project delivers an in-depth analysis of corporate financial resilience by examining how effectively companies balance liquidity and long-term debt.

The dashboard enables users to explore structural trends, stress periods, and relative positioning across companies through interactive visual analytics.

Originally prototyped in **Tableau** for rapid analytical iteration, the solution was fully rebuilt using **Python**, **Plotly Dash**, and **FastAPI** to support automation, API integration, and scalable production deployment.

---

## Live Versions

* **Tableau Prototype:** (first exploratory version)<br>
  [https://public.tableau.com/app/profile/kseniia.chepigina/viz/EvolutionofCCPLTD/Dashboard12](https://public.tableau.com/app/profile/kseniia.chepigina/viz/EvolutionofCCPLTD/Dashboard12)

* **Plotly Dash Application:** (production interactive dashboard)<br>
  [https://financial-dashboard-ep61.onrender.com/dashboard/](https://financial-dashboard-ep61.onrender.com/dashboard/)

---

## Dashboard Preview

The dashboard includes four analytical views:

### 1. CCP & LTD by Company

This chart tracks how each company’s cash reserves and long-term debt evolve over time.
It highlights structural shifts in financial strategy: expanding gaps signal strengthening liquidity, while narrowing gaps or crossovers indicate rising leverage pressure.
The view enables comparison of stability, debt dependency, and financial trajectory across firms.

![CCP & LTD by Company](images/CCP%20&%20LTD%20by%20Company.png)

### 2. Debt Coverage Ratio

This chart measures how effectively companies cover long-term debt with available liquid assets.
Rising or stable ratios indicate strengthening financial resilience, while persistently low values signal elevated refinancing and liquidity risk.
The trend view makes it possible to spot early deterioration or recovery patterns across companies.

![Debt Coverage Ratio](images/Debt%20Coverage%20Ratio.png)

### 3. Financial Resilience Heatmap

The heatmap provides a high-level view of financial resilience across companies and reporting periods.
Color intensity captures shifts in liquidity strength, allowing rapid identification of stress periods, stabilization phases, and structural improvement trends.
The format is designed for fast comparative pattern recognition.

![Financial Resilience Heatmap](images/Financial%20Resilience%20Heatmap.png)

### 4. Debt vs Liquid Assets (all)

This chart compares each company’s liquidity strength against its long-term leverage.
Bubble positioning and size reveal not only balance-sheet health, but also relative exposure to financial risk.
Median reference lines allow users to instantly evaluate positioning versus peer benchmarks.

![Debt vs Liquid Assets (all)](images/Debt%20vs%20Liquid%20Assets%20\(all\).png)

---

## Interaction

The dashboard supports:

* Interactive company selection for side-by-side comparison.
* Dynamic time range filtering from 2019 to 2024.
* Switching between absolute financial indicators (CCP & LTD) and relative ratios (CCP/LTD).
* Exploration of both short-term liquidity positioning and long-term financial trajectories.
  
### Why These Metrics?

These indicators were selected to capture the structural balance between liquidity and leverage:

* **CCP (Cash & Cash Position)** — reflects the company’s immediately available liquid capital.
* **LTD (Long‑Term Debt)** — represents long-term financial obligations that shape balance-sheet risk.
* **CCP/LTD ratio** — a direct indicator of financial resilience, showing how effectively liquid resources can cover structural debt.

Together, these metrics provide a clear framework for assessing **financial stability, risk exposure, and strategic capital structure**.

---

## Repository Structure
```
📦 financial_dashboard/
├── 📁 app/
│   ├── __init__.py
│   ├── app.py
│   └── figures_builder.py
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
│   └── fig4_Debt_vs_Liquid_Assets.json
│
├── 📁 images/
│   ├── CCP & LTD by Company.png
│   ├── Debt Coverage Ratio.png
│   ├── Debt vs Liquid Assets (all).png
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

This dashboard provides an analytical framework for evaluating corporate financial resilience through liquidity and debt dynamics.

By combining time-series trends, ratio-based benchmarking, heatmap risk visualization, and quadrant-style positioning, the project enables rapid identification of structural strengths, emerging risks, and strategic balance-sheet patterns.

The architecture supports automated data ingestion, API-driven access, and scalable extensions, making it suitable for both exploratory financial analysis and production-level deployment.

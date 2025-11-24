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

This chart tracks how each company's **cash reserves (CCP)** and **long-term debt (LTD)** evolve over time.

**Solid lines represent CCP (cash and liquid assets).**  
**Dashed lines represent LTD (long-term debt obligations).**

The distance between the two lines reflects financial strength:

- A widening gap indicates improving liquidity and strengthening balance-sheet resilience
- Converging lines signal rising leverage pressure
- Crossovers may indicate periods of financial stress or structural risk

This view enables comparison of company stability, debt dependency, and long-term financial trajectory.

![CCP & LTD by Company](images/CCP%20&%20LTD%20by%20Company.png)


### 2. Debt Coverage Ratio

This view measures how effectively companies cover long-term debt through available cash using the **CCP/LTD ratio**.

Color bands represent financial risk levels:

- **Green** → strong liquidity coverage  
- **Light green** → moderate financial stability  
- **Yellow** → weakening liquidity  
- **Red** → elevated leverage and refinancing risk

Stable or rising ratios indicate strengthening financial resilience, while persistently low values signal elevated liquidity risk.
This chart makes it possible to detect early deterioration or recovery patterns across companies.

![Debt Coverage Ratio](images/Debt%20Coverage%20Ratio.png)


### 3. Financial Resilience Heatmap

This heatmap provides a high-level overview of liquidity strength across companies and time.

Color gradients represent financial resilience:

- **Cooler tones (green)** → higher CCP/LTD, stronger liquidity
- **Warmer tones (yellow → red)** → weakening resilience and elevated financial stress

The visualization enables rapid identification of:

- stress periods
- recovery phases
- structural shifts in balance-sheet health

The format is optimized for quick comparative pattern recognition across both time and companies.

![Financial Resilience Heatmap](images/Financial%20Resilience%20Heatmap.png)


### 4. Debt vs Liquid Assets (all)

This visualization compares each company’s **liquidity strength** against its **long-term leverage**.

**How to Read the Chart**

X-axis (CCP): Available cash and liquid assets  
Y-axis (LTD): Long-term borrowing obligations  
Bubble size: CCP/LTD ratio — larger bubbles represent stronger liquidity relative to debt  
Labels: Company tickers for quick identification  

**Quadrant Interpretation**

**Bottom-right (strongest position)**  
High cash + low debt → financially resilient, low risk profile

**Top-left (weakest position)**  
Low cash + high debt → elevated liquidity risk

**Bottom-left**  
Low cash + low debt → smaller or conservative balance sheets

**Top-right**  
High cash + high debt → aggressive capital structure, reliant on debt cycles

**Reference Lines**

- **Blue dashed horizontal line** — Median Long-Term Debt (LTD) across all companies
- **Red dashed vertical line** — Median Current Cash Position (CCP) across all companies  

Both reference lines are dynamic and automatically update based on the selected reporting period, allowing real-time comparison against peer benchmarks.

These benchmarks help immediately identify which companies operate above or below industry-typical risk levels.

![Debt vs Liquid Assets (all)](images/Debt%20vs%20Liquid%20Assets%20\(all\).png)

---

## Interaction

The dashboard supports:

* Interactive company selection for side-by-side comparison.
* Dynamic time range filtering from 2019 to 2023.
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
│   ├── filings_demo_step3.sqlite
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

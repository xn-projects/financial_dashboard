## Financial Resilience Dashboard 

**Comparing Corporate Liquidity and Long-Term Debt**

This project provides an interactive dashboard to analyze how well companies can cover their long-term debt using liquid assets. It focuses on two key financial indicators extracted from SEC filings:

- **CCP**: Cash, cash equivalents, and marketable securities  
- **LTD**: Long-term debt  

The dashboard enables comparison across companies, industries, and reporting periods. It supports both static data (JSON) and dynamic data updates through MongoDB Atlas. The application is deployed on Render and accessible through a web interface.

---

## Motivation

Understanding the balance between liquidity and debt is essential for evaluating a company's financial resilience. The original prototype was created in Tableau, which was useful for rapid exploration. Tableau required manual dataset updates and did not allow integration with API-based workflows. The new version automates data access, processing, and visualization to support scalable, repeatable financial analysis.

---

## Main Features

- Interactive web dashboard built with Plotly Dash
- REST API for external access and integration
- Choice of data backend:
  - Local JSON file
  - MongoDB Atlas (recommended for continuous updates)
- Five visualization views offering time-series and cross-sectional insights
- Cloud deployment using Render for public access

---

## Live Dashboards

| Version | Link | Description |
|--------|------|-------------|
| Tableau Prototype | https://public.tableau.com/app/profile/kseniia.chepigina/viz/EvolutionofCCPLTD/Dashboard12 | Initial exploratory version |
| Plotly Dash Application | https://financial-dashboard-ep61.onrender.com/dashboard/ | Interactive web dashboard with API backend |

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

### Application Architecture  

The application integrates **data backend**, **REST API**, and **interactive dashboard** into one service.  

#### Data Sources
- Local JSON file (`financial_data.json`) – static dataset.  
- MongoDB Atlas – dynamic dataset.  
- Controlled via environment variable:  
  - `USE_MONGO=true` → use MongoDB  
  - `USE_MONGO=false` → use JSON  

#### API Layer
- Built with **FastAPI**.  
- CORS enabled (`allow_origins=["*"]`) to allow connections from external apps.  

#### Dashboard Layer
- Built with **Dash (on Flask)**.  
- Embedded into FastAPI via `WSGIMiddleware`.  
- Includes five tabs with Plotly figures.  

#### Deployment
- Runs with `uvicorn`.  
- Port is taken from environment variable `PORT` → fully compatible with **Render**.  

---

### API Endpoints  

| Endpoint               | Description |
|-------------------------|-------------|
| `/health`              | Service status (records count + data source) |
| `/data`                | Full dataset as JSON |
| `/companies`           | List of available companies |
| `/quarters`            | List of reporting quarters |
| `/metrics/{company}`   | Metrics for a specific company |
| `/`                    | Root page with message and links |

---

### Workflow & Methodology  

#### Data Collection  
- Source: **SEC EDGAR filings (10-Q, 10-K)**.  
- Extracted values: **CCP** and **LTD**.  

#### Data Structure (`financial_data.json`)

The dataset contains quarterly metrics extracted from SEC EDGAR filings.  
Each record corresponds to one company-quarter and includes the following fields:

| Field         | Type     | Description |
|---------------|----------|-------------|
| `Form_id`     | int      | Internal ID of the filing |
| `TextListLen` | int      | Parsed text length (technical parsing info) |
| `TableIndex`  | int      | Index of the extracted table |
| `SumDivider`  | int      | Normalization divider (for scaling values) |
| `JsonTable`   | int      | Indicator if parsed table was JSON-converted |
| `ValueColumn` | int      | Index of the value column in the SEC table |
| `CCP`         | float    | Cash, cash equivalents & marketable securities |
| `LTD`         | float    | Long-term debt |
| `id`          | int      | Unique record identifier |
| `FormName`    | string   | SEC form filename (e.g., `aapl-20231230`) |
| `CIK`         | int      | Central Index Key of the company |
| `ValueDate`   | date     | Date when the values are reported |
| `FilingDate`  | date     | Date when the report was filed with SEC |
| `FormURL`     | string   | Direct URL to the SEC filing |
| `Symbol`      | string   | Stock ticker symbol (e.g., AAPL) |
| `CompanyName` | string   | Company name |
| `ReportQuarter` | string | Reporting quarter (e.g., `Q4 2023`) |

####  Why MongoDB?  
While `financial_data.json` is useful for local testing and small-scale analysis, the production application uses **MongoDB Atlas** as a backend.  

Benefits of MongoDB integration:  
- **Dynamic updates** – new SEC filings can be inserted without regenerating the JSON file.  
- **Scalability** – supports larger datasets across many companies.  
- **Flexible queries** – enables filtering by company, sector, or reporting period directly in the database.  
- **Cloud availability** – MongoDB Atlas makes the data accessible from anywhere.  

#### Data Cleaning & Normalization  
- Issues with **FilingDate vs. ValueDate** caused quarter misalignment (e.g., Bath & Body Works).  
- Implemented **date normalization** to align reports to standard calendar quarters.  
- Final dataset: **consistent CCP and LTD values for 2019–2023**.  
- Analysts provide **clean data**, developers focus on frontend and API.  

#### Tableau Prototype  
- First dashboard built in Tableau.  
- Strengths: rapid exploration, strong visuals.  
- Weaknesses: manual updates, limited scalability.  
- Kept as a **baseline** (`tableau_dashboard/`).  

#### Python + Plotly Version  
- Processing and visualization in `app.py`.  
- Exported Plotly JSON figures (`fig1…fig5.json`).  
- Interactive exploration with filters and animations.  

##### JSON for React Integration  
- Plotly charts exported as **clean JSON objects**, stripped of unnecessary metadata.  
- JSON structure tailored for **Plotly.js in React**, ensuring frontend can consume figures directly.  

#### Deployment on Render  
- Exposed REST API endpoints.  
- Hosted an **interactive Plotly dashboard** online.  

#### Maintainability & Extensibility  
- Fixed versions of libraries ensure reproducibility.  
- Flexible architecture allows **new indicators and metrics** to be added later.  

---

### Dashboard Tabs

The interactive dashboard contains **five tabs**, each answering a specific analytical question:  

1. **CCP & LTD by Company**  
   Line charts showing the dynamics of **cash, cash equivalents & marketable securities (CCP)** and **long-term debt (LTD)** for each company.  
   Allows comparison of how liquidity reserves and debt burdens have evolved from 2019 to 2023.  

2. **Debt Coverage Ratio**  
   Time series of the **CCP/LTD ratio**.  
   A key indicator of financial resilience: the higher the ratio, the more capable a company is of covering its debt with liquid assets. 

3. **Financial Resilience Heatmap**  
   Heatmap of **CCP/LTD ratios per quarter** across all companies.  
   A quick way to identify periods of risk (low ratios in red) and resilience (higher ratios in green).   

4. **Debt vs Liquid Assets (latest)**  
   A **bubble chart snapshot** of the most recent reporting quarter:  
   - X-axis: liquid assets (CCP).  
   - Y-axis: long-term debt (LTD).  
   - Bubble size: relative company scale.  
   Highlights how companies are positioned in terms of liquidity versus debt.

5. **Debt vs Liquid Assets (all)**   
   A **bubble chart** showing the **evolution of CCP vs LTD over time**.  
   Users can **select a specific quarter** and see how companies shift between high-risk and resilient zones over time.

---

### Dashboards  

- **Tableau Dashboard (prototype)**: [Link](https://public.tableau.com/app/profile/kseniia.chepigina/viz/EvolutionofCCPLTD/Dashboard12)  
- **Plotly Dashboard (production)**: [Link](https://financial-dashboard-ep61.onrender.com/dashboard/)
  

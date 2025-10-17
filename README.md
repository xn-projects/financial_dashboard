## Financial Resilience Analysis – From Tableau to Plotly Dash

### Project Background  

The project was initially developed as a **Tableau dashboard** to visualize corporate financial data.  
- It focused on **cash, cash equivalents & marketable securities (CCP)** vs. **long-term debt (LTD)** across multiple companies.  
- Tableau allowed quick insights and interactive filtering, but it had clear limitations:  
  - Updates from new SEC filings required manual work.  
  - Tableau dashboards are less flexible for advanced processing.  
  - No integration with APIs or external services.  

Based on these constraints, we rebuilt the solution with **Python + Plotly + FastAPI + Dash**, deployed on **Render**.  

This evolution gave us:  
- **Automation** – parsing SEC filings directly into JSON or MongoDB.  
- **API integration** – endpoints that provide both raw data and processed figures.  
- **Interactive dashboard** – hosted online and available to users.  
- **Scalability** – new data can be added and visualized without manual work.  

---

### Objectives & Achievements  

#### Objectives
- Collect quarterly CCP and LTD data from SEC EDGAR.  
- Compare liquidity and debt across companies and industries.  
- Provide insights into **financial resilience** and debt coverage.  
- Develop both an exploratory Tableau prototype and a production-ready Python application.  
- Deploy the solution with an API and interactive web dashboard.  

#### Achievements
- Created an initial **Tableau dashboard prototype** (`/tableau_dashboard/`) with early insights.  
- Built a **Python pipeline** (`app.py`) that integrates FastAPI and Dash.  
- Implemented dual-mode data backend: local JSON file or MongoDB Atlas collection.  
- Designed **five Plotly visualizations**, each exported as `.json`.  
- Created a **REST API** with endpoints for data, companies, quarters, and metrics.  
- Deployed the application to **Render**, making it publicly available.  

---

### Repository Structure
```
├── app.py                                              # Main FastAPI + Dash application
├── financial_data.json                                 # Sample dataset (static)
├── fig1_CCP_and_LTD_by_Company.json                    # Plotly figure JSON
├── fig2_Ratio_CCP_LTD_by_Companies.json                # Plotly figure JSON
├── fig3_Financial_Resilience_Heatmap.json              # Plotly figure JSON
├── fig4_Debt_vs_Liquid_Assets_Company_Segments.json    # Plotly figure JSON
├── fig5_Debt_vs_Liquid_Assets.json                     # Plotly figure JSON
├── tableau_dashboard/                                  # Tableau prototype files
├── plotlydash_images/                                  # Screenshots of the dashboard tabs
├── requirements.txt                                    # Python dependencies
├── README.md                                           # Project documentation
├── Procfile                                            # Deployment config (Render)
└── render.yaml                                         # Deployment config for Render
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
  

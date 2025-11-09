# Technical Details

## 1. Overall Architecture

This ensures consistent data usage across the UI and external consumers and keeps deployment and maintenance simple.

This ensures data consistency across the UI and external consumers, simplifies updates, and reduces deployment overhead.

The system includes three core layers:

1. **Data Backend** – provides access to financial data (local JSON or MongoDB).
2. **REST API (FastAPI)** – exposes structured data for external use.
3. **Interactive Dashboard (Plotly Dash)** – visualizes the data in a web-based interface.

All layers run within the same server process.

---

## 2. Data Backend

The application supports two interchangeable data sources, controlled through an environment variable:

| Data Source | Location | Usage |
|------------|----------|-------|
| `financial_data.json` | `data/` directory | Local execution, offline analysis, development |
| MongoDB Atlas | Cloud-hosted database | Production deployment and dynamic updates |

**Switching the backend:**

```
USE_MONGO=true   → Use MongoDB Atlas
USE_MONGO=false  → Use JSON file
```

### Core Data Fields Used in Analysis

| Field | Description |
|-------|-------------|
| `CompanyName` | Company name |
| `Symbol` | Stock ticker |
| `ReportQuarter` | Standardized quarterly label (e.g., `Q4 2023`) |
| `CCP` | Cash, cash equivalents & marketable securities |
| `LTD` | Long-term debt |

Other fields in the dataset are artifacts of the parsing process and do not affect visualization logic.

---

## 3. Data Normalization Process

Reporting periods vary across companies. To make cross-company comparisons meaningful:

- **Reporting dates are aligned to standardized calendar quarters.**
- Each company-quarter record receives a uniform `ReportQuarter` label.

This harmonization enables clean time-based analysis.

---

## 4. REST API (FastAPI)

The API exposes both raw and structured data and can be consumed by dashboards or other analytical tools.

| Endpoint | Purpose |
|---------|---------|
| `/health` | Basic service status and active data source |
| `/data` | Full dataset as JSON |
| `/companies` | List of available companies |
| `/quarters` | List of reporting periods |
| `/metrics/{company}` | Time-series metrics for a selected company |

CORS is enabled to allow external frontends to connect.

---

## 5. Dashboard (Plotly Dash)

The dashboard is built using Plotly Dash and embedded into the FastAPI server using `WSGIMiddleware`.

All visualizations are loaded from pre-computed Plotly figure JSON files located in the `figures/` directory.  
This avoids real-time heavy computation and ensures fast UI rendering.

The dashboard provides interactive controls for:
- selecting companies,
- choosing reporting periods,
- switching between absolute values and ratios.

Detailed descriptions of each analytical view are provided in the main README.

---

## 6. Transition from Tableau to Python

The initial dashboard prototype was built in **Tableau** to explore the data quickly.  
However, Tableau had key limitations:

- No automated data refresh
- Limited integration with external systems
- Manual data preparation required

Rebuilding the dashboard in **Python + FastAPI + Dash** enabled:

- Automated data ingestion
- Scalable backend architecture
- A single deployment for both UI and API
- Reuse of Plotly figure JSONs across different frontends

---

## 7. Deployment

The application is deployed as a single service using `uvicorn`.

Key deployment files:

| File | Purpose |
|------|---------|
| `Procfile` | Defines the application start command |
| `render.yaml` | Configuration for deployment on Render |

The `PORT` environment variable is automatically provided by the hosting platform.

---

## 8. Extensibility and Future Growth

The architecture supports straightforward extension:

- New metrics (e.g., Net Debt, Free Cash Flow, EBITDA ratios)
- Additional companies or sectors
- Alternative data pipelines
- New dashboard views or analytic layers

The separation of **data → API → visualization** allows the system to scale without major refactoring.

# Technical Details

## 1. Architecture Overview

The application integrates three core layers into a single deployable service:

1. **Data Backend** – Loads financial data either from a static JSON file or from MongoDB Atlas.
2. **REST API Layer** – Provides programmatic access to data for external tools and clients.
3. **Interactive Dashboard** – A Plotly Dash interface embedded inside the same server.

This combined setup simplifies deployment, reduces infrastructure overhead, and ensures consistency between the data used by the API and the dashboard.

---

## 2. Data Sources

The application can use **one of two data sources**, controlled via environment variable `USE_MONGO`:

| Data Source                   | Description                             | When Used                              |
| ----------------------------- | --------------------------------------- | -------------------------------------- |
| `financial_data.json` (local) | Static dataset stored in `data/` folder | Local testing, offline usage           |
| MongoDB Atlas                 | Cloud-hosted scalable database          | Production deployment, dynamic updates |

**Environment Control:**

```
USE_MONGO=true   → Use MongoDB Atlas
USE_MONGO=false  → Use JSON file
```

This approach allows easy switching between development and production data contexts without modifying the application code.

---

## 3. API Layer (FastAPI)

The REST API is built using **FastAPI**, chosen for its speed, async support, and interactive documentation.

* CORS is enabled to allow usage from external dashboards or web clients.
* The API provides access to full dataset, company lists, quarter lists, and per‑company metrics.

### Available API Endpoints

| Endpoint             | Purpose                                     |
| -------------------- | ------------------------------------------- |
| `/health`            | Service status (record count + data source) |
| `/data`              | Full dataset as JSON                        |
| `/companies`         | List of all companies in the dataset        |
| `/quarters`          | List of reporting quarters                  |
| `/metrics/{company}` | Time‑series metrics for a selected company  |
| `/`                  | Root endpoint containing info and links     |

These endpoints make the service compatible with external analytics tools and frontend integrations.

---

## 4. Dashboard Layer (Dash)

The dashboard is implemented using **Plotly Dash**, running on **Flask**, and embedded inside the FastAPI application using `WSGIMiddleware`.

### Key Characteristics:

* Uses pre‑computed Plotly figure JSON files stored in `figures/`.
* Consists of **five tabs**, each answering a specific analytical question.
* Ensures separation between **data processing (done offline)** and **visualization (dynamic but lightweight)**.

This design reduces runtime computation cost and keeps UI performance fast.

---

## 5. Deployment

The application is designed for deployment on **Render** (or similar platforms):

* The server is launched via `uvicorn`.
* `PORT` environment variable controls the external port.
* Only one service needs to be deployed, since API and dashboard share the same server.

### Deployment Files

* `Procfile` – Defines the startup command
* `render.yaml` – Describes environment configuration

---

## 6. Data Workflow

### Data Collection

Data originates from **SEC EDGAR filings** (10‑Q and 10‑K). The goal is to extract:

* **CCP** – Cash, Cash Equivalents & Marketable Securities
* **LTD** – Long‑Term Debt

### Data Structure

Each row represents one **company‑quarter** record.

| Field           | Meaning                                      |
| --------------- | -------------------------------------------- |
| `Form_id`       | Internal filing identifier                   |
| `TextListLen`   | Parsed text length (supporting metadata)     |
| `TableIndex`    | Table index used during extraction           |
| `SumDivider`    | Scaling normalization factor                 |
| `JsonTable`     | Flag indicating JSON conversion stage        |
| `ValueColumn`   | Column index used during extraction          |
| `CCP`           | Liquidity reserves (cash & equivalents)      |
| `LTD`           | Long‑term debt amount                        |
| `id`            | Unique record ID                             |
| `FormName`      | Filing name (e.g., `aapl‑20231230`)          |
| `CIK`           | Official SEC Central Index Key               |
| `ValueDate`     | Reporting period date                        |
| `FilingDate`    | Date the report was filed                    |
| `FormURL`       | Direct SEC link                              |
| `Symbol`        | Stock ticker                                 |
| `CompanyName`   | Company name                                 |
| `ReportQuarter` | Standardized quarter label (e.g., `Q4 2023`) |

### Why MongoDB

MongoDB Atlas is used in production because it:

* Allows **incremental updates** (new filings without regenerating JSON)
* Supports **fast queries** across companies and time periods
* Scales well as dataset grows

### Normalization

Reporting dates vary by company. To support consistent quarter‑by‑quarter comparison:

* `ValueDate` and `FilingDate` are reconciled
* Each record is assigned to a **standardized calendar quarter**

This ensures comparability across companies.

---

## 7. Tableau Prototype → Python + Plotly Version

**Tableau Strengths:**

* Quick exploratory analysis
* Strong built‑in visuals

**Limitations:**

* Manual data refresh
* No automated integration with EDGAR
* Limited customization and API extensibility

**Python + Plotly Advantages:**

* Full automation of data loading
* Scalable backend (MongoDB)
* Flexible and interactive dashboard logic
* Ability to export Plotly figures as JSON for web reuse

---

## 8. JSON Figure Export

Plotly figures are stored as `.json` instead of being generated on every request.

Benefits:

* Faster dashboard rendering
* Consistent visuals across UI environments
* Reusable in React / plain Plotly.js frontends

---

## 9. Maintainability and Extensibility

* Clear separation of **data**, **API**, and **UI layers**
* Swappable data backend (local ↔ cloud)
* Easy to add new metrics or dashboards

This architecture supports long‑term growth of the project.

import os
import json
import pandas as pd
import plotly.io as pio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from dash import Dash, html, dcc, Input, Output
from flask import Flask
from pymongo import MongoClient

USE_MONGO = os.getenv("USE_MONGO", "true").lower() == "true"
DATA_PATH = os.getenv("DATA_PATH", "financial_data.json")
FIGURES_DIR = os.path.dirname(__file__)
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://kseniia_chepigina:sonre3-buzMum-kufvem@cluster0.oekorln.mongodb.net/financial?retryWrites=true&w=majority",
)
DB_NAME = os.getenv("DB_NAME", "financial")
COLLECTION = os.getenv("COLLECTION", "metrics")

def get_data_from_json():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    return pd.DataFrame(records)

def get_data_from_mongo():
    client = MongoClient(MONGODB_URI)
    col = client[DB_NAME][COLLECTION]
    records = list(col.find({}, {"_id": 0}))
    if not records:
        raise ValueError("MongoDB collection is empty.")
    return pd.DataFrame(records)

result_df = get_data_from_mongo() if USE_MONGO else get_data_from_json()
print(f"Loaded {len(result_df)} records from {'MongoDB' if USE_MONGO else 'JSON'}")

def load_fig(name):
    path = os.path.join(FIGURES_DIR, name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Figure not found: {path}")
    return pio.read_json(path)

try:
    fig1_1 = load_fig("fig1_CCP_and_LTD_by_Company.json")
    fig2 = load_fig("fig2_Ratio_CCP_LTD_by_Companies.json")
    fig3 = load_fig("fig3_Financial_Resilience_Heatmap.json")
    fig4 = load_fig("fig4_Debt_vs_Liquid_Assets_Company_Segments.json")
    fig5 = load_fig("fig5_Debt_vs_Liquid_Assets.json")
    print("All figures successfully loaded!")
except Exception as e:
    print(f"Warning: {e}")
    fig1_1 = fig2 = fig3 = fig4 = fig5 = None

api = FastAPI(title="Financial Dashboard API", version="2.0")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/health")
def health():
    return {"status": "ok", "records": len(result_df), "source": "MongoDB" if USE_MONGO else "JSON"}

@api.get("/data")
def get_data():
    return result_df.to_dict(orient="records")

@api.get("/companies")
def get_companies():
    return sorted(result_df["CompanyName"].dropna().unique().tolist())

@api.get("/quarters")
def get_quarters():
    return sorted(result_df["ReportQuarter"].dropna().unique().tolist())

@api.get("/metrics/{company}")
def get_company_metrics(company: str):
    subset = result_df[result_df["CompanyName"] == company]
    if subset.empty:
        return {"error": f"Company '{company}' not found"}
    return subset.to_dict(orient="records")


@api.get("/")
def root():
    return {
        "message": "Financial Dashboard API is running",
        "dash_url": "/dashboard/",
        "docs_url": "/docs"
    }

flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app, url_base_pathname="/dashboard/")

dash_app.layout = html.Div([
    html.H1("Financial Dashboard", style={"textAlign": "center", "marginBottom": "20px"}),
    dcc.Tabs(id="tabs", value="tab1", children=[
        dcc.Tab(label="CCP & LTD by Company", value="tab1"),
        dcc.Tab(label="Debt Coverage Ratio", value="tab2"),
        dcc.Tab(label="Financial Resilience Heatmap", value="tab3"),
        dcc.Tab(label="Debt vs Liquid Assets (latest)", value="tab4"),
        dcc.Tab(label="Debt vs Liquid Assets (all)", value="tab5"),
    ]),
    html.Div(id="tabs-content", style={"marginTop": "20px"}),
])

@dash_app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_tab(tab):
    if tab == "tab1" and fig1_1: return html.Div([dcc.Graph(figure=fig1_1)])
    elif tab == "tab2" and fig2: return html.Div([dcc.Graph(figure=fig2)])
    elif tab == "tab3" and fig3: return html.Div([dcc.Graph(figure=fig3)])
    elif tab == "tab4" and fig4: return html.Div([dcc.Graph(figure=fig4)])
    elif tab == "tab5" and fig5: return html.Div([dcc.Graph(figure=fig5)])
    return html.Div("Figure not available.", style={"textAlign": "center", "color": "red"})

api.mount("/", WSGIMiddleware(flask_app))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(api, host="0.0.0.0", port=port)

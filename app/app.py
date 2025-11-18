import os
from dotenv import load_dotenv
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from dash import Dash, html, dcc, Input, Output
from flask import Flask
from pymongo import MongoClient

from app.figures_builder import (
    prepare_data,    
    generate_company_colors,
    create_fig_1,
    create_fig_2,
    create_fig_3,
    create_fig_4
)

load_dotenv()

USE_MONGO = os.getenv('USE_MONGO', 'false').lower() == 'true'
DATA_PATH = os.getenv('DATA_PATH', os.path.join(os.path.dirname(__file__), '..', "data", "financial_data.json"))
MONGODB_URI = os.getenv('MONGODB_URI', '')
DB_NAME = os.getenv('DB_NAME', 'financial')
COLLECTION = os.getenv('COLLECTION', 'metrics')

def get_data_from_json():
    return pd.read_json(DATA_PATH, encoding='utf-8')

def get_data_from_mongo():
    client = MongoClient(MONGODB_URI)
    col = client[DB_NAME][COLLECTION]
    records = list(col.find({}, {"_id": 0}))
    if not records:
        raise ValueError("MongoDB collection is empty.")
    return pd.DataFrame(records)

result_df = get_data_from_mongo() if USE_MONGO else get_data_from_json()
result_df = prepare_data(result_df)
print(f"Loaded {len(result_df)} records from {'MongoDB' if USE_MONGO else 'JSON'}")

company_colors = generate_company_colors(result_df)

fig1 = create_fig_1(result_df, company_colors)
fig2 = create_fig_2(result_df, company_colors)
fig3 = create_fig_3(result_df)
fig4 = create_fig_4(result_df, company_colors)

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

flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app, url_base_pathname="/dashboard/")

dash_app.layout = html.Div([
    html.H1("Financial Dashboard", style={"textAlign": "center", "marginBottom": "20px"}),
    html.Div(
        [
            html.P(
                "This project explores how companies balance liquidity and long-term debt "
                "to evaluate their financial resilience. "
                "The goal is to provide clear, interactive insights into how well "
                "different companies can cover debt obligations with liquid assets.",
                style={
                    "textAlign": "center",
                    "maxWidth": "900px",
                    "margin": "0 auto",
                    "fontSize": "16px",
                    "color": "#333"
                }
            )
        ],
        style={"marginBottom": "25px"}
    ),
    dcc.Tabs(id="tabs", value="tab1", children=[
        dcc.Tab(label="CCP & LTD by Company", value="tab1"),
        dcc.Tab(label="Debt Coverage Ratio", value="tab2"),
        dcc.Tab(label="Financial Resilience (Heatmap)", value="tab3"),
        dcc.Tab(label="Debt vs Liquid Assets", value="tab4"),
    ]),
    html.Div(id="tabs-content", style={"marginTop": "20px"}),
])

@dash_app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_tab(tab):
    if tab == "tab1": return html.Div([dcc.Graph(figure=fig1)])
    elif tab == "tab2": return html.Div([dcc.Graph(figure=fig2)])
    elif tab == "tab3": return html.Div([dcc.Graph(figure=fig3)])
    elif tab == "tab4": return html.Div([dcc.Graph(figure=fig4)])
    return html.Div("Figure not available.", style={"textAlign": "center", "color": "red"})

api.mount("/", WSGIMiddleware(flask_app))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(api, host="0.0.0.0", port=port)

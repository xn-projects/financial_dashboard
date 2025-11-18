import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
import plotly.subplots as sp
import matplotlib.pyplot as plt


def prepare_data(df):
    df = df.copy()

    def parse_quarter(qstr):
        if pd.isna(qstr):
            return pd.NaT
        qstr = str(qstr).strip()
        match = re.match(r"Q([1-4])\s+(\d{4})", qstr)
        if match:
            q = int(match.group(1))
            year = int(match.group(2))
            return pd.Period(year=year, quarter=q, freq="Q").to_timestamp(how="start")
        return pd.NaT

    df["QuarterStart"] = df["ReportQuarter"].apply(parse_quarter)

    df["ReportQuarter"] = pd.to_datetime(df["QuarterStart"]).dt.to_period("Q").astype(str)

    return df.sort_values(["Symbol", "QuarterStart"])


def generate_company_colors(df):
    """
    Generates a consistent color palette for all companies.
    Each company is assigned a stable color based on its Symbol, ensuring the same color is used across all charts.
    """
    pairs = (
        df[["Symbol", "CompanyName"]]
        .drop_duplicates()
        .sort_values("Symbol")
        .values
    )

    n_colors = len(pairs)
    cmap = plt.cm.get_cmap('tab20', n_colors)
    palette = [plt.cm.colors.to_hex(cmap(i)) for i in range(n_colors)]

    company_colors = {}
    for i, (symbol, name) in enumerate(pairs):
        color = palette[i]
        company_colors[symbol] = color
        company_colors[name] = color

    return company_colors


def add_annotation(fig: go.Figure, text: str, position: str = "top") -> go.Figure:
    """
    Adds a persistent description text block to the figure.
    Position can be 'top' or 'bottom'.
    """
    if position == "top":
        y = 1.12
        yanchor = "bottom"
    else:
        y = -0.20
        yanchor = "top"

    fig.add_annotation(
        text=text,
        align="left",
        showarrow=False,
        xref="paper", yref="paper",
        x=0, y=y,
        xanchor="left", yanchor=yanchor,
        font=dict(size=12, color="gray")
    )
    return fig
    

def create_fig_1(df: pd.DataFrame, company_colors: dict) -> go.Figure:
    
    min_val = min(df['CCP'].min(), df['LTD'].min())
    max_val = max(df['CCP'].max(), df['LTD'].max())
    padding = (max_val - min_val) * 0.1
    y_range = [min_val - padding, max_val + padding]

    fig = sp.make_subplots(
        specs=[[{"secondary_y": True}]],
        figure=go.Figure(layout=dict(width=1100, height=600))
    )

    companies = df['Symbol'].unique()

    for company in companies:
        company_data = df[df['Symbol'] == company].sort_values('QuarterStart')
        color = company_colors.get(company, "#000000")

        hovertext_ccp = [
            f"Company: {company}<br>Quarter: {label}<br>CCP: $ {val:.0f} M"
            for label, val in zip(company_data['ReportQuarter'], company_data['CCP'])
        ]

        fig.add_trace(
            go.Scatter(
                x=company_data['QuarterStart'],
                y=company_data['CCP'],
                mode='lines',
                name=company,
                legendgroup=company,
                line=dict(color=color, width=2),
                hovertext=hovertext_ccp,
                hovertemplate="%{hovertext}<extra></extra>",
                showlegend=True
            ),
            secondary_y=False
        )

    for company in companies:
        company_data = df[df['Symbol'] == company].sort_values('QuarterStart')
        color = company_colors.get(company, "#000000")

        hovertext_ltd = [
            f"Company: {company}<br>Quarter: {label}<br>LTD: $ {val:.0f} M"
            for label, val in zip(company_data['ReportQuarter'], company_data['LTD'])
        ]

        fig.add_trace(
            go.Scatter(
                x=company_data['QuarterStart'],
                y=company_data['LTD'],
                mode='lines',
                name=company,
                legendgroup=company,
                line=dict(color=color, width=2, dash='dash'),
                hovertext=hovertext_ltd,
                hovertemplate="%{hovertext}<extra></extra>",
                showlegend=True
            ),
            secondary_y=True
        )

    fig.update_layout(
        updatemenus=[
            dict(
                active=2,
                buttons=[
                    dict(label="CCP",
                         method="update",
                         args=[{"visible": [True]*len(companies) + [False]*len(companies)}, {}]),
                    dict(label="LTD",
                         method="update",
                         args=[{"visible": [False]*len(companies) + [True]*len(companies)}, {}]),
                    dict(label="CCP & LTD",
                         method="update",
                         args=[{"visible": [True]*(2*len(companies))}, {}])
                ],
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ]
    )

    fig.update_layout(
        title="CCP and LTD by Company",
        title_x=0.5,
        title_y=0.98,
        xaxis=dict(
            title="Quarter",
            tickangle=-45,
            tickmode='array',
        ),
        plot_bgcolor="white",
        showlegend=True,
        legend_title="Companies (click to show/hide)"
    )

    fig.update_yaxes(title="USD (Millions)", range=y_range, secondary_y=False)
    fig.update_yaxes(range=y_range, secondary_y=True)
    fig.update_xaxes(
        showgrid=True,
        gridcolor="lightgray",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="lightgray",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
        secondary_y=False
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="lightgray",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
        secondary_y=True
    )

    return fig


def create_fig_2(df: pd.DataFrame, company_colors: dict) -> go.Figure:
    """
    CCP/LTD ratio trend by company.
    Uses consistent company_colors to ensure stable coloring across charts.
    """

    data = df.copy()
    data["DebtCoverage"] = data["CCP"] / data["LTD"].replace({0: pd.NA})

    fig = go.Figure()
    companies = data["CompanyName"].unique()

    for company in companies:
        company_data = data[data["CompanyName"] == company].sort_values("QuarterStart")
        color = company_colors.get(company, "#000000")

        fig.add_trace(
            go.Scatter(
                x=company_data["QuarterStart"],
                y=company_data["DebtCoverage"],
                mode="lines",
                name=company,
                line=dict(color=color, width=2),
                marker=dict(color=color, size=6),
                hovertext=[
                    f"Company: {company}<br>Quarter: {q}<br>Debt Coverage: {val:.2f}"
                    for q, val in zip(company_data["ReportQuarter"], company_data["DebtCoverage"])
                ],
                hovertemplate="%{hovertext}<extra></extra>"
            )
        )

    max_ratio = max(data["DebtCoverage"].max(), 1.2)

    fig.add_hrect(y0=0,   y1=0.2, fillcolor="#F28E8C", opacity=0.25, line_width=0)
    fig.add_hrect(y0=0.2, y1=0.5, fillcolor="#F7C600", opacity=0.25, line_width=0)
    fig.add_hrect(y0=0.5, y1=1.0, fillcolor="#B9DCD2", opacity=0.25, line_width=0)
    fig.add_hrect(y0=1.0, y1=max_ratio,
                  fillcolor="#7FA6A3", opacity=0.25, line_width=0)

    fig.update_layout(
        title="CCP/LTD Ratio by Companies",
        title_x=0.5,
        title_y=0.98,
        xaxis_title="Quarter",
        yaxis_title="CCP/LTD Ratio",
        plot_bgcolor="white",
        width=1100,
        height=600,
        showlegend=True,
        legend_title="Companies (click to show/hide)"
    )
    fig.update_xaxes(
        showgrid=True, gridcolor="lightgray",
        showline=True, linewidth=1, linecolor="black", mirror=True
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="lightgray",
        showline=True, linewidth=1, linecolor="black", mirror=True,
        rangemode="tozero"
    )
    
    return fig


def create_fig_3(df: pd.DataFrame) -> go.Figure:
    """
    Financial Resilience Heatmap (CCP/LTD Ratio per company over time).
    """

    data = df.copy()

    data["DebtCoverage"] = data["CCP"] / data["LTD"].replace({0: pd.NA})

    pivot = data.pivot_table(
        index="CompanyName",
        columns="ReportQuarter",
        values="DebtCoverage",
        aggfunc="first"
    ).sort_index()

    quarters_sorted = sorted(data["ReportQuarter"].dropna().unique())
    quarter_labels = pd.to_datetime(quarters_sorted).to_period("Q").strftime("%Y-Q%q")

    colorscale = [
        [0.0, "#F28E8C"],
        [0.2, "#F7C600"],
        [0.5, "#B9DCD2"],
        [1.0, "#7FA6A3"]
    ]

    pivot_padded = np.hstack([np.full((pivot.shape[0], 1), np.nan), pivot.values])
    x_labels_padded = [" "] + list(quarter_labels)

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_padded,
            x=x_labels_padded,
            y=pivot.index,
            colorscale=colorscale,
            zmin=0,
            zmax=np.nanmax(pivot.values),
            xgap=2,
            ygap=3,
            colorbar=dict(title="CCP/LTD Ratio"),
            hovertemplate="Company: %{y}<br>Quarter: %{x}<br>CCP/LTD: %{z:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        title="Financial Resilience: CCP/LTD Ratio Heatmap",
        title_x=0.5,
        title_y=0.98,
        xaxis_title="Quarter",
        yaxis=dict(
            autorange="reversed",
            automargin=True,
            ticklabelposition="outside left",
            showgrid=False,
        ),
        xaxis=dict(
            showgrid=False,
            domain=[0.03, 1.00],
            tickangle=-45,
        ),
        margin=dict(l=180, r=40, t=80, b=60),
        plot_bgcolor="white",
        width=1100,
        height=600,
    )

    return fig

def create_fig_4(df: pd.DataFrame, company_colors: dict) -> go.Figure:
    """
    Debt vs Liquid Assets (Bubble chart per quarter + median comparison)
    """

    result_df = df.copy()
    result_df["DebtCoverage"] = result_df["CCP"] / result_df["LTD"].replace({0: pd.NA})

    latest = (
        result_df.sort_values("QuarterStart")
                 .groupby(["CompanyName", "ReportQuarter"])
                 .tail(1)
    )

    quarters_sorted = sorted(result_df["QuarterStart"].dropna().unique())
    quarter_labels = pd.to_datetime(quarters_sorted).to_period("Q").strftime("%Y-Q%q")
    companies = sorted(latest["CompanyName"].unique())

    min_size, max_size = 10, 50
    sizes = latest["DebtCoverage"]
    scaled_sizes = min_size + (sizes - sizes.min()) * (max_size - min_size) / (sizes.max() - sizes.min())

    fig = go.Figure()

    for company in companies:
        for quarter, q_label in zip(quarters_sorted, quarter_labels):
            subset = latest[(latest["CompanyName"] == company) & (latest["QuarterStart"] == quarter)]
            if subset.empty:
                continue

            size = scaled_sizes.loc[subset.index[0]]
            color = company_colors.get(company, "#000000")

            fig.add_trace(
                go.Scatter(
                    x=subset["CCP"],
                    y=subset["LTD"],
                    mode="markers+text",
                    marker=dict(
                        color=color,
                        size=size,
                        sizemode="area",
                        line=dict(width=1, color="black")
                    ),
                    text=subset["Symbol"],
                    textfont=dict(color=color),
                    textposition="top center",
                    name=f"{company} - {q_label}",
                    legendgroup=company,
                    showlegend=True,
                    visible=False,
                    hovertext=[
                        f"Company: {company}<br>"
                        f"Quarter: {subset['ReportQuarter'].iloc[0]}<br>"
                        f"CCP: {subset['CCP'].iloc[0]:.0f}<br>"
                        f"LTD: {subset['LTD'].iloc[0]:.0f}<br>"
                        f"CCP/LTD: {subset['DebtCoverage'].iloc[0]:.2f}"
                    ],
                    hovertemplate="%{hovertext}<extra></extra>"
                )
            )

    for quarter, q_label in zip(quarters_sorted, quarter_labels):
        subset = latest[latest["QuarterStart"] == quarter]
        if subset.empty:
            continue

        median_ccp = subset["CCP"].median()
        median_ltd = subset["LTD"].median()

        fig.add_trace(go.Scatter(
            x=[median_ccp, median_ccp],
            y=[0, subset["LTD"].max() * 1.1],
            mode="lines",
            line=dict(color="red", dash="dash"),
            name=f"Quarter Median CCP - {q_label}",
            visible=False,
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[0, subset["CCP"].max() * 1.1],
            y=[median_ltd, median_ltd],
            mode="lines",
            line=dict(color="blue", dash="dash"),
            name=f"Quarter Median LTD - {q_label}",
            visible=False,
            showlegend=False
        ))

    median_all = latest.groupby("CompanyName").agg(
        CCP=("CCP", "median"),
        LTD=("LTD", "median"),
        DebtCoverage=("DebtCoverage", "median"),
        Symbol=("Symbol", "first")
    ).reset_index()

    sizes_median = median_all["DebtCoverage"]
    if sizes_median.max() == sizes_median.min():
        scaled_median_sizes = pd.Series((min_size + max_size) / 2, index=sizes_median.index)
    else:
        scaled_median_sizes = min_size + (sizes_median - sizes_median.min()) * (max_size - min_size) / (sizes_median.max() - sizes_median.min())

    for idx, row in median_all.iterrows():
        company = row["CompanyName"]
        color = company_colors.get(company, "#000000")
        size = scaled_median_sizes.loc[idx]

        fig.add_trace(
            go.Scatter(
                x=[row["CCP"]],
                y=[row["LTD"]],
                mode="markers+text",
                marker=dict(
                    color=color,
                    size=size,
                    sizemode="area",
                    line=dict(width=1, color="black")
                ),
                text=row["Symbol"],
                textfont=dict(color=color),
                textposition="top center",
                name=f"{company} - Median",
                legendgroup=company,
                showlegend=True,
                visible=False
            )
        )

    median_ccp = latest["CCP"].median(skipna=True)
    median_ltd = latest["LTD"].median(skipna=True)

    fig.add_trace(go.Scatter(
        x=[median_ccp, median_ccp],
        y=[0, latest["LTD"].max() * 1.1],
        mode="lines",
        line=dict(color="red", dash="dash"),
        name="Global Median CCP",
        visible=False,
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[0, latest["CCP"].max() * 1.1],
        y=[median_ltd, median_ltd],
        mode="lines",
        line=dict(color="blue", dash="dash"),
        name="Global Median LTD",
        visible=False,
        showlegend=False
    ))

    quarter_buttons = []
    for q_label in quarter_labels:
        visible = [(q_label in tr.name) for tr in fig.data]
        quarter_buttons.append(dict(
            label=q_label,
            method="update",
            args=[{"visible": visible},
                  {"title": f"Debt vs Liquid Assets: {q_label}"}]
        ))

    quarter_buttons.insert(0, dict(
        label="All Quarters (Median)",
        method="update",
        args=[{"visible": [("Global Median" in tr.name) or ("- Median" in tr.name)
                            for tr in fig.data]}]
    ))

    fig.update_layout(
        title=dict(
            text="Debt vs Liquid Assets: Median Across Quarters",
            x=0.5,
            y=0.98,
            xanchor="center",
            yanchor="top",
            font=dict(size=20)
        ),
        xaxis_title="Current Cash Position (CCP)",
        yaxis_title="Long-Term Debt (LTD)",
        width=1100, height=850,
        plot_bgcolor="white",
        showlegend=True,
        legend_title="Companies (click to show/hide)",
        updatemenus=[dict(
            buttons=quarter_buttons,
            active=0,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.35, xanchor="left",
            y=1.12, yanchor="top"
        )],
        margin=dict(t=180)
    )

    fig = add_annotation(
        fig,
        "This visualization compares companies <b>Current Cash Position (CCP)</b> "
        "to their <b>Long-Term Debt (LTD)</b> "
        "with the option to view either median values across all periods or any selected reporting period.<br>"
        "Bubble size shows the <b>CCP/LTD ratio</b>.<br>"
        "<b>Bottom-right quadrant</b> → stronger liquidity relative to debt "
        "<b>Top-left quadrant</b> → higher leverage pressure<br> "
        "By switching between quarters or aggregated time ranges, you can observe how company positions shift over time:<br>"
        "<b>Rightward movement</b> → growing liquid assets "
        "<b>Upward movement</b> → increasing long-term debt<br>"
        "This allows analysis of both the current financial state and longer-term strategic trends.",
        position="top",
        font=dict(size=14)
    )
    
    fig.update_layout(margin=dict(t=160))

    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True,
                     showgrid=True, gridcolor="lightgray")
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True,
                     showgrid=True, gridcolor="lightgray")

    for tr in fig.data:
        tr.visible = ("Global Median" in tr.name) or ("- Median" in tr.name)

    return fig

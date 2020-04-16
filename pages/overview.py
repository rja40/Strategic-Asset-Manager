import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import requests
import datetime
from utils import Header, make_dash_table
from dash.dependencies import Input, Output
import pandas as pd
import pathlib
from yahoo_fin import stock_info as si
from app import app

app.config['suppress_callback_exceptions']=True
df_graph = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/snp_histdata.csv')
df_hist = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/stock_treedata.csv')
df_results = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/return_results.csv')
'''
df = si.get_day_most_active()
df['Volume'] = df['Volume'].apply(lambda x: int(x))
df.drop(['Change','Avg Vol (3 month)','Market Cap','PE Ratio (TTM)'],axis=1,inplace=True)
df = df.rename(columns={"Price (Intraday)": "Price"})
df = df[0:20]

#df_gain = si.get_day_gainers()
df_gain = si.get_day_most_active()
df_gain['Volume'] = df_gain['Volume'].apply(lambda x: int(x))
df_gain.drop(['Change','Avg Vol (3 month)','Market Cap','PE Ratio (TTM)'],axis=1,inplace=True)
df_gain = df_gain.rename(columns={"Price (Intraday)": "Price"})
df_gain = df_gain[0:20]
'''
df_results['Return'] = df_results['Return'].round(2)
df_results['Today'] = df_results['Today'].round(2)
df_results['Prediction'] = df_results['Prediction'].round(2)

df_gain = df_results[df_results['Return']>0]
df_gain = df_gain.sort_values(['Error2'])[-15:]
df_gain = df_gain[['Symbol','Name','Sector','Today','Prediction','Return']]
#df_gain = df_gain.sort_values(['Return'],ascending=False)[:15]


df = df_results[df_results['Return']<0]
df = df.sort_values(['Error2'])[-15:]
df = df[['Symbol','Name','Sector','Today','Prediction','Return']]
#df = df.sort_values(['Return'])[:15]


news_requests = requests.get(
    "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=a36219e84088466ca87705bcf9f6a12f"
)

def update_news():
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url"]])
    max_rows = 10
    return html.Div(
        children=[
            #html.Div(
            #html.H6(["Headlines"], className="subtitle padded")),
            html.H6(["Headlines"],className="subtitle padded"),
            html.P(
                className="p-news float-left",
                children="Last update : "
                + datetime.datetime.now().strftime("%H:%M:%S"),
            ),
            html.Table(
                className="table-news",
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.A(
                                        className="td-link",
                                        children=df.iloc[i]["title"],
                                        href=df.iloc[i]["url"],
                                        target="_blank",
                                    )
                                ]
                            )
                        ]
                    )
                    for i in range(min(len(df), max_rows))
                ],
            ),
        ],className="six columns",
    )

# Update page


#def create_layout(app):
    # Page layouts
result = html.Div(
    [
        html.Div([Header(app)]),
        # page 1
        html.Div(
            [
                # Row 3
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Product Summary"),
                                html.Br([]),
                                html.P(
                                    "\
                                SAM provides the trader a complete interface to make trading decisions. The trader"
                                    "can opt to analyse the day's trading activity, as well as access to a company's"
                                    "historical performance. We also provide an interface of text analytics to evaluate"
                                    "organisation's annual financial reports. In addition to this, the chatbot allows"
                                    "us to provide a unique and quick way to interact with the user and service requests",
                                    style={"color": "#ffffff"},
                                    className="row",
                                ),
                            ],
                            className="product",
                        )
                    ],
                    className="row",
                ),
                # Row 4




                html.Div(
                    [
                        html.Div(

                            children=[
                                # Left Panel Div
                                html.Div(
                                    className="six columns div-left-panel",
                                    children=[

                                        # Div for News Headlines
                                        html.Div(
                                            className="div-news",
                                            children=[html.Div(id="news", children=update_news())],
                                        ),
                                    ],
                                ),
                                # Right Panel Div

                            ],
                        ),
                        html.Div(
                            [

                                html.Div(
                                    [
                                        html.H6("Index Performance", className="subtitle padded"),
dcc.Graph(
                                            id="graph2",
                                            figure={
                                                "data": [
                                                    go.Scatter(
                                                        x=df_graph["formatted_date"],
                                                        y=df_graph["mean_GSPC"],
                                                        line={"color": "#b5b5b5"},
                                                        mode="lines",
                                                        name="S&P 500",
                                                    ),
                                                    go.Scatter(
                                                        x=df_graph["formatted_date"],
                                                        y=df_graph[
                                                            "mean_OEX"
                                                        ],
                                                        line={"color": "#97151c"},
                                                        mode="lines",
                                                        name="S&P 100",
                                                    ),
                                                ],
                                                "layout": go.Layout(
                                                    autosize=True,
                                                    #width=700,
                                                    height=220,
                                                    font={"family": "Raleway", "size": 10},
                                                    margin={
                                                        "r": 30,
                                                        "t": 30,
                                                        "b": 30,
                                                        "l": 30,
                                                    },
                                                    showlegend=True,
                                                    titlefont={
                                                        "family": "Raleway",
                                                        "size": 10,
                                                    },
                                                    xaxis={
                                                        "autorange": True,
                                                        "range": [
                                                            "2007-12-31",
                                                            "2018-03-06",
                                                        ],
                                                        "rangeselector": {
                                                            "buttons": [
                                                                {
                                                                    "count": 1,
                                                                    "label": "1 Year",
                                                                    "step": "year",
                                                                    "stepmode": "backward",
                                                                },
                                                                {
                                                                    "count": 3,
                                                                    "label": "3 Year",
                                                                    "step": "year",
                                                                    "stepmode": "backward",
                                                                },
                                                                {
                                                                    "count": 5,
                                                                    "label": "5 Year",
                                                                    "step": "year",
                                                                },

                                                            ]
                                                        },
                                                        "showline": True,
                                                        "type": "date",
                                                        "zeroline": False,
                                                    },
                                                    yaxis={
                                                        "autorange": True,
                                                        "showline": True,
                                                        "type": "linear",
                                                        "zeroline": False,
                                                    },
                                                ),
                                            },
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                    className="six columns",
                                ),
                                html.Div(
                                    [
                                html.Div(
                                    [
                                        html.H6("Company Performance", className="subtitle padded"),

                                        html.Div(
                                            [
                                                dcc.Dropdown(id='company_1',
                                                             options=[
                                                                 {'label': "Apple Inc.", 'value': "AAPL"},
                                                                 {'label': "AbbVie Inc.", 'value': "ABBV"},
                                                                 {'label': "Abbott Laboratories", 'value': "ABT"},
                                                                 {'label': "Accenture", 'value': "ACN"},
                                                                 {'label': "Adobe Inc.", 'value': "ADBE"},
                                                                 {'label': "Allergan", 'value': "AGN"},
                                                                 {'label': "American International Group",
                                                                  'value': "AIG"},
                                                                 {'label': "Allstate", 'value': "ALL"},
                                                                 {'label': "Amgen Inc.", 'value': "AMGN"},
                                                                 {'label': "Amazon.com", 'value': "AMZN"},
                                                                 {'label': "American Express", 'value': "AXP"},
                                                                 {'label': "Boeing Co.", 'value': "BA"},
                                                                 {'label': "Bank of America Corp", 'value': "BAC"},
                                                                 {'label': "Biogen", 'value': "BIIB"},
                                                                 {'label': "The Bank of New York Mellon",
                                                                  'value': "BK"},
                                                                 {'label': "Booking Holdings", 'value': "BKNG"},
                                                                 {'label': "BlackRock Inc", 'value': "BLK"},
                                                                 {'label': "Bristol-Myers Squibb", 'value': "BMY"},
                                                                 {'label': "Citigroup Inc", 'value': "C"},
                                                                 {'label': "Caterpillar Inc.", 'value': "CAT"},
                                                                 {'label': "Charter Communications", 'value': "CHTR"},
                                                                 {'label': "Colgate-Palmolive", 'value': "CL"},
                                                                 {'label': "Comcast Corp.", 'value': "CMCSA"},
                                                                 {'label': "Capital One Financial Corp.",
                                                                  'value': "COF"},
                                                                 {'label': "ConocoPhillips", 'value': "COP"},
                                                                 {'label': "Costco Wholesale Corp.", 'value': "COST"},
                                                                 {'label': "Cisco Systems", 'value': "CSCO"},
                                                                 {'label': "CVS Health", 'value': "CVS"},
                                                                 {'label': "Chevron Corporation", 'value': "CVX"},
                                                                 {'label': "DuPont de Nemours Inc", 'value': "DD"},
                                                                 {'label': "Danaher Corporation", 'value': "DHR"},
                                                                 {'label': "The Walt Disney Company", 'value': "DIS"},
                                                                 {'label': "Dow Inc.", 'value': "DOW"},
                                                                 {'label': "Duke Energy", 'value': "DUK"},
                                                                 {'label': "Emerson Electric Co.", 'value': "EMR"},
                                                                 {'label': "Exelon", 'value': "EXC"},
                                                                 {'label': "Ford Motor Company", 'value': "F"},
                                                                 {'label': "Facebook, Inc.", 'value': "FB"},
                                                                 {'label': "FedEx", 'value': "FDX"},
                                                                 {'label': "General Dynamics", 'value': "GD"},
                                                                 {'label': "General Electric", 'value': "GE"},
                                                                 {'label': "Gilead Sciences", 'value': "GILD"},
                                                                 {'label': "General Motors", 'value': "GM"},
                                                                 {'label': "Alphabet Inc. (Class C)", 'value': "GOOG"},
                                                                 {'label': "Alphabet Inc. (Class A)", 'value': "GOOGL"},
                                                                 {'label': "Goldman Sachs", 'value': "GS"},
                                                                 {'label': "Home Depot", 'value': "HD"},
                                                                 {'label': "Honeywell", 'value': "HON"},
                                                                 {'label': "International Business Machines",
                                                                  'value': "IBM"},
                                                                 {'label': "Intel Corp.", 'value': "INTC"},
                                                                 {'label': "Johnson & Johnson", 'value': "JNJ"},
                                                                 {'label': "JPMorgan Chase & Co.", 'value': "JPM"},
                                                                 {'label': "Kraft Heinz", 'value': "KHC"},
                                                                 {'label': "Kinder Morgan", 'value': "KMI"},
                                                                 {'label': "The Coca-Cola Company", 'value': "KO"},
                                                                 {'label': "Eli Lilly and Company", 'value': "LLY"},
                                                                 {'label': "Lockheed Martin", 'value': "LMT"},
                                                                 {'label': "Lowe's Companies", 'value': "LOW"},
                                                                 {'label': "MasterCard Inc", 'value': "MA"},
                                                                 {'label': "McDonald's Corp", 'value': "MCD"},
                                                                 {'label': "Mondelēz International", 'value': "MDLZ"},
                                                                 {'label': "Medtronic plc", 'value': "MDT"},
                                                                 {'label': "MetLife Inc.", 'value': "MET"},
                                                                 {'label': "3M Company", 'value': "MMM"},
                                                                 {'label': "Altria Group", 'value': "MO"},
                                                                 {'label': "Merck & Co.", 'value': "MRK"},
                                                                 {'label': "Morgan Stanley", 'value': "MS"},
                                                                 {'label': "Microsoft", 'value': "MSFT"},
                                                                 {'label': "NextEra Energy", 'value': "NEE"},
                                                                 {'label': "Netflix", 'value': "NFLX"},
                                                                 {'label': "Nike, Inc.", 'value': "NKE"},
                                                                 {'label': "NVIDIA Corp.", 'value': "NVDA"},
                                                                 {'label': "Oracle Corporation", 'value': "ORCL"},
                                                                 {'label': "Occidental Petroleum Corp.",
                                                                  'value': "OXY"},
                                                                 {'label': "PepsiCo", 'value': "PEP"},
                                                                 {'label': "Pfizer Inc", 'value': "PFE"},
                                                                 {'label': "Procter & Gamble Co", 'value': "PG"},
                                                                 {'label': "Philip Morris International",
                                                                  'value': "PM"},
                                                                 {'label': "PayPal Holdings", 'value': "PYPL"},
                                                                 {'label': "Qualcomm Inc.", 'value': "QCOM"},
                                                                 {'label': "Raytheon Co.", 'value': "RTN"},
                                                                 {'label': "Starbucks Corp.", 'value': "SBUX"},
                                                                 {'label': "Schlumberger", 'value': "SLB"},
                                                                 {'label': "Southern Company", 'value': "SO"},
                                                                 {'label': "Simon Property Group, Inc.",
                                                                  'value': "SPG"},
                                                                 {'label': "AT&T Inc", 'value': "T"},
                                                                 {'label': "Target Corporation", 'value': "TGT"},
                                                                 {'label': "Thermo Fisher Scientific", 'value': "TMO"},
                                                                 {'label': "Texas Instruments", 'value': "TXN"},
                                                                 {'label': "UnitedHealth Group", 'value': "UNH"},
                                                                 {'label': "Union Pacific Corporation", 'value': "UNP"},
                                                                 {'label': "United Parcel Service", 'value': "UPS"},
                                                                 {'label': "U.S. Bancorp", 'value': "USB"},
                                                                 {'label': "United Technologies", 'value': "UTX"},
                                                                 {'label': "Visa Inc.", 'value': "V"},
                                                                 {'label': "Verizon Communications", 'value': "VZ"},
                                                                 {'label': "Walgreens Boots Alliance", 'value': "WBA"},
                                                                 {'label': "Wells Fargo", 'value': "WFC"},
                                                                 {'label': "Walmart", 'value': "WMT"},
                                                                 {'label': "Exxon Mobil Corp.", 'value': "XOM"},
                                                             ],
                                                             value='AXP'#,multi=True
                                                             )
                                            ],className="twelve columns"
                                        ),
                                        html.Div(
                                            [
                                                html.Br(),
                                                html.Br(),
                                                html.Br(),
                                            ]
                                        ),

                                        dcc.Graph(
                                            id="graph3"
                                        ),
                                    ],
                                    className="six columns",
                                ),
                                    ]
                                )


                            ],
                            className="row ",
                        ),
                    ],
                    className="row",
                    style={"margin-bottom": "10px"},
                ),
                # Row 5
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(
                                    "BUY",
                                    className="subtitle padded",
                                ),
                                html.Table(make_dash_table(df_gain)),
                            ], #style={"overflow-y": "scroll"},
                            className="six columns",
                        ),
                        html.Div(
                            [
                                html.H6(
                                    "SELL",
                                    className="subtitle padded",
                                ),
                                html.Table(make_dash_table(df)),
                            ],
                            className="six columns",
                        ),
                    ],
                    className="row ",
                ),
            ],
            className="sub_page",
        ),
    ],
    className="page",
)

@app.callback(Output('graph3', 'figure'),
              [Input('company_1', 'value'),
               ])
def render_graph(company_1):

    df_1 = df_hist[df_hist.symbol == company_1]

    company_name = df_1.iloc[0, 2]



    fig_graph3 = go.Figure()
    fig_graph3.add_trace(go.Scatter(
                                                        x=df_1["formatted_date"],
                                                        y=df_1["mean"],
                                                        line={"color": "#97151c"},
                                                        mode="lines",
                                                        name=company_name,
                                                    ),)
    fig_graph3.update_layout(
                                                    autosize=True,
                                                    #width=700,
                                                    height=220,
                                                    font={"family": "Raleway", "size": 10},
                                                    margin={
                                                        "r": 30,
                                                        "t": 30,
                                                        "b": 30,
                                                        "l": 30,
                                                    },
                                                    showlegend=True,
                                                    titlefont={
                                                        "family": "Raleway",
                                                        "size": 10,
                                                    },
                                                    xaxis={
                                                        "autorange": True,

                                                        "rangeselector": {
                                                            "buttons": [
                                                                {
                                                                    "count": 1,
                                                                    "label": "1 Year",
                                                                    "step": "year",
                                                                    "stepmode": "backward",
                                                                },
                                                                {
                                                                    "count": 3,
                                                                    "label": "3 Year",
                                                                    "step": "year",
                                                                    "stepmode": "backward",
                                                                },
                                                                {
                                                                    "count": 5,
                                                                    "label": "5 Year",
                                                                    "step": "year",
                                                                },

                                                            ]
                                                        },
                                                        "showline": True,
                                                        "type": "date",
                                                        "zeroline": False,
                                                    },
                                                    yaxis={
                                                        "autorange": True,
                                                        "showline": True,
                                                        "type": "linear",
                                                        "zeroline": False,
                                                    },
                                                )
    return fig_graph3


layout_overview = html.Div([
        #Header(app),
        result,
        ])
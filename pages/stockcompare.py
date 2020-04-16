import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header, make_dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import pathlib
from dash.dependencies import Input, Output
from app import app
from yahoo_fin import stock_info as si
app.config['suppress_callback_exceptions']=True

df = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/stock_high.csv')
df_company = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/company_data.csv')
# get relative data folder
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../data").resolve()


# df_current_prices = pd.read_csv(DATA_PATH.joinpath("df_current_prices.csv"))
# df_hist_prices = pd.read_csv(DATA_PATH.joinpath("df_hist_prices.csv"))
# df_avg_returns = pd.read_csv(DATA_PATH.joinpath("df_avg_returns.csv"))
# df_after_tax = pd.read_csv(DATA_PATH.joinpath("df_after_tax.csv"))
# df_recent_returns = pd.read_csv(DATA_PATH.joinpath("df_recent_returns.csv"))
# df_graph = pd.read_csv(DATA_PATH.joinpath("df_graph.csv"))

#app.config['suppress_callback_exceptions']=True


#def create_layout(app):
result = html.Div(
        [
            #Header(app),
            html.Div(
                [
                    html.Br(),
                ]
            ),
            # page 2

            html.Div(
                [
                    html.Div(
                        [
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
                                                     {'label': "American International Group", 'value': "AIG"},
                                                     {'label': "Allstate", 'value': "ALL"},
                                                     {'label': "Amgen Inc.", 'value': "AMGN"},
                                                     {'label': "Amazon.com", 'value': "AMZN"},
                                                     {'label': "American Express", 'value': "AXP"},
                                                     {'label': "Boeing Co.", 'value': "BA"},
                                                     {'label': "Bank of America Corp", 'value': "BAC"},
                                                     {'label': "Biogen", 'value': "BIIB"},
                                                     {'label': "The Bank of New York Mellon", 'value': "BK"},
                                                     {'label': "Booking Holdings", 'value': "BKNG"},
                                                     {'label': "BlackRock Inc", 'value': "BLK"},
                                                     {'label': "Bristol-Myers Squibb", 'value': "BMY"},
                                                     {'label': "Citigroup Inc", 'value': "C"},
                                                     {'label': "Caterpillar Inc.", 'value': "CAT"},
                                                     {'label': "Charter Communications", 'value': "CHTR"},
                                                     {'label': "Colgate-Palmolive", 'value': "CL"},
                                                     {'label': "Comcast Corp.", 'value': "CMCSA"},
                                                     {'label': "Capital One Financial Corp.", 'value': "COF"},
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
                                                     {'label': "International Business Machines", 'value': "IBM"},
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
                                                     {'label': "Occidental Petroleum Corp.", 'value': "OXY"},
                                                     {'label': "PepsiCo", 'value': "PEP"},
                                                     {'label': "Pfizer Inc", 'value': "PFE"},
                                                     {'label': "Procter & Gamble Co", 'value': "PG"},
                                                     {'label': "Philip Morris International", 'value': "PM"},
                                                     {'label': "PayPal Holdings", 'value': "PYPL"},
                                                     {'label': "Qualcomm Inc.", 'value': "QCOM"},
                                                     {'label': "Raytheon Co.", 'value': "RTN"},
                                                     {'label': "Starbucks Corp.", 'value': "SBUX"},
                                                     {'label': "Schlumberger", 'value': "SLB"},
                                                     {'label': "Southern Company", 'value': "SO"},
                                                     {'label': "Simon Property Group, Inc.", 'value': "SPG"},
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
                                                 value='AMZN'
                                                 )
                                ],className="offset-by-one columns five columns"
                            ),
                            html.Div(
                                [
                                    dcc.Dropdown(id='company_2',
                                                 options=[
                                                     {'label': "Apple Inc.", 'value': "AAPL"},
                                                     {'label': "AbbVie Inc.", 'value': "ABBV"},
                                                     {'label': "Abbott Laboratories", 'value': "ABT"},
                                                     {'label': "Accenture", 'value': "ACN"},
                                                     {'label': "Adobe Inc.", 'value': "ADBE"},
                                                     {'label': "Allergan", 'value': "AGN"},
                                                     {'label': "American International Group", 'value': "AIG"},
                                                     {'label': "Allstate", 'value': "ALL"},
                                                     {'label': "Amgen Inc.", 'value': "AMGN"},
                                                     {'label': "Amazon.com", 'value': "AMZN"},
                                                     {'label': "American Express", 'value': "AXP"},
                                                     {'label': "Boeing Co.", 'value': "BA"},
                                                     {'label': "Bank of America Corp", 'value': "BAC"},
                                                     {'label': "Biogen", 'value': "BIIB"},
                                                     {'label': "The Bank of New York Mellon", 'value': "BK"},
                                                     {'label': "Booking Holdings", 'value': "BKNG"},
                                                     {'label': "BlackRock Inc", 'value': "BLK"},
                                                     {'label': "Bristol-Myers Squibb", 'value': "BMY"},
                                                     {'label': "Citigroup Inc", 'value': "C"},
                                                     {'label': "Caterpillar Inc.", 'value': "CAT"},
                                                     {'label': "Charter Communications", 'value': "CHTR"},
                                                     {'label': "Colgate-Palmolive", 'value': "CL"},
                                                     {'label': "Comcast Corp.", 'value': "CMCSA"},
                                                     {'label': "Capital One Financial Corp.", 'value': "COF"},
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
                                                     {'label': "International Business Machines", 'value': "IBM"},
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
                                                     {'label': "Occidental Petroleum Corp.", 'value': "OXY"},
                                                     {'label': "PepsiCo", 'value': "PEP"},
                                                     {'label': "Pfizer Inc", 'value': "PFE"},
                                                     {'label': "Procter & Gamble Co", 'value': "PG"},
                                                     {'label': "Philip Morris International", 'value': "PM"},
                                                     {'label': "PayPal Holdings", 'value': "PYPL"},
                                                     {'label': "Qualcomm Inc.", 'value': "QCOM"},
                                                     {'label': "Raytheon Co.", 'value': "RTN"},
                                                     {'label': "Starbucks Corp.", 'value': "SBUX"},
                                                     {'label': "Schlumberger", 'value': "SLB"},
                                                     {'label': "Southern Company", 'value': "SO"},
                                                     {'label': "Simon Property Group, Inc.", 'value': "SPG"},
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
                                                 value='WMT'
                                                 )
                                ], className="five columns"
                            ),
                        ],
                        className="row",
                    ),
                ],
                #className="twelve columns",
            ),


            html.Div(
                [
                    # Row
                    html.Div(
                        [

                            html.Div([html.Br(),
                                html.Img(id='logo1',style={'height':'50px', 'width':'125px'}),
                                ],className="offset-by-one columns five columns"
                            ),

                            html.Div([html.Br(),
                                html.Img(id='logo2',style={'height':'50px', 'width':'125px'}),
                                ],className="five columns"
                            ),
                        ],style={'textAlign':'center'},className="row ",
                    )
                 ]
            ),
            html.Div(
                [
                            html.Div(
                                            [
                                                html.Div(
                                                    html.H6(id="text1", children=''),
                                                    className="offset-by-one columns five columns"
                                                ),
                            html.Div(
                                html.H6(id="text2", children=''),
                                className="columns five columns"
                            ),


                        ],style={'textAlign':'justify'},className="row",
                    )
                 ]
            ),


            html.Div(
                [
                    # Row
                    html.Div(
                        [
                            html.Div(
                                dcc.Graph(id='fig1'),
                                className="six columns"
                            ),
                            html.Div(
                                dcc.Graph(id='fig2'),
                                className="six columns"
                            ),
                        ],
                        className="row ",
                    ),

                ],
                #className="page",
            ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(
                                    id="table1_title",children='',
                                    className="subtitle padded",
                                ),
                                html.Div(id="table1"),
                            ], #style={"overflow-y": "scroll"},
                            className="six columns",
                        ),
                        html.Div(
                            [
                                html.H6(
                                    id="table2_title",children='',
                                    className="subtitle padded",
                                ),
                                html.Div(id="table2"),
                            ],
                            className="six columns",
                        ),
                    ],
                    className="row ",
                ),
        ],
        className="page",
    )

@app.callback(
    Output('text1', 'children'),
     [Input('company_1', 'value'),
      ])
def render_content(company_1):
    return df_company[df_company['Symbol'] == company_1]['Data']

@app.callback(
    Output('text2', 'children'),
     [Input('company_2', 'value'),
      ])
def render_content(company_2):
    return df_company[df_company['Symbol'] == company_2]['Data']

@app.callback(Output('logo1', 'src'),
              [Input('company_1', 'value'),
               ])
def render_content(company_1):

    src = "/assets/logo/" + company_1
    return src

@app.callback(Output('logo2', 'src'),
              [Input('company_2', 'value'),
               ])
def render_content(company_2):

    src = "/assets/logo/" + company_2
    return src

@app.callback(Output('fig1', 'figure'),
              [Input('company_1', 'value'),
               ])
def render_content(company_1):

    df_1 = df[df.symbol == company_1]
    company_name = df_1.iloc[0, 1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_1['year'], y=df_1['high'], mode='lines+markers'))
    fig.update_layout(title='Stock Value for ' + company_name,
                      title_x=0.5,
                      xaxis_title='Year',
                      yaxis_title='Price($)')
    return fig

@app.callback(Output('fig2', 'figure'),
              [Input('company_2', 'value'),
               ])
def render_content(company_2):

    df_1 = df[df.symbol == company_2]
    company_name = df_1.iloc[0, 1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_1['year'], y=df_1['high'], mode='lines+markers'))
    fig.update_layout(title='Stock Value for ' + company_name,
                      title_x=0.5,
                      xaxis_title='Year',
                      yaxis_title='Price($)')
    return fig

@app.callback(Output('table1', 'children'),
              [Input('company_1', 'value'),
               ])
def render_table(company_1):
    #print(company_1)
    holders = si.get_holders(company_1)
    data = holders['Top Institutional Holders']
    return html.Div(html.Table(make_dash_table(data)))

@app.callback(Output('table2', 'children'),
              [Input('company_2', 'value'),
               ])
def render_table(company_2):
    #print(company_1)
    holders = si.get_holders(company_2)
    data = holders['Top Institutional Holders']
    return html.Div(html.Table(make_dash_table(data)))

@app.callback(
    Output('table1_title', 'children'),
    [Input('company_1', 'value'),
     ])
def update_title(company_1):
    df_1 = df[df.symbol == company_1]
    company_name = df_1.iloc[0, 1]
    title = 'Top Stock Holders for '+company_name
    return title

@app.callback(
    Output('table2_title', 'children'),
    [Input('company_2', 'value'),
     ])
def update_title(company_2):
    df_1 = df[df.symbol == company_2]
    company_name = df_1.iloc[0, 1]
    title = 'Top Stock Holders for '+company_name
    return title

layout_stock = html.Div([
        Header(app),
        result,
        ])

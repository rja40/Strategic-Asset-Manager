import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header, make_dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import pathlib
from dash.dependencies import Input, Output
from app import app
import ast
from yahoo_fin import stock_info as si
app.config['suppress_callback_exceptions']=True

df_company = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/company_data.csv')
file = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/textanalytics_chart.csv')

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
                                    dcc.Dropdown(id='company_1_ta',
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
                                    dcc.Dropdown(id='year',
                                                 options=[

                                                     {'label': "2015", 'value': 2015},
                                                     {'label': "2016", 'value': 2016},
                                                     {'label': "2017", 'value': 2017},
                                                     {'label': "2018", 'value': 2018},
                                                     {'label': "2019", 'value': 2019},

                                                 ],
                                                 value='2019'
                                                 )
                                ], className="three columns"
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
                            html.Br(),
                            html.Div([html.Br(),
                                html.Img(id='logo1_ta',style={'height':'50px', 'width':'125px'}),
                                ],className="offset-by-three column five columns"
                            ),
                        ],style={'textAlign':'center'},className="row ",
                    )
                 ]
            ),

            html.Div(
                [
                    # Row
                    html.Div(
                        [
                            html.Div(
                                dcc.Graph(id='fig1_ta'),
                                className="six columns"
                            ),
                            html.Div(
                                dcc.Graph(id='fig2_ta'),
                                className="six columns"
                            ),

                        ],
                        className="row ",
                    ),

                ],
                #className="page",
            ),

        ],
        className="page",
    )


@app.callback(Output('logo1_ta', 'src'),
              [Input('company_1_ta', 'value'),
               ])
def render_content(company_1_ta):

    src = "/assets/logo/" + company_1_ta
    return src

@app.callback(Output('fig1_ta', 'figure'),
              [Input('company_1_ta', 'value'),
               Input('year', 'value')
               ])
def render_content(company_1_ta,year):

    year = int(year)
    row = file[(file.Symbol == company_1_ta)  & (file.year == year)]

    for idx, row in row['score'].iteritems():
        counter = row
    # print(counter)

    counter_dict = ast.literal_eval(counter)

    final_result = pd.DataFrame(counter_dict.items(), columns=['Word', 'Frequency'])

    top_10 = final_result.sort_values(['Frequency'], ascending=False)
    top_10 = top_10[:10]

    fig = {
        'data': [{
            'type': 'bar',
            'orientation' : 'h',

            'y': top_10['Word'],
            'x': top_10['Frequency'],

        }],
        'layout': {
            #'width': 900,
            #'height': 400,
            'title': 'MDA Emotions for ' + company_1_ta,
            'title_x' : 0.5,
            'yaxis_title': 'Frequency'

        }
    }

    return fig


@app.callback(Output('fig2_ta', 'figure'),
              [Input('company_1_ta', 'value'),
               Input('year', 'value')
               ])
def render_content(company_1_ta,year):
    #file = pd.read_csv('/home/anuj/PycharmProjects/733/result_uncertain10mar.csv')
    year = int(year)
    row = file[(file.Symbol == company_1_ta)  & (file.year == year)]

    for idx, row in row['uncertainity_words'].iteritems():
        counter = row
    # print(counter)

    counter_dict = ast.literal_eval(counter)

    final_result = pd.DataFrame(counter_dict.items(), columns=['Word', 'Frequency'])

    top_10 = final_result.sort_values(['Frequency'], ascending=False)
    top_10 = top_10[:10]

    fig = {
        'data': [{
            'type': 'bar',
            'orientation' : 'h',

            'y': top_10['Word'],
            'x': top_10['Frequency'],

        }],
        'layout': {
            #'width': 900,
            #'height': 400,
            'title': 'Uncertainty Word Count for ' + company_1_ta,
            'title_x' : 0.5,
            'yaxis_title': 'Frequency'

        }
    }

    return fig

layout_edgar = html.Div([
        Header(app),
        result,
        ])

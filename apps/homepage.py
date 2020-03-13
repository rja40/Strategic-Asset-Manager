import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from navbar import Navbar
from app import app
from dash.dependencies import Input, Output
import dash_table
from yahoo_fin import stock_info as si

nav = Navbar()
app.config['suppress_callback_exceptions']=True
df = si.get_day_most_active()
df.drop(['Change','Avg Vol (3 month)','Market Cap','PE Ratio (TTM)'],axis=1,inplace=True)
df = df.rename(columns={"Price (Intraday)": "Price"})

stockval = dbc.Container(
    [dbc.Row([
                html.Hr(),
    ]),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            (
                                dcc.Dropdown(id='company_2',
                                             options=[
                                                 {'label': 'ABBOTT LABORATORIES', 'value': 1800},
                                                 {'label': 'AMERICAN EXPRESS CO', 'value': 4962},
                                                 {'label': 'AMERICAN INTERNATIONAL GROUP INC', 'value': 5272},
                                                 {'label': 'BOEING CO', 'value': 12927},
                                                 {'label': 'BRISTOL MYERS SQUIBB CO', 'value': 14272},
                                                 {'label': 'CATERPILLAR INC', 'value': 18230},
                                                 {'label': 'JPMORGAN CHASE & CO', 'value': 19617},
                                             ],
                                             value=1800
                                             )
                            ), className="ten columns"
                        ),

                    ],
                ),

            ]
        ),
        dbc.Row(
            [
                html.Div(
                    dcc.Graph(id='fig2'),
                    className="twelve columns"
                )

            ]
        ),
        dbc.Row(
        [

        ]
    ),
        dbc.Row(
            [
                html.Div(
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
                        fixed_rows={'headers': True, 'data': 0},
                        style_table={
                            'maxHeight': '300px',
                            'maxWidth': '620px',
                            'overflowY': 'scroll',

                        },
                        style_cell={'textAlign': 'left', 'padding': '5px'},
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)',

                            },
                            {'if': {'column_id': '% Change'},
                             'width': '25%'},

                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold',
                            'backgroundColor': 'white',
                        }

                    ),className="three column"
                )

            ]
        ),

        ]
)

@app.callback(Output('fig2', 'figure'),
              [Input('company_2', 'value'),
               ])

def render_content(company_2):
    df = pd.read_csv('/home/anuj/PycharmProjects/733/stock_high.csv')

    company_2 = int(company_2)


    df_1 = df[df.cik == company_2]
    company_name = df_1.iloc[0,1]


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_1['year'], y=df_1['high'], mode='lines+markers'))
    fig.update_layout(title='Stock Value for '+company_name,
                      xaxis_title='Year',
                      yaxis_title='Price($)')
    return fig

layout = html.Div([nav,stockval])

'''
                        id='table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
                        fixed_rows={'headers': True, 'data': 0},
                        style_table={
                            'maxHeight': '300px',
                            'maxWidth': '600px',
                            'overflowY': 'scroll',
                            #'border': 'thin lightgrey solid'
                        },
                        style_data={ 'border': '1px solid blue' },
                        style_cell={'textAlign': 'right',
                                    'padding': '5px',
                                    'minWidth': '0px', 'maxWidth': '300px',},
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)',

                            },
                            {'if': {'column_id': 'Name'},
                                  'textAlign': 'left'
                             },
                            {'if': {'column_id': 'Symbol'},
                             'width': '15%'},
                            {'if': {'column_id': '% Change'},
                             'width': '15%'},
                            {'if': {'column_id': 'Volume'},
                             'width': '10%'},

                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold',
                            'backgroundColor': 'white',
                            'border': '1px solid blue'
                        }'''

import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import dash_bootstrap_components as dbc
from navbar import Navbar
from app import app
import ast
from dash.dependencies import Input, Output

nav = Navbar()

app.config['suppress_callback_exceptions']=True

factacc = dbc.Container(
    [
    dbc.Row(
            [
                html.Div
                (
                    [
                html.H4("Text Analysis on Edgar")
                    ],className="offset-by-five column"
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            (
                                dcc.Dropdown(id='company_1',
                                             options=[
                                                 {'label': 'ABBOTT LABORATORIES', 'value': 'ABBOTT LABORATORIES'},
                                                 {'label': 'AMERICAN EXPRESS CO', 'value': 'AMERICAN EXPRESS CO'},
                                                 {'label': 'AMERICAN INTERNATIONAL GROUP INC', 'value': 'AMERICAN INTERNATIONAL GROUP INC'},
                                                 {'label': 'BOEING CO', 'value': 'BOEING CO'},
                                                 {'label': 'BRISTOL MYERS SQUIBB CO', 'value': 'BRISTOL MYERS SQUIBB CO'},
                                                 {'label': 'CATERPILLAR INC', 'value': 'CATERPILLAR INC'},
                                                 {'label': 'JPMORGAN CHASE & CO', 'value': 'JPMORGAN CHASE & CO'},
                                             ],
                                             value='ABBOTT LABORATORIES'
                                             )
                            ), className="twelve columns"
                        ),

                    ],
                ),
                dbc.Col(
                    [
                        html.Div(
                            (
                                dcc.Dropdown(id='type_1',
                                             options=[
                                                 {'label': '10-K', 'value': '10-K'},
                                                 {'label': '10-Q', 'value': '10-Q'},

                                             ],
                                             value='10-K'
                                             )
                            ), className="four columns"
                        ),

                    ],
                ),
                dbc.Col(
                    [
                        html.Div(
                            (
                                dcc.Dropdown(id='year',
                                             options=[
                                                 {'label': '2017', 'value': '2017'},
                                                 {'label': '2018', 'value': '2018'},
                                                 {'label': '2019', 'value': '2019'},
                                             ],
                                             value='2017'
                                             )
                            ), className="four columns"
                        ),

                    ],
                ),

            ]
        ),
        dbc.Row(
            [
                html.Div(
                    dcc.Graph(id='fig1'),
                    className="offset-by-one column twelve columns"
                )

            ]
        ),

        ]
)

@app.callback(Output('fig1', 'figure'),
              [Input('company_1', 'value'),
               Input('type_1', 'value'),
               Input('year', 'value')
               ])
def render_content(company_1,type_1,year):
    file = pd.read_csv('/home/anuj/PycharmProjects/733/result_uncertain10mar.csv')
    year = int(year)
    row = file[(file.company == company_1) & (file.type == type_1) & (file.year == year)]

    for idx, row in row['uncertain'].iteritems():
        counter = row
    # print(counter)

    counter_dict = ast.literal_eval(counter)

    final_result = pd.DataFrame(counter_dict.items(), columns=['Word', 'Frequency'])

    top_10 = final_result.sort_values(['Frequency'], ascending=False)
    top_10 = top_10[:10]

    fig = {
        'data': [{
            'type': 'bar',

            'x': top_10['Word'],
            'y': top_10['Frequency'],

        }],
        'layout': {
            'width': 900,
            'height': 400,
            'title': 'Uncertainity Word Count for ' + company_1,
            'title_x' : 0.5,
            'yaxis_title': 'Frequency'

        }
    }

    return fig

layout = html.Div([
        nav,
        factacc,
        ])


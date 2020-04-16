import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header, make_dash_table
import numpy as np
import pandas as pd
import plotly.express as px
import pathlib
from dash.dependencies import Input, Output
from app import app
from yahoo_fin import stock_info as si
app.config['suppress_callback_exceptions']=True


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


result = html.Div([
    dcc.Dropdown(
        id='inp',
        options=[
            {'label': '1 Month Performance', 'value': 'df_1month'},
            {'label': '3 Month Performance', 'value': 'df_3month'},
            {'label': '6 Month Performance', 'value': 'df_6month'},
            {'label': '12 Month Performance', 'value': 'df_12month'},
            {'label': '2020 Performance', 'value': 'df_2020'},
            #{'label': 'San Francisco', 'value': 'SF'}
        ],
        value='df_1month'
    ),
dcc.Dropdown(
        id='inp2',
        options=[
            {'label': 'Close', 'value': 'close'},
            {'label': 'Volume', 'value': 'volume'},

            #{'label': 'San Francisco', 'value': 'SF'}
        ],
        value='close'
    ),
    html.Div(
        dcc.Graph(id='figtreemap'))
])

@app.callback(
    Output('figtreemap', 'figure'),
    [Input('inp', 'value'),
     Input('inp2', 'value')])
def update_output(inp,inp2):
    if inp =='df_1month':
        df = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/treemap_1monthmean.csv')
    elif inp =='df_3month':
        df = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/treemap_3monthmean.csv')

    elif inp =='df_6month':
        df = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/treemap_6monthmean.csv')
    elif inp == 'df_12month':
        df = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/treemap_12monthmean.csv')
    elif inp == 'df_2020':
        df = pd.read_csv('/home/anuj/PycharmProjects/SAM/data/treemap_2020.csv')
        fig = px.treemap(df, path=['sector', 'subsector', 'symbol'], values=inp2,
                         color='pct_ch', hover_data=['company', 'low'],
                         # color_continuous_scale='RdBu',
                         color_continuous_scale=[(0, "red"), (0.8, "green"), (1.0, "blue")],
                         # color_continuous_scale=["red", "green", "blue"],
                         color_continuous_midpoint=np.average(df['pct_ch'], weights=df['close']))
        fig.update_layout(margin=dict(t=10, b=10, r=10, l=10))

        return fig


    fig = px.treemap(df, path=['sector', 'subsector', 'symbol'], values=inp2,
                     color='pct_ch', hover_data=['company', 'low'],
                     #color_continuous_scale='RdBu',
                     color_continuous_scale=[(0, "red"), (0.8, "green"), (1.0, "green")],
                     #color_continuous_scale=["red", "green", "blue"],
                     color_continuous_midpoint=np.average(df['pct_ch'], weights=df['close']))
    fig.update_layout(margin=dict(t=10, b=10, r=10, l=10))

    return fig

layout_treemap = html.Div([
        Header(app),
        result,
        ])

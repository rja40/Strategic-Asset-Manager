import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import dash_bootstrap_components as dbc
from navbar import Navbar
from app import app
from sqlalchemy import create_engine
from dash.dependencies import Input, Output
from keras.models import load_model
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go

engine = create_engine('postgresql://postgres:postgres@localhost:5432/stocks')
model_aapl = load_model('/home/anuj/PycharmProjects/733/ML/apple.h5')
model_jpm = load_model('/home/anuj/PycharmProjects/733/ML/jpm.h5')
model_ba = load_model('/home/anuj/PycharmProjects/733/ML/BA.h5')

nav = Navbar()

app.config['suppress_callback_exceptions']=True

factacc = dbc.Container(
    [
    dbc.Row(
            [
                html.Div
                (
                    [
                html.H4("Stock Value Prediction using LSTM")
                    ],className="offset-by-four column"
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
                                                 {'label': 'APPLE INC', 'value': 320193},
                                                 {'label': 'BOEING CO', 'value': 12927},
                                                 {'label': 'JPMORGAN CHASE & CO', 'value': 19617},
                                             ],
                                             value=320193
                                             )
                            ), className="twelve columns"
                        ),

                    ],
                ),


            ]
        ),
        dbc.Row(
            [
                html.Div(
                    dcc.Graph(id='fig3'),
                    className="offset-by-one column twelve columns"
                )

            ]
        ),

        ]
)

@app.callback(Output('fig3', 'figure'),
              [Input('company_1', 'value')])
def render_content(company_1):

    if(company_1==320193):
        model = model_aapl
    elif(company_1==12927):
        model = model_ba
    else:
        model = model_jpm



    def inverse_transform(values):

        inv_p = np.concatenate((values, X_test[:, 0, :-1]), axis=1)
        data = scaler.inverse_transform(inv_p)
        data = data[:, 0]
        return data

    stocks_df = pd.read_sql_query("select * from stocks_prices_1 where cik =" + '{}'.format(company_1), con=engine)
    stocks_df = stocks_df.set_index('formatted_date')
    stocks_df.index = pd.to_datetime(stocks_df.index)
    stocks_df['mean_price'] = (stocks_df['open'] + stocks_df['close'] + stocks_df['low'] + stocks_df['high']) / 4
    stocks_df = stocks_df[['open', 'close', 'high', 'low', 'volume', 'mean_price']]
    n_train = 2378
    past_values = 20
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(stocks_df)
    dataX, dataY = [], []
    for timepoint in range(scaled_data.shape[0] - past_values):
        dataX.append(scaled_data[timepoint:timepoint + past_values, :])
        dataY.append(scaled_data[timepoint + past_values, 0])
    X_train, X_test = dataX[:n_train], dataX[n_train:]
    y_train, y_test = dataY[:n_train], dataY[n_train:]
    X_test = np.array(X_test)
    Y_test = np.array(y_test)

    predictions = model.predict(X_test)

    pred = inverse_transform(predictions)
    # rint(pred)
    actual = inverse_transform(Y_test.reshape(len(Y_test), 1))

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=pred,
                             mode='lines',
                             name='predicted'))

    fig.add_trace(go.Scatter(y=actual,
                             mode='lines',
                             name='actual'))
    fig.layout=go.Layout(title=go.layout.Title(text="Actual vs Predicted"),
                         title_x=0.5,
                         yaxis_title= 'Value($)',
                         xaxis_title= 'Days')

    return fig

layout = html.Div([
        nav,
        factacc,
        ])


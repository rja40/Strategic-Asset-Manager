import dash
import dash_bootstrap_components as dbc
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
app.config['suppress_callback_exceptions']=True
#FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
#CS = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP,CS])
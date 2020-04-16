# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from pages import (
    overview,
    stockcompare,
    textanalytics,
    treemap
)


# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)
app.config['suppress_callback_exceptions']=True
# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])

def display_page(pathname):
    if pathname == "/sam/stockcompare":
        #return pricePerformance.create_layout(app)
        return stockcompare.layout_stock
    elif pathname == "/sam/treemap":
        return treemap.layout_treemap
    elif pathname == "/sam/textanalytics":
        return textanalytics.layout_edgar
    # # elif pathname == "/dash-financial-report/fees":
    #     return feesMins.create_layout(app)
    # elif pathname == "/dash-financial-report/distributions":
    #     return distributions.create_layout(app)
    # elif pathname == "/dash-financial-report/news-and-reviews":
    #     return newsReviews.create_layout(app)
    # elif pathname == "/dash-financial-report/full-view":
    #     return (
    #         overview.create_layout(app),
    #         #pricePerformance.create_layout(),
    #         pricePerformance.layout,
    #         portfolioManagement.create_layout(app),
    #         feesMins.create_layout(app),
    #         distributions.create_layout(app),
    #         newsReviews.create_layout(app),
    #     )
    else:
        #return overview.create_layout(app)
        return overview.layout_overview


if __name__ == "__main__":
    app.run_server(debug=False)

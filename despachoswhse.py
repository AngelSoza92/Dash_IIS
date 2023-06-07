from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from conn3 import get_despachos
import dash_bootstrap_components as dbc
import numpy as np
import dash
from plotly.subplots import make_subplots
import urllib.parse

despachito = dash.Dash(__name__,title="Despachos",external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/despachosbodegas/')

PLOTLY_LOGO = "http://10.107.226.241/assets/caja.png"


contenidox = html.Div(id='page-content', children=[ ])
despachito.layout = html.Div([dcc.Location(id="url"), contenidox])

@despachito.callback(Output("page-content", "children"), Input("url","search"))
def render_page_content(search):
    params = urllib.parse.parse_qs(search[1:])
    param_value = params.get('datatheme', [''])[0]
    dff=get_despachos()
    origenes = dff.FECHA_SALIDA.unique()
   
    dfff = dff.pivot_table( values = "QTY",index = "WHSE", columns = "FECHA_SALIDA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    long = dfff.shape[0]
    whses = dff.WHSE.unique()

    dfrespon = dff.groupby('FECHA_SALIDA')['QTY'].sum()
    dfwhses = dff.groupby('WHSE')['QTY'].sum()

    fig8 = make_subplots(
        rows=1, cols=2,
        specs=[
            [{"type": "domain"}, {'type':'xy'}]],
        subplot_titles=("FECHA SALIDA","WHSE")
    )

    fig8.add_trace(go.Pie(labels=origenes, values=dfrespon[origenes], name="FECHA"), 1, 1)
    fig8.add_trace(go.Bar(x=whses, y=dfwhses[whses], name='WHSE'),1,2)
    if param_value == "dark":
        content = html.Div(
        [
            html.Div(
                [
                    html.H3("Despachos", style={"textAlign":"center","color":"black"}),
                    html.Div([
                    html.Label('Valor del parámetro:'),
                    html.P(param_value)]),
                    dcc.Graph(id='graph1',figure=fig8),
                    dash_table.DataTable(
                        id="table",
                        columns=[{"name": c, "id": c} for c in dfff.columns if c != 'id'],
                        data=dfff.to_dict("records"),
                        page_size=long,
                        sort_action="native",
                        filter_action="native",
                        sort_mode="multi",
                        column_selectable="multi",
                        row_selectable="multi",
                        style_header={
                                'backgroundColor': 'black',
                                'color': 'white'},
                        style_data={
                                'backgroundColor': 'black',
                                'color': 'white'
                            }),
                ],
            ),
            html.Div(id="output-graph"),
        ],style={'backgroundColor': 'black',
                                'color': 'white'}
    )
        return content
    else:
        content = html.Div(
        [
            html.Div(
                [
                    html.H3("Despachos", style={"textAlign":"center"}),
                    html.Div([
                    html.Label('Valor del parámetro:'),
                    html.P(param_value)]),
                    dcc.Graph(id='graph1',figure=fig8),
                    dash_table.DataTable(
                        id="table",
                        columns=[{"name": c, "id": c} for c in dfff.columns if c != 'id'],
                        data=dfff.to_dict("records"),
                        page_size=long,
                        sort_action="native",
                        filter_action="native",
                        sort_mode="multi",
                        column_selectable="multi",
                        row_selectable="multi",
                        style_header={
                                'backgroundColor': 'rgb(72,118,178)',
                                'color': 'white'},
                        style_data={
                                'backgroundColor': 'rgb(217,227,241)',
                                'color': 'rgb(72,118,178)'
                            }),
                ],
            ),
            html.Div(id="output-graph"),
        ],#style={"width": "70vw"}
    )
        return content


if __name__ == "__main__":
    despachito.run_server(debug=True)
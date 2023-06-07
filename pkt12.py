from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from conn1 import get_df5
import dash_bootstrap_components as dbc
import numpy as np
from plotly.subplots import make_subplots
import dash


appkt12 = dash.Dash(__name__,title="PKT", external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/pkt12/')

PLOTLY_LOGO = "http://10.107.226.241/assets/caja.png"

contenidox = html.Div(id='page-content', children=[])
appkt12.layout = html.Div([dcc.Location(id="url"),contenidox])

@appkt12.callback([Output("table1","data"),Output("table1","columns"),Output("graph1","figure")],[Input('dFecha','value'),Input('dEstado','value'),Input('dOrdenes','value'), Input('dWHSE','value')])
def updaTable(ifechas, iestados, iordenes, iwhse):
    dff=get_df5()
    dfa = dff[(dff.FECHA_SALIDA.isin(ifechas)) & (dff.ESTADO.isin(iestados)) & (dff.TIPO_ORDEN.isin(iordenes)) & (dff.WHSE.isin(iwhse))]
    etasii = dfa.FECHA_SALIDA.unique()
    ordenesii = dfa.TIPO_ORDEN.unique()
    whses =dfa.WHSE.unique()
    dfetasii = dfa.groupby('FECHA_SALIDA')['QTY'].sum()
    dfordenesii = dfa.groupby('TIPO_ORDEN')['QTY'].sum()
    dfwhses = dfa.groupby('WHSE')['QTY'].sum()
    fig8 = make_subplots(
    rows=1, cols=3,
    specs=[
           [{"type": "domain"},{"type": "domain"}, {'type':'xy'}]],
    )
    fig8.add_trace(go.Pie(labels=ordenesii, values=dfordenesii[ordenesii], name="Ordenes"), 1, 1)
    fig8.add_trace(go.Pie(labels=whses, values=dfwhses[whses], name="Whse"), 1, 2)
    fig8.add_trace(go.Bar(x=etasii, y=dfetasii[etasii], name='Fechas'),1,3)
    dfffq = dfa.pivot_table( values = "QTY",index = ["FECHA_SALIDA","WHSE"], columns = "ESTADO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    
    return dfffq.to_dict("records"), [{"name": c, "id": c} for c in dfffq.columns if c != 'id'], fig8

@appkt12.callback([Output("output-table","children"),Input("table1", "active_cell"), State('dFecha','value'),State('dEstado','value'),State('dOrdenes','value'), State('dWHSE','value')])
def cell_clicked(active_cell, fechaj, estadoj, ordenj, whsej):
    dff=get_df5()
    if active_cell is None:
        return no_update
    dfb = dff[(dff.FECHA_SALIDA.isin(fechaj)) & (dff.ESTADO.isin(estadoj)) & (dff.TIPO_ORDEN.isin(ordenj))& (dff.WHSE.isin(whsej))  ]
    row = active_cell["row"]
    col = active_cell["column_id"]
    dfc = dfb.pivot_table( values = "QTY",index = ["FECHA_SALIDA","WHSE"], columns = "ESTADO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    fechaa= dfc.at[row, dfc.columns[0]]
    fecha2= dfc.at[row, dfc.columns[1]]
    print('cumpli',col)
    print(fechaa)

    if active_cell["column_id"]=="Total" and fechaa=='Total':
        fig1=dash_table.DataTable(
        id="table2",
        columns=[{"name": c, "id": c} for c in dfb.columns],
        data=dfb.to_dict("records"),
        page_size=50,
        sort_action="native",
        filter_action="native",
        sort_mode="multi",
        column_selectable="multi",
        row_selectable="multi",
        style_header={
                        'backgroundColor': 'rgb(72,118,178)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(217,227,241)',
                        'color': 'rgb(72,118,178)'
                    },
        editable=True,
        export_format='xlsx',
        export_headers='display',
        merge_duplicate_headers=True
        ),
        return fig1
    elif active_cell["column_id"]=="Total":
        fig1=dash_table.DataTable(
        id="table2",
        columns=[{"name": c, "id": c} for c in dfb[(dfb['FECHA_SALIDA']==fechaa)&(dfb['WHSE'] == fecha2)].columns],
        data=dfb[(dfb['FECHA_SALIDA']==fechaa)&(dfb['WHSE'] == fecha2)].to_dict("records"),
        page_size=50,
        sort_action="native",
        filter_action="native",
        sort_mode="multi",
        column_selectable="multi",
        row_selectable="multi",
        style_header={
                        'backgroundColor': 'rgb(72,118,178)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(217,227,241)',
                        'color': 'rgb(72,118,178)'
                    },
        editable=True,
        export_format='xlsx',
        export_headers='display',
        merge_duplicate_headers=True
        ),
        return fig1
    elif fechaa=='Total':
        fig1 = dash_table.DataTable(
            id="table2",
            columns=[{"name": c, "id": c} for c in dfb.columns],
            data= dfb[(dfb['ESTADO']== col)].to_dict("records"),
            page_size=50,
            sort_action="native",
            filter_action="native",
            sort_mode="multi",
            column_selectable="multi",
            row_selectable="multi",
            style_header={
                            'backgroundColor': 'rgb(72,118,178)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(217,227,241)',
                            'color': 'rgb(72,118,178)'
                        },
            editable=True,
            export_format='xlsx',
            export_headers='display',
            merge_duplicate_headers=True
            ),
        return fig1

    else:
        fig1=dash_table.DataTable(        
        id="table2",
        columns=[{"name": c, "id": c} for c in dfb.columns],
        data=dfb[(dfb['FECHA_SALIDA'] == fechaa)&(dfb['ESTADO']== col)&(dfb['WHSE'] == fecha2)].to_dict("records"),
        page_size=50,
        sort_action="native",
        filter_action="native",
        sort_mode="multi",
        column_selectable="multi",
        row_selectable="multi",
        style_header={
                        'backgroundColor': 'rgb(72,118,178)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(217,227,241)',
                        'color': 'rgb(72,118,178)'
                    },
        editable=True,
        export_format='xlsx',
        export_headers='display',
        merge_duplicate_headers=True
        ),
        return fig1

@appkt12.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    dff=get_df5()
    etas = dff.FECHA_SALIDA.unique()
    estados=dff.ESTADO.unique()
    ordenes=dff.TIPO_ORDEN.unique()
    dfff = dff.pivot_table( values = "QTY",index = ["FECHA_SALIDA","WHSE"], columns = "ESTADO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    long = dfff.shape[0]
    whses =dff.WHSE.unique()
    dfetasii = dff.groupby('FECHA_SALIDA')['QTY'].sum()
    dfordenesii = dff.groupby('TIPO_ORDEN')['QTY'].sum()
    dfwhses = dff.groupby('WHSE')['QTY'].sum()
    fig8 = make_subplots(
    rows=1, cols=3,
    specs=[
           [{"type": "domain"},{"type": "domain"}, {'type':'xy'}]],
     #subplot_titles=("Tipos ods","FECHAS")
    )
    fig8.add_trace(go.Pie(labels=ordenes, values=dfordenesii[ordenes], name="Ordenes"), 1, 1)
    fig8.add_trace(go.Pie(labels=whses, values=dfwhses[whses], name="Whse"), 1, 2)
    fig8.add_trace(go.Bar(x=etas, y=dfetasii[etas], name='Fechas'),1,3)
    
    content = html.Div(
    [
        html.Div(
            [
                html.H3("Ordenes", style={"textAlign":"center"}),
                html.Div([
                html.P('whse, fechas , estados'), 
                dcc.Dropdown(
                whses,
                whses,multi=True,placeholder="WHSE...",searchable=True, id='dWHSE'
                ),
                dcc.Dropdown(
                etas,
                etas,multi=True,placeholder="Fechas...",searchable=True,id='dFecha',style={'maxHeight': '40px', 'overflowY': 'auto'}
                ),
                dcc.Dropdown(
                estados,
                estados,multi=True,placeholder="Estados...",searchable=True,id='dEstado'
                ) ,  
                html.P('Ordenes'), 
                dcc.Dropdown(
                ordenes,
                ordenes,multi=True,placeholder="Ordenes...",searchable=True,id='dOrdenes'
                ),
                ]),
                html.Div([]),
                dcc.Graph(id='graph1',figure=fig8),
                dash_table.DataTable(
                    id="table1",
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
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(217,227,241)',
                        'color': 'rgb(72,118,178)'
                    },
                ),
            ],
        ),
        html.Div(id="output-graph"),
        html.Div(id="output-table"),
    ],#style={"width": "70vw"}
    )
    return content


if __name__ == "__main__":
    appkt12.run_server(debug=True)
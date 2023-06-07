from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from conn1 import get_df8
import dash_bootstrap_components as dbc
import numpy as np
from plotly.subplots import make_subplots
import dash

applm = dash.Dash(__name__,title="LastMile", external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/ultimamilla/')
PLOTLY_LOGO = "http://10.107.226.241/assets/caja.png"

contenidox = html.Div(id='page-content',children=[])
applm.layout = html.Div([dcc.Location(id="url"), contenidox])

@applm.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    dff=get_df8()

    estados= dff.ESTADO.unique()
    locales=dff.LOCALDESPA.unique()
    etas = dff.ETA_CLIENTE.unique()
    flujos = dff.FLUJO.unique()
    dfff = dff.pivot_table( values = "QTY",index = ["DESC_EMP"], columns = "ESTADO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    long = dfff.shape[0]
 

    dfEstado = dff.groupby('ESTADO')['QTY'].sum()
    dflocaldespa = dff.groupby('LOCALDESPA')['QTY'].sum()
    dfEta = dff.groupby('ETA_CLIENTE')['QTY'].sum()
    

    fig8 = make_subplots(
        rows=1, cols=3,
        specs=[
            [{"type": "domain"}, {'type':'domain'}, {'type':'domain'}]],
        subplot_titles=("Estado","CD", "ETAs")
    )

    fig8.add_trace(go.Pie(labels=estados, values=dfEstado[estados], name="Estado"), 1, 1)
    fig8.add_trace(go.Pie(labels=locales, values=dflocaldespa[locales], name="Locales"), 1, 2)
    fig8.add_trace(go.Pie(labels=etas, values=dfEta[etas], name="Etas"), 1, 3)
  
    content = html.Div(
    [
        html.Div(
            [
                html.H3("Seguimiento Última milla", style={"textAlign":"center"}),
                html.Div([
               
                html.P('Locales, estados, flujo'), 
                dcc.Dropdown(
                locales,
                locales,multi=True,placeholder="Locales...",searchable=True,id='dLocal'
                ),
                dcc.Dropdown(
                estados,
                estados,multi=True,placeholder="Estados...",searchable=True,id='dEstado'
                ) ,
                dcc.Dropdown(
                flujos,
                flujos,multi=True,placeholder="Flujos...",searchable=True,id='dFlujo'
                ) ,
                 html.P('Fecha, Reciente'), 
                dcc.Dropdown(
                etas,
                etas,multi=True,placeholder="Fecha cliente...",searchable=True,id='dEtas'
                ),
               
                ]),
                dcc.Graph(id='graph1',figure=fig8),
            ],
        ),
        html.Div(id="output-graph"),
        
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
                    style_table={
                    'width': 'auto',
                    'overflowX': 'auto'
                    },
                    style_data_conditional=[
                    {
                        'if': {'column_id': c},
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'maxWidth': '300px',
                    } for c in dfff.columns if c != 'id'
                ],
                    filter_options={
                        "case": "insensitive",
                    },
                    style_header={
                        'backgroundColor': 'rgb(72,118,178)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(217,227,241)',
                        'color': 'rgb(72,118,178)'
                    },
                ), 
            html.Div(id="output-table"),
    ],#style={"width": "80vw"}
    )
    return content

@applm.callback([Output("table1","data"),Output("table1","columns"),Output("graph1","figure")],[Input('dLocal','value'),Input('dEstado','value'),Input('dEtas','value'),Input('dFlujo','value')])
def updaTable(local, iestado, ietas, iflujo):
    dff=get_df8()
    dfa = dff[(dff.LOCALDESPA.isin(local)) & (dff.ESTADO.isin(iestado)) & (dff.ETA_CLIENTE.isin(ietas)) &(dff.FLUJO.isin(iflujo))]
    estados= dfa.ESTADO.unique()
    locales=dfa.LOCALDESPA.unique()
    etas = dfa.ETA_CLIENTE.unique()
    flujos = dfa.FLUJO.unique()
    dfffq = dfa.pivot_table( values = "QTY",index = ["DESC_EMP"], columns = "ESTADO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    dfEstado = dfa.groupby('ESTADO')['QTY'].sum()
    dflocaldespa = dfa.groupby('LOCALDESPA')['QTY'].sum()
    dfEta = dfa.groupby('ETA_CLIENTE')['QTY'].sum()
    fig8 = make_subplots(
        rows=1, cols=3,
        specs=[
            [{"type": "domain"}, {'type':'domain'}, {'type':'domain'}]],
        subplot_titles=("Estado","CD", "ETAs")
    )

    fig8.add_trace(go.Pie(labels=estados, values=dfEstado[estados], name="Estado"), 1, 1)
    fig8.add_trace(go.Pie(labels=locales, values=dflocaldespa[locales], name="Locales"), 1, 2)
    fig8.add_trace(go.Pie(labels=etas, values=dfEta[etas], name="Etas"), 1, 3)
    

    return dfffq.to_dict("records"), [{"name": c, "id": c} for c in dfffq.columns if c != 'id'], fig8

@applm.callback([Output("output-table","children"),Input("table1", "active_cell"), State('dLocal','value'),State('dEstado','value'),State('dEtas','value'),State('dFlujo','value')])
def cell_clicked(active_cell, local, estado, eta,iflujo):
    dff=get_df8()
    if active_cell is None:
        return no_update
    dfb = dff[(dff.LOCALDESPA.isin(local)) & (dff.ESTADO.isin(estado)) & (dff.ETA_CLIENTE.isin(eta)) &(dff.FLUJO.isin(iflujo))]
    row = active_cell["row"]
    col = active_cell["column_id"]
    dfc = dfb.pivot_table(values = "QTY",index = ["DESC_EMP"], columns = "ESTADO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()

    fechaa= dfc.at[row, dfc.columns[0]]
   
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
            filter_options={
                        "case": "insensitive",
                    },
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
            columns=[{"name": c, "id": c} for c in dfb.columns],
            data=dfb[(dfb['DESC_EMP'] == fechaa)].to_dict("records"),
            page_size=50,
            sort_action="native",
            filter_action="native",
            sort_mode="multi",
            column_selectable="multi",
            row_selectable="multi",
            filter_options={
                        "case": "insensitive",
                    },
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
            data= dfb[(dfb['CUMPLIMIENTO']== col)].to_dict("records"),
            page_size=50,
            sort_action="native",
            filter_action="native",
            sort_mode="multi",
            column_selectable="multi",
            row_selectable="multi",
            filter_options={
                        "case": "insensitive",
                    },
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
        data=dfb[(dfb['DESC_EMP'] == fechaa)].to_dict("records"),
        page_size=50,
        sort_action="native",
        filter_action="native",
        sort_mode="multi",
        column_selectable="multi",
        row_selectable="multi",
        filter_options={
                        "case": "insensitive",
                    },
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

if __name__ == "__main__":
    applm.run_server(debug=True)
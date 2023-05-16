from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from conn1 import get_df6
import dash_bootstrap_components as dbc
import numpy as np
from plotly.subplots import make_subplots
import dash


appst = dash.Dash(__name__,title="Stock", external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/stock/')

PLOTLY_LOGO = "http://10.107.226.241/assets/caja.png"


sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src=PLOTLY_LOGO, style={"width": "4rem"}),
                html.H2("Menú"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("CLU")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-bar-chart"),
                        html.Span(" Despachos DD/C&C"),
                    ],
                    href="http://10.107.226.241:8050/clu",
                    active="partial",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-hourglass-end"),
                        html.Span(" Antiguedad"),
                    ],
                    href="http://10.107.226.241:8050/antiguedad/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-pie-chart"),
                        html.Span(" Stock100"),
                    ],
                    href="http://10.107.226.241:8050/stock/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-bar-chart"),
                        html.Span(" Traspasos"),
                    ],
                    href="http://10.107.226.241:8050/traspasos/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-users"),
                        html.Span(" Tracking"),
                    ],
                    href="http://10.107.226.241:8050/app2",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-tasks"),
                        html.Span(" Ordenes"),
                    ],
                    href="http://10.107.226.241:8050/pkt",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-truck"),
                        html.Span(" Despacho SameDay"),
                    ],
                    href="http://10.107.226.241:8050/sameday/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-spinner"),
                        html.Span(" Capacidades"),
                    ],
                    href="http://10.107.226.241:8050/capacidades/",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


contenidox = html.Div(id='page-content',className='content', children=[])
appst.layout = html.Div([dcc.Location(id="url"), sidebar,contenidox])
@appst.callback([Output("table1","data"),Output("table1","columns"),Output("graph1","figure")],[Input('dCds','value'),Input('dZonas','value'),Input('dDeptos','value')])
def updaTable(icds, izonas, ideptos):
    dff=get_df6()
    dfa = dff[(dff.CD.isin(icds)) & (dff.ZONA.isin(izonas)) & (dff.DEPTO.isin(ideptos))]
    cdii = dfa.CD.unique()
    deptoii = dfa.DEPTO.unique()
    dcdii = dfa.groupby('CD')['QTY'].sum()
    ddeptoii= dfa.groupby('DEPTO')['QTY'].sum()
    fig8 = make_subplots(
    rows=1, cols=2,
    specs=[
           [{"type": "domain"}, {'type':'xy'}]],
     subplot_titles=("CDs","Deptos")
    )
    fig8.add_trace(go.Pie(labels=cdii, values=dcdii[cdii], name="CD"), 1, 1)
    fig8.add_trace(go.Bar(x=deptoii, y=ddeptoii[deptoii], name='Deptos'),1,2)
    
    dfffq = dfa.pivot_table( values = "QTY",index = ["DEPTO"], columns = "TEMPORADA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    
    return dfffq.to_dict("records"), [{"name": c, "id": c} for c in dfffq.columns if c != 'id'], fig8

@appst.callback([Output("output-table","children"),Input("table1", "active_cell"), State('dCds','value'),State('dZonas','value'),State('dDeptos','value')])
def cell_clicked(active_cell, icds, izonas, ideptos):
    dff=get_df6()
    if active_cell is None:
        return no_update
    dfb = dff[(dff.CD.isin(icds)) & (dff.ZONA.isin(izonas)) & (dff.DEPTO.isin(ideptos))]
    row = active_cell["row"]
    col = active_cell["column_id"]
    dfc = dfb.pivot_table( values = "QTY",index = ["DEPTO"], columns = "TEMPORADA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    fechaa= dfc.at[row, dfc.columns[0]]
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
            data= dfb[(dfb['DEPTO']== fechaa)].to_dict("records"),
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
        columns=[{"name": c, "id": c} for c in dfb[(dfb['DEPTO'] == fechaa)].columns],
        data=dfb[(dfb['DEPTO'] == fechaa)].to_dict("records"),
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
        data=dfb[(dfb['DEPTO'] == fechaa)&(dfb['TEMPORADA']== col)].to_dict("records"),
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

@appst.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    dff=get_df6()
    cds = dff.CD.unique()
    zonas = dff.ZONA.unique()
    deptos=dff.DEPTO.unique()
    dfff = dff.pivot_table( values = "QTY",index = ["DEPTO"], columns = "TEMPORADA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    long = dfff.shape[0]
    dfcds = dff.groupby('CD')['QTY'].sum()
    dfdeptos = dff.groupby('DEPTO')['QTY'].sum()
    fig8 = make_subplots(
        rows=1, cols=2,
        specs=[
            [{"type": "domain"}, {'type':'xy'}]],
        subplot_titles=("CDs","Deptos")
    )
    fig8.add_trace(go.Pie(labels=cds, values=dfcds[cds], name="Ordenes"), 1, 1)
    fig8.add_trace(go.Bar(x=deptos, y=dfdeptos[deptos], name='Fechas'),1,2)
    content = html.Div(
    [
        html.Div(
            [
                html.H3("Stock local 100", style={"textAlign":"center"}),
                html.Div([
                
                html.P('CD'), 
                dcc.Dropdown(
                cds,
                cds,multi=True,placeholder="CDS...",searchable=True,id='dCds'
                ),
              
                
                html.P('Zonas, Deptos'), 
                dcc.Dropdown(
                zonas,
                zonas,multi=True,placeholder="Zonas...",searchable=True,id='dZonas',style={'maxHeight': '40px', 'overflowY': 'auto'}
                ),
                dcc.Dropdown(
                deptos,
                deptos,multi=True,placeholder="Deptos...",searchable=True,id='dDeptos',style={'maxHeight': '40px', 'overflowY': 'auto'}
                ) ,
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
            ],
        ),
        html.Div(id="output-graph"),
        html.Div(id="output-table"),
    ],style={"width": "70vw"}
)
    return content


if __name__ == "__main__":
    appst.run_server(debug=True)
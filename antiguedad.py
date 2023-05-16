from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from conn1 import get_df2
import dash_bootstrap_components as dbc
import numpy as np
import dash
from plotly.subplots import make_subplots

appa = dash.Dash(__name__,title="Antiguedad",external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/antiguedad/')

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



contenidox = html.Div(id='page-content',className='content', children=[ ])
appa.layout = html.Div([dcc.Location(id="url"),sidebar, contenidox])

@appa.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    dff=get_df2()
    origenes = dff.ORIGEN.unique()
    estatutes = dff.STATUS.unique()
    supervisores =dff.SUPERVISOR.unique()
    responsables=dff.RESPONSABLE.unique()
    zonas = dff.ZONA.unique()
    dfff = dff.pivot_table( values = "QTY",index = "MES", columns = "LEVEL", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    long = dfff.shape[0]

    dfrespon = dff.groupby('RESPONSABLE')['QTY'].sum()
    dfzona = dff.groupby('ZONA')['QTY'].sum()

    fig8 = make_subplots(
        rows=1, cols=2,
        specs=[
            [{"type": "domain"}, {'type':'xy'}]],
        subplot_titles=("Responsables","Zonas")
    )

    fig8.add_trace(go.Pie(labels=responsables, values=dfrespon[responsables], name="Responsables"), 1, 1)
    fig8.add_trace(go.Bar(x=zonas, y=dfzona[zonas], name='Zonas'),1,2)
    content = html.Div(
    [
        html.Div(
            [
                html.H3("Antiguedad local 100", style={"textAlign":"center"}),
                html.Div([
                dcc.RadioItems(['FECHA','RESPONSABLE'], 'RESPONSABLE', inline=True, id='radioGaga'),
                html.P('ORIGEN, STATUS'),
                dcc.Dropdown(
                origenes,
                origenes,multi=True,placeholder="ORIGEN...",searchable=True, id='dORIGEN'
                ), 
                dcc.Dropdown(
                estatutes,
                estatutes,multi=True,id='dSTATUS'
                ),
                html.P('SUPERVISOR, RESPONSABLE'), 
                dcc.Dropdown(
                supervisores,
                supervisores,multi=True,placeholder="SUPERVISOR...",searchable=True,id='dSUPERVISOR',style={'maxHeight': '40px', 'overflowY': 'auto'}
                ),
                dcc.Dropdown(
                responsables,
                responsables,multi=True,placeholder="RESPONSABLE...",searchable=True,id='dRESPONSABLE'
                )          
                ]),
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
    ],style={"width": "70vw"}
)
    return content

@appa.callback([Output("table","data"),Output("table","columns"),Output("table","page_size"),Output("graph1","figure")], [Input('radioGaga','value'),Input('dORIGEN','value'), Input('dSTATUS','value'), Input('dSUPERVISOR','value'), Input('dRESPONSABLE','value')])
def upTable(value,v_origen,v_status,v_supervisor,v_responsable):
    dff=get_df2()
    dfa = dff[(dff.ORIGEN.isin(v_origen)) & (dff.STATUS.isin(v_status)) & (dff.SUPERVISOR.isin(v_supervisor)) & (dff.RESPONSABLE.isin(v_responsable))]
    if(value=='RESPONSABLE'):
        dfff = dfa.pivot_table( values = "QTY",index = ["RESPONSABLE"], columns = ["ZONA"], aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    else:
        dfff = dfa.pivot_table( values = "QTY",index = ["MES"], columns = ["ZONA"], aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    responsables=dfa.RESPONSABLE.unique()
    zonas = dfa.ZONA.unique()
    dfrespon = dfa.groupby('RESPONSABLE')['QTY'].sum()
    dfzona = dfa.groupby('ZONA')['QTY'].sum()
    fig8 = make_subplots(
        rows=1, cols=2,
        specs=[
            [{"type": "domain"}, {'type':'xy'}]],
        subplot_titles=("Responsables","Zonas")
    )
    fig8.add_trace(go.Pie(labels=responsables, values=dfrespon[responsables], name="Responsables"), 1, 1)
    fig8.add_trace(go.Bar(x=zonas, y=dfzona[zonas], name='Zonas'),1,2)
    
    
    return dfff.to_dict("records"),[{"name": c, "id": c} for c in dfff.columns if c != 'id'],dfff.shape[0],fig8

@appa.callback(
    Output("output-graph", "children"), Input("table", "active_cell"),[State('radioGaga','value'),State('dORIGEN','value'), State('dSTATUS','value'), State('dSUPERVISOR','value'), State('dRESPONSABLE','value')]
)
def cell_clicked(active_cell,value,v_origen,v_status,v_supervisor,v_responsable):
    dff=get_df2()
    if active_cell is None:
        return no_update
    print(str(active_cell))
    dfa = dff[(dff.ORIGEN.isin(v_origen)) & (dff.STATUS.isin(v_status)) & (dff.SUPERVISOR.isin(v_supervisor)) & (dff.RESPONSABLE.isin(v_responsable))]
    print('NO')
    if(value=='FECHA'):
        ingresado = 'MES'
    else:
        ingresado='RESPONSABLE'
    row = active_cell["row"]
    print(f"row id: {row}")
    dfff = dfa.pivot_table( values = "QTY",index = ingresado, columns = "ZONA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    eta = dfff.at[row, dfff.columns[0]]
    print(eta)
    col = active_cell["column_id"]
    print(f"column id: {col}")
    print("---------------------")

    if active_cell["column_id"]=="Total" and eta=='Total':
            fig1=dash_table.DataTable(
            id="table2",
            columns=[{"name": c, "id": c} for c in dfa.columns],
            data=dfa.to_dict("records"),
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
        columns=[{"name": c, "id": c} for c in dfa[(dfa[ingresado]==eta)].columns],
        data=dfa[(dfa[ingresado]==eta)].to_dict("records"),
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
    elif eta=='Total':
        fig1 = dash_table.DataTable(
        id="table2",
        columns=[{"name": c, "id": c} for c in dfa[(dfa['ZONA']== col)].columns],
        data= dfa[(dfa['ZONA']== col)].to_dict("records"),
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
        otrodf = dfa[dfa[ingresado]==eta]
        fig1 = dash_table.DataTable(
        id="table2",
        columns=[{"name": c, "id": c} for c in otrodf[(otrodf['ZONA']== col)].columns],
        data= otrodf[(otrodf['ZONA']== col)].to_dict("records"),
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
    appa.run_server(debug=True)
from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from conn1 import capacidades
import dash_bootstrap_components as dbc
import numpy as np
import dash
from plotly.subplots import make_subplots

appcapa = dash.Dash(__name__,title="Capacidades",external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/capacidades/')

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
appcapa.layout = html.Div([dcc.Location(id="url"),sidebar, contenidox])

@appcapa.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    dff=capacidades()
    origenes = dff.ORIGEN.unique()
    meses = dff.MES.unique()
    parises =dff.PARIS.unique()
    dias=dff.DIA.unique()
    dfff = dff.pivot_table( values = "QTY",index = ["ORIGEN","CAP_TIPO"], columns = "SHIP_DATE", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    long = dfff.shape[0]
    dfasig = dff[dff['CAP_TIPO']=='ASIGNADO']
    dfasignada = dfasig.groupby('ORIGEN')['QTY'].sum()
    dfparises = dfasig.groupby('PARIS')['QTY'].sum()
    fig8 = make_subplots(
        rows=1, cols=2,
        specs=[
            [{"type": "domain"}, {'type':'domain'}]],
        subplot_titles=("Origenes","Flujos")
    )

    fig8.add_trace(go.Pie(labels=origenes, values=dfasignada[origenes], name="Origenes"), 1, 1)
    fig8.add_trace(go.Pie(labels=parises, values=dfparises[parises], name="Flujos"), 1, 2)
    content = html.Div(
    [
        html.Div(
            [
                html.H3("Capacidades CDs", style={"textAlign":"center"}),
                html.Div([
                dcc.RadioItems(['ORIGEN','SHIP_DATE'], 'ORIGEN', inline=True, id='radioGaga', style={'display': 'none'}),
                html.P('Origen, mes, días, flujo'),
                dcc.Dropdown(
                origenes,
                origenes,multi=True,placeholder="ORIGEN...",searchable=True, id='dORIGEN'
                ), 
                dcc.Dropdown(
                meses,
                meses,multi=True,id='dMESES'
                ),
                dcc.Dropdown(
                dias,dias,searchable=True,placeholder="dias..",multi=True,id='dDIAS',style={'maxHeight': '40px', 'overflowY': 'auto'}
                ),
                dcc.Dropdown(
                parises,
                parises,multi=True,id='dPARISES'
                ),      
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

@appcapa.callback([Output("table","data"),Output("table","columns"),Output("table","page_size"),Output("graph1","figure")], [Input('radioGaga','value'),Input('dORIGEN','value'), Input('dMESES','value'), Input('dDIAS','value'), Input('dPARISES','value')])
def upTable(value,v_origen,v_meses,v_dias,v_parises):
    dff=capacidades()
    dfa = dff[(dff.ORIGEN.isin(v_origen)) & (dff.MES.isin(v_meses)) & (dff.DIA.isin(v_dias)) & (dff.PARIS.isin(v_parises))]
    if(value=='ORIGEN'):
        dfff = dfa.pivot_table( values = "QTY",index = ["ORIGEN","CAP_TIPO"], columns = ["SHIP_DATE"], aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    else:
        dfff = dfa.pivot_table( values = "QTY",index = ["SHIP_DATE"], columns = ["UTILIZADO"], aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    origenes = dfa.ORIGEN.unique()
    meses = dfa.MES.unique()
    parises =dfa.PARIS.unique()
    dias=dfa.DIA.unique()
    dfff = dfa.pivot_table( values = "QTY",index = ["ORIGEN","CAP_TIPO"], columns = "SHIP_DATE", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    long = dfff.shape[0]
    dfasig = dfa[dfa['CAP_TIPO']=='ASIGNADO']
    dfasignada = dfasig.groupby('ORIGEN')['QTY'].sum()
    dfparises = dfasig.groupby('PARIS')['QTY'].sum()

    fig8 = make_subplots(
        rows=1, cols=2,
        specs=[
            [{"type": "domain"}, {'type':'domain'}]],
        subplot_titles=("Origenes","Flujos")
    )

    fig8.add_trace(go.Pie(labels=origenes, values=dfasignada[origenes], name="Origenes"), 1, 1)
    fig8.add_trace(go.Pie(labels=parises, values=dfparises[parises], name="Flujos"), 1, 2)
    
    
    return dfff.to_dict("records"),[{"name": c, "id": c} for c in dfff.columns if c != 'id'],dfff.shape[0],fig8

@appcapa.callback(
    Output("output-graph", "children"), Input("table", "active_cell"),[State('radioGaga','value'),State('dORIGEN','value'), State('dMESES','value'), State('dDIAS','value'), State('dPARISES','value')]
)
def cell_clicked(active_cell,value,v_origen,v_meses,v_dias,v_parises):
    dff=capacidades()
    if active_cell is None:
        return no_update
    print(str(active_cell))
    dfa = dff[(dff.ORIGEN.isin(v_origen)) & (dff.MES.isin(v_meses)) & (dff.DIA.isin(v_dias)) & (dff.PARIS.isin(v_parises))]
    print('NO')
    row = active_cell["row"]
    print(f"row id: {row}")
    if(value=="ORIGEN"):
        dfff = dfa.pivot_table( values = "QTY",index = ["ORIGEN","CAP_TIPO"], columns = "SHIP_DATE", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    else:
        dfff = dfa.pivot_table( values = "QTY",index = value, columns = "UTILIZADO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    eta = dfff.at[row, dfff.columns[0]]
    fecha2= dfff.at[row, dfff.columns[1]]
    print('la eta es:',eta)
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
        columns=[{"name": c, "id": c} for c in dfa[(dfa[value]==eta)&(dfa['CAP_TIPO'] == fecha2)].columns],
        data=dfa[(dfa[value]==eta)].to_dict("records"),
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
        #dfn=dfa[dfa['SHIP_DATE']==col],
        columns=[{"name": c, "id": c} for c in dfa[(dfa['SHIP_DATE']==col)&(dfa['CAP_TIPO'] == fecha2)].columns],
        data= dfa[dfa['SHIP_DATE']==col].to_dict("records"),
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
        #otrodf=dfa[(dfa['SHIP_DATE']==col)& (dfa['ORIGEN']==eta)],
        fig1 = dash_table.DataTable(
        id="table2",
        columns=[{"name": c, "id": c} for c in dfa[(dfa['SHIP_DATE']==col)&(dfa['CAP_TIPO'] == fecha2)& (dfa[value]==eta)].columns],
        data= dfa[(dfa['SHIP_DATE']==col)& (dfa[value]==eta)].to_dict("records"),
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
    appcapa.run_server(debug=True)
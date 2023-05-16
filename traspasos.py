from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
from conn1 import get_df3
import dash_bootstrap_components as dbc
import numpy as np
import dash

apptr = dash.Dash(__name__,title="Traspasos", external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/traspasos/')
PLOTLY_LOGO = "http://10.107.226.241/assets/caja.png"



sidebar = html.Div(
    [
        html.Div(
            [
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

apptr.layout = html.Div([dcc.Location(id="url"), sidebar,contenidox])

@apptr.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    dff=get_df3()
    cds = dff.CD.unique()
    instalaciones = dff.INSTALACION.unique()
    deptos=dff.DEPTO.unique()
    dfff = dff.pivot_table( values = "QTY",index = "F_COMPROMISO", columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    long = dfff.shape[0]
    columns=[{"name": c} for c in dfff.columns if c != 'id']
    columnas = len(dfff.columns)-1
    totalY =[]
    totalX=[]
    con=0

    content = html.Div(
    [
        html.Div(
            [
                html.H3("Traspasos local 100", style={"textAlign":"center"}),
                dcc.RadioItems(['FECHA','OPERACION','INSTALACION'], 'FECHA', inline=True, id='radioGaga'),
                html.Div([
                html.P('CD'),
                dcc.Dropdown(
                cds,
                cds,multi=True,placeholder="CD...",searchable=True, id='dCD'
                ), 
                html.P('DEPTO, INSTALACION'), 
                dcc.Dropdown(
                deptos,
                deptos,multi=True,placeholder="DEPTO...",searchable=True,id='dDepto',style={'maxHeight': '40px', 'overflowY': 'auto'}
                ),
                dcc.Dropdown(
                instalaciones,
                instalaciones,multi=True,placeholder="INSTALACION...",searchable=True,id='dInstalacion',style={'maxHeight': '40px', 'overflowY': 'auto'}
                )            
                ]),
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
            #style={"margin": 50},
            #className="five columns"
        ),
        html.Div(id="output-graph"),
    ],style={"width": "80vw"}
    #className="row"
    )

    return content

@apptr.callback([Output("table","data"),Output("table","columns"),Output("table","page_size")], [Input('radioGaga','value'),Input('dCD','value'), Input('dDepto','value'), Input('dInstalacion','value')])
def upTable(value, arcd,ardepto,arinstalacion):
    dff=get_df3()
    print(value)
    dfa = dff[(dff.CD.isin(arcd)) & (dff.DEPTO.isin(ardepto)) & (dff.INSTALACION.isin(arinstalacion))]
    if(value=='FECHA'):
        print('xfecha')
        dfff = dfa.pivot_table( values = "QTY",index = "F_COMPROMISO", columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
        return dfff.to_dict("records"),[{"name": c, "id": c} for c in dfff.columns if c != 'id'],dfff.shape[0]
    elif(value=='OPERACION'):
        print('opeparis')
        dfff = dfa.pivot_table( values = "QTY",index = "OPERACION", columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
        return dfff.to_dict("records"),[{"name": c, "id": c} for c in dfff.columns if c != 'id'],dfff.shape[0]
    elif(value=='INSTALACION'):
        print('instalacion')
        dfff = dfa.pivot_table( values = "QTY",index = "INSTALACION", columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
        return dfff.to_dict("records"),[{"name": c, "id": c} for c in dfff.columns if c != 'id'],dfff.shape[0]

@apptr.callback(
    Output("output-graph", "children"), Input("table", "active_cell"),[State('radioGaga','value'),State('dCD','value'), State('dDepto','value'), State('dInstalacion','value')]
)
def cell_clicked(active_cell, value, arcd,ardepto,arinstalacion):
    dff=get_df3()
    if active_cell is None:
        return no_update
    print(value)
    print(str(active_cell))
    dfa = dff[(dff.CD.isin(arcd)) & (dff.DEPTO.isin(ardepto)) & (dff.INSTALACION.isin(arinstalacion))]
    if(value=='FECHA'):
        print('xfecha')
        ingresado = 'F_COMPROMISO'
        row = active_cell["row"]
        print(f"row id: {row}")
        dfff = dfa.pivot_table( values = "QTY",index = ingresado, columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
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
        elif eta=='Total':
            fig1 = dash_table.DataTable(
            id="table2",
            columns=[{"name": c, "id": c} for c in dfa[(dfa['AREA']== col)].columns],
            data= dfa[(dfa['AREA']== col)].to_dict("records"),
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
            columns=[{"name": c, "id": c} for c in dfa[(dfa[ingresado] == eta)].columns],
            data=dfa[(dfa[ingresado]== eta)].to_dict("records"),
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
            columns=[{"name": c, "id": c} for c in dfa[(dfa[ingresado] == eta)&(dfa['AREA']== col)].columns],
            data=dfa[(dfa[ingresado]== eta)&(dfa['AREA']== col)].to_dict("records"),
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
    elif(value=='OPERACION'):
        print('opeparis')
        row = active_cell["row"]
        print(f"row id: {row}")
        dfff = dfa.pivot_table( values = "QTY",index = value, columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
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
        elif eta=='Total':
            fig1 = dash_table.DataTable(
            id="table2",
            columns=[{"name": c, "id": c} for c in dfa[(dfa['AREA']== col)].columns],
            data= dfa[(dfa['AREA']== col)].to_dict("records"),
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
            columns=[{"name": c, "id": c} for c in dfa[(dfa[value] == eta)].columns],
            data=dfa[(dfa[value]== eta)].to_dict("records"),
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
            columns=[{"name": c, "id": c} for c in dfa[(dfa[value] == eta)&(dfa['AREA']== col)].columns],
            data=dfa[(dfa[value]== eta)&(dfa['AREA']== col)].to_dict("records"),
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
    elif(value=='INSTALACION'):
        print('instalacion')
        row = active_cell["row"]
        print(f"row id: {row}")
        dfff = dfa.pivot_table( values = "QTY",index = value, columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
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
        elif eta=='Total':
            fig1 = dash_table.DataTable(
            id="table2",
            columns=[{"name": c, "id": c} for c in dfa[(dfa['AREA']== col)].columns],
            data= dfa[(dfa['AREA']== col)].to_dict("records"),
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
            columns=[{"name": c, "id": c} for c in dfa[(dfa[value] == eta)].columns],
            data=dfa[(dfa[value]== eta)].to_dict("records"),
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
            columns=[{"name": c, "id": c} for c in dfa[(dfa[value] == eta)&(dfa['AREA']== col)].columns],
            data=dfa[(dfa[value]== eta)&(dfa['AREA']== col)].to_dict("records"),
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
    apptr.run_server(debug=True)
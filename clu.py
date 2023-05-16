from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
from conn1 import get_df7
import dash_bootstrap_components as dbc
import numpy as np
import dash


#appc = dash.Dash(__name__,title="CLU", external_stylesheets=[dbc.themes.MORPH],requests_pathname_prefix='/clu/')
appc = dash.Dash(__name__,title="CLU", external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/clu/')
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
contenidox = html.Div(id='page-content',className='content',children=[])
appc.layout = html.Div([dcc.Location(id="url"), sidebar,contenidox])


@appc.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    dff=get_df7()
    cds = dff.CD.unique()
    fechas = dff.FECHA_COMPROMISO.unique()
    flujos=dff.FLUJO.unique()
    tipos=dff.TIPO_OD.unique()
    tipoolas=dff.TIPO_OLA.unique()
    retiras=dff.RETIRA.unique()
    especiales =dff.ESPECIAL.unique()
    olas = dff.NRO_OLA.unique()
    dfff = dff.pivot_table( values = "QTY",index = "FECHA_COMPROMISO", columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    long = dfff.shape[0]
    content = html.Div(
    [
        html.Div(
            [
                html.H3("Control Logistico Unificado", style={"textAlign":"center"}),
                dcc.RadioItems(['FECHA', 'OPERACION','REGION'], 'FECHA', inline=True, id='radioGaga'),
                html.Div([
                html.P('CD, ETA'),
                dcc.Dropdown(
                cds,
                cds,multi=True,placeholder="CD...",searchable=True, id='dCD'
                ), 
                dcc.Dropdown(
                fechas,
                fechas,multi=True,id='dFecha'
                ),
                html.P('TIPO OD, FLUJO, TIPO OLA'), 
                dcc.Dropdown(
                tipos,
                tipos,multi=True,placeholder="TIPO OD...",searchable=True,id='dTipood'
                ),
                dcc.Dropdown(
                flujos,
                flujos,multi=True,placeholder="FLUJO...",searchable=True,id='dFlujo'
                ),
                dcc.Dropdown(
                tipoolas,
                tipoolas,multi=True,placeholder="TIPO OLA...",searchable=True,id='dTipoola'
                ),
                dcc.Dropdown(
                olas,
                olas,multi=True,placeholder="OLA...",searchable=True,id='dOla',style={'maxHeight': '40px', 'overflowY': 'auto'}
                ),
                html.P('RETIRA'), 
                dcc.Dropdown(
                retiras,
                retiras,multi=True,placeholder="RETIRA...",searchable=True,id='dRetira'
                ),
                html.P('ESPECIAL'), 
                dcc.Dropdown(
                especiales,
                especiales,multi=True,placeholder="ESPECIAL...",searchable=True,id='dEspecial'
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
        ),
        html.Div(id="output-graph"),
    ],style={"width": "100vw"}
    )
    return content


@appc.callback([Output("table","data"),Output("table","columns"),Output("table","page_size")], [Input('radioGaga','value'),Input('dCD','value'), Input('dFecha','value'), Input('dTipood','value'), Input('dFlujo','value'),Input('dTipoola','value'),Input('dRetira','value'),Input('dEspecial','value'),Input('dOla','value')])
def upTable(value, arcd,arfecha,artod,arflujo,artola,arret,aresp,iolas):
    dff=get_df7()
    print(value)
    dfa = dff[(dff.CD.isin(arcd)) & (dff.FECHA_COMPROMISO.isin(arfecha)) & (dff.TIPO_OD.isin(artod)) & (dff.FLUJO.isin(arflujo)) & (dff.TIPO_OLA.isin(artola)) & (dff.RETIRA.isin(arret)) & (dff.ESPECIAL.isin(aresp))& (dff.NRO_OLA.isin(iolas))]
    if(value=='FECHA'):
        print('xfecha')
        dfff = dfa.pivot_table( values = "QTY",index = "FECHA_COMPROMISO", columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
        return dfff.to_dict("records"),[{"name": c, "id": c} for c in dfff.columns if c != 'id'],dfff.shape[0]
    elif(value=='OPERACION'):
        print('opeparis')
        dfff = dfa.pivot_table( values = "QTY",index = "OPERACION", columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
        return dfff.to_dict("records"),[{"name": c, "id": c} for c in dfff.columns if c != 'id'],dfff.shape[0]
    elif(value=='REGION'):
        print('region')
        dfff = dfa.pivot_table( values = "QTY",index = "REGION", columns = "AREA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
        return dfff.to_dict("records"),[{"name": c, "id": c} for c in dfff.columns if c != 'id'],dfff.shape[0]

@appc.callback(
    Output("output-graph", "children"), Input("table", "active_cell"),[State('radioGaga','value'),State('dCD','value'), State('dFecha','value'), State('dTipood','value'), State('dFlujo','value'),State('dTipoola','value'),State('dRetira','value'),State('dEspecial','value'),State('dOla','value')]
)
def cell_clicked(active_cell, value, arcd,arfecha,artod,arflujo,artola,arret,aresp,iolas):
    dff=get_df7()
    if active_cell is None:
        return no_update
    
    print(value)
    print(str(active_cell))
    dfa = dff[(dff.CD.isin(arcd)) & (dff.FECHA_COMPROMISO.isin(arfecha)) & (dff.TIPO_OD.isin(artod)) & (dff.FLUJO.isin(arflujo)) & (dff.TIPO_OLA.isin(artola)) & (dff.RETIRA.isin(arret)) & (dff.ESPECIAL.isin(aresp))& (dff.NRO_OLA.isin(iolas))]
    if(value=='FECHA'):
        print('xfecha')
        ingresado = 'FECHA_COMPROMISO'
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
    elif(value=='REGION'):
        print('region')
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

if __name__ == "__main__":
    appc.run_server(debug=True)
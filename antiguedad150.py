from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from conn2 import get_df2
import dash_bootstrap_components as dbc
import numpy as np
import dash
from plotly.subplots import make_subplots

appa150 = dash.Dash(__name__,title="Antiguedad",external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/antiguedad150/')

PLOTLY_LOGO = "http://10.107.226.241/assets/caja.png"



contenidox = html.Div(id='page-content', children=[ ])
appa150.layout = html.Div([dcc.Location(id="url"), contenidox])

@appa150.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    dff=get_df2()
    origenes = dff.ORIGEN_ASN.unique()
    estatutes = dff.STATUS.unique()
    zonas = dff.ZONA.unique()
    dfff = dff.pivot_table( values = "QTY",index = "MES", columns = "ZONA", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    long = dfff.shape[0]

    dfrespon = dff.groupby('ORIGEN_ASN')['QTY'].sum()
    dfzona = dff.groupby('ZONA')['QTY'].sum()

    fig8 = make_subplots(
        rows=1, cols=2,
        specs=[
            [{"type": "domain"}, {'type':'xy'}]],
        subplot_titles=("Origenes","Zonas")
    )

    fig8.add_trace(go.Pie(labels=origenes, values=dfrespon[origenes], name="Origen"), 1, 1)
    fig8.add_trace(go.Bar(x=zonas, y=dfzona[zonas], name='Zonas'),1,2)
    content = html.Div(
    [
        html.Div(
            [
                html.H3("Antiguedad local 150", style={"textAlign":"center"}),
                html.Div([
                html.P('ORIGEN, STATUS'),
                dcc.Dropdown(
                origenes,
                origenes,multi=True,placeholder="ORIGEN...",searchable=True, id='dORIGEN'
                ), 
                dcc.Dropdown(
                estatutes,
                estatutes,multi=True,id='dSTATUS'
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
    ],#style={"width": "70vw"}
)
    return content

@appa150.callback([Output("table","data"),Output("table","columns"),Output("table","page_size"),Output("graph1","figure")], [Input('dORIGEN','value'), Input('dSTATUS','value')])
def upTable(v_origen,v_status):
    dff=get_df2()
    dfa = dff[(dff.ORIGEN.isin(v_origen)) & (dff.STATUS.isin(v_status))]
    dfff = dfa.pivot_table( values = "QTY",index = ["MES"], columns = ["ZONA"], aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    origenes=dfa.ORIGEN_ASN.unique()
    zonas = dfa.ZONA.unique()
    dfrespon = dfa.groupby('ORIGEN_ASN')['QTY'].sum()
    dfzona = dfa.groupby('ZONA')['QTY'].sum()
    fig8 = make_subplots(
        rows=1, cols=2,
        specs=[
            [{"type": "domain"}, {'type':'xy'}]],
        subplot_titles=("Origenes","Zonas")
    )
    fig8.add_trace(go.Pie(labels=origenes, values=dfrespon[origenes], name="Origenes"), 1, 1)
    fig8.add_trace(go.Bar(x=zonas, y=dfzona[zonas], name='Zonas'),1,2)
    
    
    return dfff.to_dict("records"),[{"name": c, "id": c} for c in dfff.columns if c != 'id'],dfff.shape[0],fig8

@appa150.callback(
    Output("output-graph", "children"), Input("table", "active_cell"),[State('dORIGEN','value'), State('dSTATUS','value')]
)
def cell_clicked(active_cell,v_origen,v_status):
    dff=get_df2()
    if active_cell is None:
        return no_update
    print(str(active_cell))
    dfa = dff[(dff.ORIGEN_ASN.isin(v_origen)) & (dff.STATUS.isin(v_status))]
    print('NO')
    ingresado = 'MES'
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
        columns=[{"name": c, "id": c} for c in dfa[(dfa['MES']==eta)].columns],
        data=dfa[(dfa['MES']==eta)].to_dict("records"),
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
        otrodf = dfa[dfa['MES']==eta]
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
    appa150.run_server(debug=True)
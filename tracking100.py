import dash
import pandas as pd
import plotly.express as px
import requests
from dash import  dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go


PLOTLY_LOGO = "http://10.107.226.241/assets/caja.png"

apptra100 = dash.Dash(__name__, title="Dashboard",requests_pathname_prefix='/tracking100/',external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME])


contenidox = html.Div(id='page-content',children=[])

apptra100.layout = html.Div([dcc.Location(id="url"), contenidox])
@apptra100.callback(Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),[State(component_id='inUsr',component_property='value'),State(component_id='my-slider', component_property='value'),State(component_id='CDslctd', component_property='value')],prevent_initial_call=True)
def descargarUsr(n_clicks, usr,hrs,cds):
    bucle= usr.upper()
    buguard = bucle+'.csv'
    data1 = requests.get('http://10.107.226.241/tracking_labor_hr?horas={}'.format(hrs))
    jsondata1 = data1.json()
    #crear tabla
    columns=['QUANTITY'	,'F_MOD','DIA','HASTA','LOC','USUARIO','DESDE','FLUJO','HORA_','MINUTO','MIN_HORA','HORA','TRANSACTION_ID','TIPO','CD','ASN_ID','CONTAINER_ID','SHIPMENT_ID','NEW_CONTAINER_ID'	,'JORNADA','TRS','USR']
    dataTr=[]
    for col in jsondata1:
        for x in jsondata1[col]:
            dataTr.append([x['QUANTITY'],x['F_MOD'],x['DIA'],x['HASTA'],x['LOC'],x['USUARIO'],x['DESDE'],x['FLUJO'],x['HORA_'],x['MINUTO'],x['MIN_HORA'],x['HORA'],x['TRANSACTION_ID'],x['TIPO'],x['CD'],x['ASN_ID'],x['CONTAINER_ID'],x['SHIPMENT_ID'],x['NEW_CONTAINER_ID'],x['JORNADA'],x['TRS'],x['USR']])
    dfTr = pd.DataFrame(dataTr, columns=columns)
    if(bucle==''):
        bucle='todos'
        buguard='todos.csv'
        if(cds=='ALL'):
            df2 = dfTr
        else:
            df2 = dfTr[dfTr["CD"]==cds]
    else:        
        df2 = dfTr[dfTr["USUARIO"]==bucle]
    return dcc.send_data_frame(df2.to_csv, buguard)  
    #return dcc.send_data_frame(df2.to_excel,buguard, sheet_name=bucle)
        

@apptra100.callback([Output(component_id='output_user', component_property='children'),
Output(component_id='output_rut', component_property='children'),Output(component_id='output_nombre', component_property='children'),
Output(component_id='foto2',component_property='src'),Output(component_id='lostres',component_property='figure')],[Input(component_id='inUsr', component_property='value'),Input('my-slider', 'value')
],prevent_initial_call=True)

def actualizar(usuario,value):
    datax = requests.get('http://10.107.226.241/caras')
    jsondatax = datax.json()
    columnsx=['COL','USUARIO','RUT','NOMBRE','CARA']
    dataScarx=[]
    for col in jsondatax:
        for x in jsondatax[col]:
            dataScarx.append([col,x['USUARIO'],x['RUT'],x['NOMBRE'],x['CARA']])
    dfCar = pd.DataFrame(dataScarx, columns=columnsx)
    print(usuario)
    bucle=''
    bucle=usuario.upper()
    usuario11 = dfCar['USUARIO'] == bucle
    print(dfCar[usuario11])
    dfSalida=dfCar[usuario11]
    c = "".join(dfSalida['CARA'])
    #print(c)
    data1 = requests.get('http://10.107.226.241/tracking_labor_hr?horas={}'.format(value))
    jsondata1 = data1.json()
    #crear tabla
    columns=['QUANTITY'	,'F_MOD','DIA','HASTA','LOC','USUARIO','DESDE','FLUJO','HORA_','MINUTO','MIN_HORA','HORA','TRANSACTION_ID','TIPO','CD','ASN_ID','CONTAINER_ID','SHIPMENT_ID','NEW_CONTAINER_ID'	,'JORNADA','TRS','USR']
    dataTr=[]
    for col in jsondata1:
        for x in jsondata1[col]:
            dataTr.append([x['QUANTITY'],x['F_MOD'],x['DIA'],x['HASTA'],x['LOC'],x['USUARIO'],x['DESDE'],x['FLUJO'],x['HORA_'],x['MINUTO'],x['MIN_HORA'],x['HORA'],x['TRANSACTION_ID'],x['TIPO'],x['CD'],x['ASN_ID'],x['CONTAINER_ID'],x['SHIPMENT_ID'],x['NEW_CONTAINER_ID'],x['JORNADA'],x['TRS'],x['USR']])
    dfTr = pd.DataFrame(dataTr, columns=columns)
    df2 = dfTr[dfTr["USUARIO"]==bucle]
    filasN = df2.shape[0]/value
    filaNN = int(filasN)
    fig81 = make_subplots(
    rows=1, cols=3,
    specs=[
           [{"type": "domain"}, {}, {}]],
    subplot_titles=("","Tipo transacción", "Zona trabajo"))
    
    fig81.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = filaNN,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': ''+bucle+'', 'font': {'size': 24}},
        delta = {'reference': 200, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'axis': {'range': [None, 400], 'tickwidth': 2, 'tickcolor': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bar': {'color': "darkblue"},
            'bordercolor': "gray",
            'threshold': {
                'line': {'color': "red", 'width': 1},
                'thickness': 0.75,
                'value': 390},
            'steps': [
                {'range': [0, 200], 'color': 'cyan'},
                {'range': [200, 380], 'color': 'royalblue'},
                {'range': [0, filaNN], 'color': 'darkblue','thickness': 0.25 }
                ]   
                }),
              row=1, col=1)
    fig81.add_trace(go.Scatter(x=df2['F_MOD'], y=df2['TIPO'], mode="markers"),
              row=1, col=2)
    fig81.add_trace(go.Scatter(x=df2['F_MOD'], y=df2['LOC'], mode="markers"),
              row=1, col=3)
    fig81.update_layout(height=280,showlegend=False,template='seaborn',width=1200)
    return dfSalida['USUARIO'], dfSalida['RUT'],dfSalida['NOMBRE'],c, fig81
@apptra100.callback([Output(component_id='output_container', component_property='children'),
Output(component_id='trGraph_',component_property='figure'),
Output(component_id='znGraph_',component_property='figure')],[Input(component_id='CDslctd', component_property='value'),Input('my-slider', 'value')
])
def upgrade_graph(CDslctd,value):

    data1 = requests.get('http://10.107.226.241/tracking_labor_hr?horas={}'.format(value))
    jsondata1 = data1.json()
    #crear tabla
    columns=['QUANTITY'	,'F_MOD','DIA','HASTA','LOC','USUARIO','DESDE','FLUJO','HORA_','MINUTO','MIN_HORA','HORA','TRANSACTION_ID','TIPO','CD','ASN_ID','CONTAINER_ID','SHIPMENT_ID','NEW_CONTAINER_ID'	,'JORNADA','TRS','USR']
    dataTr=[]
    for col in jsondata1:
        for x in jsondata1[col]:
            dataTr.append([x['QUANTITY'],x['F_MOD'],x['DIA'],x['HASTA'],x['LOC'],x['USUARIO'],x['DESDE'],x['FLUJO'],x['HORA_'],x['MINUTO'],x['MIN_HORA'],x['HORA'],x['TRANSACTION_ID'],x['TIPO'],x['CD'],x['ASN_ID'],x['CONTAINER_ID'],x['SHIPMENT_ID'],x['NEW_CONTAINER_ID'],x['JORNADA'],x['TRS'],x['USR']])
    dfTr = pd.DataFrame(dataTr, columns=columns)

    print(CDslctd)
    print(type(CDslctd))
    container = "El CD elegido fue: {}".format(CDslctd)
    if (CDslctd=="ALL"):
        df2 = dfTr.copy()
        figO = px.scatter(df2, x="F_MOD", y="USUARIO",title="Gráfico por tipo de transacción",color='TIPO',height=1400,width=1200,template='seaborn')
        figA = px.scatter(df2, x="F_MOD", y="USR",title="Gráfico por zona",color='LOC', height=1400,width=1200,template='seaborn')
    elif  CDslctd=="CD2":
        df2 = dfTr[dfTr["CD"]==CDslctd]
        figO = px.scatter(df2, x="F_MOD", y="USUARIO", title="TR por Tipo",color='TIPO', height=1400,width=1200 ,template='seaborn')
        figA = px.scatter(df2, x="F_MOD", y="USR", title="TR por zona",color='LOC', height=1400,width=1200 ,template='seaborn')
        figA = figA.update_yaxes(autorange="reversed")
    elif CDslctd=="CD1":
        df2 = dfTr[dfTr["CD"]==CDslctd]
        figO = px.scatter(df2, x="F_MOD", y="USUARIO", title="TR por Tipo",color='TIPO', height=1400,width=1200 ,template='seaborn')
        figA = px.scatter(df2, x="F_MOD", y="USR", title="TR por zona",color='LOC', height=1400,width=1200 ,template='seaborn')
        figA = figA.update_yaxes(autorange="reversed")
    else:
        df2 = dfTr[dfTr["CD"]==CDslctd]
        figO = px.scatter(df2, x="F_MOD", y="USUARIO", color="TIPO",title="TR por Tipo", height=1400,width=1200 ,template='seaborn')
        figA = px.scatter(df2, x="F_MOD", y="USR", color="LOC",title="TR por zona", height=1400,width=1200,template='seaborn')
        figA = figA.update_yaxes(autorange="reversed")
    df2=df2
    return container, figO, figA
@apptra100.callback(
    Output('slider-output-container', 'children'),
    Input('my-slider', 'value'))
def update_output(value):
    return 'Has seleccionado las últimas {}'.format(value) +' horas'

maindiv = html.Div(
    id="trGraph",
    children=[
        html.Div([
        html.H1(children="Análisis TR",),
        html.P(
            children="Analiza las transacciones realizadas"
            " por el personal que marcó ingreso en huellero"
            " en un lapso determinado", className="lead"
        ),
        dcc.Graph(
            figure={}
        )]), 
    ]
)

@apptra100.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    
    fig8 = make_subplots(
        rows=1, cols=3,
        specs=[
            [{"type": "domain"}, {}, {}]],
        subplot_titles=("","Tipo transacción ejemplo", "Zona trabajo ejemplo")
    )

    fig8.add_trace(go.Indicator(
        mode = "gauge+number",
        value = 0,
        domain = {'x': [0, 1], 'y': [0, 1]}),
                row=1, col=1)
    fig8.add_trace(go.Scatter(x=[1,2,3,4,5], y=[4,3,5,1,1], mode="markers"),
                row=1, col=2)
    fig8.add_trace(go.Scatter(x=[2,3,2,0], y=[1,2,1,1], mode="markers"),
                row=1, col=3)

    fig8.update_layout(height=270, showlegend=False,template='seaborn',width=1200)

    content=html.Div([
    html.H1("Cuadro de mando", style={'text-aling':'center'}),
    html.Div([
    dcc.Slider(1, 24, 1,
               value=1,
               id='my-slider', className='dbc'
    ),
    html.Div(id='slider-output-container')
    ]),
    dcc.Dropdown(id="CDslctd",
    options=[
        {"label":"CD2", "value":"CD2"},
        {"label":"CD1", "value":"CD1"},
        {"label":"Despacho", "value":"C&C"},
        {"label":"todos los CD", "value":"ALL"}],
    multi=False,
    value="ALL",
    style={"width":"40%"}
    ),
    html.Div(id='output_container', children=[]),
    html.Br(),
    html.Div([
        html.Div(id='target'),
        dcc.Input(id='inUsr',placeholder='Ingrese usuario', type='text', value=''),
        html.Div(id='output_user', children=[]),
        html.Div(id='output_rut', children=[]),
        html.Div(id='output_nombre', children=[]),
        html.Img(id='foto2', src='',alt='SinFoto', height=60,width=60),
        html.Button("Descargar CSV", id="btn_xlsx"),
        dcc.Download(id="download-dataframe-xlsx"),
        dcc.Graph(id='lostres', figure=fig8)
    ],className="graph__container"),
    dcc.Graph(id='trGraph_',figure={}),
    dcc.Graph(id='znGraph_',figure={}),
    
    ] ,className="container")
    return content


if __name__ == "__main__":
    apptra100.run_server(debug=True)
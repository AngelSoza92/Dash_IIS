import dash
import pandas as pd
import plotly.express as px
import requests
from dash import  dcc,ctx, html, Input, Output

external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'C:/Users/angel/OneDrive/compartida/PP/dashboard/ollie.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app2 = dash.Dash(__name__, title="Dashboard_1001",requests_pathname_prefix='/otraprueba/',external_scripts=external_scripts,external_stylesheets=external_stylesheets)
#server = app2.server

datax = requests.get('http://10.107.226.241/caras')
jsondatax = datax.json()
columnsx=['COL','USUARIO','RUT','NOMBRE','CARA']
dataScarx=[]
for col in jsondatax:
    for x in jsondatax[col]:
        dataScarx.append([col,x['USUARIO'],x['RUT'],x['NOMBRE'],x['CARA']])

dfCar = pd.DataFrame(dataScarx, columns=columnsx)


data1 = requests.get('http://10.107.226.241/tracking_labor2.php')
jsondata1 = data1.json()
yy = pd.read_json('http://10.107.226.241/tracking_labor2.php')
#crear tabla
columns=['QUANTITY','F_MOD','DIA','HASTA','USUARIO','DESDE', 'FLUJO','HORA_','MINUTO','MIN_HORA','HORA','TRANSACTION_ID','TIPO','LOC','CD']

dataTr=[]
cUsr=[]
for col in jsondata1:
    for x in jsondata1[col]:
        dataTr.append([col,x['F_MOD'],x['DIA'],x['HASTA'],x['USUARIO'],x['DESDE'], x['FLUJO'],x['HORA_']*1,x['MINUTO'],x['MIN_HORA'],x['HORA']*1,x['TRANSACTION_ID'],x['TIPO'],x['LOC'],x['CD']])
        cUsr.append([col,x['USUARIO'],x['CD']])
dfTr = pd.DataFrame(dataTr, columns=columns)


csUsr=[]
cUsrCD1=[]
cUsrCD2=[]
cUsrDD=[]
acd1=[]
acd2=[]
add=[]
for usuario in cUsr:
    if usuario not in csUsr:
        csUsr.append(usuario)
alto = len(csUsr)

for usuario in yy['reporte']:
    if usuario['CD'] == 'CD1':
        cUsrCD1.append(usuario['USUARIO'])
    elif usuario['CD'] == 'CD2':
        cUsrCD2.append(usuario['USUARIO'])
    else :
        cUsrDD.append(usuario['USUARIO'])
for u in cUsrCD1:
    if u not in acd1:
        acd1.append(u)
for us in cUsrCD2:
    if us not in acd2:
        acd2.append(us)
for usu in cUsrDD:
    if usu not in add:
        add.append(usu)

alto = len(csUsr)
print(alto)
altoCD1=len(acd1)
altoCD2=len(acd2)
altoDD=len(add)

fiPi = px.scatter(dfTr, x="F_MOD", y="USUARIO", color="TIPO",title="TR por tipo",height=alto*20+200,width=3400)
fiAlm = px.scatter(dfTr, x="F_MOD", y="USUARIO", color="LOC",title="TR por zona")
fiAlm = fiAlm.update_yaxes(autorange="reversed")

SIDEBAR_STYLE={
    "position":"fixed",
    "top":0,
    "left":0,
    "bottom":0,
    "width":"86rem",
    "padding":"2rem 1rem",
    "background-color":"#f8f9fa",
    "overflow":"scroll"
}
CONTENT_STYLE={
    "margin-left":"4rem",
    "margin-right":"2rem",
    "padding":"2rem 1 rem",
    "display":"inline-block"
}

dd=html.Div([
    html.H1("Dashboard web", style={'text-aling':'center'}),
    html.Div([
    dcc.Slider(0, 24, 3,
               value=3,
               id='my-slider'
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
        #html.Button(id='submit', type='submint', children='buscar'),
        html.Img(id='foto2', src='',alt='SinFoto', height=150,width=150),
        html.Div(id='output_user', children=[]),
        html.Div(id='output_rut', children=[]),
        html.Div(id='output_nombre', children=[]),
    ]),
    
    dcc.Graph(id='trGraph_',figure={}),
    dcc.Graph(id='znGraph_',figure={})
])

@app2.callback([Output(component_id='output_user', component_property='children'),
Output(component_id='output_rut', component_property='children'),Output(component_id='output_nombre', component_property='children'),
Output(component_id='foto2',component_property='src')],[Input(component_id='inUsr', component_property='value')
],prevent_initial_call=True)

def actualizar(usuario):
    print(usuario)
    bucle=''
    bucle=usuario.upper()
    usuario11 = dfCar['USUARIO'] == bucle
    print(dfCar[usuario11])
    dfSalida=dfCar[usuario11]
    c = "".join(dfSalida['CARA'])
    print(c)
    return dfSalida['USUARIO'], dfSalida['RUT'],dfSalida['NOMBRE'],c

df2 = dfTr.copy()
@app2.callback([Output(component_id='output_container', component_property='children'),
Output(component_id='trGraph_',component_property='figure'),
Output(component_id='znGraph_',component_property='figure')],[Input(component_id='CDslctd', component_property='value')
])
def upgrade_graph(CDslctd):
    print(CDslctd)
    print(type(CDslctd))
    container = "El CD elegido fue: {}".format(CDslctd)
    if (CDslctd=="ALL"):
        df2 = dfTr.copy()
        figO = px.scatter(df2, x="F_MOD", y="USUARIO",title="TR por Tipo",color='TIPO', height=alto*20+200,width=1000)
        figA = px.scatter(df2, x="F_MOD", y="USUARIO",title="TR por zona",color='LOC', height=alto*20+200,width=1000)
        figA = figA.update_yaxes(autorange="reversed")
        print(altoCD2)
    elif  CDslctd=="CD2":
        df2 = dfTr[dfTr["CD"]==CDslctd]
        figO = px.scatter(df2, x="F_MOD", y="USUARIO", title="TR por Tipo",color='TIPO', height=altoCD2*20+200,width=1000 )
        figA = px.scatter(df2, x="F_MOD", y="USUARIO", title="TR por zona",color='LOC', height=altoCD2*20+200,width=1000 )
        figA = figA.update_yaxes(autorange="reversed")
        print(altoCD2)
    elif CDslctd=="CD1":
        df2 = dfTr[dfTr["CD"]==CDslctd]
        figO = px.scatter(df2, x="F_MOD", y="USUARIO", title="TR por Tipo",color='TIPO', height=altoCD1*20+200,width=1000 )
        figA = px.scatter(df2, x="F_MOD", y="USUARIO", title="TR por zona",color='LOC', height=altoCD1*20+200,width=1000 )
        figA = figA.update_yaxes(autorange="reversed")
        print(altoCD1)
    else:
        df2 = dfTr[dfTr["CD"]==CDslctd]
        figO = px.scatter(df2, x="F_MOD", y="USUARIO", color="TIPO",title="TR por Tipo", height=altoDD*20+200,width=1000 )
        figA = px.scatter(df2, x="F_MOD", y="USUARIO", color="LOC",title="TR por zona", height=altoDD*20+200,width=1000 )
        figA = figA.update_yaxes(autorange="reversed")
        print(altoDD)
    df2=df2
    return container, figO, figA
@app2.callback(
    Output('slider-output-container', 'children'),
    Input('my-slider', 'value'))
def update_output(value):
    datatimeline = requests.get('http://10.107.226.241/tracking_labor_hr?horas={}'.format(value))
    return 'Has seleccionado las últimas {}'.format(value) +' horas'

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display.4"),
        html.Hr(),
        html.P("Deslizar", className="lead"),
    ],
    style=SIDEBAR_STYLE
)

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



app2.layout = html.Div([dd])

if __name__ == "__main__":
    app2.run_server(debug=True, port=8000)
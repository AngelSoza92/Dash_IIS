import dash
import pandas as pd
import plotly.express as px
import requests
from dash import  dcc,ctx, html, Input, Output

app = dash.Dash(__name__, title="Dashboard_100",requests_pathname_prefix='/Dashboard/')
server = app.server



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
#dfTr = dfTr.index.values
#dfTr = pd.to_datetime(dfTr)
dfTr = dfTr.sort_values('MIN_HORA')

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

fiPi = px.scatter(dfTr, x="HORA", y="USUARIO", color="TIPO",title="TR por tipo",height=alto*20+200,width=3400)
fiPi = fiPi.update_xaxes(scaleratio=1)
fiAlm = px.scatter(dfTr, x="HORA", y="USUARIO", color="LOC",title="TR por zona")
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
    html.H1("Dashboards web", style={'text-aling':'center'}),
    html.Div([
    dcc.Slider(0, 24, 3,
               value=3,
               id='my-slider'
    ),
    html.Div(id='slider-output-container')
]),
    dcc.Dropdown(id="CDslctd",
    options=[
        {"label":"sólo CD2", "value":"CD2"},
        {"label":"sólo CD1", "value":"CD1"},
        {"label":"sólo DD", "value":"C&C"},
        {"label":"todos los CD", "value":"ALL"}],
    multi=False,
    value="ALL",
    style={"width":"40%"}
    ),
    html.Div(id='output_container', children=[]),
    dcc.Dropdown(id="TRslctd",
    options=[
        {"label":"Todo", "value":"Todo"},
        {"label":"Picking", "value":"Picking"},
        {"label":"Empaque", "value":"Empaque"},
        {"label":"Pre despacho", "value":"Pre despacho"},
        {"label":"Carga", "value":"Carga"},
        {"label":"Consulta", "value":"Consulta"},
        {"label":"Recepcion", "value":"Recepcion"},
        {"label":"Almacenamiento", "value":"Almacenamiento"},
        {"label":"Ciclico", "value":"Ciclico"}
        ],
    multi=False,
    value="Todo",
    style={"width":"40%"}
    ),
    html.Div(id='output_container2', children=[]),
    html.Br(),
    html.Div([
        html.Div(id='target'),
        dcc.Input(id='inUsr',placeholder='Ingrese usuario', type='text', value=''),
        html.Button(id='submit', type='submint', children='buscar'),
    ]),
    
    dcc.Graph(id='trGraph_',figure={}),
    dcc.Graph(id='znGraph_',figure={})
])

df2 = dfTr.copy()

@app.callback([Output(component_id='output_container', component_property='children'),
Output(component_id='trGraph_',component_property='figure'),
Output(component_id='znGraph_',component_property='figure')],[Input(component_id='CDslctd', component_property='value'),Input(component_id='TRslctd', component_property='value')
],prevent_initial_call=True)
def upgrade_graph(CDslctd,TRslctd):
    option_slctd = CDslctd
    print(option_slctd)
    print(TRslctd)
    print(type(option_slctd))
    container = "El CD elegido fue: {}".format(option_slctd)," la TR elegida fue: {}".format(TRslctd)
    if (option_slctd=="ALL" and TRslctd=="Todo"):
        df2 = dfTr.copy()
        figO = px.scatter(df2, x="HORA", y="USUARIO",title="TR por Tipo", height=alto*20+200,width=1000)
        figA = px.scatter(df2, x="HORA", y="LOC",title="TR por zona", height=alto*20+200,width=1000)
        figA = figA.update_yaxes(autorange="reversed")
    elif(TRslctd=="Todo"):
        df2 = dfTr.copy()
        df2 = dfTr[dfTr["CD"]==option_slctd]
        figO = px.scatter(df2, x="HORA", y="USUARIO",title="TR por Tipo", height=alto*20+200,width=1000)
        figA = px.scatter(df2, x="HORA", y="LOC",title="TR por zona", height=alto*20+200,width=1000)
        figA = figA.update_yaxes(autorange="reversed")
    elif(option_slctd=="ALL"):
        df2 = dfTr.copy()
        df2 = df2[df2["TIPO"]==TRslctd]
        figO = px.scatter(df2, x="HORA", y="USUARIO", title="TR por Tipo", height=altoCD2*20+200,width=1000 )
        figA = px.scatter(df2, x="HORA", y="USUARIO", title="TR por zona", height=altoCD2*20+200,width=1000 )
        figA = figA.update_yaxes(autorange="reversed")
        print(altoCD2)
    elif  option_slctd=="CD2":
        df2 = dfTr[dfTr["CD"]==option_slctd]
        df2 = df2[df2["TIPO"]==TRslctd]
        figO = px.scatter(df2, x="HORA", y="USUARIO", title="TR por Tipo", height=altoCD2*20+200,width=1000 )
        figA = px.scatter(df2, x="HORA", y="USUARIO", title="TR por zona", height=altoCD2*20+200,width=1000 )
        figA = figA.update_yaxes(autorange="reversed")
        print(altoCD2)
    elif option_slctd=="CD1":
        df2 = dfTr[dfTr["CD"]==option_slctd]
        df2 = df2[df2["TIPO"]==TRslctd]
        figO = px.scatter(df2, x="HORA", y="USUARIO", title="TR por Tipo", height=altoCD1*20+200,width=1000 )
        figA = px.scatter(df2, x="HORA", y="USUARIO", title="TR por zona", height=altoCD1*20+200,width=1000 )
        figA = figA.update_yaxes(autorange="reversed")
        print(altoCD1)
    else:
        df2 = dfTr[dfTr["CD"]==option_slctd]
        df2 = df2[df2["TIPO"]==TRslctd]
        figO = px.scatter(df2, x="HORA", y="USUARIO", color="TIPO",title="TR por Tipo", height=altoDD*20+200,width=1000 )
        figA = px.scatter(df2, x="HORA", y="USUARIO", color="LOC",title="TR por zona", height=altoDD*20+200,width=1000 )
        figA = figA.update_yaxes(autorange="reversed")
        print(altoDD)
    df2=df2
    return container, figO, figA


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



app.layout = html.Div([dd])

if __name__ == "__main__":
    app.run_server(debug=True)
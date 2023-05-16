import dash
import pandas as pd
import requests
from dash import  dcc,ctx, html, Input, Output, dash_table

dataz = requests.get('http://10.107.226.241/no_marcaciones')
jsondataz = dataz.json()
columnsz=['COL','USUARIO','RUT','NOMBRE','JORNADA','CARA']
dataScarz=[]
for col in jsondataz:
    for x in jsondataz[col]:
        dataScarz.append([col,x['USUARIO'],x['RUT'],x['NOMBRE'],x['JORNADA'],x['CARA']])

dfCarz = pd.DataFrame(dataScarz, columns=columnsz)


#print(dfCarz)
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


app9 = dash.Dash(__name__, title="No marcaciones",requests_pathname_prefix='/nomarcaciones/',external_scripts=external_scripts,external_stylesheets=external_stylesheets)

dd=html.Div([
    html.Br(),
        html.Div([
            dash_table.DataTable(dfCarz.to_dict('records'), [{"name": i, "id": i} for i in dfCarz.columns])
        ]),])
app9.layout = html.Div([dd])


if __name__ == "__main__":
    app9.run_server(debug=True)
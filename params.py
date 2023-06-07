import dash
from dash import dcc,html,Input,Output
import urllib.parse

apppa = dash.Dash(__name__,title="params",requests_pathname_prefix='/params/')

apppa.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='output')
])

@apppa.callback(Output('output', 'children'),[Input('url', 'search')])
def update_output(search):
    params = urllib.parse.parse_qs(search[1:])
    # Aquí puedes realizar las acciones que necesites con los parámetros de consulta
    # Por ejemplo, extraer un parámetro específico
    param_value = params.get('datatheme', [''])[0]
    # Luego puedes mostrar el resultado en la página
    return html.Div([
        html.Label('Valor del parámetro:'),
        html.P(param_value)
    ])

if __name__ == '__main__':
    apppa.run_server(debug=True)

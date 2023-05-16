from cubiscan.cubiscan import CubiScan
import os
import json
from dash import Dash
import dash_html_components as html


appcubi  = Dash(__name__,
			requests_pathname_prefix='/cubiscan1/')
server = appcubi.server

obj = CubiScan('10.107.230.87', '1050', timeout=5)
a= obj.measure()

print(a)
b = json.dumps(a)

#file = open("C:/Sitio/cubiscan1.txt", "w")
#file.write(b)
#file.close()

appcubi.layout = html.Div([
	html.P(b)
	]
	)

if __name__ == '__main__':
	appcubi.run_server(debug=True)

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dte
from flask import send_file
import io
import flask
import pandas as pd


app8 = dash.Dash(requests_pathname_prefix='/app8/')
app8.layout = html.Div(children=[
    html.A("download excel", href="/download_excel/"),
])


@app8.server.route('/download_excel/')
def download_excel():
    #Create DF
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)

    #Convert DF
    strIO = io.BytesIO()
    excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")
    df.to_excel(excel_writer, sheet_name="sheet1")
    excel_writer.save()
    excel_data = strIO.getvalue()
    strIO.seek(0)

    return send_file(strIO,
                     attachment_filename='test.xlsx',
                     as_attachment=True)

if __name__ == '__main__':
    app8.run_server(debug=True)
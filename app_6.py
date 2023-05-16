from dash import Dash, dcc, html, Input, Output
import pandas as pd
import io
app6 = Dash(__name__,requests_pathname_prefix='/app6/')
app6.layout = html.Div([
    html.Button("Download Excel", id="btn_xlsx"),
    dcc.Download(id="download-dataframe-xlsx"),
])


df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})


@app6.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_excel, "mydf.xlsx")


if __name__ == "__main__":
    app6.run_server(debug=True)
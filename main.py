from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
app.title = "DataProject"

app.layout = html.Div([
    html.H1("Bonjour 👋"),
    html.P("Ceci est mon premier dashboard Dash minimal.")
])

if __name__ == "__main__":
    app.run(debug=True)


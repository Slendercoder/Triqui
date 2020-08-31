import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import my_app.triqui_callbacks as tc
import my_app.triqui_layout as tl

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
app.title='Triqui'

app.layout = dbc.Container(fluid=True, children=[
    html.Br(),
    ## Top
    html.H1(children = 'El juego del TRIQUI',
        style = {'textAlign': 'center'}
    ),
    html.Br(),
    html.Br(),
    html.Div(
        id="row",
        className='row',
        children=[tl.root_layout]
    ),
    dbc.Modal(
    [
        dbc.ModalHeader("Resultado"),
        dbc.ModalBody("Este es el resultado", id="resultado"),
        dbc.ModalFooter(children=[
            dbc.Button("OK", id="close", className="ml-auto"),
        ]),
    ],
    id="modal",
    centered=True,
    ),
        dbc.Modal(
        [
            dbc.ModalHeader("¿En qué consiste este engine?"),
            dbc.ModalBody("", id="explicacion"),
            dbc.ModalFooter(children=[
                dbc.Button("OK", id="close1", className="ml-auto"),
            ]),
        ],
        id="modal1",
        centered=True,
        is_open=False,
        )
])

tc.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)

import plotly.graph_objects as go
import dash
from dash.dependencies import State, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import numpy as np
import base64

# values = [['a11', 'a21', 'a31'], #1st col
#             ['a12', 'a22', 'a32'], #1st col
#             ['a13', 'a23', 'a33'], #1st col
#             ]
#
# fig = go.Figure(data=[go.Table(
#   columnorder = [1,2,3],
#   columnwidth = [10,10,10],
#   # header = dict(
#   #   values = [['<b>EXPENSES</b><br>as of July 2017'],
#   #                 ['<b>DESCRIPTION</b>'],
#   #                 ['<b>Otra</b>']],
#   #   line_color='darkslategray',
#   #   fill_color='royalblue',
#   #   align=['center','center','center'],
#   #   font=dict(color='white', size=12),
#   #   height=40
#   # ),
#   cells=dict(
#     values=values,
#     line_color='darkslategray',
#     fill=dict(color=['paleturquoise', 'white']),
#     align=['left', 'center'],
#     font_size=12,
#     height=30)
#     )
# ])

# triqui = dash.Dash()
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
app.title='Triqui'

colors = {
    'background': '#b2b5df',
    'text': '#6c788e',
    'Nada': '#b2b5df'
}

ficha = {}
for i in range(3):
    for j in range(3):
        ficha[str(i + 1) + str(j + 1)] = '_'

ficha['22'] = 'O'

app.layout = dbc.Container(fluid=True, children=[
    html.Br(),
    ## Top
    html.H1(children = 'El juego del TRIQUI',
        style = {
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Br(),
    html.Br(),
    html.H6(children = 'Haga su jugada con las \'X\''+\
                       ' dando click en alguna de las casillas libres:',
        style = {'color': colors['text']}
    ),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(''),
        dbc.Col(children=[
            dbc.Row([
                dbc.Col(dbc.Button(ficha['11'],
                                    id="boton-11",
                                    style={'font-size':'30px'}
                                    )),
                dbc.Col(html.H1(children = ficha['12'],
                    style = {'color': colors['text']},
                    id='boton-12'
                    )),
                dbc.Col(html.H1(children = ficha['13'],
                    style = {'color': colors['text']}
                    ))
            ]),
            dbc.Row([
                dbc.Col(html.H1(children = ficha['21'],
                    style = {'color': colors['text']}
                    )),
                dbc.Col(html.H1(children = ficha['22'],
                    style = {'color': colors['text']}
                    )),
                dbc.Col(html.H1(children = ficha['23'],
                    style = {'color': colors['text']}
                    ))
            ]),
            dbc.Row([
                dbc.Col(html.H1(children = ficha['31'],
                    style = {'color': colors['text']}
                    )),
                dbc.Col(html.H1(children = ficha['32'],
                    style = {'color': colors['text']}
                    )),
                dbc.Col(html.H1(children = ficha['33'],
                    style = {'color': colors['text']}
                    ))
            ])
        ]),
        dbc.Col('')
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col('Computador en espera', id='comp_status'),
        dbc.Col(''),
        dbc.Col('')
    ])
])

# Pone una X en el boton-11
@app.callback(Output('boton-11', 'children'), [Input('boton-11', 'n_clicks')])
def on_button_click(n):
    if n is None:
        return '_'
    else:
        return 'X'
# Desactiva el boton-11
@app.callback(Output('boton-11', 'disabled'), [Input('boton-11', 'children')])
def on_button_change(t):
    if t == 'X':
        return True
# Cambia etiqueta del estado del computador
@app.callback(Output('comp_status', 'children'), [Input('boton-11', 'n_clicks')])
def on_button_disabled(dis):
    if dis:
        return 'Computando jugada...'
    else:
        return 'Computador en espera'

if __name__ == '__main__':
    app.run_server(debug=True)

from dash.dependencies import Output, Input, State
import numpy as np
from my_app.Logica import *
from my_app.Minmax import *

def ver(v):
    if v == 0:
        return "-"
    elif v == 1:
        return "O"
    else:
        return "X"

tablero = tablero_inicial()
T = triqui()
game_engine = "DPLL"
b1 = 0
b2 = 0
estado_engine = "Computador a la espera"
contador = 0

def register_callbacks(app):

    # BOTON-11
    # Pone una X en el boton-11
    @app.callback([Output('boton-11', 'color'),
    Output('boton-11', 'disabled'),#
    #Output('comp_status', 'children')
    ], [Input('boton-11', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[0, 0] = 2
            return 'secondary', True#, 'Computando jugada...'
    # BOTON-12
    @app.callback([Output('boton-12', 'color'),
    Output('boton-12', 'disabled')#,
    #Output('comp_status', 'children')
    ], [Input('boton-12', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[0, 1] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-13
    @app.callback([Output('boton-13', 'color'),
    Output('boton-13', 'disabled')],
    [Input('boton-13', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[0, 2] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-21
    @app.callback([Output('boton-21', 'color'),
    Output('boton-21', 'disabled')],
    [Input('boton-21', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[1, 0] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-22
    @app.callback([Output('boton-22', 'color'),
    Output('boton-22', 'disabled')],
    [Input('boton-22', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[1, 1] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-23
    @app.callback([Output('boton-23', 'color'),
    Output('boton-23', 'disabled')],
    [Input('boton-23', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[1, 2] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-31
    @app.callback([Output('boton-31', 'color'),
    Output('boton-31', 'disabled')],
    [Input('boton-31', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[2, 0] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-32
    @app.callback([Output('boton-32', 'color'),
    Output('boton-32', 'disabled')],
    [Input('boton-32', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[2, 1] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-33
    @app.callback([Output('boton-33', 'color'),
    Output('boton-33', 'disabled')],
    [Input('boton-33', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[2, 2] = 2
            return 'secondary', True#, 'Computando jugada...'

    @app.callback(Output('comp_status', 'children'),
    [Input('boton-11', 'n_clicks'),
    Input('boton-12', 'n_clicks'),
    Input('boton-13', 'n_clicks'),
    Input('boton-21', 'n_clicks'),
    Input('boton-22', 'n_clicks'),
    Input('boton-23', 'n_clicks'),
    Input('boton-31', 'n_clicks'),
    Input('boton-32', 'n_clicks'),
    Input('boton-33', 'n_clicks')
    ])
    def frase_final(a,b,c,d,e,f,g,h,i):

        global contador

        suma = contador
        if a is not None:
            suma += a
        elif b is not None:
            suma += b
        elif c is not None:
            suma += c
        elif d is not None:
            suma += d
        elif e is not None:
            suma += e
        elif f is not None:
            suma += f
        elif g is not None:
            suma += g
        elif h is not None:
            suma += h
        elif i is not None:
            suma += i

        if suma > contador:
            estado_engine = 'Computando Jugada...' + " " + str(suma) + " " + str(contador)
            contador = suma
        else:
            estado_engine = 'Computador a la espera'  + " " + str(suma) + " " + str(contador)

        return estado_engine

    @app.callback(
        [Output('tablero', 'children'),
        Output('boton-11', 'children'),
        Output('boton-12', 'children'),
        Output('boton-13', 'children'),
        Output('boton-21', 'children'),
        Output('boton-22', 'children'),
        Output('boton-23', 'children'),
        Output('boton-31', 'children'),
        Output('boton-32', 'children'),
        Output('boton-33', 'children')],
        [Input('comp_status', 'children')]
        )
    def computa_jugada(estado):

        global tablero
        global estado_engine

        if estado[:20] == 'Computando Jugada...':
            if np.count_nonzero(tablero==0) > 0:
                if hay_triqui(tablero,0) == 0:
                    antiguo_tablero = tablero
                    if game_engine == "DPLL":
                        tablero = jugar_dpll(tablero)
                    elif game_engine == "Minmax":
                        tablero = jugar_minmax(T, tablero)
                    else:
                        raise Exception('Engine invalido')
                    if len(tablero) == 0:
                        cambio = False
                        for fila in range(3):
                            for columna in range(3):
                                if not cambio and antiguo_tablero[fila,columna]==0:
                                    antiguo_tablero[fila,columna] = 1
                                    cambio = True
                        tablero = antiguo_tablero
                    mensaje = "Ganan las O" if hay_triqui(tablero,0)==1 else ''
                    estado_engine = "Computador a la espera"
                    return mensaje, ver(tablero[0,0]), ver(tablero[0,1]), ver(tablero[0,2]),\
                        ver(tablero[1,0]), ver(tablero[1,1]), ver(tablero[1,2]),\
                        ver(tablero[2,0]), ver(tablero[2,1]), ver(tablero[2,2])
                else:
                    estado_engine = "Computador a la espera"
                    return "Ganan las X", ver(tablero[0,0]), ver(tablero[0,1]), ver(tablero[0,2]),\
                        ver(tablero[1,0]), ver(tablero[1,1]), ver(tablero[1,2]),\
                        ver(tablero[2,0]), ver(tablero[2,1]), ver(tablero[2,2])

            estado_engine = "Juego terminado"
            return "Empate", ver(tablero[0,0]), ver(tablero[0,1]), ver(tablero[0,2]),\
                ver(tablero[1,0]), ver(tablero[1,1]), ver(tablero[1,2]),\
                ver(tablero[2,0]), ver(tablero[2,1]), ver(tablero[2,2])

        tablero = tablero_inicial()
        estado_engine = "Computador a la espera"
        return '', ver(tablero[0,0]), ver(tablero[0,1]), ver(tablero[0,2]),\
            ver(tablero[1,0]), ver(tablero[1,1]), ver(tablero[1,2]),\
            ver(tablero[2,0]), ver(tablero[2,1]), ver(tablero[2,2])

    @app.callback(
        [Output("modal", "is_open"),Output("resultado", "children")],
        [Input('tablero', 'children'),Input("close", "n_clicks")]
    )
    def toggle_modal(texto, n2):

        if ((texto=='Ganan las O') or (texto=='Ganan las X') or (texto=='Empate')) and not n2:
            return True, texto
        elif  ((texto=='Ganan las O') or (texto=='Ganan las X')) and n2:
            return False, ""
        else:
            return False, ""

    @app.callback(
        [Output('casillas', 'children'),
        Output('dpll', 'active'),
        Output('minmax', 'active')],
        [Input('dpll', 'n_clicks'), Input('minmax', 'n_clicks')]
    )
    def choose_engine(n1, n2):

        global b1
        global b2
        global game_engine

        if n2:
            if n2 > b2:
                game_engine = "Minmax"
                b1 = n1
                b2 = n2
                return game_engine, False, True

        return game_engine, True, False

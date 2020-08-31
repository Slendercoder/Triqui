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
e1 = 0
e2 = 0
estado_engine = "Computador a la espera"
contador = 0

def register_callbacks(app):

    # BOTON-11
    # Pone una X en el boton-11
    @app.callback(Output('boton-11', 'color'),
    [Input('boton-11', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[0, 0] = 2
            return 'secondary', True#, 'Computando jugada...'
    # BOTON-12
    @app.callback(Output('boton-12', 'color'),
    [Input('boton-12', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[0, 1] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-13
    @app.callback(Output('boton-13', 'color'),
    [Input('boton-13', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[0, 2] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-21
    @app.callback(Output('boton-21', 'color'),
    [Input('boton-21', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[1, 0] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-22
    @app.callback(Output('boton-22', 'color'),
    [Input('boton-22', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[1, 1] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-23
    @app.callback(Output('boton-23', 'color'),
    [Input('boton-23', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[1, 2] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-31
    @app.callback(Output('boton-31', 'color'),
    [Input('boton-31', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[2, 0] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-32
    @app.callback(Output('boton-32', 'color'),
    [Input('boton-32', 'n_clicks')])
    def on_button_click(n):

        global tablero

        if n is None:
            return 'secondary', False#, 'Computador en espera'
        else:
            tablero[2, 1] = 2
            return 'secondary', True#, 'Computando jugada...'

    # BOTON-33
    @app.callback(Output('boton-33', 'color'),
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

        if a or b or c or d or e or f or g or h or i:
            estado_engine = "..."
        else:
            estado_engine = ""



        # if suma > contador:
        #     estado_engine = 'Computando Jugada...' + " " + str(suma) + " " + str(contador)
        #     contador = suma
        # else:
        #     estado_engine = 'Computador a la espera'  + " " + str(suma) + " " + str(contador)

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
        Output('boton-33', 'children'),
        Output('boton-11', 'disabled'),
        Output('boton-12', 'disabled'),
        Output('boton-13', 'disabled'),
        Output('boton-21', 'disabled'),
        Output('boton-22', 'disabled'),
        Output('boton-23', 'disabled'),
        Output('boton-31', 'disabled'),
        Output('boton-32', 'disabled'),
        Output('boton-33', 'disabled'),
        ],
        [Input('comp_status', 'children')]
        )
    def computa_jugada(estado):

        global tablero
        btn11_dis = False
        btn12_dis = False
        btn13_dis = False
        btn21_dis = False
        btn22_dis = False
        btn23_dis = False
        btn31_dis = False
        btn32_dis = False
        btn33_dis = False

        if estado == '...':
            if hay_triqui(tablero) == 0:
                if np.count_nonzero(tablero==0) > 0:
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
                    mensaje = "Ganan las O" if hay_triqui(tablero)==1 else ''
                    if tablero[0,0] != 0:
                        btn11_dis = True
                    if tablero[0,1] != 0:
                        btn12_dis = True
                    if tablero[0,2] != 0:
                        btn13_dis = True
                    if tablero[1,0] != 0:
                        btn21_dis = True
                    if tablero[1,1] != 0:
                        btn22_dis = True
                    if tablero[1,2] != 0:
                        btn23_dis = True
                    if tablero[2,0] != 0:
                        btn31_dis = True
                    if tablero[2,1] != 0:
                        btn32_dis = True
                    if tablero[2,2] != 0:
                        btn33_dis = True
                    return mensaje, ver(tablero[0,0]), ver(tablero[0,1]), ver(tablero[0,2]),\
                        ver(tablero[1,0]), ver(tablero[1,1]), ver(tablero[1,2]),\
                        ver(tablero[2,0]), ver(tablero[2,1]), ver(tablero[2,2]),\
                        btn11_dis, btn12_dis, btn13_dis, btn21_dis, btn22_dis, btn23_dis,\
                        btn31_dis, btn32_dis, btn33_dis
                else:
                    if tablero[0,0] != 0:
                        btn11_dis = True
                    if tablero[0,1] != 0:
                        btn12_dis = True
                    if tablero[0,2] != 0:
                        btn13_dis = True
                    if tablero[1,0] != 0:
                        btn21_dis = True
                    if tablero[1,1] != 0:
                        btn22_dis = True
                    if tablero[1,2] != 0:
                        btn23_dis = True
                    if tablero[2,0] != 0:
                        btn31_dis = True
                    if tablero[2,1] != 0:
                        btn32_dis = True
                    if tablero[2,2] != 0:
                        btn33_dis = True
                    return "Empate", ver(tablero[0,0]), ver(tablero[0,1]), ver(tablero[0,2]),\
                        ver(tablero[1,0]), ver(tablero[1,1]), ver(tablero[1,2]),\
                        ver(tablero[2,0]), ver(tablero[2,1]), ver(tablero[2,2]),\
                        btn11_dis, btn12_dis, btn13_dis, btn21_dis, btn22_dis, btn23_dis,\
                        btn31_dis, btn32_dis, btn33_dis
            else:
                if tablero[0,0] != 0:
                    btn11_dis = True
                if tablero[0,1] != 0:
                    btn12_dis = True
                if tablero[0,2] != 0:
                    btn13_dis = True
                if tablero[1,0] != 0:
                    btn21_dis = True
                if tablero[1,1] != 0:
                    btn22_dis = True
                if tablero[1,2] != 0:
                    btn23_dis = True
                if tablero[2,0] != 0:
                    btn31_dis = True
                if tablero[2,1] != 0:
                    btn32_dis = True
                if tablero[2,2] != 0:
                    btn33_dis = True
                return "Ganan las X", ver(tablero[0,0]), ver(tablero[0,1]), ver(tablero[0,2]),\
                    ver(tablero[1,0]), ver(tablero[1,1]), ver(tablero[1,2]),\
                    ver(tablero[2,0]), ver(tablero[2,1]), ver(tablero[2,2]),\
                    btn11_dis, btn12_dis, btn13_dis, btn21_dis, btn22_dis, btn23_dis,\
                    btn31_dis, btn32_dis, btn33_dis

        tablero = tablero_inicial()
        return '', ver(tablero[0,0]), ver(tablero[0,1]), ver(tablero[0,2]),\
            ver(tablero[1,0]), ver(tablero[1,1]), ver(tablero[1,2]),\
            ver(tablero[2,0]), ver(tablero[2,1]), ver(tablero[2,2]),\
            btn11_dis, btn12_dis, btn13_dis, btn21_dis, btn22_dis, btn23_dis,\
            btn31_dis, btn32_dis, btn33_dis

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
        if n1:
            game_engine = "DPLL"

        return game_engine, True, False

    @app.callback(
        [Output("modal1", "is_open"),Output("explicacion", "children")],
        [Input('explica', 'n_clicks'),Input("close1", "n_clicks")],
    [State("modal1", "is_open")],
    )
    def toggle_modal1(n1, n2, is_open):

        global game_engine

        if game_engine == "DPLL":
            msg = """
                Cuando se selecciona el engine DPLL, el proceso de toma de decisiones del computador está basado en el algortimo DPLL (cf. Russell & Norvig (2016), sec. 7.6), el cual es un método de \'model checking\' para fórmulas de la lógica proposicional. Usamos una fórmula que combina 27 letras proposicionales para representar las posiciones del tablero, y mediante ella implementamos la conjunción de cinco reglas de decisión. Las reglas incluyen bloquear el triqui del otro jugador y hacer triqui de ser posible. Este algoritmo, así como la resolución de este tipo de problemas, se estudian en la asignatura \'Lógica para ciencias de la computación\'.
                """
        elif game_engine == "Minmax":
            msg = """
                 Cuando se selecciona el engine Minmax, el proceso de toma de decisiones del computador está basado en el algoritmo Minmax (cf. Russell & Norvig (2016), sec. 5.2), mediante el cual se crea un árbol de estados, partiendo desde el estado actual del juego, atribuyéndole una utilidad a cada estado con base en los pagos generados por una condición final. Los pagos para el jugador 1 con las $X$ son positivos, y los del jugador 2 con las $O$ son negativos, así que el primero buscará estados que maximicen la utilidad, mientras que el segundo buscará estados que la minimicen. Este algoritmo así como la resolución de juegos competitivos se estudian en la asignatura \'Inteligencia Artificial\'.
                """

        if n1 or n2:
            return (not is_open), msg
        return is_open, msg

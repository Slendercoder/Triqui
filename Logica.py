import json
from DPLL import *
from Codificacion import *

def cargar_reglas():
    # Cargando reglas
    with open('reglas.json', 'r') as file:
        reglas = json.load(file)

    print("Trabajando con reglas", list(reglas.keys()))

    inicial = True
    for r in reglas.keys():
        if inicial:
            formula = reglas[r]
            inicial = False
        else:
            formula += reglas[r]

    return formula

def calcular_resultado(formula):

    S, I = DPLL(formula, {})

    Nfilas = 2
    Ncolumnas = 2
    Nnumeros = 2 # Se asume que E es 0, O es 1, X es 2
    Nturnos = 2

    print(S)
    # print(I)
    resultado_turno0 = []
    resultado_turno1 = []
    letras = [chr(x) for x in range(256, 311)]
    for i in I.keys():
        if i in letras:
            if I[i] == 1:
                fila = list(Pinv(i, Nfilas, Ncolumnas, Nnumeros, Nturnos))
                if fila[3] == 0:
                    resultado_turno0.append(fila)
                elif fila[3] == 1:
                    resultado_turno1.append(fila)
                else:
                    print("Oops!", i, fila)

    imprime(resultado_turno0)
    imprime(resultado_turno1)

formula = cargar_reglas()
calcular_resultado(formula)

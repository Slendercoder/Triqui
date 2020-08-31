# Crea reglas y pasa a archivo
from FNC import *
from Codificacion import *
from Logica import *
import json

Nfilas = 3
Ncolumnas = 3
Nnumeros = 3 # Se asume que E es 0, O es 1, X es 2
Nturnos = 2

# Esta regla pone la restriccion de que una casilla no puede tener mas de un numero
def regla0():
    inicial = True
    for x in range(Nfilas):
        for y in range(Ncolumnas):
            for o in range(Nnumeros):
                for t in range(Nturnos):
                    inicial_clausula = True
                    for oP in range(Nnumeros):
                        if oP!=o:
                            if inicial_clausula:
                                inicial_clausula = False
                                clausula = P(x, y, oP, t, Nfilas, Ncolumnas, Nnumeros, Nturnos) + "-"
                            else:
                                clausula += P(x, y, oP, t, Nfilas, Ncolumnas, Nnumeros, Nturnos) + "-Y"

                    if inicial:
                        inicial = False
                        regla = clausula + P(x, y, o, t, Nfilas, Ncolumnas, Nnumeros, Nturnos) + "="
                    else:
                        regla += clausula + P(x, y, o, t, Nfilas, Ncolumnas, Nnumeros, Nturnos) + "=Y"
    return regla

# Esta regla pone la restriccion de que se preserva el X/O de un turno a otro
def regla1():
    inicial = True
    for x in range(Nfilas):
        for y in range(Ncolumnas):
            for o in range(1, Nnumeros):
                if inicial:
                    inicial = False
                    regla = P(x, y, o, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(x, y, o, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + ">"
                else:
                    regla += P(x, y, o, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(x, y, o, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + ">Y"

    return regla

# Esta regla pone la restriccion de que solo se puede poner una O en el turno siguiente
def regla2():
    inicial_impl = True
    for x in range(Nfilas):
        for y in range(Ncolumnas):
            x_aux = [i for i in range(Nfilas) if i != x]
            y_aux = [i for i in range(Ncolumnas) if i != y]
            inicial = True
            otros_numeros = [i for i in range(Nnumeros) if i != 1]
            for z in otros_numeros:
                for xP in range(Nfilas):
                    for yP in range(Ncolumnas):
                        if (xP!=x) or (yP!=y):
                            P_anterior = P(xP, yP, z, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos)
                            P_nuevo = P(xP, yP, z, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos)
                            if inicial:
                                inicial = False
                                betas = P_nuevo + P_anterior + ">"
                            else:
                                betas += P_nuevo + P_anterior + ">Y"

            P_anterior = P(x, y, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos)
            P_nuevo = P(x, y, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos)
            if inicial_impl:
                inicial_impl = False
                impl =betas + P_nuevo + P_anterior + "Y="
                # print("Primera imp", impl)
            else:
                # print("Segunda imp", impl)
                impl += betas + P_nuevo + P_anterior + "Y=Y"

    return impl

# Esta regla pone la restriccion de que no puede haber ninguna X adicional
def regla3():
    inicial = True
    for f in range(Nfilas):
        for c in range(Ncolumnas):
            if inicial:
                inicial=False
                reg = P(f, c, 2, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + "-" + P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + ">"
            else:
                reg += P(f, c, 2, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + "-" + P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + ">Y"

    return reg

# Esta regla indica que se deben bloquear las oportunidades de ganar del otro jugador
def regla4():
    # Crear restriccion de no tomar en cuenta la regla si es posible ganar
    # Parte A: Verificar si se puede ganar por columnas
    inicial = True
    for f in range(Nfilas):
        for c in range(Ncolumnas):
            if inicial:
                A = P(f, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                    P(f, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                    P(f, (c+2)%3, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
                inicial = False
            else:
                A += P(f, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                     P(f, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                     P(f, (c+2)%3, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'YO'

    # Parte B: Verificar si se puede ganar por filas
    inicial = True
    for f in range(Nfilas):
        for c in range(Ncolumnas):
            if inicial:
                B = P(f, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                    P((f+1)%3, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                    P((f+2)%3, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
                inicial = False
            else:
                B += P(f, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                     P((f+1)%3, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                     P((f+2)%3, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'YO'

    # Parte C: Verificar si se puede ganar por diagonal principal
    inicial = True
    for a in range(Nfilas):
        if inicial:
            C = P((a+1)%3, (a+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                P((a+2)%3, (a+2)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                P(a, a, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
            inicial = False
        else:
            C += P((a+1)%3, (a+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                 P((a+2)%3, (a+2)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                 P(a, a, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'YO'

    # Parte D: Verificar si se puede ganar por diagonal secundaria
    inicial = True
    for f in range(Nfilas):
        c = 2-f
        if inicial:
            D = P((f-1)%3, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                P((f-2)%3, (c+2)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
            inicial = False
        else:
            D += P((f-1)%3, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                P((f-2)%3, (c+2)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'YO'

    restriccion = A + B + 'O' + C + 'O' + D + 'O-'

    # Se crean las instrucciones de verificar las oportunidades del otro jugador

    # Parte E: Evitar columna
    inicial=True
    columnas = range(Ncolumnas)
    filas = range(Nfilas)
    for c in columnas:
        for f in filas:
            inicial1 = True
            alfas = [x for x in filas if x != f]
            for a in alfas:
                if inicial1:
                    clau = P(a,c,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
                    inicial1 = False
                else:
                     clau += P(a,c,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
            if inicial:
                E = P(f,c,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>'
                inicial = False
            else:
                E += P(f,c,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>' + 'Y'

    # Parte F: Evitar fila
    inicial=True
    for f in filas:
        for c in columnas:
            inicial1 = True
            for a in columnas:
                if a != c and inicial1:
                    clau = P(f,a,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
                    inicial1 = False
                elif a != c:
                     clau += P(f,a,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
            if inicial:
                F = P(f,c,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>'
                inicial = False
            else:
                F += P(f,c,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>' + 'Y'

    #Parte G: Evitar diagonal principal
    inicial=True
    for a in columnas:
        inicial1 = True
        for b in columnas:
            if a != b and inicial1:
                clau = P(b,b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
                inicial1 = False
            elif a != b:
                clau += P(b,b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
        if inicial:
            G = P(a,a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau +  '>'
            inicial = False
        else:
            G += P(a,a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>' + 'Y'

    #Parte H: Evitar diagonal secundaria
    inicial=True
    for a in columnas:
        inicial1 = True
        for b in columnas:
            if a != b and inicial1:
                clau = P(b,2-b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
                inicial1 = False
            elif a != b:
                clau += P(b,2-b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
        if inicial:
            H = P(a,2-a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>'
            inicial = False
        else:
            H += P(a,2-a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau +  '>' + 'Y'

    return E + F + 'Y' + G + 'Y' + H + 'Y' + restriccion + '>'

# Esta regla indica que se debe ganar siempre que sea posible
def regla5():
    # Parte A: Rellenar fila
    inicial = True
    for f in range(Nfilas):
        for c in range(Ncolumnas):
            if inicial:
                A = P(f, c, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + \
                    P(f, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                    P(f, (c+2)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                    P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y>'
                inicial = False
            else:
                A += P(f, c, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + \
                    P(f, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + \
                    P(f, (c+2)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                    P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y>Y'

    # Parte B: Rellenar columna
    inicial = True
    for f in range(Nfilas):
        for c in range(Ncolumnas):
            if inicial:
                B = P(f, c, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                    P((f+1)%3, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + \
                    P((f+2)%3, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                    P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y>'
                inicial = False
            else:
                B += P(f, c, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                    P((f+1)%3, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                    P((f+2)%3, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                    P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y>Y'

    # Parte C: Rellenar diagonal principal
    inicial = True
    for a in range(Nfilas):
        if inicial:
            C = P(a, a, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                P((a+1)%3, (a+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                P((a+2)%3, (a+2)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                P(a, a, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y>'
            inicial = False
        else:
            C += P(a, a, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                 P((a+1)%3, (a+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                 P((a+2)%3, (a+2)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                 P(a, a, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y>Y'

    # Parte D: Rellenar diagonal secundaria
    inicial = True
    for f in range(Nfilas):
        c = 2-f
        if inicial:
            D = P(f, c, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                P((f-1)%3, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                P((f-2)%3, (c+2)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y>'
            inicial = False
        else:
            D += P(f, c, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                 P((f-1)%3, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) +\
                 P((f-2)%3, (c+2)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' +\
                 P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y>Y'

    # Regla completa y solucion
    return A + B + 'Y' + C + 'Y' + D + 'Y'

#Esta regla es verdadera si existe algún ganador
def regla_ganador():
    #Parte A: Ganador por fila
    inicial = True
    for f in range(Nfilas):
        for n in range(1,3):
            for t in range(Nturnos):
                if inicial:
                    A = P(f,(f+2)%3,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + P(f,(f+1)%3,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + 'Y' + P(f,f%3,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + 'Y'
                    inicial = False
                else:
                    A += P(f,(f+2)%3,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + P(f,(f+1)%3,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + 'Y' + P(f,f%3,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + 'Y' + 'O'

    #Parte B: Ganador por columna
    inicial = True
    for c in range(Ncolumnas):
        for n in range(1,3):
            for t in range(Nturnos):
                if inicial:
                    B = P((c+2)%3,c,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + P((c+1)%3,c,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + 'Y' + P(c%3,c,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + 'Y'
                    inicial = False
                else:
                    B += P((c+2)%3,c,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + P((c+1)%3,c,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + 'Y' + P(c%3,c,n,t,Nfilas,Ncolumnas, Nnumeros, Nturnos) + 'Y' + 'O'

    #Parte C: Ganador por diagonal principal
    inicial = True
    for n in range (1,3):
        for t in range (Nturnos):
            inicial1 = True
            for f in range(Nfilas):
                if inicial1:
                    clau = P(f,f,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos)
                    inicial1 = False
                else:
                    clau += P(f,f,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
            if inicial:
                C = clau
                inicial = False
            else:
                C += clau + 'O'

    #Parte D: Ganador por diagonal secundaria
    inicial = True
    for n in range (1,3):
        for t in range (Nturnos):
            if inicial:
                D = P(0,2,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(1,1,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + P(2,0,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
                inicial = False
            else:
                D += P(0,2,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(1,1,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + P(2,0,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + 'O'

    return A + B + 'O' + C + 'O' + D + 'O'

def actualizar_dict(
        r:int,
        letrasB_inicial:int,
        rango:int,
        letrasProposicionalesA:list,
        imprimir=False,
        imp_regla=True):

    if r == 0:
        regla = regla0()
    elif r == 1:
        regla = regla1()
    elif r == 2:
        regla = regla2()
    elif r == 3:
        regla = regla3()
    elif r == 4:
        regla = regla4()
    elif r == 5:
        regla = regla5()

    if imprimir:
        print("Regla", r, "NPI:", regla)
    regla = String2Tree(regla)
    if imp_regla:
        print("Regla", r, "decodificada:", Inorderp(regla))
    regla = Inorder(regla)
    if imprimir:
        print("Regla", r, "codificada:", regla)
    letrasProposicionalesB = [chr(x) for x in range(letrasB_inicial, letrasB_inicial + rango)]
    regla = Tseitin(regla, letrasProposicionalesA, letrasProposicionalesB)
    if imprimir:
        print("Tseitin:", regla)
    regla = formaClausal(regla)
    if imprimir:
        print("Forma clausal:", regla)

    return regla

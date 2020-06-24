# Crea reglas y pasa a archivo
from FNC import *
from Codificacion import *
import json

Nfilas = 3
Ncolumnas = 3
Nnumeros = 3 # Se asume que E es 0, O es 1, X es 2
Nturnos = 2

class Tree(object):
    def __init__(self, label, left, right):
        self.left = left
        self.right = right
        self.label = label

def String2Tree(A):
    letrasProposicionales=[chr(x) for x in range(256, 400)]
    Conectivos = ['O','Y','>','=']
    Pila = []
    for c in A:
        # print("Procesando", c)
        if c in letrasProposicionales:
            Pila.append(Tree(c,None,None))
        elif c=='-':
            FormulaAux = Tree(c,None,Pila[-1])
            del Pila[-1]
            Pila.append(FormulaAux)
        elif c in Conectivos:
            FormulaAux = Tree(c,Pila[-1],Pila[-2])
            del Pila[-1]
            del Pila[-1]
            Pila.append(FormulaAux)
        else:
            print(u"Hay un problema: el símbolo " + str(c)+ " no se reconoce")

    return Pila[-1]

def Inorder(f):
    if f.right == None:
        return f.label
    elif f.label == '-':
        return f.label + Inorder(f.right)
    else:
        return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def Inorderp(f):
    if f.right == None:
        return "P" + str(Pinv(f.label, Nfilas, Ncolumnas, Nnumeros, Nturnos))
    elif f.label == '-':
        return f.label + Inorderp(f.right)
    else:
        return "(" + Inorderp(f.left) + f.label + Inorderp(f.right) + ")"

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
    pass

# Esta regla pone la condicion inicial
def regla4():

    x0 = 1
    y0 = 1
    letra = P(x0, y0, 2, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos)
    for x in range(Nfilas):
        for y in range(Ncolumnas):
            if (x!=x0) or (y!=y0):
                letra += P(x, y, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + "Y"

    return letra

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

######################
reglas = {}
letrasProposicionalesA = [chr(x) for x in range(256, 400)]
letrasB_inicial = 400
rango = 350

reglas_seleccionadas = [0, 1, 2, 4]

for r in reglas_seleccionadas:
    regla = actualizar_dict(r, letrasB_inicial, rango, letrasProposicionalesA)
    reglas['regla' + str(r)] = regla
    letrasB_inicial += rango

with open('reglas.json', 'w') as outfile:
    json.dump(reglas, outfile)

print("Listas reglas!")

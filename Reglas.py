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
    inicial = True
    for f in range(Nfilas):
        for c in range(Ncolumnas):
            if inicial:
                inicial=False
                reg = P(f, c, 2, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + "-" + P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + ">"
            else:
                reg += P(f, c, 2, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + "-" + P(f, c, 0, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + ">Y"

    return reg

def regla4():
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
    F = ""
    for f in filas:
        for c in columnas:
            inicial1 = True
            for a in columnas:
                if a != c and inicial1:
                    F += P(f,a,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
                    inicial1 = False
                if a != c:
                     F += P(f,a,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
            if inicial:
                F += P(f,c,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + '>'
                inicial = False
            else:
                F += P(f,c,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + '>' + 'Y'

    #Parte G: Evitar columna principal
    inicial=True
    G = ""
    for a in columnas:
        inicial1 = True
        for b in columnas:
            if a != b and inicial1:
                G += P(b,b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
            if a != c:
                G += P(b,b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
        if inicial:
            G += P(a,a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + '>'
            inicial = False
        else:
            G += P(a,a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + '>' + 'Y'

    #Parte H: Evitar columna secundaria
    inicial=True
    H = ""
    for a in columnas:
        inicial1 = True
        for b in columnas:
            if a != b and inicial1:
                H += P(b,2-b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
            if a != c:
                H += P(b,2-b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
        if inicial:
            H += P(a,2-a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + '>'
            inicial = False
        else:
            H += P(a,a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + '>' + 'Y'

    return E# + F + 'Y' + G + 'Y' + H + 'Y'

def regla5():
    # Parte A: Rellenar columna
    inicial = True
    for f in range(Nfilas):
        for c in range(Ncolumnas):
            if inicial:
                A = P(f, (c+2)%3, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(f, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(f, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + '>'
                inicial = False
            else:
                A += P(f, (c+2)%3, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(f, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(f, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + '>' + 'Y'

    # Parte B: Rellenar fila
    inicial = True
    for f in range(Nfilas):
        for c in range(Ncolumnas):
            if inicial:
                B = P((f+2)%3, c, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(f, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P((f+1)%3, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + '>'
                inicial = False
            else:
                B += P((f+2)%3, c, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(f, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P((f+1)%3, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + '>' + 'Y'

    # Parte C: Rellenar diagonal principal
    inicial = True
    for a in range(Nfilas):
        if inicial:
            C = P((a+2)%3, (a+2)%3, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P((a+1)%3, (a+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(a, a, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + '>'
            inicial = False
        else:
            C += P((a+2)%3, (a+2)%3, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P((a+1)%3, (a+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(a, a, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + '>' + 'Y'

    # Parte D: Rellenar diagonal secundaria
    inicial = True
    for f in range(Nfilas):
        c = 2-f
        if inicial:
            D = P((f-2)%3, (c+2)%3, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P((f-1)%3, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(f, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + '>'
            inicial = False
        else:
            D += P((f-2)%3, (c+2)%3, 1, 1, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P((f-1)%3, (c+1)%3, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + P(f, c, 1, 0, Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + '>' + 'Y'

    # Regla completa y solucion
    return A + B + 'Y' + C + 'Y' + D + 'Y'

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

reglas_seleccionadas = [0, 1, 2, 3, 4, 5]
# reglas_seleccionadas = [0, 1, 2]

for r in reglas_seleccionadas:
    regla = actualizar_dict(r, letrasB_inicial, rango, letrasProposicionalesA)
    reglas['regla' + str(r)] = regla
    letrasB_inicial += rango

with open('reglas.json', 'w') as outfile:
    json.dump(reglas, outfile)

print("Listas reglas!")

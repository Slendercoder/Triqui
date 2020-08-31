# -*- coding: utf-8 -*-

# Subrutinas para la transformacion de una
# formula a su forma clausal

def enFNC(A):
    # Subrutina de Tseitin para encontrar la FNC de
    # la formula en la pila
    # Input: A (cadena) de la forma
    #                   p=-q
    #                   p=(qYr)
    #                   p=(qOr)
    #                   p=(q>r)
    # Output: B (cadena), equivalente en FNC
    assert(len(A)==4 or len(A)==7), u"Fórmula incorrecta!"
    B = ''
    p = A[0]
    # print('p', p)
    if "-" in A:
        q = A[-1]
        # print('q', q)
        B = "-"+p+"O-"+q+"Y"+p+"O"+q
    elif "Y" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O-"+p+"Y"+r+"O-"+p+"Y-"+q+"O-"+r+"O"+p
    elif "O" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = "-"+q+"O"+p+"Y-"+r+"O"+p+"Y"+q+"O"+r+"O-"+p
    elif ">" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O"+p+"Y-"+r+"O"+p+"Y-"+q+"O"+r+"O-"+p
    elif "=" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        #qO-rO-pY-qOrO-pY-qO-rOpYqOrOp
        B = q+"O"+"-"+r+"O"+"-"+p+"Y"+"-"+q+"O"+r+"O"+"-"+p+"Y"+"-"+q+"O"+"-"+r+"O"+p+"Y"+q+"O"+r+"O"+p
    else:
        print(u'Error enENC(): Fórmula incorrecta!')

    return B

# Algoritmo de transformacion de Tseitin
# Input: A (cadena) en notacion inorder
# Output: B (cadena), Tseitin
def Tseitin(A, letrasProposicionalesA, letrasProposicionalesB):
    assert(not bool(set(letrasProposicionalesA) & set(letrasProposicionalesB))), u"¡Hay letras proposicionales en común!"

    L = [] # Inicializamos lista de conjunciones
    Pila = [] # Inicializamos pila
    i = -1 # Inicializamos contador de variables nuevas
    s = A[0] # Inicializamos símbolo de trabajo

    letrasProposicionales = letrasProposicionalesA + letrasProposicionalesB

    while len(A) > 0:

        # print("Pila:", Pila, " L:", L, " s:", s)

        if (s in letrasProposicionales) and (len(Pila) > 0) and (Pila[-1]=='-'):
            i += 1
            atomo = letrasProposicionalesB[i]
            Pila = Pila[:-1]
            Pila.append(atomo)
            L.append(atomo + "=-" + s)
            A = A[1:]
            if len(A) > 0:
                s = A[0]

        elif s == ')':
            w = Pila[-1]
            O = Pila[-2]
            v = Pila[-3]
            Pila = Pila[:len(Pila)-4]
            i += 1
            atomo = letrasProposicionalesB[i]
            L.append(atomo + "=(" + v + O + w + ")")
            s = atomo

        else:
            Pila.append(s)
            A = A[1:]
            if len(A) > 0:
                s = A[0]

    # print("Final:")
    # print("Pila:", Pila, " L:", L, " s:", s)

    B = ""
    if i < 0:
        atomo = Pila[-1]
    else:
        atomo = letrasProposicionalesB[i]

    for X in L:
        Y = enFNC(X)
        B += "Y" + Y

    B = atomo + B

    return B

# Subrutina Clausula para obtener lista de literales
# Input: C (cadena) una clausula
# Output: L (lista), lista de literales
# Se asume que cada literal es un solo caracter
def Clausula(C):

    L = []

    while len(C) > 0:

        s = C[0]

        # print("L:", L, " C:", C, " s:", s)

        if s == '-':
            L.append(s + C[1])
            C = C[3:]

        else:
            L.append(s)
            C = C[2:]

    # print("Final:")
    # print("L:", L)

    return L

# Algoritmo para obtencion de forma clausal
# Input: A (cadena) en notacion inorder en FNC
# Output: L (lista), lista de listas de literales
def formaClausal(A):

    L = []
    i = 0

    while len(A) > 0:

        if i >= len(A):
            L.append(Clausula(A))
            A = []

        else:
            if A[i] == "Y":
                L.append(Clausula(A[:i]))
                A = A[i+1:]
                i = 0
            else:
                i += 1

    return L

# Test enFNC()
# Descomente el siguiente código y corra el presente archivo
# formula = "p=(qYr)"
# print(enFNC(formula)) # Debe obtener qO-pYrO-pY-qO-rOp

# Test Tseitin()
# Descomente el siguiente código y corra el presente archivo
# formula = "(pYq)"
# print(Tseitin(formula)) # Debe obtener AYpO-AYqO-AY-pO-qOA (la A tiene una raya encima)

# Test Clausula()
# Descomente el siguiente código y corra el presente archivo
# c = "pO-qOr"
# print(Clausula(c)) # Debe obtener ['p', '-q', 'r']

# Test formaClausal()
# Descomente el siguiente código y corra el presente archivo
# f = "pO-qOrY-sOt"
# print(formaClausal(f)) # Debe obtener [['p', '-q', 'r'], ['-s', 't']]

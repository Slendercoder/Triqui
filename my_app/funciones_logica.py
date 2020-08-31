import re

conectivos = ['O', 'Y', '>', '=']
Nfilas = 3
Ncolumnas = 3
Nnumeros = 3
Nturnos = 2

class Tree(object):
    def __init__(self, label, left, right):
        self.left = left
        self.right = right
        self.label = label

def inorder(A):
    #Convierte un Tree en una cadena de símbolos
    #Input: A, formula como Tree
    #Output: formula como string
    if A.right == None:
        return A.label
    elif A.label == "-":
        return '-'+ inorder(A.right)
    elif A.label in conectivos:
        return '(' + inorder(A.left) + A.label + inorder(A.right) + ')'

def elim_doble_negacion(T):
    #Elimina las dobles negaciones en una formula dada como Tree
    #Input: Formula como Tree
    #Output: Formula como Tree sin dobles negaciones
    if T.right == None:
        return T
    elif T.label == '-':
        if T.right.label == '-':
            return elim_doble_negacion(T.right.right)
        else:
            return Tree('-',None,elim_doble_negacion(T.right))
    elif T.label in conectivos:
        return Tree(T.label,elim_doble_negacion(T.left),elim_doble_negacion(T.right))

def String2Tree(polaco_inverso, LetrasProposicionales):
    #Crea una formula como Tree dada una formula como string en notacion polaca inversa
    #Input: polaco_inverso, Lista de caracteres con una formula escrita en notacion polaca inversa
    #       LetrasProposicionales, lista de strings
    #Output: Formula como Tree
    A = []
    for i in polaco_inverso:
        A.append(i)
    pila = []
    for c in A:
        if c in LetrasProposicionales:
            pila.append(Tree(c, None, None))
        elif c =='-':
            formulaAux = Tree(c, None, pila[-1])
            del pila[-1]
            pila.append(formulaAux)
        elif c in conectivos:
            formulaAux = Tree(c, pila[-1], pila[-2])
            del pila[-1]
            del pila[-1]
            pila.append(formulaAux)
    return pila[-1]

def Tseitin(T, LetrasProposicionales):
    #Dada una formula T, halla una formula T' igual de buena que T en forma normal conjuntiva
    #Input: T formula como Tree
    #       LetrasProposicionales, lista de strings
    #Output: Formula como Tree en forma normal conjuntiva
    T = elim_doble_negacion(T)
    A = inorder(T)
    LetrasProposicionales2 = [chr(x) for x in range(900, 1399)]
    L  = []
    pila = []
    i = -1
    s = A [0]
    while len(A) > 0:
        if s in LetrasProposicionales and len(pila) > 0 and pila[-1] == "-":
            i += 1
            atomo = LetrasProposicionales2[i]
            pila = pila[:-1]
            pila.append(atomo)
            L.append(Tree("=", Tree(atomo,None,None), Tree("-",None, Tree(s, None, None))))
            A = A[1:]
            if len(s)>0:
                s = A[0]
        elif s == ")":
            w = pila[-1]
            o = pila[-2]
            v = pila[-3]
            pila = pila[:len(pila) -4]
            i += 1
            atomo = LetrasProposicionales2[i]
            L.append(Tree("=", Tree(atomo, None, None), Tree(o, Tree(v, None, None), Tree(w,None, None))))
            s = atomo
        else:
            pila.append(s)
            A = A[1:]
            if len(A)>0:
                s = A[0]
    B = ""
    if i < 0:
        atomo = pila[-1]
    else:
        atomo = LetrasProposicionales2[i]
    for T in L:
        if T.right.label == "-":
            T= Tree("Y", Tree("O", Tree("-", None, T.left), Tree("-", None, T.right.right)), Tree("O", T.left, T.right.right))
        elif T.right.label == "Y":
            T= Tree("Y", Tree("Y", Tree("O", T.right.left, Tree("-", None, T.left)), Tree("O", T.right.right, Tree("-", None, T.left))), Tree("O", Tree("O",Tree("-", None, T.right.left), Tree("-", None, T.right.right)), T.left))
        elif T.right.label == "O":
            T= Tree("Y", Tree("Y", Tree("O", Tree("-", None, T.right.left), T.left), Tree("O", Tree("-", None, T.right.right), T.left )), Tree("O", Tree("O",T.right.left, T.right.right), Tree("-", None, T.left)))
        elif T.right.label == ">":
            T= Tree("Y", Tree("Y", Tree("O", T.right.left, T.left), Tree("O", Tree("-", None, T.right.right), T.left)), Tree("O", Tree("O", Tree("-", None, T.right.left), T.right.right), Tree("-", None, T.left)))
        B += "Y" + inorder(T)
    B = atomo + B
    return B

def TseitinJL(T, LetrasProposicionales):
    #Dada una formula T, halla una formula T' igual de buena que T en forma normal conjuntiva
    #Input: T formula como Tree
    #       LetrasProposicionales, lista de strings
    #Output: Formula como Tree en forma normal conjuntiva
    T = elim_doble_negacion(T)
    A = inorder(T)
    LetrasProposicionales2 = [chr(x) for x in range(1400, 1899)]
    L  = []
    pila = []
    i = -1
    s = A [0]
    while len(A) > 0:
        if s in LetrasProposicionales and len(pila) > 0 and pila[-1] == "-":
            i += 1
            atomo = LetrasProposicionales2[i]
            pila = pila[:-1]
            pila.append(atomo)
            L.append(Tree("=", Tree(atomo,None,None), Tree("-",None, Tree(s, None, None))))
            A = A[1:]
            if len(s)>0:
                s = A[0]
        elif s == ")":
            w = pila[-1]
            o = pila[-2]
            v = pila[-3]
            pila = pila[:len(pila) -4]
            i += 1
            atomo = LetrasProposicionales2[i]
            L.append(Tree("=", Tree(atomo, None, None), Tree(o, Tree(v, None, None), Tree(w,None, None))))
            s = atomo
        else:
            pila.append(s)
            A = A[1:]
            if len(A)>0:
                s = A[0]
    B = ""
    if i < 0:
        atomo = pila[-1]
    else:
        atomo = LetrasProposicionales2[i]
    for T in L:
        if T.right.label == "-":
            T= Tree("Y", Tree("O", Tree("-", None, T.left), Tree("-", None, T.right.right)), Tree("O", T.left, T.right.right))
        elif T.right.label == "Y":
            T= Tree("Y", Tree("Y", Tree("O", T.right.left, Tree("-", None, T.left)), Tree("O", T.right.right, Tree("-", None, T.left))), Tree("O", Tree("O",Tree("-", None, T.right.left), Tree("-", None, T.right.right)), T.left))
        elif T.right.label == "O":
            T= Tree("Y", Tree("Y", Tree("O", Tree("-", None, T.right.left), T.left), Tree("O", Tree("-", None, T.right.right), T.left )), Tree("O", Tree("O",T.right.left, T.right.right), Tree("-", None, T.left)))
        elif T.right.label == ">":
            T= Tree("Y", Tree("Y", Tree("O", T.right.left, T.left), Tree("O", Tree("-", None, T.right.right), T.left)), Tree("O", Tree("O", Tree("-", None, T.right.left), T.right.right), Tree("-", None, T.left)))
        B += "Y" + inorder(T)
    B = atomo + B
    return B

def forma_clausal(formula):
    # Crea una formula en su forma clausal dada una formula en forma normal conjuntiva
    #Input: formula, formula como Tree en forma normal conjuntiva
    #Output: Formula en su forma clausal
    lista = []
    count = 0
    while len(formula)>0:
        if count == len(formula) or formula[count] == "Y":
            lista1 = formula[:count]
            lista2 = []
            while len(lista1)>0:
                caracter = lista1[0]
                if caracter in ["O", "(" ,")"]:
                    lista1 = lista1[1:]
                elif caracter == "-":
                    literal = caracter + lista1[1]
                    lista2.append(literal)
                    lista1 = lista1[2:]
                else:
                    lista2.append(caracter)
                    lista1 = lista1[1:]
            lista.append(lista2)
            formula = formula[count+1:]
            count = 0
        else:
            count +=1
    string = ""
    listaFinal = []
    for i in lista:
        for j in i:
            string += j
        listaFinal.append(string)
        string = ""
    return listaFinal

def clausulaUnitaria(lista):
    #Encuentra una clausula unitaria en una lista de strings
    #Input: lista, Lista de strings
    #Output:Clausula unitaria
    for i in lista:
        if (len(i)==1):
            return i
        elif (len(i)==2 and i[0]=="-"):
            return i
    return None

## Clausula Vacía

def clausulaVacia(lista):
    #Verifica si una lista contiene una clausula vacía
    #Input: lista, lista de strings
    #Output: booleano
    for i in lista:
        if(i==''):
            return(True)
    return False
#interps= {}

## Unit Propagate

def unitPropagate(lista,interps):
    # Hace Unit Propagate a un conjunto de clausulas
    #Input: lista, lista de strings (formula en forma clausal)
    #       interps, diccionario (interpretacion parcial)
    #Output: lista, lista de strings (formula en forma clausal)
    #        interps, diccionario con interpretaciones parciales
    x = clausulaUnitaria(lista)
    while(x!= None and clausulaVacia(lista)!=True):
        if (len(x)==1):
            interps[str(x)]=1
            j = 0
            for i in range(0,len(lista)):
                lista[i]=re.sub('-'+x,'',lista[i])
            for i in range(0,len(lista)):
                if(x in lista[i-j]):
                    lista.remove(lista[i-j])
                    j+=1
        else:
            interps[str(x[1])]=0
            j = 0
            for i in range(0,len(lista)):
                if(x in lista[i-j]):
                    lista.remove(lista[i-j])
                    j+=1
            for i in range(0,len(lista)):
                lista[i]=re.sub(x[1],'',lista[i])
        x = clausulaUnitaria(lista)
    return(lista, interps)

## Literal Complemento

def literal_complemento(lit):
    #Encuentra el literal complemento de un literal
    #Input:Literal
    #Output:Literal complemento.
    if lit[0] == "-":
        return lit[1]
    else:
        lit = "-" + lit
        return lit
## DPLL

def DPLL(lista, interps):
    #Verifica si una formula es satisfacible
    #Input: lista, lista de strings (formula en forma clausal)
    #       interps, diccionario (interpretacion parcial)
    #Output: lista, lista de strings (formula en forma clausal)
    #        interps, diccionario (interpretacion parcial)
    lista, interps = unitPropagate(lista,interps)
    if(len(lista)==0):
        listaFinal = lista
        interpsFinal = interps
        return(lista,interps)
    elif("" in lista):
        listaFinal = lista
        interpsFinal = interps
        return (lista,{})
    else:
        listaTemp = [x for x in lista]
        for l in listaTemp[0]:
            if (len(listaTemp)==0):
                return (listaTemp, interps)
            if (l not in interps.keys() and l!='-'):
                break
        listaTemp.insert(0,l)
        lista2, inter2 = DPLL(listaTemp, interps)
        if inter2 == {}:
            listaTemp = [x for x in lista]
            a =literal_complemento(l)
            listaTemp.insert(0,a)
            lista2, inter2 = DPLL(listaTemp, interps)
        return lista2, inter2

## Interps final

def interpsFinal(interps, LetrasProposicionales):
    #Dada una interpretacion ecuentra la interpretacion correspondiente usando solo las letras
    #proposicionales necesarias.
    #Input:Iterpretacion con todas las letras de LetrasProposicionales2
    #Output:Interpretacion con las letras de LetrasProposicionales
    interpsf = {i: interps[i] for i in LetrasProposicionales if i in interps}
    return interpsf

## RESULTADO

def DPLLResultado(lista, LetrasProposicionales):
    #Encuentra la interpretacion usando DPLL
    #Input:lista en forma clausal
    #Output:Interpretacion
    lista, inter = DPLL(lista,{})
    interpretacion = interpsFinal(inter, LetrasProposicionales)
    return interpretacion

def codifica(f, c, Nf, Nc):
    # Funcion que codifica la fila f y columna c
    assert((f >= 0) and (f <= Nf - 1)), 'Primer argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nf) - 1  + "\nSe recibio " + str(f)
    assert((c >= 0) and (c <= Nc - 1)), 'Segundo argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nc - 1)  + "\nSe recibio " + str(c)
    n = Nc * f + c
    # print(u'Número a codificar:', n)
    return n

def decodifica(n, Nf, Nc):
    # Funcion que codifica un caracter en su respectiva fila f y columna c de la tabla
    assert((n >= 0) and (n <= Nf * Nc - 1)), 'Codigo incorrecto! Debe estar entre 0 y' + str(Nf * Nc - 1) + "\nSe recibio " + str(n)
    f = int(n / Nc)
    c = n % Nc
    return f, c

def codifica3(f, c, o, Nf, Nc, No):
    # Funcion que codifica tres argumentos
    assert((f >= 0) and (f <= Nf - 1)), 'Primer argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nf - 1) + "\nSe recibio " + str(f)
    assert((c >= 0) and (c <= Nc - 1)), 'Segundo argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nc - 1) + "\nSe recibio " + str(c)
    assert((o >= 0) and (o <= No - 1)), 'Tercer argumento incorrecto! Debe ser un numero entre 0 y ' + str(No - 1)  + "\nSe recibio " + str(o)
    v1 = codifica(f, c, Nf, Nc)
    v2 = codifica(v1, o, Nf * Nc, No)
    return v2

def decodifica3(codigo, Nf, Nc, No):
    # Funcion que codifica un caracter en su respectiva fila f, columna c y objeto o
    v1, o = decodifica(codigo, Nf * Nc, No)
    f, c = decodifica(v1, Nf, Nc)
    return f, c, o

def P(fila, columna, signo, turno, numfilas, numcolumnas, numsignos, numturnos):
    v1 = codifica3(fila, columna, signo, numfilas, numcolumnas, numsignos)
    v2 = codifica(v1, turno, numfilas*numcolumnas*numsignos, numturnos)
    codigo = chr(256 + v2)
    return codigo

def Pinv(codigo, numfilas, numcolumnas, numsignos, numturnos):
    v2 = ord(codigo) - 256
    v1, turno = decodifica(v2, numfilas*numcolumnas*numsignos, numturnos)
    fila, columna, signo = decodifica3(v1, numfilas, numcolumnas, numsignos)
    return fila, columna, signo, turno

def Inorderp(f):
    if f.right == None:
        return "P" + str(Pinv(f.label, Nfilas, Ncolumnas, Nnumeros, Nturnos))
    elif f.label == '-':
        return f.label + Inorderp(f.right)
    else:
        return "(" + Inorderp(f.left) + f.label + Inorderp(f.right) + ")"

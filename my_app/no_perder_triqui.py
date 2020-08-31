import funciones_logica as Fun

letras = []
Nfilas = 3
Ncolumnas = 3
Nnumeros = 3
Nturnos = 2
filas=[0,1,2]
columnas =[0,1,2]


for fila in range(Nfilas):
    for columna in range(Ncolumnas):
        for signo in range(Nnumeros):
            for turno in range (Nturnos):
                letras.append(Fun.P(fila,columna,signo,turno,Nfilas,Ncolumnas,Nnumeros,Nturnos))

# Parte E: Evitar columna
inicial=True
E = ""
for c in columnas:
    for f in filas:
        inicial1 = True
        for a in filas:
            if a != f and inicial1:
                clau = Fun.P(a,c,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
                inicial1 = False
            elif a != f:
                 clau += Fun.P(a,c,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
        if inicial:
            E = Fun.P(f,c,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>'
            inicial = False
        else:
            E += Fun.P(f,c,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>' + 'Y'

# Parte F: Evitar fila
inicial=True
for f in filas:
    for c in columnas:
        inicial1 = True
        for a in columnas:
            if a != c and inicial1:
                clau = Fun.P(f,a,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
                inicial1 = False
            elif a != c:
                 clau += Fun.P(f,a,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
        if inicial:
            F = Fun.P(f,c,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>'
            inicial = False
        else:
            F += Fun.P(f,c,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>' + 'Y'

#Parte G: Evitar columna principal
inicial=True
for a in columnas:
    inicial1 = True
    for b in columnas:
        if a != b and inicial1:
            clau = Fun.P(b,b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
            inicial1 = False
        elif a != b:
            clau += Fun.P(b,b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
    if inicial:
        G = Fun.P(a,a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau +  '>'
        inicial = False
    else:
        G += Fun.P(a,a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>' + 'Y'

#Parte H: Evitar columna secundaria
inicial=True
for a in columnas:
    inicial1 = True
    for b in columnas:
        if a != b and inicial1:
            clau = Fun.P(b,2-b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos)
            inicial1 = False
        elif a != b:
            clau += Fun.P(b,2-b,2,0,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
    if inicial:
        H = Fun.P(a,2-a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau + '>'
        inicial = False
    else:
        H += Fun.P(a,2-a,1,1,Nfilas, Ncolumnas, Nnumeros, Nturnos) + clau +  '>' + 'Y'

def regla_ganador():
    inicial = True
    for n in range (1,3):
        for t in range (Nturnos):
            if inicial:
                D = Fun.P(0,2,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + Fun.P(1,1,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + Fun.P(2,0,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y'
                inicial = False
            else:
                D += Fun.P(0,2,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + Fun.P(1,1,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + Fun.P(2,0,n,t,Nfilas, Ncolumnas, Nnumeros, Nturnos) + 'Y' + 'O'

    return D

# Regla completa y solucion
#regla_ganar = E + F + 'Y' + G + 'Y' + H + 'Y'
#regla_ganar = regla_ganador()
#arbol = Fun.String2Tree(regla_ganar,letras)
#tseitin = Fun.TseitinJL(arbol, letras)
#clausal = Fun.forma_clausal(tseitin)
#interpretacion = Fun.DPLLResultado(clausal, letras)
#print(interpretacion)
tree = Fun.String2Tree(regla_ganador(),letras)
print(Fun.Inorderp(tree))

 #(((P(1, 2, 2, 0)YP(0, 2, 2, 0))>P(2, 2, 1, 1))Y(((P(2, 2, 2, 0)YP(0, 2, 2, 0))>P(1, 2, 1, 1))Y(((P(2, 2, 2, 0)YP(1, 2, 2, 0))>P(0, 2, 1, 1))Y(((P(1, 1, 2, 0)YP(0, 1, 2, 0))>P(2, 1, 1, 1))Y(((P(2, 1, 2, 0)YP(0, 1, 2, 0))>P(1, 1, 1, 1))Y(((P(2, 1, 2, 0)YP(1, 1, 2, 0))>P(0, 1, 1, 1))Y(((P(1, 0, 2, 0)YP(0, 0, 2, 0))>P(2, 0, 1, 1))Y(((P(2, 0, 2, 0)YP(0, 0, 2, 0))>P(1, 0, 1, 1))Y((P(2, 0, 2, 0)YP(1, 0, 2, 0))>P(0, 0, 1, 1))))))))))

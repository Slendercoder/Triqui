import funciones_logica as F

letras = []
numfilas = 3
numcolumnas = 3
numsignos = 3
numturnos = 2

for fila in range(numfilas):
    for columna in range(numcolumnas):
        for signo in range(numsignos):
            for turno in range (numturnos):
                letras.append(F.P(fila,columna,signo,turno,numfilas,numcolumnas,numsignos,numturnos))

# Parte A: Rellenar columna
inicial = True
for f in range(numfilas):
    for c in range(numcolumnas):
        if inicial:
            A = F.P(f, (c+2)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P(f, c, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P(f, (c+1)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + 'Y' + '>'
            inicial = False
        else:
            A += F.P(f, (c+2)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P(f, c, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P(f, (c+1)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + 'Y' + '>' + 'Y'

# Parte B: Rellenar fila
inicial = True
for f in range(numfilas):
    for c in range(numcolumnas):
        if inicial:
            B = F.P((f+2)%3, c, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P(f, c, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P((f+1)%3, c, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + 'Y' + '>'
            inicial = False
        else:
            B += F.P((f+2)%3, c, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P(f, c, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P((f+1)%3, c, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + 'Y' + '>' + 'Y'

# Parte C: Rellenar diagonal principal
inicial = True
for a in range(numfilas):
    if inicial:
        C = F.P((a+2)%3, (a+2)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P((a+1)%3, (a+1)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P(a, a, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + 'Y' + '>'
        inicial = False
    else:
        C += F.P((a+2)%3, (a+2)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P((a+1)%3, (a+1)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P(a, a, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + 'Y' + '>' + 'Y'

# Parte D: Rellenar diagonal secundaria
inicial = True
for f in range(numfilas):
    c = 2-f
    if inicial:
        D = F.P((f-2)%3, (c+2)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P((f-1)%3, (c+1)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P(f, c, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + 'Y' + '>'
        inicial = False
    else:
        D += F.P((f-2)%3, (c+2)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P((f-1)%3, (c+1)%3, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + F.P(f, c, 0, 0, numfilas, numcolumnas, numsignos, numturnos) + 'Y' + '>' + 'Y'

# Regla completa y solucion
regla_ganar = A + B + 'Y' + C + 'Y' + D + 'Y'
arbol = F.String2Tree(regla_ganar,letras)
tseitin = F.Tseitin(arbol, letras)
clausal = F.forma_clausal(tseitin)
interpretacion = F.DPLLResultado(clausal, letras)
print(interpretacion)
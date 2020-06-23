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

def P(f, c, o, t, Nf, Nc, No, Nt):
    # Funcion que codifica cuatro argumentos
    assert((f >= 0) and (f <= Nf - 1)), 'Primer argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nf - 1) + "\nSe recibio " + str(f)
    assert((c >= 0) and (c <= Nc - 1)), 'Segundo argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nc - 1) + "\nSe recibio " + str(c)
    assert((o >= 0) and (o <= No - 1)), 'Tercer argumento incorrecto! Debe ser un numero entre 0 y ' + str(No - 1)  + "\nSe recibio " + str(o)
    assert((t >= 0) and (t <= Nt - 1)), 'Cuarto argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nt - 1)  + "\nSe recibio " + str(t)
    v1 = codifica(f, c, Nf, Nc)
    v2 = codifica(v1, o, Nf * Nc, No)
    v3 = codifica(v2, t, Nf * Nc * No, Nt)
    codigo = chr(256 + v3)
    return codigo

def Pinv(codigo, Nf, Nc, No, Nt):
    # Funcion que codifica un caracter en su respectiva fila f, columna, objeto o y turno n
    x = ord(codigo) - 256
    v2, t = decodifica(x, Nf * Nc * No, Nt)
    v1, o = decodifica(v2, Nf * Nc, No)
    f, c = decodifica(v1, Nf, Nc)
    return f, c, o, t

def imprime(tablero):
    print("Turno -", tablero[0][3])
    for l in tablero:
        print(l[0:3])

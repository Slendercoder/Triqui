from Logica import *
from Minmax import *
from Codificacion import *
import numpy as np
from Reglas import regla1, regla2, regla3, regla4, regla5

Nfilas = 3
Ncolumnas = 3
Nnumeros = 3 # Se asume que E es 0, O es 1, X es 2
Nturnos = 2

regla = regla5()
# regla = regla1() + regla2() + 'Y' + regla3() + 'Y' + regla4() + 'Y' + regla5() + 'Y'
# print(regla)
f = String2Tree(regla)
# print(Inorderp(f))

T = triqui()
s = T.estado_inicial()
s = T.transicion(s, (1,1))
s = T.transicion(s, (2,0))
s = T.transicion(s, (1,0))
s = T.transicion(s, (1,2))
s = T.transicion(s, (0,0))
s = T.transicion(s, (2,2))
s = T.transicion(s, (0,2))
# s = T.transicion(s, (0,1))
print(s)
I = tablero2interpretacion(s)
# print(I)

# s1 = T.estado_inicial()
# s1 = T.transicion(s1, (1,1))
# s1 = T.transicion(s1, (0,0))
# s1 = T.transicion(s1, (2,2))
# s1 = T.transicion(s1, (1,0))
# s1 = T.transicion(s1, (2,1))
# s1 = T.transicion(s1, (1,2))

s1 = T.transicion(s, (2,1))

print("")
print(s1)
I = actualiza_interpretacion(s1, I)
# print(I)

print(V_I(f, I))

a = jugar_dpll(s)
print(a)

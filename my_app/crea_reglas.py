from Reglas import *
import json

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

from random import choice

def complemento(l):
    # Devuelve el complemento de un literal
    # Input: l, que es una cadena con un literal (ej: p, -p)
    # Output: l complemento
    if '-' in l:
        return l[1:]
    else:
        return '-' + l

def unitPropagation(S, I):
    # Algoritmo para eliminar clausulas unitarias de un conjunto de clausulas, manteniendo su satisfacibilidad
    # Input: Conjunto de clausulas S, interpretacion I (diccionario {literal: True/False})
    # Output: Conjunto de clausulas S, interpretacion I (diccionario {literal: True/False})

    while [] not in S:
        unit = ""
        for x in S:
            if len(x) == 1:
                unit = x[0]
                break
        if len(unit) == 0:
            break
        complement = complemento(unit)
        S = [x for x in S if unit not in x]
        for x in S:
            if complement in x:
                x.remove(complement)
        if '-' in unit:
            I[complement] = 0
        else:
            I[unit] = 1
    return S, I

def DPLL(S, I):
    # Algoritmo para verificar la satisfacibilidad de una formula, y encontrar un modelo de la misma
    # Input: Conjunto de clausulas S, interpretacion I (diccionario literal->True/False)
    # Output: String Satisfacible/Insatisfacible, interpretacion I (diccionario literal->True/False)

    # print("Entra a unitPropagate")
    # print('S', S, 'I', I)

    S, I = unitPropagation(S, I)

    # print("Sale de unitPropagate")
    # print('S', S, 'I', I)

    if len(S) == 0:
        return "Satisfacible", I
    if [] in S:
        return "Insatisfacible", {}
    literales = []
    for x in S:
        for y in x:
            if y not in literales:
                literales.append(y)
    literal = choice(literales)
    complement = complemento(literal)
    newS = [y for y in S if literal not in y]
    for z in newS:
        if complement in z:
            z.remove(complement)
    newI = I
    if '-' in literal:
        newI[complement] = 0
    else:
        newI[literal] = 1
    sat, newI = DPLL(newS, newI)
    if sat == "Satisfacible":
        return sat, newI
    else:
        newS = [y for y in S if complement not in y]
        for z in newS:
            if literal in z:
                z.remove(literal)
        newI = I
        if '-' in complement:
            newI[literal] = 0
        else:
            newI[complement] = 1
        return DPLL(newS, newI)

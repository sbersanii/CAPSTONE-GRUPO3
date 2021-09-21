from datos import Flujos, Tonelaje, P, Profit
import pandas as pd

P_original = P.copy()

#Construir un cono (lista con IDs) a partir de bloque base (id_base)
def constructor_conos(id_base, lista_bloques, P):
    if len(P[f"{id_base}"]) == 0:
        lista_bloques.append(id_base)
        return id_base
    else:
        lista_predecesores = list()
        for id_predecesor in P[f"{id_base}"]:
            if id_predecesor not in lista_bloques:
                lista_bloques.append(id_predecesor)
                lista_predecesores.append(constructor_conos(id_predecesor, lista_bloques, P))
        return [id_base, lista_predecesores]

    
#Función utilizada para aplanar la lista conos: lista de listas irregulares.
#https://stackabuse.com/python-how-to-flatten-list-of-lists/
def aplanar(lista_de_listas):
    if isinstance(lista_de_listas, list):
        if len(lista_de_listas) == 0:
            return lista_de_listas
        if isinstance(lista_de_listas[0], list):
            return aplanar(lista_de_listas[0]) + aplanar(lista_de_listas[1:])
        return lista_de_listas[:1] + aplanar(lista_de_listas[1:])
    else:
        return lista_de_listas

#Calculo del valor total de un cono (Flujo máx)
def valor_total(cono):
    if isinstance(cono, list):
        valor_final = 0
        for bloque in cono:
            valor1 = Flujos[f"{bloque}"][str(1)]
            valor2 = Flujos[f"{bloque}"][str(2)]
            valor_final += max(valor1, valor2)

        return valor_final
    else:
        valor1 = Flujos[f"{cono}"][str(1)]
        valor2 = Flujos[f"{cono}"][str(2)]

        return max(valor1, valor2)

#Calculo del tonelaje total de un cono
def tonelaje_total(cono):
    if isinstance(cono, list):
        tonelaje_final = 0
        for bloque in cono:
            tonelaje_final += Tonelaje[bloque]

        return tonelaje_final
    else:
        return Tonelaje[cono]

def ordenar_conos(lista_conos):
    lista_conos.sort(key=lambda x: x[1], reverse=True)

    return lista_conos

def comprobar_disponibilidad(id_base, conos_seleccionados):
    if len(conos_seleccionados) == 0:
        return True
    else:
        disponible = True
        for cono in conos_seleccionados:
            if isinstance(cono, list):
                for bloque in cono:
                    if bloque == id_base:
                        disponible = False
            else:
                if cono == id_base:
                    disponible = False
        return disponible


def seleccionar_solucion(soluciones_periodo):
    mejor_solucion = [None, 0]
    for solucion in soluciones_periodo:
        if solucion[1] > mejor_solucion[1]:
            mejor_solucion = solucion

    return mejor_solucion

def actualizar_conjuntos(sol, B, P): # sol: [variables, VO]
    for variable in sol[0]:
        if variable[0][0] == "x":
            if variable[1] == 1:
                bloque = variable[0][2:]
                B.remove(int(bloque))
                del P[bloque]
                for key in P.keys():
                    for bloque_precedente in P[key]:
                        if bloque_precedente == int(bloque):
                            P[key].remove(int(bloque))

    return B, P

def crear_conjunto_P(bloques):
    Precedencias = dict()
    for key in P_original.keys():
        if int(key) in bloques:
            Precedencias[key] = list()
            for bloque_precedente in P_original[key]:
                if bloque_precedente in bloques:
                    Precedencias[key].append(bloque_precedente)

    return Precedencias

def crear_conjunto_B(soluciones_RSC, periodo, w): #Soluciones_RSC: [[t0, solt0], [t1, solt1], ...]
    Bloques = list()
    for i in range(w):
        t = periodo - i
        for solucion in soluciones_RSC:
            if solucion[0] == t:
                for variable in solucion[1]:
                    if variable[0][0] == "x":
                        if variable[1] == 1:
                            indices = variable[0].split("_")
                            id_bloque = int(indices[1])
                            Bloques.append(id_bloque)
    
    return Bloques

def incluir_periodo(variables, periodo):
    for variable in variables:
        variable[0] = variable[0] + f"_{periodo}"

    return variables

def actualizar_valor_objetivo(soluciones_ventanas): # [[t, varst], [t2, varst2], ...]
    suma = 0
    for sol_periodo in soluciones_ventanas:
        for variable in sol_periodo[1]:
            if variable[0][0] == "y":
                indices = variable[0].split("_")
                suma += variable[1] * Profit[indices[1]][indices[2]][indices[3]]

    return suma

def actualizar_soluciones_ventanas(soluciones_ventanas, variables_ventana, w, periodo):
    minados = list()
    for i in range(w, 0, -1):
        t = periodo - i + 1
        sol = list()
        for variable in variables_ventana:
            if variable[0][0] == "x":
                if variable[1] == 1:
                    indices = variable[0].split("_")
                    if int(indices[2]) == t and (indices[1] not in minados):
                        sol.append(variable)
                        minados.append(indices[1])

            if variable[0][0] == "y":
                indices = variable[0].split("_")
                if int(indices[3]) == t:
                    if indices[1] in minados:
                        sol.append(variable)

            
        soluciones_ventanas[t] = [t, sol]

    return soluciones_ventanas

def comprobar_solucion(soluciones_ventanas):
    minados = list()
    for soluciones_periodo in soluciones_ventanas:
        for variable in soluciones_periodo[1]:
            if variable[0][0] == "x":
                minados.append(variable)

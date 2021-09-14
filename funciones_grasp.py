from datos import P, Flujos, Tonelaje

#Construir un cono (lista con IDs) a partir de bloque base (id_base)
def constructor_conos(id_base, lista_bloques):
    if len(P[f"{id_base}"]) == 0:
        lista_bloques.append(id_base)
        return id_base
    else:
        lista_predecesores = list()
        for id_predecesor in P[f"{id_base}"]:
            if id_predecesor not in lista_bloques:
                lista_bloques.append(id_predecesor)
                lista_predecesores.append(constructor_conos(id_predecesor, lista_bloques))
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
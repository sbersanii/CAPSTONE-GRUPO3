#Random solution contruction

from funciones_grasp import constructor_conos, aplanar, valor_total, tonelaje_total, ordenar_conos, comprobar_disponibilidad
from datos import B, T, D, R, P, Profit, Tonelaje, Recursos
from time import time
from random import uniform

p = 0.5
ro = 0.4
mu = 1.1
limite_recursos = Recursos[str(0)]

t0 = time()
for periodo in range(1):
    lista_conos = list()
    #Construcción de todos los conos en el modelo en t = periodo
    for bloque in B:
        cono = constructor_conos(bloque, [])
        cono = aplanar(cono)
        lista_conos.append([cono, valor_total(cono)])
    #Ordenamiento por valor de lista de todos los conos
    ordenar_conos(lista_conos)
    
    #Seleccion aleatoria de conos hasta límite de recursos x mu
    conos_seleccionados = list()
    recursos_utilizados = 0
    for cono in lista_conos:
        if recursos_utilizados < mu*limite_recursos:
            disponible = comprobar_disponibilidad(cono[0][0], conos_seleccionados)
            if disponible:
                if tonelaje_total(cono[0]) < 0.4*limite_recursos:
                    n_aleatorio = uniform(0, 1)
                    if n_aleatorio < p:
                        conos_seleccionados.append(cono[0])
                        recursos_utilizados += tonelaje_total(cono[0])
        else:
            break

print(f"Cantidad de conos seleccionados: {len(conos_seleccionados)}")
valor_solucion = 0
for cono in conos_seleccionados:
    valor_solucion += valor_total(cono)
print(f"Valor total de conos selccionados: {valor_solucion}")
print(f"Tiempo de construcción y seleccion de conos: {round(time() - t0, 2)} segundos")
print("\n")
#Random solution contruction
from funciones_grasp import constructor_conos, aplanar, valor_total, tonelaje_total, ordenar_conos, comprobar_disponibilidad
from datos import B, T, D, R, P, Profit, Tonelaje, Recursos
from MIP_model import solve_MIP

from gurobipy import Model
from time import time
from random import uniform

p = 0.5
ro = 0.4
mu = 1.1#?
n = 5
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
    lista_conos = ordenar_conos(lista_conos)

    t1 = time()
    print(f"Tiempo de construcción de conos del problema: {round(t1 - t0, 2)} segundos\n")
    
    #Seleccion aleatoria de conos hasta límite de recursos x mu
    soluciones = list()
    for i in range(n):
        conos_seleccionados = list()
        recursos_utilizados = 0
        for cono in lista_conos:
            if recursos_utilizados < mu*limite_recursos:
                if isinstance(cono[0], list):
                    disponible = comprobar_disponibilidad(cono[0][0], conos_seleccionados)
                else:
                    disponible = comprobar_disponibilidad(cono[0], conos_seleccionados)
                if disponible:
                    if tonelaje_total(cono[0]) < ro*limite_recursos:
                        n_aleatorio = uniform(0, 1)
                        if n_aleatorio < p:
                            conos_seleccionados.append(cono[0])
                            recursos_utilizados += tonelaje_total(cono[0])
            else:
                break

        #Resolución de modelo MIP
        solucion, obj = solve_MIP(conos_seleccionados)
        soluciones.append([solucion, obj])

    print(f"\nTiempo de {len(soluciones)} soluciones random sin tiempo de construcción de conos: {round(time() - t1, 2)} segundos")
    print(f"Tiempo total de construcción de {len(soluciones)} soluciones random: {round(time() - t0, 2)} segundos")

    print("\n")
    for i in range(n):
        print(f"Valor objetivo solución {i+1}: {round(soluciones[i][1], 2)}")
    print("\n")
#Random solution contruction
from funciones_grasp import constructor_conos, aplanar, valor_total, tonelaje_total, ordenar_conos, comprobar_disponibilidad, seleccionar_solucion, actualizar_conjuntos
from datos import B, T, D, R, P, Profit, Tonelaje, Recursos
from MIP_model import solve_MIP

from gurobipy import Model
from time import time
from random import uniform

###########  RANDOM SOLUTON CONSTRUCTION   ###########

p = 0.5
ro = 0.4
mu = 1.1#?
n = 5
w = 2

limite_recursos = Recursos[str(0)]

soluciones_RSC = list() #Soluciones Random Solution Construction

t0 = time()
for periodo in range(T):

    lista_conos = list()
    #Construcción de todos los conos en el modelo en t = periodo
    for bloque in B:
        cono = constructor_conos(bloque, [], P)
        cono = aplanar(cono)
        lista_conos.append([cono, valor_total(cono)])
    #Ordenamiento por valor de lista de todos los conos
    lista_conos = ordenar_conos(lista_conos)
    
    #Seleccion aleatoria de conos hasta límite de recursos x mu
    soluciones_periodo = list()
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
        solucion, obj = solve_MIP(conos_seleccionados, P)
        soluciones_periodo.append([solucion, obj])
        
    
    sol = seleccionar_solucion(soluciones_periodo)
    B, P = actualizar_conjuntos(sol, B, P)
    soluciones_RSC.append(sol)


###########  LOCAL IMPROVEMENT HEURISTIC   ###########


print(f"Tiempo total de Random Solution Construction: {round(time() - t0, 2)}")
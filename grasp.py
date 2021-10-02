#Random solution contruction
from funciones_grasp import constructor_conos, aplanar, valor_total, tonelaje_total, ordenar_conos, comprobar_disponibilidad, seleccionar_solucion, actualizar_conjuntos, crear_conjunto_P, crear_conjunto_B, incluir_periodo, actualizar_valor_objetivo, actualizar_soluciones_ventanas, comprobar_solucion
from MIP_model import solve_MIP, solve_MIP2

from gurobipy import Model
from time import time
from random import uniform

def ejecutar_grasp(B, T, D, R, P, Profit, Tonelaje, Recursos, P2):
    ###########  RANDOM SOLUTION CONSTRUCTION   ###########

    p = 0.5
    ro = 0.4
    mu = 1.1#?
    n = 5
    limite_recursos = Recursos[str(0)]

    soluciones_RSC = list() #Soluciones Random Solution Construction

    t0 = time()
    for periodo in range(T):
        t_conos = time()

        lista_conos = list()
        #Construcción de todos los conos en el modelo en t = periodo
        for bloque in B:
            cono = constructor_conos(bloque, [], P)
            cono = aplanar(cono)
            lista_conos.append([cono, valor_total(cono)])
        #Ordenamiento por valor de lista de todos los conos
        lista_conos = ordenar_conos(lista_conos)

        #print(f"Tiempo contrucción conos periodo {periodo}: {round(time() - t_conos, 2)}")
        
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
            variables, obj = solve_MIP(conos_seleccionados, P)
            soluciones_periodo.append([variables, obj])
            
        
        sol = seleccionar_solucion(soluciones_periodo) #sol = [vars, VO]
        B, P = actualizar_conjuntos(sol, B, P)
        soluciones_RSC.append([periodo, incluir_periodo(sol[0], periodo)]) #[[t, varst], [t2, varst2]]

        #print(f"Tiempo solución RSC completa periodo {periodo}: {round(time() - t_conos, 2)} segundos")

    #print(f"Tiempo total de Random Solution Construction: {round((time() - t0)/60, 2)} minutos")
    ###########  LOCAL IMPROVEMENT HEURISTIC   ###########

    w = 2
    gap = 0.000001 # %
    time_limit = 10 #minutos

    soluciones_ventanas = soluciones_RSC
    termino = False
    VO = 1
    t_inicio = time()
    while not termino:
        for t in range(T - w + 1):

            periodo = T - t - 1
            Bloques_ventana = crear_conjunto_B(soluciones_ventanas, periodo, w)
            Precedencias_ventana = crear_conjunto_P(Bloques_ventana, P2)
            variables_ventana, valor_ventana = solve_MIP2(Bloques_ventana, Precedencias_ventana, w, periodo)

            soluciones_ventanas = actualizar_soluciones_ventanas(soluciones_ventanas, variables_ventana, w, periodo)


        nuevo_VO = actualizar_valor_objetivo(soluciones_ventanas)
        #print(f"Valor objetivo actual: {nuevo_VO}")
        if (100*(nuevo_VO - VO)/VO) < gap:
            termino = True
            #print(f"Convergencia de la solución alcanzada (gap: {gap}%)")
            #print(f"Tiempo en alcanzar la convergencia: {round(time() - t_inicio, 2)} segundos")
        else:
            VO = nuevo_VO

        if (time() - t_inicio) >= (time_limit * 60):
            termino = True
            #print(f"Límite de tiempo alcanzado: {time_limit} minutos.")

    return VO, time()-t0

#print(f'Comparacion: {(2.222626362436*(10**7)) - nuevo_VO}')

#Formato solución: soluciones_ventanas = [[t0, [varst0]], [t1, [varst1]], ...]
from grasp import ejecutar_grasp
from datos2 import obtener_datos
from numpy import std

def run(iteraciones):
    suma_VO = 0
    lista_soluciones = list()
    tiempo_total = 0

    for i in range(iteraciones):
        B, T, D, R, P, Profit, Tonelaje, Recursos, P2, t_carga = obtener_datos()
        VO, tiempo, solucion = ejecutar_grasp(B, T, D, R, P, Profit, Tonelaje, Recursos, P2, i)
        suma_VO += VO
        lista_soluciones.append(VO)
        tiempo_total += tiempo - t_carga

    print(f"VO promedio: {suma_VO/iteraciones}")
    print(f"Desviación estándar: {std(lista_soluciones)}")
    print(f"Tiempo promedio: {tiempo_total/iteraciones}")

run(20)
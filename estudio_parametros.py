import os
import numpy as np

from grasp import ejecutar_grasp
from datos2 import obtener_datos
from funciones_grasp import comprobar_solucion
from parametros import dataset

ruta_guardado = os.path.join("Resultados Estudio Parametros", f"resultados.txt")
filesize = os.path.getsize(ruta_guardado)

if filesize == 0:
    with open(ruta_guardado, "wt", encoding = "UTF-8") as archivo:
        archivo.write("Iteración,Dataset,p,ro,mu,n,w,Valor Objetivo,Tiempo,Factibilidad\n")

def run(iteraciones, p, ro, mu, n, w):

    for i in range(iteraciones):
        B, T, D, R, P, Profit, Tonelaje, Recursos, P2, t_carga = obtener_datos()
        VO, tiempo, solucion = ejecutar_grasp(B, T, D, R, P, Profit, Tonelaje, Recursos, P2, i, p, ro, mu, n, w)
        factible = comprobar_solucion(solucion)

        with open(ruta_guardado, "a", encoding = "UTF-8") as archivo:
            archivo.write(f"{i},{dataset},{p},{ro},{mu},{n},{w},{VO},{tiempo - t_carga},{factible}\n")

#Ejemplo de iteraciones:
for mu in np.arange(1.1, 2, 0.1).tolist():
    run(1, 0.5, 0.4, mu, 5, 3)
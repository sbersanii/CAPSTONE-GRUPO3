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

#Rangos de parámetros a estudiar:
#p: [0.4, 0.6]
#ro: [0.3, 0.7]
#mu: [1, 3.5]

#Iteraciones stefano:
for ro in np.arange(0.3, 0.5, 0.1).tolist():
    for mu in np.arange(1, 4, 0.5).tolist():
        run(3, 0.6, ro, mu, 5, 2)

#Iteraciones nico alegria:
for ro in np.arange(0.5, 0.8, 0.1).tolist():
    for mu in np.arange(1, 4, 0.5).tolist():
        run(3, 0.6, ro, mu, 5, 2)

#Iteraciones nico greco:
for ro in np.arange(0.3, 0.5, 0.1).tolist():
    for mu in np.arange(1, 4, 0.5).tolist():
        run(3, 0.5, ro, mu, 5, 2)

#Iteraciones juan:
for ro in np.arange(0.5, 0.8, 0.1).tolist():
    for mu in np.arange(1, 4, 0.5).tolist():
        run(3, 0.5, ro, mu, 5, 2)

#Iteraciones javi:
for ro in np.arange(0.3, 0.5, 0.1).tolist():
    for mu in np.arange(1, 4, 0.5).tolist():
        run(3, 0.4, ro, mu, 5, 2)

#Iteraciones cata:
for ro in np.arange(0.5, 0.8, 0.1).tolist():
    for mu in np.arange(1, 4, 0.5).tolist():
        run(3, 0.4, ro, mu, 5, 2)

#Iteraciones clau:
for ro in np.arange(0.3, 0.8, 0.1).tolist():
    for mu in np.arange(1, 4, 0.5).tolist():
        run(3, 0.7, ro, mu, 5, 2)
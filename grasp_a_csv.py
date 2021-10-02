import os
from grasp import soluciones_ventanas, T

#Formato solución: soluciones_ventanas = [[t0, [varst0]], [t1, [varst1]], ...]
#Hay que tomar soluciones_ventanas y crear a conjunto de solución de todos los x
#Esto es: Cada bloque por cada periodo t, con su valor respectivo 1 o 0.

for t in range(T):

    var_names = list()

    for var in soluciones_ventanas[t][1]:
        if "x" == var[0][0] and var[0][-1] == f"{t}":
            var_names.append([var[0], str(var[1])])

    ruta_guardado = os.path.join("Resultados_Grasp", f"periodo_{t}.csv")
    with open(ruta_guardado, "wt", encoding = "UTF-8") as archivo:
        for lista in var_names:
            archivo.write(",".join(lista) + "\n")
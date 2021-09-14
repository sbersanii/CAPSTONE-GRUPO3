from gurobipy import GRB, quicksum, Model
from datos import R, D, Recursos, P, Flujos, Tonelaje

def solve_MIP(conos_seleccionados):
    #Construcción del conjunto B para el modelo MIP
    B_mip = list()
    for cono in conos_seleccionados:
        if isinstance(cono, list):
            for bloque in cono:
                if bloque not in B_mip:
                    B_mip.append(bloque)
        else:
            if cono not in B_mip:
                B_mip.append(cono)

    #Construcción del conjunto P para el modelo MIP, a partir de conjunto P original.
    P_mip = dict()
    for key in P.keys():
        if int(key) in B_mip:
            P_mip[key] = list()
            for bloque_precedente in P[key]:
                P_mip[key].append(bloque_precedente)

    #Creación del modelo:
    modelo = Model()

    #Variables
    x = {}
    y = {}

    for bloque in B_mip:
        x[bloque] = modelo.addVar(vtype = GRB.BINARY, name = f"x_{bloque}")
        for destino in D:
            y[bloque, destino] = modelo.addVar(vtype = GRB.CONTINUOUS, name = f"y_{bloque}_{destino}")

    #Restricciones

    #Tipo 1, (8) en formulación reducida, paper "Towards Solving ..."
    for bloque in B_mip:
        for bloque_precedente in P_mip[f"{bloque}"]:
            modelo.addConstr(x[bloque] <= x[bloque_precedente], 
            f"{bloque_precedente} precedente de {bloque}")

    #Tipo 2, (9) en formulación reducida, paper "Towards Solving ..."
    for bloque in B_mip:
        modelo.addConstr(quicksum(y[bloque, destino] for destino in D)
        == (x[bloque]))

    #Tipo 3, (10) en formulación reducida, paper "Towards Solving ..."
    for restriccion in R:
        modelo.addConstr(quicksum(quicksum(Tonelaje[bloque] * y[bloque, destino] for destino in D) for bloque in B_mip)
        <= Recursos[f"{restriccion}"])

    #Restricciones Naturaleza de Variables
    for destino in D:
        for bloque in B_mip:
            modelo.addConstr(y[bloque, destino] >= 0)

        for bloque in B_mip:
            modelo.addConstr(x[bloque] <= 1)
            modelo.addConstr(x[bloque] >= 0)

    #Función Objetivo
    FO = quicksum(quicksum(
         Flujos[f"{bloque}"][f"{destino}"] * y[bloque, destino]
         for destino in D) for bloque in B_mip)

    modelo.update()
    modelo.setObjective(FO, GRB.MAXIMIZE)
    modelo.optimize()

    solucion = list()
    for variable in modelo.getVars():
        solucion.append([variable.varName, variable.x])

    return solucion
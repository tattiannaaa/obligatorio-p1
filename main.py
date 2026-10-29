from entities.Criterio import Criterio
from entities.CasoUso import CasoUso
from exceptions.ErrorLaboratorio import ErrorLaboratorio

#Prueba de Criterio
c = Criterio(1, "Precisión", 5)
print(c)

try:
    malo = Criterio(2, "", 5)
except ErrorLaboratorio as e:
    print("Error atajado:", e)

#Prueba de CasoUso
caso = CasoUso(1, "Atención al cliente", 500, 7)
print(caso)

casos_malos = [
    (2, "", 500, 7),
    (3, "Ventas", -5, 7),
    (4, "Ventas", 500, 11),
]

for datos in casos_malos:
    try:
        CasoUso(datos[0], datos[1], datos[2], datos[3])
        print("ERROR: esto no debería haber andado:", datos)
    except ErrorLaboratorio as e:
        print("Atajado bien:", e)

cero = CasoUso(5, "Cero", 0, 0)
print(cero)
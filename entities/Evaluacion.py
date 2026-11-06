from datetime import datetime


class Evaluacion():
    FUERA_PRESUPUESTO = "fuera de presupuesto"
    PUNTAJE_INSUFICIENTE = "puntaje insuficiente"
    RECOMENDADA = "recomendada"

    FORMATO_FECHA = "%d/%m/%Y %H:%M:%S"

    def __init__(self, codigo, opcion, caso, criterios):
        self.__codigo = codigo
        self.__opcion = opcion
        self.__caso = caso
        self.__criterios = criterios
        self.__fecha = datetime.now()
        self.__estado = ""
        self.actualizar_estado()

    @property
    def codigo(self):
        return self.__codigo

    @property
    def opcion(self):
        return self.__opcion

    @property
    def caso(self):
        return self.__caso

    @property
    def fecha(self):
        return self.__fecha

    @property
    def estado(self):
        return self.__estado

    def fecha_texto(self):
        return self.__fecha.strftime(Evaluacion.FORMATO_FECHA)

    def costo_total(self):
        return self.__opcion.costo_estimado()

    def puntaje_total(self):
        suma_ponderada = 0
        suma_pesos = 0
        for criterio in self.__criterios:
            puntaje = self.__opcion.puntajes[criterio.codigo]
            suma_ponderada = suma_ponderada + puntaje * criterio.peso
            suma_pesos = suma_pesos + criterio.peso
        return suma_ponderada / suma_pesos

    def actualizar_estado(self):
        # Los montos se comparan redondeados a centavos para que errores de
        # punto flotante (ej. 0.1 * 3 = 0.30000000000000004) no hagan que un
        # costo igual al presupuesto quede "fuera de presupuesto".
        costo = round(self.costo_total(), 2)
        presupuesto = round(self.__caso.presupuesto, 2)
        puntaje = self.puntaje_total()
        minimo = self.__caso.puntaje_minimo

        if costo > presupuesto:
            self.__estado = Evaluacion.FUERA_PRESUPUESTO
        elif puntaje < minimo:
            self.__estado = Evaluacion.PUNTAJE_INSUFICIENTE
        else:
            self.__estado = Evaluacion.RECOMENDADA

    def __str__(self):
        return (
            f"Código de evaluación: {self.__codigo}\n"
            f"Fecha: {self.fecha_texto()}\n"
            f"Opción: {self.__opcion.nombre}\n"
            f"Caso de uso: {self.__caso.nombre}\n"
            f"Puntaje total: {self.puntaje_total():.2f}\n"
            f"Costo mensual: USD {self.costo_total():.2f}\n"
            f"Presupuesto: USD {self.__caso.presupuesto:.2f}\n"
            f"Estado: {self.__estado}"
        )

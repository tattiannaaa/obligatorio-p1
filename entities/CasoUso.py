from exceptions.ErrorLaboratorio import ErrorLaboratorio


class CasoUso:
    def __init__(self, codigo, nombre, presupuesto, puntaje_minimo):
        self.__codigo = codigo
        self.nombre = nombre
        self.presupuesto = presupuesto
        self.puntaje_minimo = puntaje_minimo

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ErrorLaboratorio("El nombre del caso de uso no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def presupuesto(self):
        return self.__presupuesto

    @presupuesto.setter
    def presupuesto(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ErrorLaboratorio("El presupuesto debe ser mayor o igual que cero.")
        self.__presupuesto = valor

    @property
    def puntaje_minimo(self):
        return self.__puntaje_minimo

    @puntaje_minimo.setter
    def puntaje_minimo(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0 or valor > 10:
            raise ErrorLaboratorio("El puntaje mínimo debe estar entre 0 y 10.")
        self.__puntaje_minimo = valor

    def __str__(self):
        return ("Código: " + str(self.__codigo)
                + " | Nombre: " + self.__nombre
                + " | Presupuesto: " + str(self.__presupuesto)
                + " | Puntaje mínimo: " + str(self.__puntaje_minimo))
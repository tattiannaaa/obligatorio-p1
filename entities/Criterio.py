from exceptions.ErrorLaboratorio import ErrorLaboratorio


class Criterio:
    def __init__(self, codigo, nombre, peso):
        self.__codigo = codigo
        self.nombre = nombre
        self.peso = peso

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ErrorLaboratorio("El nombre del criterio no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def peso(self):
        return self.__peso

    @peso.setter
    def peso(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ErrorLaboratorio("El peso debe ser un entero positivo.")
        self.__peso = valor

    def __str__(self):
        return "Código: " + str(self.__codigo) + " | Nombre: " + self.__nombre + " | Peso: " + str(self.__peso)
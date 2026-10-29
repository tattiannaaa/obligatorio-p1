from abc import ABC, abstractmethod
from exceptions.ErrorLaboratorio import ErrorLaboratorio

class OpcionIA(ABC):
    def __init__(self, codigo, nombre, puntajes):
        self.__codigo = codigo
        self.nombre = nombre
        self.puntajes = puntajes

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ErrorLaboratorio("El nombre de la opción no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def puntajes(self):
        return self.__puntajes

    @puntajes.setter
    def puntajes(self, valor):
        if not isinstance(valor, dict) or len(valor) == 0:
            raise ErrorLaboratorio("Los puntajes deben ser un diccionario con al menos un criterio.")
        for codigo_criterio in valor:
            puntaje = valor[codigo_criterio]
        if not isinstance(puntaje, int) or puntaje < 0 or puntaje > 10:
                raise ErrorLaboratorio("Cada puntaje debe ser un entero entre 0 y 10.")
        self.__puntajes = valor

    @abstractmethod
    def costo_estimado(self):
        pass

    def __str__(self):
        return "Código: " + str(self.__codigo) + " | Nombre: " + self.__nombre

class ServicioAPI(OpcionIA):
    def __init__(self, codigo, nombre, puntajes, costo_por_1000, consultas_estimadas):
        super().__init__(codigo, nombre, puntajes)
        self.costo_por_1000 = costo_por_1000
        self.consultas_estimadas = consultas_estimadas

    @property
    def costo_por_1000(self):
        return self.__costo_por_1000

    @costo_por_1000.setter
    def costo_por_1000(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ErrorLaboratorio("El costo por 1000 consultas no puede ser negativo.")
        self.__costo_por_1000 = valor

    @property
    def consultas_estimadas(self):
        return self.__consultas_estimadas   

    @consultas_estimadas.setter
    def consultas_estimadas(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ErrorLaboratorio("Las consultas estimadas deben ser un valor positivo.")
        self.__consultas_estimadas = valor

    def costo_estimado(self):
        return (self.__consultas_estimadas / 1000) * self.__costo_por_1000

    def __str__(self):
        return (super().__str() + " | Tipo: Servicio API"
                + " | Costo por 1000: " + str(self.__costo_por_1000)
                + " | Consultas estimadas: " + str(self.__consultas_estimadas))

class PlanMensual(OpcionIA):
    def __init__(self, codigo, nombre, puntajes, usuarios, costo_por_usuario):
        super().__init__(codigo, nombre, puntajes)
        self.costo_por_usuario = costo_por_usuario
        self.usuarios = usuarios

    @property
    def usuarios(self):
        return self.__usuarios

    @usuarios.setter   
    def usuarios(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ErrorLaboratorio("Los usuarios deben ser un entero positivo.")
        self.__usuarios = valor

    @property
    def costo_por_usuario(self):
        return self.costo_por_usuario

    @costo_por_usuario.setter
    def costo_por_usuario(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ErrorLaboratorio("El costo por usuario no debe ser negativo")
        self.costo_por_usuario = valor



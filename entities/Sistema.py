from entities.Criterio import Criterio
from entities.CasoUso import CasoUso
from entities.OpcionIA import ServicioAPI, PlanMensual
from entities.Evaluacion import Evaluacion
from exceptions.ErrorLaboratorio import ErrorLaboratorio


class Sistema:
    def __init__(self):
        self.__criterios = []
        self.__opciones = []
        self.__casos = []
        self.__evaluaciones = []
        self.__proximo_codigo_criterio = 1
        self.__proximo_codigo_opcion = 1
        self.__proximo_codigo_caso = 1
        self.__proximo_codigo_evaluacion = 1

    @property
    def criterios(self):
        return self.__criterios

    @property
    def opciones(self):
        return self.__opciones

    @property
    def casos(self):
        return self.__casos

    @property
    def evaluaciones(self):
        return self.__evaluaciones

    def __existe_nombre(self, lista, nombre):
        nombre_buscado = str(nombre).strip().lower()
        existe = False
        for elemento in lista:
            if elemento.nombre.lower() == nombre_buscado:
                existe = True
        return existe

    def __validar_nueva_opcion(self, nombre, puntajes):
        if len(self.__criterios) == 0:
            raise ErrorLaboratorio(
                "Debe existir al menos un criterio para registrar opciones."
            )

        if self.__existe_nombre(self.__opciones, nombre):
            raise ErrorLaboratorio("Ya existe una opción con ese nombre.")

        if not isinstance(puntajes, dict):
            raise ErrorLaboratorio("Los puntajes deben ser un diccionario.")

        if len(puntajes) != len(self.__criterios):
            raise ErrorLaboratorio("Debe ingresar un puntaje por cada criterio.")

        for criterio in self.__criterios:
            if criterio.codigo not in puntajes:
                raise ErrorLaboratorio(
                    "Falta el puntaje del criterio " + criterio.nombre + "."
                )

    def registrar_criterio(self, nombre, peso):
        if len(self.__opciones) > 0:
            raise ErrorLaboratorio(
                "No se pueden registrar criterios después de registrar la primera opción."
            )
        if self.__existe_nombre(self.__criterios, nombre):
            raise ErrorLaboratorio("Ya existe un criterio con ese nombre.")
        criterio = Criterio(self.__proximo_codigo_criterio, nombre, peso)
        self.__criterios.append(criterio)
        self.__proximo_codigo_criterio = self.__proximo_codigo_criterio + 1
        return criterio

    def registrar_caso(self, nombre, presupuesto, puntaje_minimo):
        if self.__existe_nombre(self.__casos, nombre):
            raise ErrorLaboratorio("Ya existe un caso con ese nombre.")
        caso = CasoUso(self.__proximo_codigo_caso, nombre, presupuesto, puntaje_minimo)
        self.__casos.append(caso)
        self.__proximo_codigo_caso = self.__proximo_codigo_caso + 1
        return caso

    def registrar_servicio_api(
        self, nombre, puntajes, costo_por_1000, consultas_estimadas
    ):
        self.__validar_nueva_opcion(nombre, puntajes)
        opcion = ServicioAPI(
            self.__proximo_codigo_opcion,
            nombre,
            puntajes,
            costo_por_1000,
            consultas_estimadas,
        )
        self.__opciones.append(opcion)
        self.__proximo_codigo_opcion = self.__proximo_codigo_opcion + 1
        return opcion

    def registrar_plan_mensual(self, nombre, puntajes, usuarios, costo_por_usuario):
        self.__validar_nueva_opcion(nombre, puntajes)
        opcion = PlanMensual(
            self.__proximo_codigo_opcion,
            nombre,
            puntajes,
            usuarios,
            costo_por_usuario,
        )
        self.__opciones.append(opcion)
        self.__proximo_codigo_opcion = self.__proximo_codigo_opcion + 1
        return opcion

    def buscar_opcion(self, codigo):
        encontrada = None
        for opcion in self.__opciones:
            if opcion.codigo == codigo:
                encontrada = opcion
        if encontrada is None:
            raise ErrorLaboratorio("No existe una opción con ese código.")
        return encontrada

    def buscar_caso(self, codigo):
        encontrado = None
        for caso in self.__casos:
            if caso.codigo == codigo:
                encontrado = caso
        if encontrado is None:
            raise ErrorLaboratorio("No existe un caso de uso con ese código.")
        return encontrado

    def registrar_evaluacion(self, codigo_opcion, codigo_caso):
        opcion = self.buscar_opcion(codigo_opcion)
        caso = self.buscar_caso(codigo_caso)

        for evaluacion in self.__evaluaciones:
            if (
                evaluacion.opcion.codigo == opcion.codigo
                and evaluacion.caso.codigo == caso.codigo
            ):
                raise ErrorLaboratorio(
                    "Ya existe una evaluación de "
                    + opcion.nombre
                    + " para "
                    + caso.nombre
                    + "."
                )

        evaluacion = Evaluacion(
            self.__proximo_codigo_evaluacion,
            opcion,
            caso,
            self.__criterios,
        )
        self.__evaluaciones.append(evaluacion)
        self.__proximo_codigo_evaluacion = self.__proximo_codigo_evaluacion + 1
        return evaluacion

    def comparar_caso(self, codigo_caso):
        caso = self.buscar_caso(codigo_caso)
        if len(self.__opciones) == 0:
            raise ErrorLaboratorio("No hay opciones registradas para comparar.")

        evaluaciones_que_quedan = []
        for evaluacion in self.__evaluaciones:
            if evaluacion.caso.codigo != caso.codigo:
                evaluaciones_que_quedan.append(evaluacion)
        self.__evaluaciones = evaluaciones_que_quedan

        nuevas = []
        for opcion in self.__opciones:
            evaluacion = Evaluacion(
                self.__proximo_codigo_evaluacion,
                opcion,
                caso,
                self.__criterios,
            )
            self.__evaluaciones.append(evaluacion)
            self.__proximo_codigo_evaluacion = self.__proximo_codigo_evaluacion + 1
            nuevas.append(evaluacion)

        return nuevas

    def recalcular(self):
        for evaluacion in self.__evaluaciones:
            evaluacion.actualizar_estado()

    def actualizar_presupuesto(self, codigo_caso, nuevo_presupuesto):
        caso = self.buscar_caso(codigo_caso)
        caso.presupuesto = nuevo_presupuesto
        self.recalcular()
        return caso

    def actualizar_servicio_api(
        self, codigo_opcion, costo_por_1000, consultas_estimadas
    ):
        opcion = self.buscar_opcion(codigo_opcion)
        if not isinstance(opcion, ServicioAPI):
            raise ErrorLaboratorio("La opcion seleccionada no es un Servicio API.")

        costo_anterior = opcion.costo_por_1000
        consultas_anteriores = opcion.consultas_estimadas
        try:
            opcion.costo_por_1000 = costo_por_1000
            opcion.consultas_estimadas = consultas_estimadas
        except ErrorLaboratorio:
            opcion.costo_por_1000 = costo_anterior
            opcion.consultas_estimadas = consultas_anteriores
            raise
        self.recalcular()
        return opcion

    def actualizar_plan_mensual(self, codigo_opcion, usuarios, costo_por_usuario):
        opcion = self.buscar_opcion(codigo_opcion)
        if not isinstance(opcion, PlanMensual):
            raise ErrorLaboratorio("La opción seleccionada no es un Plan mensual.")

        usuarios_anterior = opcion.usuarios
        costo_anterior = opcion.costo_por_usuario
        try:
            opcion.usuarios = usuarios
            opcion.costo_por_usuario = costo_por_usuario
        except ErrorLaboratorio:
            opcion.usuarios = usuarios_anterior
            opcion.costo_por_usuario = costo_anterior
            raise
        self.recalcular()
        return opcion

    def evaluaciones_de_caso(self, codigo_caso):
        caso = self.buscar_caso(codigo_caso)
        resultado = []
        for evaluacion in self.__evaluaciones:
            if evaluacion.caso.codigo == caso.codigo:
                resultado.append(evaluacion)
        return resultado

    def evaluaciones_de_opcion(self, codigo_opcion):
        opcion = self.buscar_opcion(codigo_opcion)
        resultado = []
        for evaluacion in self.__evaluaciones:
            if evaluacion.opcion.codigo == opcion.codigo:
                resultado.append(evaluacion)
        return resultado

    def cantidad_recomendadas(self, codigo_caso):
        contador = 0
        for evaluacion in self.evaluaciones_de_caso(codigo_caso):
            if evaluacion.estado == Evaluacion.RECOMENDADA:
                contador = contador + 1
        return contador

    def __clave_ranking(self, evaluacion):
        return (
            -evaluacion.puntaje_total(),
            evaluacion.costo_total(),
            evaluacion.opcion.codigo,
        )

    def ranking_de_caso(self, codigo_caso):
        recomendadas = []
        for evaluacion in self.evaluaciones_de_caso(codigo_caso):
            if evaluacion.estado == Evaluacion.RECOMENDADA:
                recomendadas.append(evaluacion)
        return sorted(recomendadas, key=self.__clave_ranking)

    def existe_criterio(self, nombre):
        return self.__existe_nombre(self.__criterios, nombre)

    def existe_opcion(self, nombre):
        return self.__existe_nombre(self.__opciones, nombre)

    def existe_caso(self, nombre):
        return self.__existe_nombre(self.__casos, nombre)

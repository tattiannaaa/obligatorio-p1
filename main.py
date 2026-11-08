from entities.Sistema import Sistema
from entities.OpcionIA import ServicioAPI
from exceptions.ErrorLaboratorio import ErrorLaboratorio

##Funciones para pedir datos


def pedir_texto(mensaje):
    valido = False
    texto = ""
    while not valido:
        texto = input(mensaje).strip()
        if texto == "":
            print("El campo no puede estar vacío.")
        else:
            valido = True
    return texto


def pedir_entero(mensaje, minimo, maximo=None):
    resultado = None
    while resultado is None:
        texto = input(mensaje).strip()
        try:
            numero = int(texto)
            if numero < minimo:
                print("El valor debe ser mayor o igual que " + str(minimo) + ".")
            elif maximo is not None and numero > maximo:
                print("El valor debe ser menor o igual que " + str(maximo) + ".")
            else:
                resultado = numero
        except ValueError:
            print("Debe ingresar un número entero.")
    return resultado


def pedir_decimal(mensaje, minimo, maximo=None):
    resultado = None
    while resultado is None:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            numero = float(texto)

            if numero != numero:
                print("Debe ingresar un número.")
            elif numero < minimo:
                print("El valor debe ser mayor o igual que " + str(minimo) + ".")
            elif maximo is not None and numero > maximo:
                print("El valor debe ser menor o igual que " + str(maximo) + ".")
            else:
                resultado = numero
        except ValueError:
            print("Debe ingresar un número.")
    return resultado


##Funciones para elegir un caso o una opción


def elegir_caso(sistema):
    if len(sistema.casos) == 0:
        print("No hay casos de uso registrados.")
        return None
    print("Casos de uso:")
    for caso in sistema.casos:
        print(str(caso.codigo) + ". " + caso.nombre)
    elegido = None
    while elegido is None:
        codigo = pedir_entero("Código del caso: ", 1)
        try:
            elegido = sistema.buscar_caso(codigo)
        except ErrorLaboratorio as e:
            print("Error:", e)
    return elegido


def elegir_opcion(sistema):
    if len(sistema.opciones) == 0:
        print("No hay opciones registradas.")
        return None
    print("Opciones de IA:")
    for opcion in sistema.opciones:
        print(str(opcion.codigo) + ". " + opcion.nombre)
    elegida = None
    while elegida is None:
        codigo = pedir_entero("Código de la opción: ", 1)
        try:
            elegida = sistema.buscar_opcion(codigo)
        except ErrorLaboratorio as e:
            print("Error:", e)
    return elegida


##Registrar


def registrar_criterio(sistema):
    print("Registrar criterio")
    if len(sistema.opciones) > 0:
        print(
            "No se pueden registrar criterios después de registrar la primera opción."
        )
        return

    nombre = ""
    nombre_valido = False
    while not nombre_valido:
        nombre = pedir_texto("Nombre del criterio: ")
        if sistema.existe_criterio(nombre):
            print("Ya existe un criterio con ese nombre.")
        else:
            nombre_valido = True

    peso = pedir_entero("Peso (entero positivo): ", 1)

    try:
        criterio = sistema.registrar_criterio(nombre, peso)
        print("Criterio registrado:", criterio)
    except ErrorLaboratorio as e:
        print("Error:", e)


def registrar_caso(sistema):
    print("Registrar caso de uso")

    nombre = ""
    nombre_valido = False
    while not nombre_valido:
        nombre = pedir_texto("Nombre del caso de uso: ")
        if sistema.existe_caso(nombre):
            print("Ya existe un caso de uso con ese nombre.")
        else:
            nombre_valido = True

    presupuesto = pedir_decimal("Presupuesto mensual en USD (mayor o igual que 0): ", 0)
    puntaje_minimo = pedir_decimal("Puntaje mínimo aceptable (0 a 10): ", 0, 10)

    try:
        caso = sistema.registrar_caso(nombre, presupuesto, puntaje_minimo)
        print("Caso registrado:", caso)
    except ErrorLaboratorio as e:
        print("Error:", e)


def registrar_opcion(sistema):
    print("Registrar opción de IA")
    if len(sistema.criterios) == 0:
        print("Debe existir al menos un criterio para registrar opciones.")
        return

    nombre = ""
    nombre_valido = False
    while not nombre_valido:
        nombre = pedir_texto("Nombre de la opción: ")
        if sistema.existe_opcion(nombre):
            print("Ya existe una opción con ese nombre.")
        else:
            nombre_valido = True

    tipo = pedir_entero("Tipo (1. Servicio API, 2. Plan mensual): ", 1, 2)

    if tipo == 1:
        costo_por_1000 = pedir_decimal("Precio por cada 1000 consultas (USD): ", 0)
        consultas = pedir_entero("Cantidad estimada de consultas al mes: ", 1)
    else:
        usuarios = pedir_entero("Cantidad de usuarios: ", 1)
        costo_por_usuario = pedir_decimal("Costo mensual por usuario (USD): ", 0)

    print("Ingrese un puntaje de 0 a 10 para cada criterio:")
    puntajes = {}
    for criterio in sistema.criterios:
        puntajes[criterio.codigo] = pedir_entero(
            criterio.nombre + " (peso " + str(criterio.peso) + "): ", 0, 10
        )

    try:
        if tipo == 1:
            opcion = sistema.registrar_servicio_api(
                nombre, puntajes, costo_por_1000, consultas
            )
        else:
            opcion = sistema.registrar_plan_mensual(
                nombre, puntajes, usuarios, costo_por_usuario
            )
        print("Opción registrada:", opcion)
        print("Costo mensual estimado:", opcion.costo_estimado())
    except ErrorLaboratorio as e:
        print("Error:", e)


def registrar_evaluacion_individual(sistema):
    print("Evaluación individual")
    opcion = elegir_opcion(sistema)
    if opcion is None:
        return
    caso = elegir_caso(sistema)
    if caso is None:
        return
    try:
        evaluacion = sistema.registrar_evaluacion(opcion.codigo, caso.codigo)
        print("Evaluación registrada:")
        print(evaluacion)
    except ErrorLaboratorio as e:
        print("Error:", e)


##Comparar


def comparar_opciones(sistema):
    print("\n-- Comparar opciones para un caso --")
    caso = elegir_caso(sistema)
    if caso is None:
        return
    try:
        nuevas = sistema.comparar_caso(caso.codigo)
        print("Resultado de la comparación para " + caso.nombre + ":")
        for evaluacion in nuevas:
            print(evaluacion)
    except ErrorLaboratorio as e:
        print("Error:", e)


##Actualizar


def actualizar_presupuesto_caso(sistema):
    print("Actualizar presupuesto de un caso")
    caso = elegir_caso(sistema)
    if caso is None:
        return
    nuevo = pedir_decimal("Nuevo presupuesto mensual en USD (mayor o igual que 0): ", 0)
    try:
        sistema.actualizar_presupuesto(caso.codigo, nuevo)
        cantidad = len(sistema.evaluaciones_de_caso(caso.codigo))
        print("Presupuesto actualizado. Evaluaciones recalculadas:", cantidad)
    except ErrorLaboratorio as e:
        print("Error:", e)


def actualizar_opcion(sistema):
    print("Actualizar precio o consumo de una opción")
    opcion = elegir_opcion(sistema)
    if opcion is None:
        return
    try:
        if isinstance(opcion, ServicioAPI):
            costo_por_1000 = pedir_decimal(
                "Nuevo precio por cada 1000 consultas (USD): ", 0
            )
            consultas = pedir_entero("Nueva cantidad estimada de consultas: ", 1)
            sistema.actualizar_servicio_api(opcion.codigo, costo_por_1000, consultas)
        else:
            usuarios = pedir_entero("Nueva cantidad de usuarios: ", 1)
            costo_por_usuario = pedir_decimal(
                "Nuevo costo mensual por usuario (USD): ", 0
            )
            sistema.actualizar_plan_mensual(opcion.codigo, usuarios, costo_por_usuario)
        print("Opción actualizada:", opcion)
        print("Nuevo costo mensual:", opcion.costo_estimado())
        print("Evaluaciones recalculadas.")
    except ErrorLaboratorio as e:
        print("Error:", e)


# "Listar


def listar_criterios(sistema):
    print("\n-- Criterios --")
    if len(sistema.criterios) == 0:
        print("No hay criterios registrados.")
        return
    for criterio in sistema.criterios:
        print(criterio)


def listar_opciones(sistema):
    print("Opciones de IA")
    if len(sistema.opciones) == 0:
        print("No hay opciones registradas.")
        return
    for opcion in sistema.opciones:
        print(opcion)
        print("   Costo mensual:", opcion.costo_estimado())
        for criterio in sistema.criterios:
            print(
                "   " + criterio.nombre + ": " + str(opcion.puntajes[criterio.codigo])
            )


def listar_casos(sistema):
    print("Casos de uso")
    if len(sistema.casos) == 0:
        print("No hay casos de uso registrados.")
        return
    for caso in sistema.casos:
        recomendadas = sistema.cantidad_recomendadas(caso.codigo)
        print(str(caso) + " | Recomendadas: " + str(recomendadas))


def listar_evaluaciones(sistema):
    print("Evaluaciones de un caso")
    caso = elegir_caso(sistema)
    if caso is None:
        return
    evaluaciones = sistema.evaluaciones_de_caso(caso.codigo)
    if len(evaluaciones) == 0:
        print("No existen evaluaciones para este caso.")
        return
    for ev in evaluaciones:
        print(
            str(ev.codigo)
            + " | "
            + ev.fecha.strftime("%d/%m/%Y %H:%M")
            + " | "
            + ev.opcion.nombre
            + " | Presupuesto del caso: "
            + str(ev.caso.presupuesto)
            + " | Costo: "
            + str(ev.costo_total())
            + " | Puntaje: "
            + format(ev.puntaje_total(), ".2f")
            + " | Estado: "
            + ev.estado
        )


def listar_ranking(sistema):
    print("Ranking de un caso")
    caso = elegir_caso(sistema)
    if caso is None:
        return
    ranking = sistema.ranking_de_caso(caso.codigo)
    if len(ranking) == 0:
        print("No hay opciones recomendadas para este caso.")
        return
    posicion = 1
    for ev in ranking:
        print(
            str(posicion)
            + ". "
            + ev.opcion.nombre
            + " | Puntaje: "
            + format(ev.puntaje_total(), ".2f")
            + " | Costo: "
            + str(ev.costo_total())
        )
        posicion = posicion + 1


##Menús


def menu_registrar(sistema):
    salir = False
    while not salir:
        print("Registrar")
        print("1. Criterio")
        print("2. Opción de IA")
        print("3. Caso de uso")
        print("4. Evaluación individual")
        print("5. Salir")
        opcion = pedir_entero("Elija una opción: ", 1, 5)
        if opcion == 1:
            registrar_criterio(sistema)
        elif opcion == 2:
            registrar_opcion(sistema)
        elif opcion == 3:
            registrar_caso(sistema)
        elif opcion == 4:
            registrar_evaluacion_individual(sistema)
        else:
            salir = True


def menu_actualizar(sistema):
    salir = False
    while not salir:
        print("Actualizar")
        print("1. Presupuesto de un caso")
        print("2. Precio o consumo de una opción")
        print("3. Salir")
        opcion = pedir_entero("Elija una opción: ", 1, 3)
        if opcion == 1:
            actualizar_presupuesto_caso(sistema)
        elif opcion == 2:
            actualizar_opcion(sistema)
        else:
            salir = True


def menu_listar(sistema):
    salir = False
    while not salir:
        print("Listar")
        print("1. Criterios")
        print("2. Opciones")
        print("3. Casos de uso")
        print("4. Evaluaciones de un caso")
        print("5. Ranking de un caso")
        print("6. Salir")
        opcion = pedir_entero("Elija una opción: ", 1, 6)
        if opcion == 1:
            listar_criterios(sistema)
        elif opcion == 2:
            listar_opciones(sistema)
        elif opcion == 3:
            listar_casos(sistema)
        elif opcion == 4:
            listar_evaluaciones(sistema)
        elif opcion == 5:
            listar_ranking(sistema)
        else:
            salir = True


def main():
    sistema = Sistema()
    salir = False
    while not salir:
        print("Comparador de opciones de IA")
        print("1. Registrar")
        print("2. Comparar opciones para un caso")
        print("3. Actualizar")
        print("4. Listar")
        print("5. Salir del sistema")
        opcion = pedir_entero("Elija una opción: ", 1, 5)
        if opcion == 1:
            menu_registrar(sistema)
        elif opcion == 2:
            comparar_opciones(sistema)
        elif opcion == 3:
            menu_actualizar(sistema)
        elif opcion == 4:
            menu_listar(sistema)
        else:
            salir = True
    print("Hasta luego.")


if __name__ == "__main__":
    main()

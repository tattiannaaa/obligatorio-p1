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
            if numero != numero or numero in (float("inf"), float("-inf")):
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


##Funciones de formato

def usd(monto):
    return f"USD {monto:.2f}"


def plural(cantidad, singular, plural_texto):
    if cantidad == 1:
        return singular
    return plural_texto


def imprimir_tabla(encabezados, filas):
    anchos = []
    for i in range(len(encabezados)):
        ancho = len(encabezados[i])
        for fila in filas:
            if len(fila[i]) > ancho:
                ancho = len(fila[i])
        anchos.append(ancho)

    lineas = [encabezados] + filas
    for fila in lineas:
        celdas = []
        for i in range(len(fila)):
            celdas.append(fila[i].ljust(anchos[i]))
        print("  ".join(celdas).rstrip())


def mostrar_tabla_opciones(sistema):
    filas = []
    for opcion in sistema.opciones:
        filas.append([
            str(opcion.codigo),
            opcion.nombre,
            opcion.tipo(),
            usd(opcion.costo_estimado()),
        ])
    imprimir_tabla(["Código", "Nombre", "Tipo", "Costo mensual"], filas)


def mostrar_tabla_casos(sistema):
    filas = []
    for caso in sistema.casos:
        filas.append([
            str(caso.codigo),
            caso.nombre,
            usd(caso.presupuesto),
            f"{caso.puntaje_minimo:.2f}",
        ])
    imprimir_tabla(["Código", "Nombre", "Presupuesto", "Puntaje mínimo"], filas)


def mostrar_tabla_evaluaciones(evaluaciones, mostrar_caso=False):
    # Por defecto la segunda columna es la opción; al actualizar una opción
    # interesa ver a qué caso pertenece cada evaluación.
    filas = []
    for ev in evaluaciones:
        if mostrar_caso:
            nombre = ev.caso.nombre
        else:
            nombre = ev.opcion.nombre
        filas.append([
            str(ev.codigo),
            nombre,
            f"{ev.puntaje_total():.2f}",
            usd(ev.costo_total()),
            ev.estado,
        ])
    if mostrar_caso:
        segunda_columna = "Caso de uso"
    else:
        segunda_columna = "Opción"
    imprimir_tabla(
        ["Código", segunda_columna, "Puntaje", "Costo mensual", "Estado"], filas
    )


##Funciones para elegir un caso o una opción

def elegir_caso(sistema):
    if len(sistema.casos) == 0:
        print("No hay casos de uso registrados.")
        return None
    print("\nCASOS DE USO")
    mostrar_tabla_casos(sistema)
    print()
    elegido = None
    while elegido is None:
        codigo = pedir_entero("Código del caso de uso: ", 1)
        try:
            elegido = sistema.buscar_caso(codigo)
        except ErrorLaboratorio as e:
            print("Error:", e)
    return elegido


def elegir_opcion(sistema):
    if len(sistema.opciones) == 0:
        print("No hay opciones registradas.")
        return None
    print("\nOPCIONES DISPONIBLES")
    mostrar_tabla_opciones(sistema)
    print()
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
    if len(sistema.opciones) > 0:
        print("No se pueden registrar criterios después de registrar la primera opción.")
        return

    nombre = ""
    nombre_valido = False
    while not nombre_valido:
        nombre = pedir_texto("Nombre del criterio: ")
        if sistema.existe_criterio(nombre):
            print("Ya existe un criterio con ese nombre.")
        else:
            nombre_valido = True

    peso = pedir_entero("Peso: ", 1)

    try:
        criterio = sistema.registrar_criterio(nombre, peso)
        print("\nCriterio registrado correctamente.")
        print("Código:", criterio.codigo)
        print("Nombre:", criterio.nombre)
        print("Peso:", criterio.peso)
    except ErrorLaboratorio as e:
        print("Error:", e)


def registrar_caso(sistema):
    nombre = ""
    nombre_valido = False
    while not nombre_valido:
        nombre = pedir_texto("Nombre del caso de uso: ")
        if sistema.existe_caso(nombre):
            print("Ya existe un caso de uso con ese nombre.")
        else:
            nombre_valido = True

    presupuesto = pedir_decimal("Presupuesto mensual en USD: ", 0)
    puntaje_minimo = pedir_decimal("Puntaje mínimo aceptable (0 a 10): ", 0, 10)

    try:
        caso = sistema.registrar_caso(nombre, presupuesto, puntaje_minimo)
        print("\nCaso de uso registrado correctamente.")
        print("Código:", caso.codigo)
        print("Nombre:", caso.nombre)
        print("Presupuesto mensual:", usd(caso.presupuesto))
        print(f"Puntaje mínimo: {caso.puntaje_minimo:.2f}")
    except ErrorLaboratorio as e:
        print("Error:", e)


def registrar_opcion(sistema):
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

    print("\nTipo de opción:")
    print("1. Servicio API")
    print("2. Plan mensual")
    tipo = pedir_entero("Seleccione un tipo: ", 1, 2)
    print()

    if tipo == 1:
        costo_por_1000 = pedir_decimal("Costo en USD por cada 1000 consultas: ", 0)
        consultas = pedir_entero("Cantidad de consultas mensuales estimadas: ", 1)
    else:
        usuarios = pedir_entero("Cantidad de usuarios: ", 1)
        costo_por_usuario = pedir_decimal("Costo mensual en USD por usuario: ", 0)

    print("\nPUNTAJES POR CRITERIO")
    puntajes = {}
    for criterio in sistema.criterios:
        puntajes[criterio.codigo] = pedir_entero(
            criterio.nombre + " (0 a 10): ", 0, 10
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
        print("\nOpción registrada correctamente.")
        print("Código:", opcion.codigo)
        print("Nombre:", opcion.nombre)
        print("Tipo:", opcion.tipo())
        print("Costo mensual estimado:", usd(opcion.costo_estimado()))
    except ErrorLaboratorio as e:
        print("Error:", e)


def registrar_evaluacion_individual(sistema):
    opcion = elegir_opcion(sistema)
    if opcion is None:
        return
    caso = elegir_caso(sistema)
    if caso is None:
        return
    try:
        evaluacion = sistema.registrar_evaluacion(opcion.codigo, caso.codigo)
        print("\nEvaluación registrada correctamente.")
        print(evaluacion)
    except ErrorLaboratorio as e:
        print(e)
        print("No se creó una nueva evaluación.")


##Comparar

def comparar_opciones(sistema):
    if len(sistema.opciones) == 0:
        print("No hay opciones registradas para comparar.")
        return
    caso = elegir_caso(sistema)
    if caso is None:
        return
    try:
        anteriores = len(sistema.evaluaciones_de_caso(caso.codigo))
        nuevas = sistema.comparar_caso(caso.codigo)

        print("\nComparación realizada para " + caso.nombre + ".")
        if anteriores > 0:
            print(
                plural(anteriores, "Se reemplazó ", "Se reemplazaron ")
                + str(anteriores)
                + plural(anteriores, " evaluación anterior.", " evaluaciones anteriores.")
            )
        print(
            plural(len(nuevas), "Se generó ", "Se generaron ")
            + str(len(nuevas))
            + plural(len(nuevas), " evaluación nueva.", " evaluaciones nuevas.")
        )
        print()
        mostrar_tabla_evaluaciones(nuevas)
        print("\nOpciones recomendadas:", sistema.cantidad_recomendadas(caso.codigo))
    except ErrorLaboratorio as e:
        print("Error:", e)


##Actualizar

def mostrar_recalculadas(evaluaciones, mostrar_caso=False):
    cantidad = len(evaluaciones)
    print(
        plural(cantidad, "Se recalculó ", "Se recalcularon ")
        + str(cantidad)
        + plural(cantidad, " evaluación.", " evaluaciones.")
    )
    if cantidad > 0:
        print()
        mostrar_tabla_evaluaciones(evaluaciones, mostrar_caso)


def actualizar_presupuesto_caso(sistema):
    caso = elegir_caso(sistema)
    if caso is None:
        return
    nuevo = pedir_decimal("Nuevo presupuesto mensual en USD: ", 0)
    try:
        anterior = caso.presupuesto
        sistema.actualizar_presupuesto(caso.codigo, nuevo)
        print("\nPresupuesto actualizado correctamente.")
        print("Presupuesto anterior:", usd(anterior))
        print("Presupuesto nuevo:", usd(caso.presupuesto))
        mostrar_recalculadas(sistema.evaluaciones_de_caso(caso.codigo))
    except ErrorLaboratorio as e:
        print("Error:", e)


def actualizar_opcion(sistema):
    opcion = elegir_opcion(sistema)
    if opcion is None:
        return
    print("\nOpción seleccionada:", opcion.nombre)
    print("Tipo:", opcion.tipo())
    costo_anterior = opcion.costo_estimado()
    try:
        if isinstance(opcion, ServicioAPI):
            costo_por_1000 = pedir_decimal(
                "Costo en USD por cada 1000 consultas: ", 0
            )
            consultas = pedir_entero("Cantidad de consultas mensuales estimadas: ", 1)
            sistema.actualizar_servicio_api(opcion.codigo, costo_por_1000, consultas)
        else:
            usuarios = pedir_entero("Cantidad de usuarios: ", 1)
            costo_por_usuario = pedir_decimal("Costo mensual en USD por usuario: ", 0)
            sistema.actualizar_plan_mensual(opcion.codigo, usuarios, costo_por_usuario)
        print("\nOpción actualizada correctamente.")
        print("Costo mensual anterior:", usd(costo_anterior))
        print("Costo mensual nuevo:", usd(opcion.costo_estimado()))
        mostrar_recalculadas(sistema.evaluaciones_de_opcion(opcion.codigo), True)
    except ErrorLaboratorio as e:
        print("Error:", e)


##Listar

def listar_criterios(sistema):
    if len(sistema.criterios) == 0:
        print("No hay criterios registrados.")
        return
    print()
    filas = []
    for criterio in sistema.criterios:
        filas.append([str(criterio.codigo), criterio.nombre, str(criterio.peso)])
    imprimir_tabla(["Código", "Nombre", "Peso"], filas)


def listar_opciones(sistema):
    if len(sistema.opciones) == 0:
        print("No hay opciones registradas.")
        return
    encabezados = ["Código", "Nombre", "Tipo", "Costo mensual"]
    for criterio in sistema.criterios:
        encabezados.append(criterio.nombre)

    filas = []
    for opcion in sistema.opciones:
        fila = [
            str(opcion.codigo),
            opcion.nombre,
            opcion.tipo(),
            usd(opcion.costo_estimado()),
        ]
        for criterio in sistema.criterios:
            fila.append(str(opcion.puntajes[criterio.codigo]))
        filas.append(fila)

    print()
    imprimir_tabla(encabezados, filas)
    print()
    for opcion in sistema.opciones:
        print(opcion.nombre + ": " + opcion.descripcion_costo())


def listar_casos(sistema):
    if len(sistema.casos) == 0:
        print("No hay casos de uso registrados.")
        return
    filas = []
    for caso in sistema.casos:
        filas.append([
            str(caso.codigo),
            caso.nombre,
            usd(caso.presupuesto),
            f"{caso.puntaje_minimo:.2f}",
            str(sistema.cantidad_recomendadas(caso.codigo)),
        ])
    print()
    imprimir_tabla(
        ["Código", "Nombre", "Presupuesto", "Mínimo", "Recomendadas"], filas
    )


def listar_evaluaciones(sistema):
    caso = elegir_caso(sistema)
    if caso is None:
        return
    evaluaciones = sistema.evaluaciones_de_caso(caso.codigo)
    print("\nEVALUACIONES DE " + caso.nombre.upper())
    print("Presupuesto actual:", usd(caso.presupuesto))
    print(f"Puntaje mínimo: {caso.puntaje_minimo:.2f}")
    print()
    if len(evaluaciones) == 0:
        print("No existen evaluaciones para este caso.")
        return
    filas = []
    for ev in evaluaciones:
        filas.append([
            str(ev.codigo),
            ev.fecha_texto(),
            ev.opcion.nombre,
            usd(ev.caso.presupuesto),
            usd(ev.costo_total()),
            f"{ev.puntaje_total():.2f}",
            ev.estado,
        ])
    imprimir_tabla(
        ["Código", "Fecha", "Opción", "Presupuesto", "Costo mensual", "Puntaje", "Estado"],
        filas,
    )


def listar_ranking(sistema):
    caso = elegir_caso(sistema)
    if caso is None:
        return
    ranking = sistema.ranking_de_caso(caso.codigo)
    print("\nRANKING DE " + caso.nombre.upper())
    print()
    if len(ranking) == 0:
        print("No hay opciones recomendadas para este caso.")
        return
    filas = []
    posicion = 1
    for ev in ranking:
        filas.append([
            str(posicion),
            ev.opcion.nombre,
            f"{ev.puntaje_total():.2f}",
            usd(ev.costo_total()),
        ])
        posicion = posicion + 1
    imprimir_tabla(["Posición", "Opción", "Puntaje", "Costo mensual"], filas)
    print("\nTotal de opciones recomendadas:", len(ranking))


##Menús

def menu_registrar(sistema):
    salir = False
    while not salir:
        print("\nREGISTRAR")
        print("1. Criterio")
        print("2. Opción de IA")
        print("3. Caso de uso")
        print("4. Evaluación individual")
        print("5. Salir")
        opcion = pedir_entero("\nSeleccione una opción: ", 1, 5)
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
        print("\nACTUALIZAR")
        print("1. Presupuesto de un caso")
        print("2. Precio o consumo de una opción")
        print("3. Salir")
        opcion = pedir_entero("\nSeleccione una opción: ", 1, 3)
        if opcion == 1:
            actualizar_presupuesto_caso(sistema)
        elif opcion == 2:
            actualizar_opcion(sistema)
        else:
            salir = True


def menu_listar(sistema):
    salir = False
    while not salir:
        print("\nLISTAR")
        print("1. Criterios")
        print("2. Opciones")
        print("3. Casos de uso")
        print("4. Evaluaciones de un caso")
        print("5. Ranking de un caso")
        print("6. Salir")
        opcion = pedir_entero("\nSeleccione una opción: ", 1, 6)
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
        print("\nMENÚ PRINCIPAL")
        print("1. Registrar")
        print("2. Comparar opciones para un caso")
        print("3. Actualizar")
        print("4. Listar")
        print("5. Salir del sistema")
        opcion = pedir_entero("\nSeleccione una opción: ", 1, 5)
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
    print("Programa finalizado.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado.")

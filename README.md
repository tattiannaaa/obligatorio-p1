# Laboratorio Programación 1 – 2026

Comparador de opciones de IA en modo consola.

**Equipo N°:** _COMPLETAR con el número asignado al enviar el mail_

## Requisitos

- Python **3.10 o superior**.
- No se usan librerías externas: solo la biblioteca estándar (`abc` y `datetime`).
- No requiere conexión a internet ni archivos de datos.

## Cómo ejecutar

Desde la carpeta raíz del proyecto (la que contiene `main.py`):

```bash
python3 main.py
```

En Windows puede usarse `python main.py` o `py main.py`.

## Estructura

```
main.py                     Menús e interacción con el usuario
README.md
entities/
    Sistema.py              Listas de criterios, opciones, casos y evaluaciones; coordina operaciones
    OpcionIA.py             Clase abstracta OpcionIA y sus derivadas ServicioAPI y PlanMensual
    Criterio.py
    CasoUso.py
    Evaluacion.py
exceptions/
    ErrorLaboratorio.py     Excepción propia para datos inválidos o duplicados
```

## Uso

1. **Registrar**: primero todos los criterios (luego de registrar la primera opción ya no se permiten nuevos criterios), después las opciones de IA y los casos de uso. También se puede registrar una evaluación individual.
2. **Comparar opciones para un caso**: evalúa todas las opciones para el caso elegido y reemplaza sus evaluaciones anteriores.
3. **Actualizar**: presupuesto de un caso o precio/consumo de una opción; recalcula el estado de las evaluaciones afectadas.
4. **Listar**: criterios, opciones, casos, evaluaciones de un caso y ranking de un caso.
5. **Salir del sistema**.

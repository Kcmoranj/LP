# Reglas semánticas
# - If con condición booleana
# - Funciones no-void deben retornar
# - Tipo de retorno compatible

def regla_if(cond_type: str):
    """
    Condición del if debe ser booleana.
    """
    if cond_type != "bool":
        return (
            f"La condición del if debe ser de tipo 'bool', "
            f"se encontró '{cond_type}'."
        )
    return None


def regla_funcion_retorno_obligatorio(ret_type: str, has_return: bool, nombre: str):
    """
    Regla: funciones/métodos no-void deben tener al menos un return.
    """
    if ret_type != "void" and not has_return:
        return (
            f"La función/método '{nombre}' de tipo '{ret_type}' "
            f"no tiene ninguna sentencia return."
        )
    return None


def regla_return_tipo(ret_type: str, expr_type: str, nombre: str):
    """
    Chequeo de tipo de la expresión de retorno.
    La compatibilidad exacta se valida en semantico_comun.tipos_compatibles,
    pero aquí podemos dar un mensaje genérico.
    """
    if ret_type == "void":
        # El caso void ya lo maneja Kiara
        return None

    # Retornar error genérico, semantico_comun ya marca compatibilidad fina.
    # Aquí solo reforzamos que si expr_type es 'error' lo notamos.
    if expr_type == "error":
        return (
            f"En la función/método '{nombre}' de tipo '{ret_type}' "
            f"la expresión de retorno tiene tipo desconocido o incorrecto."
        )
    # La verificación fina de tipos se hizo al detectar incompatibilidad
    # en semantico_comun (tipos_compatibles), así que aquí podemos
    # opcionalmente no decir nada más.
    return None
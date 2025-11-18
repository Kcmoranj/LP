# semantico_kiara.py
# Reglas semánticas de Kiara:
# - While con condición booleana
# - Métodos/funciones void no retornan valores

def regla_while(cond_type: str):
    """
    Devuelve mensaje de error (str) si hay problema,
    o None si está correcto.
    """
    if cond_type != "bool":
        return (
            f"La condición del while debe ser de tipo 'bool', "
            f"se encontró '{cond_type}'."
        )
    return None


def regla_return_void(ret_type: str, expr_type: str | None):
    """
    Para funciones/métodos void: no pueden retornar valor.
    ret_type: tipo declarado de la función
    expr_type: tipo de la expresión retornada
    """
    if ret_type == "void" and expr_type is not None and expr_type != "error":
        return (
            f"Un método/función de tipo 'void' no puede retornar un valor "
            f"(se encontró expresión de tipo '{expr_type}')."
        )
    return None


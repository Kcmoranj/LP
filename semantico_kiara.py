
from semantico_comun import (
    add_error, function_stack, tipos_compatibles
)

# -------- WHILE --------
def validar_while(cond, lineno):
    cond_type = cond.get("type", "desconocido")

    if cond_type != "bool":
        add_error(
            f"La condición del while debe ser 'bool', se encontró '{cond_type}'.",
            lineno
        )


# -------- RETURN EN VOID --------
def validar_return_void(expr, lineno):
    fun = function_stack[-1]
    ret_type = fun["ret_type"]

    if ret_type == "void" and expr is not None:
        add_error(
            f"El método '{fun['name']}' es void y no puede retornar valores.",
            lineno
        )

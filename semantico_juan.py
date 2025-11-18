
def regla_for(cond_type: str):
    """
    Regla: condición del for debe ser bool (si existe).
    """
    if cond_type != "bool":
        return (
            f"La condición del for debe ser de tipo 'bool', "
            f"se encontró '{cond_type}'."
        )
    return None

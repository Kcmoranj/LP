# Aporte Juan Romero
# Reglas semánticas:
# 1. Condición del FOR debe ser booleana
# 2. Las clases no pueden tener miembros con nombres duplicados

def regla_for(cond_type: str):
    """
    Regla 1: La condición del for debe ser de tipo bool.
    """
    if cond_type != "bool":
        return (
            f"La condición del for debe ser de tipo 'bool', "
            f"se encontró '{cond_type}'."
        )
    return None


def regla_clase_miembros_duplicados(nombre_clase: str, miembros: list):
    """
    Regla 2: Verifica que no haya miembros duplicados en una clase.
    miembros: lista de nombres de propiedades/métodos de la clase
    """
    nombres_vistos = set()
    duplicados = []
    
    for miembro in miembros:
        if miembro in nombres_vistos:
            if miembro not in duplicados:
                duplicados.append(miembro)
        else:
            nombres_vistos.add(miembro)
    
    if duplicados:
        return (
            f"La clase '{nombre_clase}' tiene miembros duplicados: "
            f"{', '.join(duplicados)}."
        )
    return None

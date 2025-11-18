from datetime import datetime
import os

import semantico_kiara
import semantico_juan
import semantico_daniel


class Symbol:
    def __init__(self, name, sym_type, kind, extra=None):
        self.name = name
        self.type = sym_type
        self.kind = kind          # "var", "array", "func", "method", "class"
        self.extra = extra or {}  # params, etc.


# Tabla de símbolos (solo scope global para simplificar)
symbol_table = {}
semantic_errors = []

# Pila de funciones/métodos en los que estamos (para return)
# Cada elemento: {"name": str, "ret_type": str, "kind": "func"|"method"}
function_stack = []


# ==========================
# Utilidades básicas
# ==========================

def reset_semantic_state():
    global symbol_table, semantic_errors, function_stack
    symbol_table = {}
    semantic_errors = []
    function_stack = []


def add_error(msg):
    semantic_errors.append(msg)


def declare_symbol(name, sym_type, kind, extra=None):
    if name in symbol_table:
        add_error(f"Identificador redeclarado: '{name}'.")
    else:
        symbol_table[name] = Symbol(name, sym_type, kind, extra)


def lookup_symbol(name):
    return symbol_table.get(name)


def tipos_compatibles(expected, actual):
    if expected == actual:
        return True
    # promoción simple int -> double
    if expected == "double" and actual == "int":
        return True
    return False


def write_semantic_log(user_git="usuario"):
    """Genera el archivo logs/semantico-usuarioGit-fecha-hora.txt."""
    if not semantic_errors:
        print("Analizador semántico: sin errores.")
        return

    os.makedirs("logs", exist_ok=True)
    filename = datetime.now().strftime(f"semantico-%s-%%d%%m%%Y-%%Hh%%M.txt" % user_git)
    path = os.path.join("logs", filename)
    with open(path, "w", encoding="utf-8") as f:
        for e in semantic_errors:
            f.write(e + "\n")
    print(f"Log semántico generado en: {path}")


# ==========================
# Análisis de EXPRESIONES
# ==========================

def analizar_expresion(node):
    """
    Devuelve el tipo de la expresión como string:
    'int', 'double', 'bool', 'string', 'char', 'null', 'error'
    AST esperado según tu parser:
      - ("literal", valor)
      - ("var", nombre)
      - ("binop", op, left, right)
    """
    if node is None:
        return "error"

    tag = node[0]

    if tag == "literal":
        val = node[1]
        # Deducción muy simple por tipo de Python / tokens esperados
        if isinstance(val, int):
            return "int"
        if isinstance(val, float):
            return "double"
        if val in ("true", "false", True, False):
            return "bool"
        if isinstance(val, str) and len(val) == 1:
            # char con comillas simples en el original, aquí ya vino como string
            return "char"
        if val is None or val == "null":
            return "null"
        # por defecto, asumimos string
        return "string"

    if tag == "var":
        name = node[1]
        sym = lookup_symbol(name)
        if sym is None:
            add_error(f"Uso de variable no declarada: '{name}'.")
            return "error"
        return sym.type

    if tag == "binop":
        op, left, right = node[1], node[2], node[3]
        t_left = analizar_expresion(left)
        t_right = analizar_expresion(right)

        # Operadores relacionales y de igualdad
        if op in ("==", "!=", "<", ">", "<=", ">="):
            # podrías chequear que sean comparables; aquí asumimos que sí
            return "bool"

        # Operadores lógicos
        if op in ("&&", "||"):
            # regla de Juan/Daniel/ Kiara podría exigir bool en ambos
            if t_left != "bool" or t_right != "bool":
                add_error(
                    f"Operador lógico '{op}' con operandos no booleanos "
                    f"('{t_left}', '{t_right}')."
                )
            return "bool"

        # Operadores aritméticos (+, -, *, /, etc.)
        # Simplificación: si alguno es double, resultado double; si ambos int, int
        if t_left == "double" or t_right == "double":
            return "double"
        if t_left == "int" and t_right == "int":
            return "int"

        # Si llega aquí, tipo desconocido
        add_error(f"Operación '{op}' con tipos incompatibles: '{t_left}', '{t_right}'.")
        return "error"

    # Si viene algo que no conocemos
    add_error(f"Expresión desconocida: {node}")
    return "error"


# ==========================
# Análisis de STATEMENTS
# ==========================

def analizar_statement(node):
    """
    Usa el tag del AST (primer elemento de la tupla)
    para decidir qué hacer.
    """
    if not isinstance(node, tuple):
        return

    tag = node[0]

    # Declaración simple: ("declaration", type, ident)
    if tag == "declaration":
        _, tipo, nombre = node
        declare_symbol(nombre, map_type_token_to_type(tipo), "var")

    # Declaración con inicialización: ("declaration_init", type, ident, expr)
    elif tag == "declaration_init":
        _, tipo, nombre, expr = node
        declare_symbol(nombre, map_type_token_to_type(tipo), "var")
        expr_type = analizar_expresion(expr)
        if not tipos_compatibles(map_type_token_to_type(tipo), expr_type):
            add_error(
                f"No se puede asignar valor de tipo '{expr_type}' "
                f"a variable '{nombre}' de tipo '{tipo}'."
            )

    # Asignación: ("assign", ident, expr)
    elif tag == "assign":
        _, nombre, expr = node
        sym = lookup_symbol(nombre)
        if sym is None:
            add_error(f"Asignación a variable no declarada: '{nombre}'.")
        else:
            expr_type = analizar_expresion(expr)
            if not tipos_compatibles(sym.type, expr_type):
                add_error(
                    f"No se puede asignar valor de tipo '{expr_type}' "
                    f"a variable '{nombre}' de tipo '{sym.type}'."
                )

    # Array: ("array_decl", type, ident, size_literal)
    elif tag == "array_decl":
        _, tipo, nombre, size = node
        declare_symbol(nombre, map_type_token_to_type(tipo), "array", extra={"size": size})

    # IF: ("if", cond, block) o IF-ELSE: ("if_else", cond, then_block, else_block)
    elif tag == "if":
        _, cond, block = node
        cond_type = analizar_expresion(cond)
        msg = semantico_daniel.regla_if(cond_type)
        if msg:
            add_error(msg)
        analizar_block(block)

    elif tag == "if_else":
        _, cond, then_block, else_block = node
        cond_type = analizar_expresion(cond)
        msg = semantico_daniel.regla_if(cond_type)
        if msg:
            add_error(msg)
        analizar_block(then_block)
        analizar_block(else_block)

    # WHILE: asumimos AST ("while", cond, block) cuando tengas la regla en el parser
    elif tag == "while":
        _, cond, block = node
        cond_type = analizar_expresion(cond)
        msg = semantico_kiara.regla_while(cond_type)
        if msg:
            add_error(msg)
        analizar_block(block)

    # FOR: ("for", init_assign, cond_expr, update_assign, block)
    elif tag == "for":
        _, init, cond, update, block = node
        if init:
            analizar_statement(init)
        cond_type = analizar_expresion(cond) if cond else "bool"  # for(;;) → ok
        msg = semantico_juan.regla_for(cond_type)
        if msg:
            add_error(msg)
        if update:
            analizar_statement(update)
        analizar_block(block)

    # Funciones con retorno: ("function_def", type, name, params, block)
    elif tag == "function_def":
        _, tipo, nombre, params, block = node
        ret_type = map_type_token_to_type(tipo)
        declare_symbol(nombre, ret_type, "func", extra={"params": params})
        function_stack.append({"name": nombre, "ret_type": ret_type, "kind": "func", "has_return": False})
        # parámetros no se declaran a fondo para simplificar
        analizar_block(block)
        info = function_stack.pop()
        # Regla de Daniel: funciones no void deben retornar algo
        msg = semantico_daniel.regla_funcion_retorno_obligatorio(info["ret_type"], info["has_return"], info["name"])
        if msg:
            add_error(msg)

    # Métodos: ("method", type, name, params, block)
    elif tag == "method":
        _, tipo, nombre, params, block = node
        ret_type = map_type_token_to_type(tipo)
        declare_symbol(nombre, ret_type, "method", extra={"params": params})
        function_stack.append({"name": nombre, "ret_type": ret_type, "kind": "method", "has_return": False})
        analizar_block(block)
        info = function_stack.pop()
        # Regla de Juan (retorno correcto) + Daniel (retorno obligatorio si no es void)
        msg_oblig = semantico_daniel.regla_funcion_retorno_obligatorio(info["ret_type"], info["has_return"], info["name"])
        if msg_oblig:
            add_error(msg_oblig)

    # RETURN: ("return", expr)
    elif tag == "return":
        _, expr = node
        if not function_stack:
            add_error("Sentencia 'return' fuera de función o método.")
        else:
            ctx = function_stack[-1]
            ctx["has_return"] = True
            expr_type = analizar_expresion(expr)
            # Kiara: métodos void no retornan valor
            msg_void = semantico_kiara.regla_return_void(ctx["ret_type"], expr_type)
            if msg_void:
                add_error(msg_void)
            # Daniel + Juan: retorno compatible con tipo del método/función
            msg_ret = semantico_daniel.regla_return_tipo(ctx["ret_type"], expr_type, ctx["name"])
            if msg_ret:
                add_error(msg_ret)

    # CLASES: ("class", name, members)
    elif tag == "class":
        _, nombre, members = node
        declare_symbol(nombre, nombre, "class")
        for m in members:
            analizar_statement(m)

    # Bloque: ("block", [statements])
    elif tag == "block":
        analizar_block(node)

    # Expresión sola: ("expr_stmt", expr)
    elif tag == "expr_stmt":
        analizar_expresion(node[1])

    else:
        # Nodo no contemplado → solo lo ignoramos
        pass


def analizar_block(block_node):
    """block_node = ('block', [stmts])"""
    if not isinstance(block_node, tuple):
        return
    tag = block_node[0]
    if tag != "block":
        return
    for stmt in block_node[1]:
        analizar_statement(stmt)


# ==========================
# FUNCIÓN PRINCIPAL DEL SEMÁNTICO
# ==========================

def analizar_programa(ast, user_git="usuarioGit"):
    """
    ast: lo que devuelve parser_cs.py (programa).
    """
    reset_semantic_state()

    if not ast or ast[0] != "program":
        add_error("AST inválido: no inicia con 'program'.")
    else:
        _, stmt_list = ast
        for stmt in stmt_list:
            analizar_statement(stmt)

    write_semantic_log(user_git)
    return semantic_errors

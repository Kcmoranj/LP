from datetime import datetime
import os

class Symbol:
    def __init__(self, name, sym_type, kind, extra=None):
        self.name = name
        self.type = sym_type
        self.kind = kind
        self.extra = extra or {}

symbol_stack = [ {} ]
semantic_errors = []
function_stack = []


# ----------------------------
# TABLA DE SÍMBOLOS Y ERRORES
# ----------------------------
def current_scope():
    return symbol_stack[-1]

def enter_scope():
    symbol_stack.append({})

def exit_scope():
    symbol_stack.pop()

def lookup(name):
    for scope in reversed(symbol_stack):
        if name in scope:
            return scope[name]
    return None

def declare_symbol(name, sym_type, kind, extra=None, lineno=None):
    scope = current_scope()
    if name in scope:
        add_error(f"Identificador '{name}' redeclarado.", lineno)
    else:
        scope[name] = Symbol(name, sym_type, kind, extra)

def add_error(msg, lineno=None):
    if lineno:
        semantic_errors.append(f"[línea {lineno}] {msg}")
    else:
        semantic_errors.append(msg)

def tipos_compatibles(expected, actual):
    if expected == actual:
        return True
    if expected == "double" and actual == "int":
        return True
    return False


# ----------------------------
# MANEJO DE FUNCIONES
# ----------------------------
def start_function(name, ret_type):
    function_stack.append({"name": name, "ret_type": ret_type, "has_return": False})

def end_function(lineno=None):
    info = function_stack.pop()
    if info["ret_type"] != "void" and not info["has_return"]:
        add_error(
            f"La función '{info['name']}' debe retornar un valor.",
            lineno
        )


# ----------------------------
# GUARDAR LOG
# ----------------------------
def write_semantic_log(user_git="usuario"):
    if not semantic_errors:
        return
    
    os.makedirs("logs", exist_ok=True)
    filename = datetime.now().strftime(f"semantico-{user_git}-%d%m%Y-%Hh%M.txt")

    with open("logs/" + filename, "w", encoding="utf-8") as f:
        for e in semantic_errors:
            f.write(e + "\n")

    print(f"Log generado: logs/{filename}")

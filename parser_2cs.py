# ==========================
# parser_cs.py  (ejemplo)
# ==========================

from semantico_comun import *
from semantico_kiara import validar_while, validar_return_void
from semantico_juan import validar_for, validar_retorno_metodo
from semantico_daniel import validar_if, validar_return_no_void

# -------------------------
# ejemplo usando WHILE
# -------------------------
def p_statement_while(p):
    "statement : WHILE LPAREN expression RPAREN statement"
    validar_while(p[3], p.lineno(1))


# -------------------------
# ejemplo usando FOR
# -------------------------
def p_statement_for(p):
    "statement : FOR LPAREN expression_opt SEMICOLON expression_opt SEMICOLON expression_opt RPAREN statement"
    validar_for(p[5], p.lineno(1))


# -------------------------
# ejemplo usando IF / ELSE
# -------------------------
def p_statement_if(p):
    "statement : IF LPAREN expression RPAREN statement"
    validar_if(p[3], p.lineno(1))


# -------------------------
# ejemplo RETURN
# -------------------------
def p_return_void(p):
    "statement : RETURN SEMICOLON"
    fun = function_stack[-1]
    fun["has_return"] = True
    validar_return_void(None, p.lineno(1))


def p_return_expr(p):
    "statement : RETURN expression SEMICOLON"
    fun = function_stack[-1]
    fun["has_return"] = True
    expr_type = p[2]["type"]

    # Lógica compartida Kiara + Daniel + Juan:
    validar_return_void(p[2], p.lineno(1))      # void no puede retornar
    validar_return_no_void(expr_type, p.lineno(1))   # funciones no-void deben tener tipo correcto

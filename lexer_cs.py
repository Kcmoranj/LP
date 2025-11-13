import ply.lex as lex
import sys

# Definición de Tokens
tokens = (
    'KEYWORD', 'IDENTIFIER',
    'INT_LITERAL', 'FLOAT_LITERAL', 'STRING_LITERAL', 'CHAR_LITERAL',
    'OPERATOR', 'DELIMITER',
    'TOK_ERROR',
)

# Palabras Reservadas (Keywords y Tipos)
reserved = {
    'if': 'KEYWORD_IF', 'else': 'KEYWORD_ELSE', 'while': 'KEYWORD_WHILE', 'for': 'KEYWORD_FOR',
    'switch': 'KEYWORD_SWITCH', 'case': 'KEYWORD_CASE', 'default': 'KEYWORD_DEFAULT',
    'break': 'KEYWORD_BREAK', 'continue': 'KEYWORD_CONTINUE', 'return': 'KEYWORD_RETURN',
    'const': 'KEYWORD_CONST', 'var': 'KEYWORD_VAR', 'class': 'KEYWORD_CLASS', 'new': 'KEYWORD_NEW',
    'true': 'KEYWORD_TRUE', 'false': 'KEYWORD_FALSE', 'null': 'KEYWORD_NULL',
    'int': 'KEYWORD_TYPE_INT', 'double': 'KEYWORD_TYPE_DOUBLE', 'bool': 'KEYWORD_TYPE_BOOL',
    'char': 'KEYWORD_TYPE_CHAR', 'string': 'KEYWORD_TYPE_STRING',
}
tokens = list(tokens) + list(reserved.values())

# Función para calcular la columna
def find_column(input, t):
    line_start = input.rfind('\n', 0, t.lexpos) + 1
    return (t.lexpos - line_start) + 1

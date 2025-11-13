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

# ==========================================================
# Aporte: Daniel Vilema
# Identificadores
def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Literales
t_INT_LITERAL = r'\d+'
t_FLOAT_LITERAL = r'\d+\.\d+'
t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'
t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))?\''

# ==========================================================
# Aporte: Kiara Morán
# Operadores
t_OPERATOR = r'\+\+|--|==|!=|<=|>=|&&|\|\|[+*/%=!~?-]'

# Delimitadores
t_DELIMITER = r'[\{\}\[\]\(\)\,\;\.]'

# ==========================================================
# Aporte: Juan Romero
# Comentarios
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass

def t_COMMENT_MULTI(t):
    r'/\(.|\n)?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres a ignorar
t_ignore = ' \t'

# ==========================================================


# --- Manejo de Errores Léxicos ---
def t_TOK_ERROR(t):
    r'.'
    print(f"TOK_ERROR: Carácter ilegal '{t.value[0]}' en línea {t.lineno}, columna {find_column(t.lexer.lexdata, t)}", file=sys.stderr)
    t.lexer.skip(1)
    t.value = t.value[0]
    return t

# --- Construcción del Analizador Léxico ---
lexer = lex.lex()

# --- Lógica de Ejecución ---
if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
        try:
            with open(file_path, 'r') as f:
                data = f.read()
        except FileNotFoundError:
            sys.stderr.write(f"Error: Archivo de entrada '{file_path}' no encontrado.\n")
            sys.exit(1)

        lexer.input(data)
        
        # Formato de salida para el log (stdout)
        print("--- Análisis Léxico de C# (PLY) ---")
        print("{:<20} {:<20} {:<10} {:<10}".format("Tipo", "Lexema", "Línea", "Columna"))
        print("-" * 60)
        
        # Imprime los tokens y errores
        for tok in lexer:
            columna = find_column(data, tok)
            print("{:<20} {:<20} {:<10} {:<10}".format(
                tok.type, 
                tok.value, 
                tok.lineno, 
                columna
            ))
    else:
        sys.stderr.write("Uso: python lexer_cs.py <archivo_fuente.cs> > archivo_log.txt\n")
        sys.stderr.write("Uso alternativo (más robusto): python lexer_cs.py archivo_fuente.cs > archivo_log.txt\n")

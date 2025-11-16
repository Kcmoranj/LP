# LEXER CORREGIDO PARA EL PROYECTO (AVANCE 2)
import ply.lex as lex
import sys

# PALABRAS RESERVADAS
reserved = {
    'int': 'KEYWORD_TYPE_INT','double': 'KEYWORD_TYPE_DOUBLE',
    'bool': 'KEYWORD_TYPE_BOOL','char': 'KEYWORD_TYPE_CHAR',
    'string': 'KEYWORD_TYPE_STRING','true': 'KEYWORD_TRUE',
    'false': 'KEYWORD_FALSE','null': 'KEYWORD_NULL',
    'if': 'KEYWORD_IF','else': 'KEYWORD_ELSE',
    'while': 'KEYWORD_WHILE','for': 'KEYWORD_FOR',
    'switch': 'KEYWORD_SWITCH','case': 'KEYWORD_CASE',
    'default': 'KEYWORD_DEFAULT','break': 'KEYWORD_BREAK',
    'continue': 'KEYWORD_CONTINUE','return': 'KEYWORD_RETURN',
    'const': 'KEYWORD_CONST','var': 'KEYWORD_VAR',
    'class': 'KEYWORD_CLASS','new': 'KEYWORD_NEW',
}

# LISTA DE TOKENS
tokens = [
    'IDENTIFIER',
    # Literales
    'INT_LITERAL',
    'FLOAT_LITERAL',
    'STRING_LITERAL',
    'CHAR_LITERAL',
    # Operadores
    'OPERATOR',
    # Delimitadores específicos
    'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',
    'LPAREN', 'RPAREN',
    'COMMA', 'SEMICOLON', 'DOT',
] + list(reserved.values())

# Función para Calcular columna
def find_column(input_text, token):
    """Calcula la columna de un token en el código fuente"""
    line_start = input_text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# ==========================================================
# Aporte: Daniel Vilema
# ==========================================================

def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Literales
t_INT_LITERAL = r'\d+'
t_FLOAT_LITERAL = r'\d+\.\d+'
t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'  # ✅ Maneja escapes
t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))?\''

# ==========================================================
# Aporte: Kiara Morán
# ==========================================================

# Operadores
t_OPERATOR = r'\+\+|--|==|!=|<=|>=|&&|\|\||[+\-*/%=!<>~?]'

# Delimitadores específicos (corregido para parser)
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'

# ==========================================================
# Aporte: Juan Romero
# ==========================================================

# Comentarios de una línea
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass  

# Comentarios multilínea
def t_COMMENT_MULTI(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass 

# MANEJO DE ESPACIOS Y SALTOS DE LÍNEA
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# MANEJO DE ERRORES
def t_error(t):
    sys.stderr.write(
        f"ERROR LÉXICO: Carácter ilegal '{t.value[0]}' "
        f"en línea {t.lineno}, columna {find_column(t.lexer.lexdata, t)}\n"
    )
    t.lexer.skip(1)

# CONSTRUCCIÓN DEL LEXER
lexer = lex.lex()

# BLOQUE PRINCIPAL (para pruebas)
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
        try:
            with open(file_path, 'r') as f:
                data = f.read()
        except FileNotFoundError:
            sys.stderr.write(f"Error: Archivo '{file_path}' no encontrado.\n")
            sys.exit(1)

        lexer.input(data)
        
        # Formato de salida
        print("--- Análisis Léxico de C# (PLY) ---")
        print("{:<20} {:<20} {:<10} {:<10}".format("Tipo", "Lexema", "Línea", "Columna"))
        print("-" * 60)
        
        for tok in lexer:
            columna = find_column(data, tok)
            print("{:<20} {:<20} {:<10} {:<10}".format(
                tok.type, 
                str(tok.value), 
                tok.lineno, 
                columna
            ))
    else:
        sys.stderr.write("Uso: python lexer_cs.py <archivo.cs> > log.txt\n")

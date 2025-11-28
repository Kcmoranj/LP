###############################################################
# PARSER DEL LENGUAJE C# - AVANCE 2
# Autores:
# - Daniel Vilema: Arrays, IF-ELSE, Funciones con retorno
# - Kiara Morán: WHILE, I/O (print/input), Procedimientos
# - Juan Romero: FOR, Clases, Métodos
###############################################################

import ply.yacc as yacc
from lexer_cs import tokens, lexer
import sys
import datetime
from semantico_comun import analizar_programa

###############################################################
# PRECEDENCIA DE OPERADORES
###############################################################

precedence = (
    ('left', 'OPERATOR'),
)

###############################################################
# REGLA PRINCIPAL
###############################################################

def p_program(p):
    """program : statement_list"""
    p[0] = ("program", p[1])

def p_statement_list(p):
    """statement_list : statement_list statement
                      | statement"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

###############################################################
# STATEMENTS GENERALES
###############################################################

def p_statement(p):
    """statement : declaration
                 | assignment
                 | array_declaration
                 | if_statement
                 | while_statement
                 | for_statement
                 | function_def
                 | procedure_def
                 | print_statement
                 | input_statement
                 | class_def
                 | return_statement
                 | expression_statement"""
    p[0] = p[1]

def p_block(p):
    """block : LBRACE statement_list RBRACE
             | LBRACE RBRACE"""
    if len(p) == 4:
        p[0] = ("block", p[2])
    else:
        p[0] = ("block", [])

###############################################################
# DECLARACIONES Y ASIGNACIONES (COMPARTIDO)
###############################################################

def p_declaration(p):
    """declaration : type IDENTIFIER SEMICOLON
                   | type IDENTIFIER OPERATOR expression SEMICOLON"""
    if len(p) == 4:
        p[0] = ("declaration", p[1], p[2])
    else:
        if p[3] == '=':
            p[0] = ("declaration_init", p[1], p[2], p[4])

def p_type(p):
    """type : KEYWORD_TYPE_INT
            | KEYWORD_TYPE_DOUBLE
            | KEYWORD_TYPE_BOOL
            | KEYWORD_TYPE_CHAR
            | KEYWORD_TYPE_STRING"""
    p[0] = p[1]

def p_assignment(p):
    """assignment : IDENTIFIER OPERATOR expression SEMICOLON"""
    if p[2] == '=':
        p[0] = ("assign", p[1], p[3])

###############################################################
# EXPRESIONES (COMPARTIDO)
###############################################################

def p_expression_binop(p):
    """expression : expression OPERATOR expression"""
    p[0] = ("binop", p[2], p[1], p[3])

def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]

def p_expression_literal(p):
    """expression : INT_LITERAL
                  | FLOAT_LITERAL
                  | STRING_LITERAL
                  | CHAR_LITERAL
                  | KEYWORD_TRUE
                  | KEYWORD_FALSE
                  | KEYWORD_NULL"""
    value = p[1]
    # Convertir literales a sus tipos apropiados
    if p.slice[1].type == 'INT_LITERAL':
        value = int(value)
    elif p.slice[1].type == 'FLOAT_LITERAL':
        value = float(value)
    elif p.slice[1].type in ('KEYWORD_TRUE', 'KEYWORD_FALSE'):
        value = value  # mantener como string 'true'/'false'
    p[0] = ("literal", value)

def p_expression_var(p):
    """expression : IDENTIFIER"""
    p[0] = ("var", p[1])

def p_expression_statement(p):
    """expression_statement : expression SEMICOLON"""
    p[0] = ("expr_stmt", p[1])

###############################################################
# 1️⃣ SECCIÓN DE DANIEL VILEMA
# Responsabilidad:
# - Estructura de datos: Arrays
# - Estructura de control: IF-ELSE
# - Tipo de función: Funciones con retorno
###############################################################

# ARRAYS: int[] arr = new int[5];
def p_array_declaration(p):
    """array_declaration : type LBRACKET RBRACKET IDENTIFIER OPERATOR KEYWORD_NEW type LBRACKET INT_LITERAL RBRACKET SEMICOLON"""
    if p[5] == '=':
        p[0] = ("array_decl", p[1], p[4], p[9])

# IF-ELSE
def p_if_statement(p):
    """if_statement : KEYWORD_IF LPAREN expression RPAREN block
                    | KEYWORD_IF LPAREN expression RPAREN block KEYWORD_ELSE block"""
    if len(p) == 6:
        p[0] = ("if", p[3], p[5])
    else:
        p[0] = ("if_else", p[3], p[5], p[7])

# FUNCIONES CON RETORNO
def p_function_def(p):
    """function_def : type IDENTIFIER LPAREN params RPAREN block"""
    p[0] = ("function_def", p[1], p[2], p[4], p[6])

# RETURN STATEMENT
def p_return_statement(p):
    """return_statement : KEYWORD_RETURN expression SEMICOLON"""
    p[0] = ("return", p[2])

def p_params(p):
    """params : param_list
              | empty"""
    p[0] = p[1] if p[1] else []

def p_param_list(p):
    """param_list : param_list COMMA type IDENTIFIER
                  | type IDENTIFIER"""
    if len(p) == 5:
        p[0] = p[1] + [(p[3], p[4])]
    else:
        p[0] = [(p[1], p[2])]

###############################################################
# 2️⃣ SECCIÓN DE KIARA MORÁN
# Responsabilidad:
# - Estructura de control: WHILE
# - I/O: Console.WriteLine / Console.ReadLine
# - Tipo de función: Procedimientos (void)
###############################################################

# WHILE
def p_while_statement(p):
    """while_statement : KEYWORD_WHILE LPAREN expression RPAREN block"""
    p[0] = ("while", p[3], p[5])

# PRINT: Console.WriteLine(expr);
def p_print_statement(p):
    """print_statement : IDENTIFIER DOT IDENTIFIER LPAREN expression RPAREN SEMICOLON"""
    if p[1] == "Console" and p[3] == "WriteLine":
        p[0] = ("print", p[5])

# INPUT: var = Console.ReadLine();
def p_input_statement(p):
    """input_statement : IDENTIFIER OPERATOR IDENTIFIER DOT IDENTIFIER LPAREN RPAREN SEMICOLON"""
    if p[2] == '=' and p[3] == "Console" and p[5] == "ReadLine":
        p[0] = ("input", p[1])

# PROCEDIMIENTO (void function)
def p_procedure_def(p):
    """procedure_def : IDENTIFIER IDENTIFIER LPAREN params RPAREN block"""
    if p[1] == "void":
        p[0] = ("procedure_def", p[2], p[4], p[6])


###############################################################
# 3️⃣ SECCIÓN DE JUAN ROMERO
# Responsabilidad:
# - Estructura de control: FOR
# - Estructura de datos: Clases
# - Tipo de función: Métodos de clase
###############################################################

# FOR
def p_for_statement(p):
    """for_statement : KEYWORD_FOR LPAREN for_init expression SEMICOLON for_update RPAREN block"""
    p[0] = ("for", p[3], p[4], p[6], p[8])

def p_for_init(p):
    """for_init : type IDENTIFIER OPERATOR expression SEMICOLON
                | IDENTIFIER OPERATOR expression SEMICOLON"""
    if len(p) == 6:
        # Declaración con inicialización: int i = 0;
        if p[3] == '=':
            p[0] = ("declaration_init", p[1], p[2], p[4])
    else:
        # Asignación simple: i = 0;
        if p[2] == '=':
            p[0] = ("assign", p[1], p[3])

def p_for_update(p):
    """for_update : IDENTIFIER OPERATOR expression"""
    if p[2] == '=':
        p[0] = ("assign", p[1], p[3])

# CLASES
def p_class_def(p):
    """class_def : KEYWORD_CLASS IDENTIFIER LBRACE class_body RBRACE
                 | KEYWORD_CLASS IDENTIFIER LBRACE RBRACE"""
    if len(p) == 6:
        p[0] = ("class", p[2], p[4])
    else:
        p[0] = ("class", p[2], [])

def p_class_body(p):
    """class_body : class_body class_member
                  | class_member"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_class_member(p):
    """class_member : declaration
                    | method_def"""
    p[0] = p[1]

# MÉTODOS DE CLASE
def p_method_def(p):
    """method_def : type IDENTIFIER LPAREN params RPAREN block"""
    p[0] = ("method", p[1], p[2], p[4], p[6])

###############################################################
# EMPTY
###############################################################

def p_empty(p):
    """empty :"""
    pass

###############################################################
# MANEJO DE ERRORES
###############################################################

def p_error(p):
    if p:
        sys.stderr.write(
            f"ERROR SINTÁCTICO: Token inesperado '{p.value}' "
            f"(tipo: {p.type}) en línea {p.lineno}\n"
        )
    else:
        sys.stderr.write("ERROR SINTÁCTICO: Fin inesperado del archivo\n")

###############################################################
# CONSTRUCCIÓN DEL PARSER
###############################################################

parser = yacc.yacc()

###############################################################
# MAIN - EJECUCIÓN
###############################################################

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
        # Extraer nombre de usuario de git desde el archivo (si tiene formato estándar)
        import os
        base_name = os.path.basename(file_path)
        # Intentar extraer usuario: algoritmo_sintactico_<usuario>.cs o algoritmo_<usuario>.cs
        if "daniel" in base_name.lower():
            user_git = "DanieljVilema"
        elif "kiara" in base_name.lower():
            user_git = "Kcmoranj"
        elif "juan" in base_name.lower():
            user_git = "jcarrome"
        else:
            user_git = "usuario"
        
        try:
            with open(file_path, 'r') as f:
                data = f.read()
            
            result = parser.parse(data, lexer=lexer)
            print("--- ANÁLISIS SINTÁCTICO EXITOSO ---")
            if result:
                print(result)
                # Ejecutar análisis semántico
                print("\n--- INICIANDO ANÁLISIS SEMÁNTICO ---")
                errores = analizar_programa(result, user_git)
                if errores:
                    print(f"Se encontraron {len(errores)} errores semánticos.")
                    for error in errores:
                        print(f"  - {error}")
                else:
                    print("Análisis semántico: sin errores.")
            
        except FileNotFoundError:
            sys.stderr.write(f"Error: Archivo '{file_path}' no encontrado.\n")
            sys.exit(1)
        except Exception as e:
            sys.stderr.write(f"Error durante el análisis: {str(e)}\n")
            sys.exit(1)
    else:
        sys.stderr.write("Uso: python parser_cs.py <archivo.cs> 2> sintactico-log.txt\n")



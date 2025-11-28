#!/usr/bin/env python3
"""
Backend API Flask para el Compilador C#
Conecta la GUI React con los analizadores Python (léxico, sintáctico, semántico)

Autores: Daniel Vilema, Kiara Morán, Juan Romero
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import io
import datetime
import re
from contextlib import redirect_stdout, redirect_stderr

# Importar los analizadores
from lexer_cs import lexer, find_column
import ply.yacc as yacc
from parser_cs import *
from semantico_comun import analizar_programa

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde React

# Función auxiliar para capturar salida
def capture_output(func, *args):
    """Captura stdout y stderr de una función"""
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
        try:
            result = func(*args)
        except Exception as e:
            result = None
            stderr_capture.write(f"Error: {str(e)}\n")
    
    return result, stdout_capture.getvalue(), stderr_capture.getvalue()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servidor está corriendo"""
    return jsonify({"status": "ok", "message": "Backend funcionando correctamente"})

@app.route('/api/analyze/lexical', methods=['POST'])
def analyze_lexical():
    """Análisis léxico del código C#"""
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({"error": "No se proporcionó código"}), 400
        
        # Resetear el lexer
        lexer.lineno = 1
        lexer.input(code)
        
        tokens_list = []
        errors_list = []
        
        # Tokenizar
        while True:
            tok = lexer.token()
            if not tok:
                break
            
            column = find_column(code, tok)
            tokens_list.append({
                "type": tok.type,
                "lexeme": tok.value,
                "line": tok.lineno,
                "column": column
            })
        
        # Verificar si hubo errores (tokens de error)
        # Los errores se capturan en t_error del lexer
        
        return jsonify({
            "success": True,
            "tokens": tokens_list,
            "errors": errors_list,
            "message": f"Análisis léxico completado. {len(tokens_list)} tokens encontrados."
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Error durante el análisis léxico"
        }), 500

@app.route('/api/analyze/syntactic', methods=['POST'])
def analyze_syntactic():
    """Análisis sintáctico del código C#"""
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({"error": "No se proporcionó código"}), 400
        
        # Crear el parser
        parser = yacc.yacc()
        
        # Capturar errores sintácticos
        errors_list = []
        syntax_errors = []
        
        # Crear una clase personalizada para capturar errores
        class ErrorCapture:
            def __init__(self):
                self.errors = []
            
            def write(self, message):
                if message.strip():
                    self.errors.append(message.strip())
        
        error_capture = ErrorCapture()
        
        # Parsear el código
        try:
            result = parser.parse(code, lexer=lexer)
            ast_tree = format_ast(result) if result else "No se pudo generar el AST"
            success = True
        except Exception as e:
            ast_tree = f"Error: {str(e)}"
            success = False
            errors_list.append({
                "line": 0,
                "column": 0,
                "message": str(e)
            })
        
        return jsonify({
            "success": success,
            "ast": ast_tree,
            "errors": errors_list,
            "message": "Análisis sintáctico completado" if success else "Errores sintácticos encontrados"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Error durante el análisis sintáctico"
        }), 500

@app.route('/api/analyze/semantic', methods=['POST'])
def analyze_semantic():
    """Análisis semántico del código C#"""
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({"error": "No se proporcionó código"}), 400
        
        # Primero hacer análisis sintáctico
        parser = yacc.yacc()
        
        try:
            # Resetear estado semántico
            from semantico_comun import reset_semantic_state
            reset_semantic_state()
            
            ast = parser.parse(code, lexer=lexer)
            
            if not ast:
                return jsonify({
                    "success": False,
                    "errors": [{"line": 0, "column": 0, "message": "No se pudo generar el AST"}],
                    "symbols": [],
                    "message": "Error en análisis sintáctico previo"
                })
            
            # Analizar semánticamente
            semantic_errors_raw = analizar_programa(ast)
            
            # Formatear errores para el frontend con búsqueda de línea/columna
            semantic_errors = []
            import re
            lines = code.split('\n')
            
            for error in semantic_errors_raw:
                line = 0
                column = 0
                
                # Buscar palabras clave en el mensaje de error para determinar ubicación
                error_lower = error.lower()
                
                # Buscar IF, WHILE, FOR, RETURN en el error
                if 'if' in error_lower and 'condición' in error_lower:
                    keyword = 'if'
                elif 'while' in error_lower and 'condición' in error_lower:
                    keyword = 'while'
                elif 'for' in error_lower and 'condición' in error_lower:
                    keyword = 'for'
                elif ('retornar' in error_lower and 'valor' in error_lower) or ('void' in error_lower and 'retornar' in error_lower):
                    keyword = 'return'
                else:
                    keyword = None
                
                if keyword:
                    # Buscar la palabra clave en el código
                    for i, line_text in enumerate(lines, 1):
                        if keyword in line_text.lower():
                            line = i
                            column = line_text.lower().find(keyword) + 1
                            break
                else:
                    # Buscar identificadores mencionados en el error
                    matches = re.findall(r"'(\w+)'", error)
                    if matches:
                        # Buscar el primer identificador que no sea un tipo de dato
                        for identifier in matches:
                            if identifier not in ['int', 'double', 'bool', 'char', 'string', 'void']:
                                # Buscar el identificador en el código
                                for i, line_text in enumerate(lines, 1):
                                    if identifier in line_text:
                                        line = i
                                        column = line_text.find(identifier) + 1
                                        break
                                if line > 0:
                                    break
                
                semantic_errors.append({
                    "line": line,
                    "column": column,
                    "message": error
                })
            
            # Obtener tabla de símbolos (reimportar para obtener estado actualizado)
            from semantico_comun import symbol_table
            symbols = []
            for name, symbol in symbol_table.items():
                kind_map = {"var": "variable", "array": "array", "func": "function", "method": "method", "class": "class"}
                symbols.append({
                    "scope": "Global",
                    "name": symbol.name,
                    "type": symbol.type,
                    "category": kind_map.get(symbol.kind, "variable")
                })
            
            return jsonify({
                "success": len(semantic_errors) == 0,
                "errors": semantic_errors,
                "symbols": symbols,
                "message": f"Análisis semántico completado. {len(semantic_errors)} errores encontrados." if semantic_errors else "Sin errores semánticos"
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e),
                "errors": [{"line": 0, "column": 0, "message": str(e)}],
                "message": "Error durante el análisis semántico"
            })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Error durante el análisis semántico"
        }), 500

@app.route('/api/analyze/all', methods=['POST'])
def analyze_all():
    """Análisis completo (léxico + sintáctico + semántico)"""
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({"error": "No se proporcionó código"}), 400
        
        result = {
            "lexical": {},
            "syntactic": {},
            "semantic": {},
            "symbols": []
        }
        
        # 1. Análisis léxico
        lexer.lineno = 1
        lexer.input(code)
        
        tokens_list = []
        lexical_errors = []
        
        while True:
            tok = lexer.token()
            if not tok:
                break
            
            column = find_column(code, tok)
            tokens_list.append({
                "type": tok.type,
                "lexeme": tok.value,
                "line": tok.lineno,
                "column": column
            })
        
        result["lexical"] = {
            "success": len(lexical_errors) == 0,
            "tokens": tokens_list,
            "errors": lexical_errors
        }
        
        # 2. Análisis sintáctico
        parser = yacc.yacc()
        syntactic_errors = []
        ast = None
        
        try:
            ast = parser.parse(code, lexer=lexer)
            ast_formatted = format_ast(ast) if ast else "No se pudo generar el AST"
            
            result["syntactic"] = {
                "success": True,
                "ast": ast_formatted,
                "errors": syntactic_errors
            }
        except Exception as e:
            result["syntactic"] = {
                "success": False,
                "ast": f"Error: {str(e)}",
                "errors": [{"line": 0, "column": 0, "message": str(e)}]
            }
        
        # 3. Análisis semántico (solo si el sintáctico fue exitoso)
        if ast and result["syntactic"]["success"]:
            try:
                from semantico_comun import reset_semantic_state
                reset_semantic_state()
                
                semantic_errors_raw = analizar_programa(ast)
                
                # Formatear errores con búsqueda de línea/columna
                semantic_errors = []
                import re
                lines = code.split('\n')
                
                for error in semantic_errors_raw:
                    line = 0
                    column = 0
                    
                    # Buscar palabras clave en el mensaje de error para determinar ubicación
                    error_lower = error.lower()
                    
                    # Buscar IF, WHILE, FOR, RETURN en el error
                    if 'if' in error_lower and 'condición' in error_lower:
                        keyword = 'if'
                    elif 'while' in error_lower and 'condición' in error_lower:
                        keyword = 'while'
                    elif 'for' in error_lower and 'condición' in error_lower:
                        keyword = 'for'
                    elif ('retornar' in error_lower and 'valor' in error_lower) or ('void' in error_lower and 'retornar' in error_lower):
                        keyword = 'return'
                    else:
                        keyword = None
                    
                    if keyword:
                        # Buscar la palabra clave en el código
                        for i, line_text in enumerate(lines, 1):
                            if keyword in line_text.lower():
                                line = i
                                column = line_text.lower().find(keyword) + 1
                                break
                    else:
                        # Buscar identificadores mencionados en el error
                        matches = re.findall(r"'(\w+)'", error)
                        if matches:
                            # Buscar el primer identificador que no sea un tipo de dato
                            for identifier in matches:
                                if identifier not in ['int', 'double', 'bool', 'char', 'string', 'void']:
                                    # Buscar el identificador en el código
                                    for i, line_text in enumerate(lines, 1):
                                        if identifier in line_text:
                                            line = i
                                            column = line_text.find(identifier) + 1
                                            break
                                    if line > 0:
                                        break
                    
                    semantic_errors.append({
                        "line": line,
                        "column": column,
                        "message": error
                    })
                
                # Obtener tabla de símbolos (reimportar para obtener estado actualizado)
                from semantico_comun import symbol_table
                symbols = []
                for name, symbol in symbol_table.items():
                    kind_map = {"var": "variable", "array": "array", "func": "function", "method": "method", "class": "class"}
                    symbols.append({
                        "scope": "Global",
                        "name": symbol.name,
                        "type": symbol.type,
                        "category": kind_map.get(symbol.kind, "variable")
                    })
                
                result["semantic"] = {
                    "success": len(semantic_errors) == 0,
                    "errors": semantic_errors,
                    "symbols": symbols
                }
            except Exception as e:
                result["semantic"] = {
                    "success": False,
                    "errors": [{"line": 0, "column": 0, "message": str(e)}],
                    "symbols": []
                }
        else:
            result["semantic"] = {
                "success": False,
                "errors": [{"line": 0, "column": 0, "message": "No se pudo realizar análisis semántico debido a errores sintácticos"}],
                "symbols": []
            }
        
        # Determinar éxito general
        overall_success = (
            result["lexical"]["success"] and
            result["syntactic"]["success"] and
            result["semantic"]["success"]
        )
        
        return jsonify({
            "success": overall_success,
            "result": result,
            "message": "Análisis completo realizado" if overall_success else "Se encontraron errores durante el análisis"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Error durante el análisis completo"
        }), 500

@app.route('/api/save-log', methods=['POST'])
def save_log():
    """Guardar log de análisis"""
    try:
        data = request.json
        log_type = data.get('type', 'general')  # lexico, sintactico, semantico
        username = data.get('username', 'user')
        content = data.get('content', '')
        
        # Crear directorio logs si no existe
        os.makedirs('logs', exist_ok=True)
        
        # Generar nombre del archivo
        timestamp = datetime.datetime.now().strftime('%d%m%Y-%H%M')
        filename = f"logs/{log_type}-{username}-{timestamp}.txt"
        
        # Guardar archivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            "success": True,
            "filename": filename,
            "message": f"Log guardado en {filename}"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Error al guardar el log"
        }), 500

def format_ast(node, indent=0):
    """Formatea el AST para visualización"""
    if not node:
        return "Empty"
    
    if isinstance(node, tuple):
        result = "  " * indent + str(node[0]) + "\n"
        for child in node[1:]:
            if isinstance(child, (tuple, list)):
                result += format_ast(child, indent + 1)
            else:
                result += "  " * (indent + 1) + str(child) + "\n"
        return result
    elif isinstance(node, list):
        result = ""
        for item in node:
            result += format_ast(item, indent)
        return result
    else:
        return "  " * indent + str(node) + "\n"

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Servidor Backend del Compilador C# iniciado")
    print("=" * 60)
    print("Endpoints disponibles:")
    print("  - GET  /api/health - Verificar estado del servidor")
    print("  - POST /api/analyze/lexical - Análisis léxico")
    print("  - POST /api/analyze/syntactic - Análisis sintáctico")
    print("  - POST /api/analyze/semantic - Análisis semántico")
    print("  - POST /api/analyze/all - Análisis completo")
    print("  - POST /api/save-log - Guardar log de análisis")
    print("=" * 60)
    print("Escuchando en http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

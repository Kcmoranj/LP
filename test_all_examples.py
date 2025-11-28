#!/usr/bin/env python3
"""
Script para probar todos los ejemplos de código de la GUIA_USO.md
"""
import requests
import json

BASE_URL = "http://localhost:5000"

ejemplos = [
    {
        "nombre": "Ejemplo 1: Variables y Console.WriteLine",
        "codigo": """int x = 10;
int y = 20;
int suma = x + y;
Console.WriteLine(suma);"""
    },
    {
        "nombre": "Ejemplo 2: Condicional IF-ELSE",
        "codigo": """int edad = 18;
if (edad >= 18) {
    Console.WriteLine("Mayor de edad");
} else {
    Console.WriteLine("Menor de edad");
}"""
    },
    {
        "nombre": "Ejemplo 3: Bucle WHILE",
        "codigo": """int contador = 0;
while (contador < 5) {
    Console.WriteLine(contador);
    contador = contador + 1;
}"""
    },
    {
        "nombre": "Ejemplo 4: Bucle FOR",
        "codigo": """for (int i = 0; i < 10; i = i + 1) {
    Console.WriteLine(i);
}"""
    },
    {
        "nombre": "Ejemplo 5: Funciones",
        "codigo": """int sumar(int a, int b) {
    return a + b;
}

int resultado = sumar(5, 3);
Console.WriteLine(resultado);"""
    },
    {
        "nombre": "Ejemplo 6: Arrays",
        "codigo": """int[] numeros;
numeros = [1, 2, 3, 4, 5];
Console.WriteLine(numeros[0]);"""
    },
    {
        "nombre": "Ejemplo 7: Clases",
        "codigo": """class Persona {
    int edad;
    
    int getEdad() {
        return edad;
    }
}"""
    },
    {
        "nombre": "Ejemplo 8: IF (Daniel)",
        "codigo": """if (condicion) {
    // código
} else {
    // código
}"""
    },
    {
        "nombre": "Ejemplo 9: WHILE (Kiara)",
        "codigo": """while (condicion) {
    // código
}"""
    },
    {
        "nombre": "Ejemplo 10: Procedimiento void con return incorrecto",
        "codigo": """int x = 2;
void imprimir() {
    return 10;
}"""
    },
    {
        "nombre": "Ejemplo 11: Variable no declarada",
        "codigo": """int x = 10;
y = 20;
Console.WriteLine(x);"""
    },
    {
        "nombre": "Ejemplo 12: Condición no booleana en IF",
        "codigo": """int x = 5;
if (x) {
    Console.WriteLine("Error");
}"""
    },
    {
        "nombre": "Ejemplo 13: Condición no booleana en WHILE",
        "codigo": """int contador = 0;
while (10) {
    contador = contador + 1;
}"""
    },
    {
        "nombre": "Ejemplo 14: Condición no booleana en FOR",
        "codigo": """for (int i = 0; 100; i = i + 1) {
    Console.WriteLine(i);
}"""
    },
    {
        "nombre": "Ejemplo 15: Función sin return",
        "codigo": """int calcular(int x) {
    int y = x + 10;
}"""
    },
    {
        "nombre": "Ejemplo 16: Array con índice",
        "codigo": """int[] datos;
datos = [10, 20, 30];
int primero = datos[0];
Console.WriteLine(primero);"""
    },
    {
        "nombre": "Ejemplo 17: Clase con método",
        "codigo": """class Calculadora {
    int resultado;
    
    int sumar(int a, int b) {
        resultado = a + b;
        return resultado;
    }
}"""
    },
    {
        "nombre": "Ejemplo 18: Console.ReadLine",
        "codigo": """Console.WriteLine("Ingrese su nombre:");
string nombre = Console.ReadLine();
Console.WriteLine(nombre);"""
    }
]

def test_example(numero, ejemplo):
    """Prueba un ejemplo individual"""
    print(f"\n{'='*80}")
    print(f"🧪 Prueba #{numero}: {ejemplo['nombre']}")
    print(f"{'='*80}")
    print(f"\n📝 Código:")
    print(ejemplo['codigo'])
    print()
    
    try:
        # Realizar análisis completo
        response = requests.post(
            f"{BASE_URL}/api/analyze/all",
            json={"code": ejemplo['codigo']},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extraer result si existe
            result = data.get('result', data)
            
            # Análisis Léxico
            if 'lexical' in result and result['lexical']['success']:
                tokens = result['lexical']['tokens']
                print(f"✅ Léxico: {len(tokens)} tokens detectados")
            elif 'lexical' in result:
                print(f"❌ Léxico: Error")
            else:
                print(f"⚠️  Léxico: Clave no encontrada en respuesta")
                
            # Análisis Sintáctico
            if 'syntactic' in result and result['syntactic']['success']:
                print(f"✅ Sintáctico: AST generado correctamente")
                if result['syntactic']['errors']:
                    print(f"   ⚠️  {len(result['syntactic']['errors'])} advertencias")
            elif 'syntactic' in result:
                print(f"❌ Sintáctico: Error")
                for err in result['syntactic']['errors']:
                    print(f"   - L{err['line']}:C{err['column']}: {err['message']}")
            else:
                print(f"⚠️  Sintáctico: Clave no encontrada en respuesta")
                    
            # Análisis Semántico
            if 'semantic' in result:
                semantic = result['semantic']
                
                if semantic.get('success', False):
                    errors = semantic.get('errors', [])
                    symbols = semantic.get('symbols', [])
                    
                    if errors:
                        print(f"⚠️  Semántico: {len(errors)} error(es) detectado(s)")
                        for err in errors:
                            print(f"   - L{err['line']}:C{err['column']}: {err['message']}")
                    else:
                        print(f"✅ Semántico: Sin errores")
                        
                    print(f"📊 Tabla de símbolos: {len(symbols)} símbolo(s)")
                    if symbols:
                        for sym in symbols[:5]:  # Mostrar primeros 5
                            print(f"   - {sym['name']}: {sym['type']} ({sym['category']})")
                        if len(symbols) > 5:
                            print(f"   ... y {len(symbols) - 5} más")
                else:
                    # Análisis semántico falló - mostrar errores si existen
                    errors = semantic.get('errors', [])
                    if errors:
                        print(f"❌ Semántico: {len(errors)} error(es)")
                        for err in errors:
                            print(f"   - L{err['line']}:C{err['column']}: {err['message']}")
                    else:
                        print(f"❌ Semántico: Error en análisis previo (sin AST)")
            else:
                print(f"⚠️  Semántico: Clave no encontrada en respuesta")
                
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Excepción: {str(e)}")
    
    print()

def main():
    """Ejecuta todas las pruebas"""
    print("╔" + "═"*78 + "╗")
    print("║" + " "*20 + "🧪 PRUEBAS AUTOMATIZADAS - COMPILADOR C#" + " "*18 + "║")
    print("╚" + "═"*78 + "╝")
    
    # Verificar que el backend esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("\n✅ Backend conectado correctamente\n")
        else:
            print(f"\n❌ Backend respondió con código {response.status_code}\n")
            return
    except Exception as e:
        print(f"\n❌ No se pudo conectar al backend: {str(e)}")
        print("💡 Asegúrate de que el backend esté corriendo: python3 backend.py\n")
        return
    
    # Ejecutar todas las pruebas
    exitosos = 0
    total = len(ejemplos)
    
    for i, ejemplo in enumerate(ejemplos, 1):
        test_example(i, ejemplo)
    
    print("\n" + "="*80)
    print(f"✅ Pruebas completadas: {total}/{total} ejemplos ejecutados")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

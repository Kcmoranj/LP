# Compilador de C# - Proyecto de Lenguajes de Programación

## 👥 Equipo de Desarrollo

- **Daniel Vilema** (@DanieljVilema) - Arrays, IF-ELSE, Funciones con retorno
- **Kiara Morán** (@Kcmoranj) - WHILE, I/O (Console.WriteLine/ReadLine), Procedimientos void
- **Juan Romero** (@jcarrome) - FOR, Clases, Métodos

---

## 📋 Descripción

Compilador educativo para un subconjunto del lenguaje C# que implementa:
- ✅ Análisis Léxico
- ✅ Análisis Sintáctico  
- ✅ Análisis Semántico
- ✅ Interfaz Gráfica Web (React + Flask)

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.7 o superior
- Node.js 16 o superior
- npm 8 o superior

### Instalar Dependencias

```bash
# Dependencias Python
pip install -r requirements.txt

# Dependencias Node.js
npm install
```

---

## 🎯 Cómo Ejecutar el Proyecto

### Opción 1: Interfaz Gráfica (Recomendado)

#### Paso 1: Iniciar el Backend

Abre una terminal y ejecuta:

```bash
python3 backend.py
```

Deberías ver:
```
============================================================
🚀 Servidor Backend del Compilador C# iniciado
============================================================
Escuchando en http://localhost:5000
```

**⚠️ IMPORTANTE:** Deja esta terminal abierta corriendo el backend.

---

#### Paso 2: Iniciar el Frontend

Abre **OTRA terminal nueva** (sin cerrar la anterior) y ejecuta:

```bash
npm run dev
```

Deberías ver:
```
VITE v6.3.5  ready in XXX ms

➜  Local:   http://localhost:5173/
```

---

#### Paso 3: Usar la Aplicación

1. Abre tu navegador en: **http://localhost:5173**
2. Haz clic en **"Cargar Código"**
3. Escribe o pega tu código C#
4. Haz clic en **"Guardar"**
5. Usa los botones de análisis:
   - **Analizar Léxico** - Muestra tokens detectados
   - **Analizar Sintaxis** - Genera árbol sintáctico (AST)
   - **Analizar Semántica** - Verifica reglas semánticas
   - **Analizar Todo** - Ejecuta los 3 análisis en secuencia

6. Ve los resultados en las pestañas:
   - **🧩 Tokens** - Lista de tokens reconocidos
   - **🧠 Errores** - Errores con línea y columna
   - **📊 Tabla de Símbolos** - Variables, funciones, clases
   - **🌳 AST** - Árbol sintáctico

---

### Opción 2: Línea de Comandos

#### Análisis Léxico

```bash
python3 lexer_cs.py algoritmo_daniel.cs
```

#### Análisis Sintáctico + Semántico

```bash
python3 parser_cs.py algoritmo_sintactico_daniel.cs
```

Los logs se guardan automáticamente en el directorio `logs/`.

---

## 🧪 Pruebas Automatizadas

Para probar todos los ejemplos de forma automática:

**Paso 1:** Asegúrate de que el backend esté corriendo:
```bash
python3 backend.py
```

**Paso 2:** En otra terminal, ejecuta:
```bash
python3 test_all_examples.py
```

Esto probará 18 ejemplos de código y mostrará los resultados de forma detallada.

---

## 📝 Ejemplos de Código Soportado

### Ejemplo 1: Variables y Operaciones
```csharp
int x = 10;
int y = 20;
int suma = x + y;
Console.WriteLine(suma);
```

### Ejemplo 2: Condicionales (IF-ELSE)
```csharp
int edad = 18;
if (edad >= 18) {
    Console.WriteLine("Mayor de edad");
} else {
    Console.WriteLine("Menor de edad");
}
```

### Ejemplo 3: Bucle WHILE
```csharp
int contador = 0;
while (contador < 5) {
    Console.WriteLine(contador);
    contador = contador + 1;
}
```

### Ejemplo 4: Bucle FOR
```csharp
for (int i = 0; i < 10; i = i + 1) {
    Console.WriteLine(i);
}
```

### Ejemplo 5: Funciones
```csharp
int sumar(int a, int b) {
    return a + b;
}

int resultado;
resultado = sumar(5, 3);
Console.WriteLine(resultado);
```

### Ejemplo 6: Clases
```csharp
class Persona {
    int edad;
    
    int getEdad() {
        return edad;
    }
}
```

### Ejemplo 7: Procedimientos Void
```csharp
void imprimir(string mensaje) {
    Console.WriteLine(mensaje);
}
```

### Ejemplo 8: Console.ReadLine
```csharp
string nombre;
Console.WriteLine("Ingrese su nombre:");
nombre = Console.ReadLine();
Console.WriteLine(nombre);
```

---

## 🔍 Características Implementadas

### Analizador Léxico
- Identificadores y literales (int, double, bool, char, string)
- Palabras reservadas (if, else, while, for, class, void, return, etc.)
- Operadores aritméticos (+, -, *, /, %)
- Operadores relacionales (<, >, <=, >=, ==, !=)
- Operadores lógicos (&&, ||, !)
- Delimitadores ({, }, (, ), [, ], ;, ,, .)
- Comentarios (// y /* */)

### Analizador Sintáctico
- Declaraciones de variables
- Estructuras de control: IF-ELSE, WHILE, FOR
- Arrays
- Funciones con retorno y procedimientos void
- Clases con atributos y métodos
- Expresiones aritméticas y lógicas
- I/O: Console.WriteLine, Console.ReadLine

### Analizador Semántico

**Reglas de Daniel Vilema:**
- La condición del IF debe ser de tipo 'bool'
- Funciones no-void deben tener sentencia return
- Tipo de retorno compatible con la declaración de función

**Reglas de Kiara Morán:**
- La condición del WHILE debe ser de tipo 'bool'
- Métodos/funciones void no pueden retornar valores

**Reglas de Juan Romero:**
- La condición del FOR debe ser de tipo 'bool'

**Reglas Comunes:**
- Variables deben ser declaradas antes de usarse
- Compatibilidad de tipos en asignaciones
- Tabla de símbolos con scope global

---

## 📂 Estructura del Proyecto

```
LP/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias Python
├── package.json                       # Dependencias Node.js
│
├── ANALIZADORES PYTHON
│   ├── backend.py                     # API REST Flask
│   ├── lexer_cs.py                    # Analizador léxico
│   ├── parser_cs.py                   # Analizador sintáctico
│   ├── semantico_comun.py             # Coordinador semántico
│   ├── semantico_daniel.py            # Reglas de Daniel
│   ├── semantico_kiara.py             # Reglas de Kiara
│   └── semantico_juan.py              # Reglas de Juan
│
├── ALGORITMOS DE PRUEBA
│   ├── algoritmo_daniel.cs            # Prueba léxico - Daniel
│   ├── algoritmo_kiara.cs             # Prueba léxico - Kiara
│   ├── algoritmo_juan.cs              # Prueba léxico - Juan
│   ├── algoritmo_sintactico_daniel.cs # Prueba sintáctico - Daniel
│   ├── algoritmo_sintactico_kiara.cs  # Prueba sintáctico - Kiara
│   └── algoritmo_sintactico_juan.cs   # Prueba sintáctico - Juan
│
├── PRUEBAS
│   └── test_all_examples.py           # Suite de pruebas automatizadas
│
├── LOGS
│   └── logs/                          # Logs generados automáticamente
│
└── INTERFAZ GRÁFICA
    ├── src/                           # Código fuente React
    │   ├── App.tsx                    # Componente principal
    │   └── components/                # Componentes UI
    ├── index.html                     # HTML principal
    └── vite.config.ts                 # Configuración Vite
```

---

## 🛠️ Tecnologías Utilizadas

**Backend:**
- Python 3.12
- PLY (Python Lex-Yacc) 3.11
- Flask 3.0.0
- Flask-CORS 4.0.0

**Frontend:**
- React 18.3.1
- TypeScript 5.3.3
- Vite 6.3.5
- Tailwind CSS 3.4.0
- Shadcn/ui (componentes)

---

## 📊 Algoritmos de Prueba Incluidos

### Análisis Léxico
- `algoritmo_daniel.cs` - Identificadores y literales
- `algoritmo_kiara.cs` - Operadores y delimitadores
- `algoritmo_juan.cs` - Comentarios

### Análisis Sintáctico y Semántico
- `algoritmo_sintactico_daniel.cs` - Arrays, IF-ELSE, funciones
- `algoritmo_sintactico_kiara.cs` - WHILE, I/O, procedimientos void
- `algoritmo_sintactico_juan.cs` - FOR, clases, métodos

---

## 🐛 Solución de Problemas

### Error: "Address already in use" (Puerto 5000 ocupado)

```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Error: "Module not found"

Reinstala las dependencias:
```bash
pip install -r requirements.txt
npm install
```

### Error: "Cannot connect to backend"

1. Verifica que el backend esté corriendo en http://localhost:5000
2. Abre otra terminal y ejecuta: `curl http://localhost:5000/api/health`
3. Si no responde, reinicia el backend

---

## 📄 Licencia

Este proyecto es parte del curso de Lenguajes de Programación.  
Noviembre 2025 - Universidad [Nombre]

---

## 👨‍💻 Contacto

- Daniel Vilema - @DanieljVilema
- Kiara Morán - @Kcmoranj  
- Juan Romero - @jcarrome

---

**¡Gracias por usar nuestro compilador de C#! 🎉**

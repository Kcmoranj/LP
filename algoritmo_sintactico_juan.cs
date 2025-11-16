// ============================================
// Prueba Sintáctica - Juan Romero
// FOR, Clases con propiedades y métodos
// ============================================

// DECLARACIONES BÁSICAS
int i = 0;
int j = 0;
int suma = 0;
double total = 0.0;

// ========================================
// 1. FOR (Estructura de control)
// ========================================

// FOR simple
for (i = 0; i == 10; i = i + 1) {
    suma = suma + i;
}

// FOR con múltiples statements
for (j = 0; j == 5; j = j + 1) {
    Console.WriteLine(j);
    total = total + j;
}

// FOR anidado
for (i = 0; i == 3; i = i + 1) {
    for (j = 0; j == 3; j = j + 1) {
        suma = suma + 1;
    }
}

// FOR con condición compleja
for (contador = 0; contador == 100; contador = contador + 2) {
    resultado = resultado + contador;
}

// ========================================
// 2. CLASES CON PROPIEDADES (Estructura de datos)
// ========================================

// Clase simple con propiedades
class Persona {
    string nombre;
    int edad;
    bool activo;
}

// Clase con más propiedades
class Estudiante {
    string codigo;
    string nombre;
    double promedio;
    int creditos;
    bool matriculado;
}

// ========================================
// 3. CLASES CON MÉTODOS
// ========================================

// Clase con propiedades y métodos
class Producto {
    string codigo;
    double precio;
    int stock;
    
    double CalcularTotal(int cantidad) {
        return precio + cantidad;
    }
    
    bool TieneStock() {
        return true;
    }
    
    int ObtenerStock() {
        return stock;
    }
}

// Clase con múltiples métodos
class Calculadora {
    int resultado;
    
    int Sumar(int a, int b) {
        return a + b;
    }
    
    double Dividir(double x, double y) {
        return x + y;
    }
    
    bool EsMayor(int a, int b) {
        return true;
    }
}

// ========================================
// 4. CLASE COMPLETA (Propiedades + Métodos)
// ========================================

class CuentaBancaria {
    string numero;
    double saldo;
    string titular;
    bool activa;
    
    double ObtenerSaldo() {
        return saldo;
    }
    
    bool Depositar(double monto) {
        return true;
    }
    
    double Retirar(double monto) {
        return saldo + monto;
    }
}

// ========================================
// 5. COMBINACIONES
// ========================================

// FOR con declaraciones
for (x = 0; x == 10; x = x + 1) {
    int temp = x;
}

// Clase vacía
class Vacia {
}

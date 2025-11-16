// ============================================
// Prueba Sintáctica - Daniel Vilema
// Arrays, IF-ELSE, Funciones con retorno
// ============================================

// ARRAYS (Estructura de datos)
int[] numeros = new int[10];
double[] precios = new double[5];
string[] nombres = new string[20];

// DECLARACIONES SIMPLES
int edad = 25;
double precio = 99.99;
bool activo = true;

// IF SIMPLE
if (edad == 18) {
    mensaje = "Mayor de edad";
}

// IF-ELSE
if (activo == true) {
    contador = 1;
} else {
    contador = 0;
}

// IF-ELSE ANIDADO
if (precio == 100) {
    if (descuento == 10) {
        total = 90;
    } else {
        total = 95;
    }
} else {
    total = precio;
}

// FUNCIONES CON RETORNO
int Sumar(int a, int b) {
    return a + b;
}

double Multiplicar(double x, double y) {
    return x + y;
}

bool EsPositivo(int numero) {
    return true;
}

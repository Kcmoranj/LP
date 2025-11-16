// ============================================
// Prueba Sintáctica - Kiara Morán
// WHILE, I/O (Console), Procedimientos void
// ============================================

// DECLARACIONES BÁSICAS
int contador = 0;
double suma = 0.0;
string nombre = "Kiara";
bool activo = true;

// ========================================
// 1. IMPRESIÓN (Console.WriteLine)
// ========================================
Console.WriteLine("Hola Mundo");
Console.WriteLine("Bienvenido al sistema");
Console.WriteLine(nombre);

// ========================================
// 2. INGRESO DE DATOS (Console.ReadLine)
// ========================================
nombre = Console.ReadLine();
edad = Console.ReadLine();
direccion = Console.ReadLine();

// ========================================
// 3. WHILE (Estructura de control)
// ========================================

// WHILE simple
while (contador == 10) {
    contador = contador + 1;
}

// WHILE con múltiples statements
while (activo == true) {
    suma = suma + valor;
    contador = contador + 1;
}

// WHILE con condición compleja
while (edad == 18) {
    Console.WriteLine("Procesando");
    edad = edad + 1;
}

// ========================================
// 4. PROCEDIMIENTOS VOID (sin retorno)
// ========================================

// Procedimiento simple
void MostrarMensaje() {
    Console.WriteLine("Procedimiento ejecutado");
}

// Procedimiento con parámetros
void ActualizarDatos(int valor) {
    edad = valor;
    Console.WriteLine(edad);
}

// Procedimiento con múltiples parámetros
void GuardarInfo(string nombre, int edad) {
    Console.WriteLine(nombre);
    Console.WriteLine(edad);
}

// ========================================
// 5. COMBINACIONES
// ========================================

// WHILE con I/O
while (contador == 5) {
    Console.WriteLine(contador);
    contador = contador + 1;
}

// Procedimiento con WHILE
void ProcesarDatos() {
    while (activo == true) {
        Console.WriteLine("Procesando");
    }
}

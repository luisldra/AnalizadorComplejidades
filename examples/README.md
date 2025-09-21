# EJEMPLOS DE PSEUDOCÓDIGO
========================

Esta carpeta contiene archivos de ejemplo con pseudocódigo para probar el Analizador de Complejidades.

## Archivos Disponibles:

### 🔢 `factorial.txt`
- **Algoritmo**: Factorial recursivo
- **Patrón**: Recursión lineal
- **Complejidad esperada**: O(n)
- **Características**: Ideal para probar análisis de recursión y árboles de recurrencia

### 🌀 `fibonacci.txt`
- **Algoritmo**: Fibonacci recursivo (versión ingenua)
- **Patrón**: Recursión binaria exponencial
- **Complejidad esperada**: O(2^n)
- **Características**: Excelente para demostrar árboles de recurrencia complejos

### ➕ `suma_iterativa.txt`
- **Algoritmo**: Suma de 1 a n con bucle
- **Patrón**: Iterativo lineal
- **Complejidad esperada**: O(n)
- **Características**: Algoritmo simple sin recursión

### 🔄 `merge_sort.txt`
- **Algoritmo**: Merge Sort (divide y vencerás)
- **Patrón**: Recursión con división binaria
- **Complejidad esperada**: O(n log n)
- **Características**: Ejemplo clásico de divide y vencerás

### 🔍 `busqueda_binaria.txt`
- **Algoritmo**: Búsqueda binaria recursiva
- **Patrón**: Recursión con división binaria
- **Complejidad esperada**: O(log n)
- **Características**: Recursión que descarta la mitad en cada llamada

### 📈 `algoritmo_cubico.txt`
- **Algoritmo**: Triple bucle anidado
- **Patrón**: Iterativo con bucles anidados
- **Complejidad esperada**: O(n³)
- **Características**: Ejemplo de complejidad polinómica alta

## Cómo Usar:

1. Ejecute el programa principal:
   ```bash
   python src/main.py
   ```

2. Cuando se le solicite, ingrese la ruta de uno de estos archivos:
   ```
   examples/factorial.txt
   examples/fibonacci.txt
   examples/suma_iterativa.txt
   etc.
   ```

3. O simplemente presione Enter para usar el archivo por defecto (`factorial.txt`)

## Sintaxis del Pseudocódigo:

El pseudocódigo debe seguir estas reglas:

- Las funciones se declaran con `function nombre(parametros)`
- Los bloques comienzan con `begin` y terminan con `end`
- Las condiciones usan `if condition begin ... end else begin ... end`
- Los bucles: `for variable = inicio to fin do begin ... end`
- Las llamadas recursivas: `call nombre_funcion(argumentos)`
- Los retornos: `return valor`

## Experimentación:

¡Siéntase libre de crear sus propios archivos .txt con pseudocódigo personalizado para experimentar con el analizador!
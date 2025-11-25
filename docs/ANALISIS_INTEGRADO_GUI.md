# Análisis Integrado en la GUI

## 📋 Descripción General

La interfaz gráfica del Analizador de Complejidades ha sido diseñada para proporcionar un **análisis completo e integrado** de algoritmos, mostrando toda la información relevante en un solo lugar, similar a cómo lo hace el analizador de consola.

## 🎯 Características Principales

### 1. Análisis Unificado
- **Un solo algoritmo, análisis completo**: La GUI analiza el algoritmo una sola vez y muestra todos los resultados de manera integrada.
- **No hay análisis separados**: A diferencia de versiones anteriores con múltiples pestañas independientes, ahora todo está centralizado.

### 2. Ecuación de Recurrencia General
- **Forma general, no específica**: Se muestra la ecuación de recurrencia en su forma general (ej: `T(n) = T(n-1) + c`), no para un valor específico de n.
- **Casos base incluidos**: Se muestran todos los casos base identificados.

### 3. Complejidad Asintótica con Notación Precisa
- **Cota ajustada (Θ)**: Cuando es posible determinar una cota exacta.
- **Cotas superior/inferior**: O(f(n)) o Ω(f(n)) cuando solo se puede determinar una cota débil.
- **Indicación del tipo de cota**: Se especifica si es ajustada, superior o inferior.

### 4. Análisis de Casos
Todos los casos se muestran juntos en el análisis integrado:
- **Mejor Caso**: Escenario óptimo con su complejidad
- **Peor Caso**: Escenario crítico con su complejidad
- **Caso Promedio**: Comportamiento esperado típico

Cada caso incluye:
- Complejidad asintótica
- Descripción del escenario
- Ejemplo concreto
- Explicación detallada

### 5. Detalles de Recursión
Para algoritmos recursivos, se muestran:
- Nombre de la función analizada
- Patrón de recursión detectado (linear, binary, divide-and-conquer, etc.)
- Número de llamadas recursivas
- Trabajo por llamada
- Lista de todas las llamadas recursivas encontradas

## 📊 Estructura de las Pestañas

La GUI está organizada en 4 pestañas principales:

### 1. 📝 Pseudocódigo
- Editor de código con sintaxis básica
- Carga de archivos `.txt`
- Ejemplo inicial de factorial

### 2. 📊 Análisis Completo
**La pestaña principal** que muestra:
```
╔════════════════════════════════════════════════════════════════════╗
║              ANÁLISIS COMPLETO DEL ALGORITMO                       ║
╚════════════════════════════════════════════════════════════════════╝

┌─ 📐 ECUACIÓN DE RECURRENCIA Y COMPLEJIDAD ASINTÓTICA ──────────────┐

  Ecuación de Recurrencia GENERAL:
    T(n) = T(n-1) + c

  Casos Base:
    • T(0) = c
    • T(1) = c

  Complejidad Asintótica:
    Θ(n)  [Cota ajustada]

  Método de Análisis:
    Substitution

  Explicación:
    [Explicación detallada del método y resultado]

└────────────────────────────────────────────────────────────────────┘

┌─ 🔍 ANÁLISIS DE MEJOR, PEOR Y CASO PROMEDIO ───────────────────────┐

  ╭─ ✅ MEJOR CASO ─────────────────────────────────────────────────╮
  │ Complejidad: Θ(1)
  │
  │ Escenario:
  │   [Descripción del mejor escenario]
  │
  │ Ejemplo:
  │   [Ejemplo concreto]
  │
  │ Explicación:
  │   [Explicación detallada]
  ╰──────────────────────────────────────────────────────────────────╯

  ╭─ ❌ PEOR CASO ──────────────────────────────────────────────────╮
  │ [Similar estructura]
  ╰──────────────────────────────────────────────────────────────────╯

  ╭─ 📊 CASO PROMEDIO ──────────────────────────────────────────────╮
  │ [Similar estructura]
  ╰──────────────────────────────────────────────────────────────────╯

└────────────────────────────────────────────────────────────────────┘

┌─ 📚 DETALLES DE LA RECURSIÓN ──────────────────────────────────────┐

  Función analizada: factorial
  Patrón detectado: linear
  Número de llamadas recursivas: 1
  Trabajo por llamada: O(1)
  
  Llamadas recursivas encontradas:
    1. factorial(n - 1)

└────────────────────────────────────────────────────────────────────┘
```

### 3. 🌳 Árbol de Recurrencia
- Visualización gráfica del árbol de recurrencia
- **Estructura general simbólica**: Muestra T(n), T(n-1), T(n-2), etc., no niveles específicos
- Control de profundidad para visualización
- Exportación a imagen PNG

### 4. 📈 Diagrama de Flujo
- Para algoritmos iterativos
- Diagrama de flujo con nodos coloreados
- Muestra el comportamiento del algoritmo
- Exportación a imagen PNG

## 🔧 Uso de la Interfaz

### Paso 1: Cargar o Escribir Código
1. Hacer clic en "📁 Abrir Archivo" para cargar un archivo `.txt`, o
2. Escribir directamente en el editor de la pestaña "📝 Pseudocódigo"

**Sintaxis esperada:**
```
function nombre_funcion(parametros)
begin
    # Cuerpo de la función
    if condicion
    begin
        # código
    end
    else
    begin
        # código
    end
end
```

### Paso 2: Analizar
1. Hacer clic en "▶️ Analizar"
2. La GUI automáticamente:
   - Parsea el código
   - Analiza la complejidad asintótica
   - Determina la ecuación de recurrencia
   - Analiza mejor/peor/caso promedio
   - Identifica el tipo de cota (Θ, O, Ω)

### Paso 3: Revisar Resultados
La pestaña "📊 Análisis Completo" se abre automáticamente mostrando:
- Ecuación de recurrencia general
- Complejidad con tipo de cota
- Análisis de casos
- Detalles de recursión (si aplica)

### Paso 4: Visualizaciones Adicionales (Opcional)
- Ir a "🌳 Árbol de Recurrencia" para ver la estructura recursiva
- Ir a "📈 Diagrama de Flujo" para algoritmos iterativos

### Paso 5: Exportar (Opcional)
- Hacer clic en "💾 Exportar" para guardar:
  - Análisis completo en formato texto
  - Imágenes de visualizaciones

## 📐 Notación Asintótica

### Cota Ajustada: Θ(f(n))
- **Significa**: El algoritmo tiene exactamente complejidad f(n)
- **Cuándo se usa**: Cuando podemos determinar tanto cota superior como inferior
- **Ejemplo**: `Θ(n)` para búsqueda lineal recursiva

### Cota Superior: O(f(n))
- **Significa**: El algoritmo es **a lo más** f(n)
- **Cuándo se usa**: Cuando solo podemos determinar el límite superior
- **Ejemplo**: `O(n²)` para algunos algoritmos de ordenamiento

### Cota Inferior: Ω(f(n))
- **Significa**: El algoritmo es **al menos** f(n)
- **Cuándo se usa**: Cuando solo podemos determinar el límite inferior
- **Ejemplo**: `Ω(n)` para algoritmos que deben revisar todos los elementos

## 🎨 Casos de Uso

### Ejemplo 1: Factorial Recursivo
```
function factorial(n)
begin
    if n <= 1
    begin
        return 1
    end
    else
    begin
        return n * call factorial(n - 1)
    end
end
```

**Resultado del Análisis:**
- Ecuación: `T(n) = T(n-1) + c`
- Complejidad: `Θ(n)` [Cota ajustada]
- Mejor caso: `Θ(1)` (cuando n=0 o n=1)
- Peor caso: `Θ(n)` (cuando n es grande)
- Patrón: Linear recursion

### Ejemplo 2: Fibonacci Recursivo
```
function fib(n)
begin
    if n <= 1
    begin
        return n
    end
    else
    begin
        return call fib(n - 1) + call fib(n - 2)
    end
end
```

**Resultado del Análisis:**
- Ecuación: `T(n) = T(n-1) + T(n-2) + c`
- Complejidad: `Θ(2^n)` [Cota ajustada]
- Peor caso: `Θ(2^n)`
- Patrón: Binary recursion

### Ejemplo 3: Merge Sort
```
function mergeSort(arr, left, right)
begin
    if left < right
    begin
        mid := (left + right) / 2
        call mergeSort(arr, left, mid)
        call mergeSort(arr, mid + 1, right)
        call merge(arr, left, mid, right)
    end
end
```

**Resultado del Análisis:**
- Ecuación: `T(n) = 2T(n/2) + n`
- Complejidad: `Θ(n log n)` [Cota ajustada]
- Mejor caso: `Θ(n log n)`
- Peor caso: `Θ(n log n)`
- Patrón: Divide and conquer

## 🔍 Diferencias con Versión Anterior

| Aspecto | Versión Anterior | Versión Actual |
|---------|------------------|----------------|
| Análisis | Separado en múltiples pestañas | Integrado en una sola pestaña |
| Ecuación | Podía mostrar valores específicos | Siempre muestra forma general |
| Notación | Solo O(n) | Distingue entre Θ, O, Ω |
| Casos | Pestañas separadas | Todo en análisis integrado |
| Árbol | Niveles específicos (n=5) | Estructura general simbólica |

## 💡 Recomendaciones

1. **Siempre revisar el análisis completo primero**: Contiene toda la información esencial
2. **Usar visualizaciones para entender**: El árbol y diagrama de flujo ayudan a comprender la estructura
3. **Comparar casos**: Entender la diferencia entre mejor/peor caso es crucial
4. **Verificar el tipo de cota**: Saber si es Θ, O o Ω es importante para análisis preciso

## 🐛 Solución de Problemas

### Error al Analizar
- **Verificar sintaxis**: Asegurarse de usar `begin/end`, no `then/end if`
- **Usar `call` para recursión**: Las llamadas recursivas deben usar `call nombre_funcion()`
- **Sin comentarios**: El parser no soporta comentarios con `#`

### Resultados Inesperados
- **Revisar lógica del algoritmo**: Verificar que la implementación sea correcta
- **Casos base**: Asegurarse de que estén bien definidos
- **Condiciones**: Verificar que las condiciones if/else sean correctas

## 📚 Referencias

- [COMPLEXITY_ANALYZER_GUIDE.md](COMPLEXITY_ANALYZER_GUIDE.md) - Guía técnica del analizador
- [RECURRENCE_TREES_GUIDE.md](RECURRENCE_TREES_GUIDE.md) - Guía de árboles de recurrencia
- [GUI_GUIDE.md](GUI_GUIDE.md) - Guía completa de la interfaz gráfica
- [../examples/](../examples/) - Ejemplos de algoritmos

---

**Universidad de Caldas**  
Análisis y Diseño de Algoritmos - Proyecto 2025-2

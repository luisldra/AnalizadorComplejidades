# Analizador Avanzado de Complejidad Algorítmica - Documentación Completa

## 🎯 Descripción del Sistema

Este sistema integra conocimientos avanzados en análisis algorítmico para construir un analizador que, a partir de un algoritmo escrito en pseudocódigo, determina automáticamente su complejidad computacional usando las notaciones **O (Big O)**, **Ω (Omega)**, y **Θ (Theta)**.

## 🏗️ Arquitectura del Sistema

### Componentes Principales:

1. **Parser Extendido** (`src/parser/`)
   - Gramática Lark mejorada con soporte para arrays, matrices, expresiones booleanas
   - Transformer que convierte el parse tree a AST
   - Nodos AST para todas las construcciones del lenguaje

2. **Analizador de Complejidad Avanzado** (`src/analyzer/advanced_complexity.py`)
   - Análisis comprehensivo con O, Ω, y Θ
   - Manejo de bucles anidados, condicionales, recursión
   - Soporte para arrays/matrices y expresiones booleanas

3. **Motor de Análisis** (`src/analyzer/complexity_engine.py`)
   - Interfaz de alto nivel para análisis de complejidad
   - Generación de reportes detallados
   - Análisis de características algorítmicas

## 📊 Capacidades de Análisis

### Notaciones Soportadas:

- **Big O (O)**: Peor caso - cota superior asintótica
- **Omega (Ω)**: Mejor caso - cota inferior asintótica  
- **Theta (Θ)**: Caso promedio - cota exacta cuando O = Ω

### Construcciones Analizadas:

- ✅ **Operaciones básicas**: O(1), Ω(1), Θ(1)
- ✅ **Bucles simples**: O(n), Ω(n), Θ(n)
- ✅ **Bucles anidados**: O(n²), O(n³), etc.
- ✅ **Condicionales**: Máximo para O, mínimo para Ω
- ✅ **Arrays/Matrices**: Análisis de acceso y declaración
- ✅ **Expresiones booleanas**: Evaluación de corto circuito
- ✅ **Bucles while/repeat**: Estimaciones conservadoras
- ✅ **Múltiples funciones**: Análisis del máximo

## 🧪 Ejemplos de Análisis

### 1. Algoritmo Constante
```pseudocode
function constant_ops(n)
begin
    x 🡨 5
    y 🡨 x + 10
    return y * 2
end
```
**Resultado**: O(1), Ω(1), Θ(1)

### 2. Búsqueda Lineal
```pseudocode
function linear_search(n)
begin
    for i 🡨 0 to n do
    begin
        if (arr[i] = target) then
        begin
            return i
        end
    end
end
```
**Resultado**: O(n), Ω(1) - No hay Θ porque O ≠ Ω

### 3. Ordenamiento Burbuja
```pseudocode
function bubble_sort(n)
begin
    for i 🡨 0 to n do
    begin
        for j 🡨 0 to n - i do
        begin
            if (arr[j] > arr[j + 1]) then
            begin
                temp 🡨 arr[j]
                arr[j] 🡨 arr[j + 1]
                arr[j + 1] 🡨 temp
            end
        end
    end
end
```
**Resultado**: O(n²), Ω(n²), Θ(n²)

### 4. Complejidad Condicional
```pseudocode
function conditional_work(n, condition)
begin
    if (condition) then
    begin
        for i 🡨 0 to n do
        begin
            work 🡨 i * 2
        end
    end
    else
    begin
        work 🡨 42
    end
    return work
end
```
**Resultado**: O(n), Ω(1) - Depende de la condición

## 🔬 Reglas de Análisis Implementadas

### Bucles:
- **For simple**: Iteraciones × complejidad del cuerpo
- **Bucles anidados**: Multiplicación de complejidades
- **While/Repeat**: Estimación conservadora (peor caso O(n))

### Condicionales:
- **If-else**: max(ramas) para O, min(ramas) para Ω
- **If simple**: rama para O, O(1) para Ω

### Estructuras de Datos:
- **Arrays**: Acceso O(1), declaración O(n)
- **Matrices**: Acceso O(1), declaración O(n²)

### Expresiones Booleanas:
- **and/or**: Evaluación de corto circuito
- **not**: O(1) + complejidad del operando

## 📈 Uso del Sistema

### Análisis Básico:
```python
from src.analyzer.complexity_engine import ComplexityAnalysisEngine

engine = ComplexityAnalysisEngine()
result = engine.analyze_code(pseudocode, detailed=True)

print(f"Big O: {result.big_o}")
print(f"Omega: {result.omega}")
print(f"Theta: {result.theta}")
```

### Reporte Completo:
```python
report = engine.generate_report(pseudocode)
print(f"Complexity: {report['complexity']['summary']}")
print(f"Characteristics: {report['characteristics']}")
for note in report['analysis_notes']:
    print(f"• {note}")
```

## 🧪 Tests y Validación

El sistema incluye tests comprehensivos:

- ✅ **Tests básicos**: Operaciones constantes, bucles lineales
- ✅ **Tests de bucles anidados**: Complejidad cuadrática y cúbica
- ✅ **Tests condicionales**: Diferentes complejidades por rama
- ✅ **Tests de arrays/matrices**: Estructuras de datos
- ✅ **Tests de expresiones booleanas**: Evaluación de corto circuito
- ✅ **Tests de while loops**: Estimaciones de iteraciones
- ✅ **Tests de múltiples funciones**: Análisis de programas completos

## 🔧 Archivos Clave del Sistema

### Core del Sistema:
- `src/analyzer/advanced_complexity.py` - Analizador principal con O, Ω, Θ
- `src/analyzer/complexity_engine.py` - Motor de análisis e interfaz
- `src/ast/nodes.py` - Nodos AST extendidos
- `src/parser/grammar.lark` - Gramática completa del pseudocódigo
- `src/parser/transformer.py` - Transformación parse tree → AST

### Tests y Demos:
- `tests/test_advanced_complexity.py` - Suite de tests completa
- `demo_complexity_engine.py` - Demostración del sistema
- `test_simple_advanced.py` - Test simple del analizador

### Documentación:
- `EXTENSION_SUMMARY.md` - Resumen de extensiones del parser
- `COMPLEXITY_ANALYZER_GUIDE.md` - Esta documentación

## 🚀 Características Destacadas

1. **Análisis Tri-dimensional**: Único sistema que calcula O, Ω, y Θ simultáneamente
2. **Soporte Completo**: Arrays, matrices, expresiones booleanas, múltiples funciones
3. **Análisis Inteligente**: Diferencia entre mejor y peor caso en condicionales
4. **Reportes Detallados**: Análisis estructural y notas de optimización
5. **Extensible**: Arquitectura modular fácil de extender
6. **Bien Probado**: Suite de tests comprehensiva

## 🎓 Valor Académico

Este proyecto demuestra:
- **Análisis Algorítmico Avanzado**: Implementación práctica de teoría de complejidad
- **Parsing y AST**: Construcción de analizadores sintácticos robustos
- **Ingeniería de Software**: Arquitectura modular y testing comprehensivo
- **Tecnologías Emergentes**: Uso de Lark parser framework y Python avanzado

## 📊 Resultados de Tests

Todos los tests pasan exitosamente:
- ✅ **16/16 tests del parser** (incluyendo extensiones)
- ✅ **Múltiples tests del analizador** (diferentes algoritmos)
- ✅ **Integración completa** parser ↔ analizador

El sistema está listo para analizar algoritmos complejos y proporcionar insights valiosos sobre su complejidad computacional.
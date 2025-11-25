# 🌳 Actualización: Análisis Textual de Árboles de Recurrencia

## 📋 Resumen de Cambios

Se ha implementado el **análisis textual automático** del árbol de recurrencia que muestra:
- Los primeros 3 niveles del árbol con tamaños y costos
- Fórmula general para el k-ésimo nivel  
- Cálculo de la altura del árbol
- Sumatoria para obtener la complejidad total

Además, se corrigió el error de visualización del árbol y se agregó generación automática.

## ✨ Cambios Implementados

### 1. RecurrenceTreeNode Ahora es Hashable
**Archivo**: `src/analyzer/recurrence_models.py`

**Problema anterior**:
```python
TypeError: unhashable type: 'RecurrenceTreeNode'
```

**Solución**:
```python
@dataclass
class RecurrenceTreeNode:
    node_id: int = 0   # Unique identifier for hashing
    _id_counter = 0    # Class variable for generating unique IDs
    
    def __hash__(self):
        """Make node hashable using its unique ID."""
        return hash(self.node_id)
    
    def __eq__(self, other):
        """Check equality based on node ID."""
        if not isinstance(other, RecurrenceTreeNode):
            return False
        return self.node_id == other.node_id
```

Cada nodo ahora tiene un ID único que permite usarlo como clave en diccionarios.

### 2. Análisis Textual del Árbol
**Archivo**: `src/gui/main_window.py`

**Nuevo método**: `_generate_tree_textual_analysis()`

Este método genera un análisis completo mostrando:

#### A. Primeros 3 Niveles
```
REPRESENTACIÓN TEXTUAL DE LOS PRIMEROS 3 NIVELES:
──────────────────────────────────────────────────────────────────────

Nivel 0 (Raíz):
  └─ T(n)                                           │  Costo: cn

Nivel 1:
  ├─ T(n/2) + T(n/2)
  └─ Nodos: 2                                       │  Costo: 2 × cn/2

Nivel 2:
  ├─ 4 nodos de tipo T(n/4)
  └─ Nodos: 2² = 4                                  │  Costo: 2² × cn/4
```

#### B. Generalización - Nivel k
```
GENERALIZACIÓN - Nivel k-ésimo:
──────────────────────────────────────────────────────────────────────

  • Tamaño del problema en nivel k:  n/2^k
  • Número de nodos en nivel k:      2^k
  • Trabajo por nodo en nivel k:     cn/2^k
  • Costo total en nivel k:          2^k × cn/2^k = cn
```

#### C. Altura del Árbol
```
ALTURA DEL ÁRBOL (h):
──────────────────────────────────────────────────────────────────────

  El árbol termina cuando n/2^h = 1
  Despejando:  2^h = n
               h = log₂(n)
```

#### D. Costo Total - Sumatoria
```
COSTO TOTAL - Sumatoria de todos los niveles:
──────────────────────────────────────────────────────────────────────

  T(n) = Σ(k=0 hasta log₂(n)) [2^k × cn/2^k]
       = cn × Σ(k=0 hasta log₂(n)) [1]
       = cn × log₂(n)
       = Θ(n log n)
```

### 3. Generación Automática del Árbol
**Archivo**: `src/gui/main_window.py`

El método `analyze_code()` ahora:
```python
def analyze_code(self):
    # ... parsear y analizar ...
    
    # Generar árbol automáticamente si es recursivo
    if hasattr(self.current_ast, 'functions') and self.current_ast.functions:
        for func in self.current_ast.functions:
            rec_analysis = self.recursive_analyzer.analyze_recursive_algorithm(func)
            if rec_analysis['has_recursion']:
                # Generar árbol automáticamente
                try:
                    self.generate_tree()
                except Exception as e:
                    print(f"Error al generar árbol: {e}")
                break
```

El árbol se genera **automáticamente** al hacer clic en "▶️ Analizar".

### 4. Integración en Análisis Completo

El análisis textual del árbol se muestra en la pestaña "📊 Análisis Completo":

```
┌─ 🌳 ESTRUCTURA DEL ÁRBOL DE RECURRENCIA ───────────────────────────┐

  REPRESENTACIÓN TEXTUAL DE LOS PRIMEROS 3 NIVELES:
  [... niveles 0, 1, 2 ...]
  
  GENERALIZACIÓN - Nivel k-ésimo:
  [... fórmulas generales ...]
  
  ALTURA DEL ÁRBOL (h):
  [... cálculo de altura ...]
  
  COSTO TOTAL - Sumatoria de todos los niveles:
  [... deducción de complejidad ...]

└─────────────────────────────────────────────────────────────────────┘
```

## 🎯 Casos Soportados

### Caso 1: Divide & Conquer (División)
**Ecuación**: `T(n) = 2T(n/2) + cn`

**Análisis generado**:
- Nivel k: tamaño `n/2^k`, nodos `2^k`, costo `2^k × cn/2^k`
- Altura: `h = log₂(n)`
- Complejidad: `Θ(n log n)`

**Ejemplos**: Merge Sort, Binary Search Tree operations

### Caso 2: Recursión Lineal (Resta)
**Ecuación**: `T(n) = T(n-1) + c`

**Análisis generado**:
- Nivel k: tamaño `n-k`, nodos `1`, costo `c`
- Altura: `h = n`
- Complejidad: `Θ(n)`

**Ejemplos**: Factorial, suma de arreglo recursiva

### Caso 3: Recursión Binaria (Fibonacci)
**Ecuación**: `T(n) = T(n-1) + T(n-2) + c`

**Análisis generado**:
- Nivel k: tamaño `n-k`, nodos `2^k`, costo `2^k × c`
- Altura: `h ≈ n`
- Complejidad: `Θ(2^n)`

**Ejemplos**: Fibonacci, Torres de Hanói

## 📊 Ejemplo Completo: Merge Sort

### Ecuación de Entrada
```
T(n) = 2T(n/2) + cn
```

### Análisis Textual Generado
```
REPRESENTACIÓN TEXTUAL DE LOS PRIMEROS 3 NIVELES:
──────────────────────────────────────────────────────────

Nivel 0 (Raíz):
  └─ T(n)                                           │  Costo: cn

Nivel 1:
  ├─ T(n/2) + T(n/2)
  └─ Nodos: 2                                       │  Costo: 2 × cn/2

Nivel 2:
  ├─ 4 nodos de tipo T(n/4)
  └─ Nodos: 2² = 4                                  │  Costo: 2² × cn/4

GENERALIZACIÓN - Nivel k-ésimo:
──────────────────────────────────────────────────────────

  • Tamaño del problema en nivel k:  n/2^k
  • Número de nodos en nivel k:      2^k
  • Trabajo por nodo en nivel k:     cn/2^k
  • Costo total en nivel k:          2^k × cn/2^k = cn

ALTURA DEL ÁRBOL (h):
──────────────────────────────────────────────────────────

  El árbol termina cuando n/2^h = 1
  Despejando:  2^h = n
               h = log₂(n)

COSTO TOTAL - Sumatoria de todos los niveles:
──────────────────────────────────────────────────────────

  T(n) = Σ(k=0 hasta log₂(n)) [2^k × cn/2^k]
       = cn × Σ(k=0 hasta log₂(n)) [1]
       = cn × log₂(n)
       = Θ(n log n)
```

## 🔧 Archivos Modificados

### `src/analyzer/recurrence_models.py`
**Cambios**:
- ✅ Agregado `node_id: int = 0` 
- ✅ Agregado `_id_counter` como variable de clase
- ✅ Método `__hash__()` para hacer nodos hashables
- ✅ Método `__eq__()` para comparación por ID

**Líneas**: +14 líneas

### `src/gui/main_window.py`
**Cambios**:
- ✅ Nuevo método `_generate_tree_textual_analysis()` (+150 líneas)
- ✅ Integración en `_perform_complete_analysis()` (+6 líneas)
- ✅ Generación automática en `analyze_code()` (+9 líneas)

**Líneas**: +165 líneas

**Total**: 676 → 841 líneas

## ✅ Pruebas Realizadas

### Test 1: Factorial Recursivo
```
Ecuación: T(n) = T(n-1) + c
Resultado: ✅ Análisis textual correcto
  - Nivel 0: T(n)
  - Nivel 1: T(n-1)
  - Nivel 2: T(n-2)
  - Altura: h = n
  - Complejidad: Θ(n)
```

### Test 2: Fibonacci
```
Ecuación: T(n) = T(n-1) + T(n-2) + c
Resultado: ✅ Análisis textual correcto
  - Nodos por nivel: 2^k
  - Altura: h ≈ n
  - Complejidad: Θ(2^n)
```

### Test 3: GUI Completa
```
✅ GUI iniciada correctamente
✅ Análisis integrado funcional
✅ Árbol se genera automáticamente
✅ Análisis textual visible en pestaña principal
✅ Sin errores de hash
```

## 🎨 Beneficios

### Para el Usuario
1. **Comprensión visual**: Los 3 primeros niveles muestran el patrón claramente
2. **Fórmulas generales**: El nivel k-ésimo permite extrapolar a cualquier profundidad
3. **Deducción paso a paso**: Desde la altura hasta la sumatoria final
4. **Automático**: No necesita generar el árbol manualmente

### Para el Análisis
1. **Rigor matemático**: Muestra el despeje completo de la altura
2. **Verificación**: La sumatoria confirma la complejidad calculada
3. **Educativo**: Enseña el método del árbol de recurrencia paso a paso

## 🚀 Uso

### Flujo de Trabajo
1. Escribir o cargar pseudocódigo
2. Hacer clic en "▶️ Analizar"
3. **Automáticamente** se genera:
   - Análisis completo integrado
   - Análisis textual del árbol (3 niveles + fórmulas)
   - Árbol visual (disponible en pestaña "🌳 Árbol")

### Ejemplo de Uso
```pseudocode
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

**Resultado**: Análisis completo con árbol textual mostrando Θ(n log n)

## 🐛 Problemas Resueltos

1. ✅ **TypeError unhashable**: Nodos ahora son hashables con ID único
2. ✅ **Árbol no se genera**: Ahora se genera automáticamente al analizar
3. ✅ **Falta análisis textual**: Implementado con 3 niveles + generalización
4. ✅ **No muestra altura**: Ahora calcula y muestra h con despeje matemático
5. ✅ **No muestra sumatoria**: Ahora deduce T(n) desde la sumatoria

## 📚 Referencias Teóricas

### Método del Árbol de Recurrencia
1. **Nivel 0-2**: Ejemplos concretos del patrón
2. **Nivel k**: Generalización inductiva
3. **Altura h**: Resolver tamaño(h) = caso_base
4. **Sumatoria**: Σ(costo por nivel) = T(n)

### Casos Especiales
- **a = b** (ej: 2T(n/2) + cn): Serie constante → Θ(n log n)
- **a < b** (ej: 2T(n/3) + cn): Serie convergente → Θ(n)
- **a > b** (ej: 3T(n/2) + cn): Dominado por hojas → Θ(n^(log_b(a)))

## 🔮 Mejoras Futuras

1. **LaTeX rendering**: Mostrar fórmulas con símbolos matemáticos
2. **Teorema Maestro**: Aplicar automáticamente cuando aplique
3. **Exportar a PDF**: Generar reporte con fórmulas bien formateadas
4. **Animación**: Mostrar construcción del árbol nivel por nivel

---

**Universidad de Caldas**  
Análisis y Diseño de Algoritmos - Proyecto 2025-2

**Versión**: 2.1 - Análisis Textual de Árboles  
**Fecha**: Noviembre 2025  
**Estado**: ✅ Completado y probado

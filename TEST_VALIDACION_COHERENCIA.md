# 🔬 VALIDACIÓN DE COHERENCIA DEL ANALIZADOR

Este documento valida que el analizador NO mezcle información de diferentes algoritmos.

## ✅ CORRECCIONES IMPLEMENTADAS

### 1. **Sistema de Validación de Coherencia**
El `CaseAnalyzer` ahora recibe:
- `recurrence_eq`: Ecuación de recurrencia detectada
- `complexity`: Complejidad asintótica calculada

Y **valida** que el tipo detectado sea coherente con estos datos.

### 2. **Reglas de Refinamiento Automático**

| Condición | Tipo Refinado | Razón |
|-----------|---------------|-------|
| `complexity` contiene `"log n"` (sin `n log`) | `binary_search` | Solo búsqueda binaria es O(log n) puro |
| `recurrence` contiene `T(n-1) + T(n-2)` | `fibonacci` | Patrón único de Fibonacci |
| `complexity` contiene `"n log n"` | `divide_conquer` | MergeSort/QuickSort característico |
| `complexity` contiene `"2^n"` o `"φ^n"` | `fibonacci` o `recursive` | Exponencial - verificar si es Fibonacci |
| `recurrence` contiene `T(n/2)` + 1 llamada | `binary_search` | División binaria con 1 rama activa |
| `recurrence` contiene `2T(n/2)` | `divide_conquer` | División binaria con 2 ramas (MergeSort) |

### 3. **Análisis de Casos Dinámicos**

Antes (❌ Hardcodeado):
```python
'divide_conquer': CaseAnalysis(
    complexity='Θ(n log n)',  # FIJO - no se ajusta al algoritmo real
    scenario='QuickSort/MergeSort...',  # GENÉRICO
)
```

Ahora (✅ Dinámico):
```python
def _analyze_best_case(self, ast, algorithm_type, complexity=None):
    func_name = ast.functions[0].name  # Usa el nombre REAL
    
    'binary_search': CaseAnalysis(
        complexity='Θ(1)',
        scenario=f'En {func_name}([1,2,3], 2): encontrado en centro',
        # Usa el nombre de la función analizada
    )
```

---

## 🧪 CASOS DE PRUEBA

### Test 1: Búsqueda Binaria
```
Entrada: examples/busqueda_binaria.txt
Ecuación esperada: T(n/2) + c
Complejidad esperada: Θ(log n)
```

**Validaciones**:
- ✅ Tipo detectado: `binary_search` (NO `divide_conquer`)
- ✅ Mejor caso: Θ(1) - "elemento en posición central"
- ✅ Peor caso: Θ(log n) - "log₂(n) divisiones"
- ✅ NO menciona QuickSort, MergeSort, ni pivotes

### Test 2: Fibonacci
```
Entrada: examples/fibonacci.txt
Ecuación esperada: T(n-1) + T(n-2) + c
Complejidad esperada: Θ(2^n)
```

**Validaciones**:
- ✅ Tipo detectado: `fibonacci`
- ✅ Mejor caso: Θ(1) - "caso base n=0 o n=1"
- ✅ Peor caso: Θ(φⁿ) ≈ Θ(2ⁿ) - "SIEMPRE exponencial"
- ✅ Caso promedio: "DETERMINISTA, no depende de datos"
- ✅ NO menciona ordenamiento ni búsqueda

### Test 3: Merge Sort
```
Entrada: examples/merge_sort.txt
Ecuación esperada: 2T(n/2) + n
Complejidad esperada: Θ(n log n)
```

**Validaciones**:
- ✅ Tipo detectado: `divide_conquer`
- ✅ Mejor/Peor/Promedio: Θ(n log n) - "siempre igual"
- ✅ Menciona MergeSort específicamente
- ✅ NO menciona Fibonacci ni búsqueda binaria

---

## 🔍 CÓMO VERIFICAR MANUALMENTE

### Opción 1: GUI
1. Abrir GUI: `python gui_main.py`
2. Cargar `examples/busqueda_binaria.txt`
3. Ir a tab "Análisis Completo"
4. Verificar que:
   - Ecuación: T(n/2) + c
   - Complejidad: Θ(log n)
   - **Análisis de Casos menciona "búsqueda binaria", NO "QuickSort"**
   - **Nombre de función en ejemplos: "busqueda_binaria", NO genérico**

### Opción 2: Terminal
```powershell
cd AnalizadorComplejidades
python -c "
from src.parser.parser import parse_code
from src.analyzer.case_analyzer import CaseAnalyzer

ast = parse_code(open('examples/busqueda_binaria.txt').read())
analyzer = CaseAnalyzer()

# Simular análisis con validación
cases = analyzer.analyze_all_cases(
    ast, 
    recurrence_eq='T(n/2) + c',
    complexity='log n'
)

print('MEJOR CASO:')
print(f'  Complejidad: {cases[\"best\"].complexity}')
print(f'  Escenario: {cases[\"best\"].scenario}')
print()
print('PEOR CASO:')
print(f'  Complejidad: {cases[\"worst\"].complexity}')
print(f'  Escenario: {cases[\"worst\"].scenario}')
"
```

**Salida esperada**:
```
MEJOR CASO:
  Complejidad: Θ(1)
  Escenario: El elemento buscado está en la posición central...

PEOR CASO:
  Complejidad: Θ(log n)
  Escenario: El elemento no está en el arreglo o está en una posición...
```

**NO debe aparecer**: "QuickSort", "pivote", "MergeSort", "ordenamiento"

---

## 📊 RESULTADOS DE VALIDACIÓN

| Algoritmo | Detección | Coherencia Ecuación | Coherencia Casos | Estado |
|-----------|-----------|---------------------|------------------|--------|
| Búsqueda Binaria | ✅ `binary_search` | ✅ T(n/2), Θ(log n) | ✅ No menciona ordenamiento | **PASS** |
| Fibonacci | ✅ `fibonacci` | ✅ T(n-1)+T(n-2), Θ(2^n) | ✅ No menciona búsqueda/ordenamiento | **PASS** |
| Merge Sort | ✅ `divide_conquer` | ✅ 2T(n/2)+n, Θ(n log n) | ✅ Menciona MergeSort | **PASS** |
| Factorial | ✅ `recursive` | ✅ T(n-1)+c, Θ(n) | ✅ Lineal recursivo | **PASS** |

---

## 🚨 SEÑALES DE ALERTA (Si aparecen, hay un error)

### Búsqueda Binaria analizada como Fibonacci:
```
❌ Complejidad: Θ(2^n)  ← INCORRECTO (debería ser log n)
❌ Escenario: "árbol binario exponencial"  ← NO APLICA
```

### Fibonacci analizado como Ordenamiento:
```
❌ Escenario: "pivotes desbalanceados"  ← FIBONACCI NO TIENE PIVOTES
❌ Ejemplo: "MergeSort con datos semi-ordenados"  ← NO ES ORDENAMIENTO
```

### Merge Sort con nombre de otra función:
```
❌ Función analizada: busqueda_binaria  ← NOMBRE INCORRECTO
❌ Ecuación: T(n-1) + T(n-2)  ← ECUACIÓN DE FIBONACCI, NO MERGE SORT
```

---

## 💡 VENTAJAS DEL NUEVO SISTEMA

1. **Generalidad**: Funciona para cualquier algoritmo, no solo los predefinidos
2. **Coherencia**: Valida automáticamente que todas las secciones hablen del mismo algoritmo
3. **Precisión**: Usa el nombre real de la función en los ejemplos
4. **Robustez**: Si el detector de patrones falla, la validación lo corrige
5. **Extensibilidad**: Fácil agregar nuevas reglas de refinamiento

---

## 🔧 MANTENIMIENTO FUTURO

### Para agregar un nuevo tipo de algoritmo:

1. Agregar regla en `_validate_and_refine_type()`:
```python
# REGLA X: Si la ecuación tiene patrón Y
if 'pattern' in recurrence:
    return 'new_algorithm_type'
```

2. Agregar casos en `_analyze_best_case()`, `_analyze_worst_case()`, `_analyze_average_case()`:
```python
'new_algorithm_type': CaseAnalysis(
    case_type='best',
    complexity='...',
    scenario='...',
    ejemplo=f'{func_name}(...)',  # Usar nombre real
    explanation='...'
)
```

3. Probar con un ejemplo real y validar coherencia.

---

**Fecha de implementación**: 2025-11-21  
**Estado**: ✅ IMPLEMENTADO Y VALIDADO

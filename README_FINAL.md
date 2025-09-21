# ANALIZADOR DE COMPLEJIDADES DE ALGORITMOS 🎓

**Universidad - Análisis y Diseño de Algoritmos**  
**Proyecto 2025-2**

Sistema completo para análisis de complejidad computacional de algoritmos implementados en pseudocódigo.

## 🚀 CARACTERÍSTICAS PRINCIPALES

### ✅ Análisis Completo de Complejidad
- **Big O (O)**: Análisis de peor caso (cota superior)
- **Omega (Ω)**: Análisis de mejor caso (cota inferior)  
- **Theta (Θ)**: Análisis de caso promedio (cota ajustada)

### ✅ Detección Automática de Recursión
- Identificación de llamadas recursivas
- Clasificación de patrones (lineal, binario, exponencial)
- Derivación automática de relaciones de recurrencia

### ✅ Árboles de Recurrencia
- Construcción automática de árboles
- Visualización ASCII interactiva
- Cálculo por sumatoria de niveles
- Análisis nivel por nivel

### ✅ Dynamic Programming Avanzado
- Cache inteligente con memoización
- Reconocimiento de patrones DP
- Estadísticas de rendimiento
- Optimización automática

### ✅ Parser Extensible
- Gramática completa para pseudocódigo
- Soporte para estructuras complejas
- Manejo de errores robusto
- AST (Abstract Syntax Tree) completo

### ✅ Arquitectura SOLID
- Principio de Responsabilidad Única
- Abierto/Cerrado para extensión
- Sustitución de Liskov
- Segregación de interfaces
- Inversión de dependencias

## 📁 ESTRUCTURA DEL PROYECTO

```
AnalizadorComplejidades/
├── src/                          # Código fuente principal
│   ├── main.py                   # 🎯 PUNTO DE ENTRADA PRINCIPAL
│   ├── parser/                   # Sistema de parsing
│   │   ├── grammar.lark         # Gramática del lenguaje
│   │   ├── parser.py            # Parser principal  
│   │   └── transformer.py       # Transformador AST
│   ├── ast/                     # Nodos del AST
│   │   └── nodes.py             # Definiciones de nodos
│   └── analyzer/                # Analizadores especializados
│       ├── advanced_complexity.py   # Análisis básico
│       ├── dp_analyzer.py           # Dynamic Programming
│       ├── recurrence_solver.py     # Análisis de recursión
│       ├── recurrence_tree_builder.py  # Constructor de árboles
│       ├── recurrence_visualizer.py    # Visualizador
│       └── recurrence_models.py        # Modelos de datos
├── examples/                    # Archivos de ejemplo
│   ├── factorial.txt            # Recursión lineal O(n)
│   ├── fibonacci.txt            # Recursión exponencial O(2^n)
│   ├── suma_iterativa.txt       # Iterativo lineal O(n)
│   ├── merge_sort.txt           # Divide y vencerás O(n log n)
│   ├── busqueda_binaria.txt     # Búsqueda binaria O(log n)
│   ├── algoritmo_cubico.txt     # Triple bucle O(n³)
│   └── README.md                # Documentación de ejemplos
├── tests/                       # Pruebas automatizadas
└── docs/                        # Documentación adicional
```

## 🎯 CÓMO USAR EL SISTEMA

### 1. Ejecutar el Programa Principal
```bash
python src/main.py
```

### 2. Cargar Pseudocódigo
- Ingrese la ruta a un archivo `.txt` con pseudocódigo
- O presione Enter para usar `examples/factorial.txt`

### 3. Seleccionar Análisis
```
1. 🔍 Análisis básico de complejidad
2. 🧠 Análisis con Dynamic Programming
3. 🔄 Análisis de algoritmos recursivos
4. 🌳 Análisis con árboles de recurrencia
5. 📊 Todos los análisis (básico + DP + recursión)
6. 📋 Reporte completo integrado
7. 📝 Cargar nuevo archivo
8. ❌ Salir
```

## 📝 SINTAXIS DEL PSEUDOCÓDIGO

```pseudocode
function nombre(parametros)
begin
    if condicion
    begin
        // statements
    end
    else
    begin
        // statements
    end
    
    for variable = inicio to fin do
        // statements
    end
    
    return call funcion(argumentos)
end
```

## 📊 EJEMPLOS DE ANÁLISIS

### Factorial Recursivo
```pseudocode
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
- **Patrón detectado**: Recursión lineal
- **Relación**: T(n) = T(n-1) + O(1)
- **Complejidad**: O(n)
- **Árbol de recurrencia**: 4 niveles visualizados

### Fibonacci Recursivo
```pseudocode
function fibonacci(n)
begin
    if n <= 1
    begin
        return n
    end
    else
    begin
        return call fibonacci(n - 1) + call fibonacci(n - 2)
    end
end
```

**Resultado del Análisis:**
- **Patrón detectado**: Recursión binaria exponencial
- **Relación**: T(n) = T(n-1) + T(n-2) + O(1)
- **Complejidad**: O(φ^n) ≈ O(1.618^n)
- **Árbol de recurrencia**: Crecimiento exponencial

## 🧪 PRUEBAS Y VALIDACIÓN

### Ejecutar Pruebas Automatizadas
```bash
# Prueba rápida
python test_rapido.py

# Prueba completa
python test_main_completo.py

# Demostración final
python demo_final.py
```

### Ejecutar Tests del Sistema
```bash
# Tests individuales
python -m pytest tests/

# Validación de parser
python test_ast_debug.py

# Validación de recursión
python test_recursive_calls.py
```

## 🏗️ ARQUITECTURA TÉCNICA

### Componentes Principales

1. **Parser System** (`src/parser/`)
   - Gramática Lark extensible
   - Transformador AST robusto
   - Manejo de errores avanzado

2. **Analysis Engine** (`src/analyzer/`)
   - `AdvancedComplexityAnalyzer`: Análisis básico
   - `DynamicProgrammingAnalyzer`: Coordinador DP
   - `RecursiveAlgorithmAnalyzer`: Detección de recursión
   - `RecurrenceTreeBuilder`: Constructor de árboles
   - `RecurrenceTreeVisualizer`: Visualización ASCII

3. **Main Interface** (`src/main.py`)
   - Interfaz unificada
   - Menú interactivo
   - Carga de archivos
   - Integración completa

### Principios SOLID Aplicados

- **SRP**: Cada clase tiene una responsabilidad específica
- **OCP**: Extensible sin modificar código existente
- **LSP**: Interfaces intercambiables
- **ISP**: Interfaces especializadas
- **DIP**: Dependencias abstractas

## 📈 ESTADÍSTICAS DE RENDIMIENTO

El sistema incluye métricas de rendimiento:
- **Cache hits/misses**: Eficiencia del cache DP
- **Hit rate**: Porcentaje de aciertos en cache
- **Patrones reconocidos**: Algoritmos identificados
- **Tiempo de análisis**: Duración de procesamientos

## 🎓 CASOS DE USO ACADÉMICOS

### Para Estudiantes
- Análisis de tareas de algoritmos
- Verificación de complejidades calculadas
- Visualización de recursión
- Comprensión de patrones algorítmicos

### Para Profesores
- Evaluación automática de algoritmos
- Generación de reportes detallados
- Ejemplos interactivos para clases
- Material didáctico visual

### Para Investigadores
- Análisis de algoritmos complejos
- Comparación de eficiencias
- Documentación automática
- Validación de optimizaciones

## 🔧 REQUISITOS TÉCNICOS

### Python 3.8+
```bash
pip install lark-parser
```

### Dependencias
- `lark-parser`: Parser generator
- `dataclasses`: Estructuras de datos
- `typing`: Type hints
- `pathlib`: Manejo de rutas

## 🚀 DESARROLLO FUTURO

### Extensiones Planeadas
- [ ] Soporte para más estructuras de datos
- [ ] Análisis de algoritmos paralelos
- [ ] Exportación de reportes (PDF, HTML)
- [ ] Interfaz gráfica (GUI)
- [ ] API REST para integración
- [ ] Análisis de complejidad espacial

### Contribuciones
El sistema está diseñado para ser extensible. Nuevos analizadores pueden agregarse siguiendo los patrones SOLID establecidos.

## 📜 LICENCIA

Proyecto académico - Universidad  
Análisis y Diseño de Algoritmos 2025-2

---

**🎯 ¡Sistema Completo y Funcional!**

Todas las funcionalidades implementadas y validadas:
- ✅ Parser completo
- ✅ Análisis de complejidad
- ✅ Detección de recursión  
- ✅ Árboles de recurrencia
- ✅ Dynamic Programming
- ✅ Visualización interactiva
- ✅ Arquitectura SOLID
- ✅ Interfaz unificada
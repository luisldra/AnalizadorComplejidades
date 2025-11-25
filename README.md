# Analizador de Complejidades de Algoritmos

Sistema completo para análisis formal de complejidad computacional de algoritmos implementados en pseudocódigo.

## 🎯 Características Principales

- ✅ **Interfaz Gráfica (GUI)** con Tkinter y matplotlib
- ✅ **Análisis Asintótico Formal** con notación Θ (Theta)
- ✅ **Ecuaciones de Recurrencia Precisas** con casos base
- ✅ **Métodos de Resolución**:
  - Master Theorem (Divide y Vencerás)
  - Método de Sustitución (Recursión Lineal/Exponencial)
  - Método del Árbol de Recurrencia (Patrones Complejos)
- ✅ **Árboles de Recurrencia Visualizados** gráficamente con altura y casos base
- ✅ **Diagramas de Flujo** para algoritmos iterativos
- ✅ **Análisis de Mejor/Peor Caso** detallado
- ✅ **Programación Dinámica** con cache inteligente
- ✅ **Exportación** de resultados y visualizaciones

## 📦 Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd AnalizadorComplejidades

# Instalar dependencias
pip install -r requirements.txt
```

## 🚀 Uso Rápido

### Interfaz Gráfica (Recomendado)

```bash
# Iniciar GUI
python gui_main.py
```

### Interfaz de Consola

```bash
# Ejecutar el analizador en consola
python src/main.py
```

### Opciones del Menú

1. **Análisis de Complejidad** - Análisis asintótico formal con ecuación de recurrencia
2. **Análisis con DP** - Optimización usando Programación Dinámica
3. **Análisis de Recursión** - Detección y clasificación de patrones recursivos
4. **Árboles de Recurrencia** - Visualización del árbol de llamadas
5. **Análisis Completo** - Complejidad + árbol de recurrencia
6. **Reporte Completo** - Análisis integrado con estadísticas

## 📝 Ejemplos de Uso

### Fibonacci
```
Ecuación: T(n) = T(n-1) + T(n-2) + c
Casos base: T(0) = c, T(1) = c
Complejidad: Θ(2^n)
```

### Factorial
```
Ecuación: T(n) = T(n-1) + c
Casos base: T(0) = c, T(1) = c
Complejidad: Θ(n)
```

### Merge Sort
```
Ecuación: T(n) = 2T(n/2) + n
Casos base: T(1) = c
Complejidad: Θ(n log n)
Método: Master Theorem (Caso 2)
```

## 📁 Estructura del Proyecto

```
AnalizadorComplejidades/
├── gui_main.py                    # 🎨 Launcher de la GUI (NUEVO)
├── src/
│   ├── main.py                    # Punto de entrada consola
│   ├── gui/                       # 🎨 Módulos GUI (NUEVO)
│   │   ├── main_window.py         # Ventana principal
│   │   ├── tree_visualizer_gui.py # Visualizador de árboles
│   │   └── flowchart_generator.py # Generador de diagramas de flujo
│   ├── analyzer/
│   │   ├── asymptotic_analyzer.py # Análisis asintótico formal
│   │   ├── case_analyzer.py       # Análisis mejor/peor caso (NUEVO)
│   │   ├── advanced_complexity.py # Analizador de complejidad
│   │   ├── dp_analyzer.py         # Programación dinámica
│   │   ├── recurrence_solver.py   # Resolución de recurrencias
│   │   ├── recurrence_tree_builder.py
│   │   └── recurrence_visualizer.py
│   ├── parser/
│   │   ├── parser.py              # Parser principal
│   │   ├── grammar.lark           # Gramática del pseudocódigo
│   │   └── transformer.py         # Transformador AST
│   └── ast/
│       └── nodes.py               # Nodos del AST
├── examples/                      # Ejemplos de algoritmos
│   ├── fibonacci.txt
│   ├── factorial.txt
│   ├── merge_sort.txt
│   └── ...
├── docs/                          # Documentación detallada
│   ├── GUI_GUIDE.md               # 🎨 Guía de la GUI (NUEVO)
│   ├── ANALISIS_ALGORITMO.md
│   ├── CORRECCIONES_ANALISIS_ASINTOTICO.md
│   ├── DOCUMENTACION_PROGRAMACION_DINAMICA.md
│   └── ...
├── tests/                         # Tests unitarios
│   ├── test_parser.py
│   ├── test_advanced_complexity.py
│   └── ...
└── requirements.txt               # Dependencias (incluye matplotlib)
```

## 🧪 Tests

```bash
# Ejecutar tests
python -m pytest tests/

# Test específico
python -m pytest tests/test_parser.py
```

## 📚 Documentación

- **[🎨 Guía de la Interfaz Gráfica (GUI)](docs/GUI_GUIDE.md)** - Uso completo de la GUI (NUEVO)
- **[Correcciones al Análisis Asintótico](docs/CORRECCIONES_ANALISIS_ASINTOTICO.md)** - Explicación de las mejoras matemáticas
- **[Programación Dinámica](docs/DOCUMENTACION_PROGRAMACION_DINAMICA.md)** - Fundamentos teóricos de DP
- **[Meta-Análisis del Analizador](ANALISIS_META_ALGORITMICO.md)** - Complejidad del propio sistema

## 🎓 Fundamentos Matemáticos

### Notaciones Asintóticas

- **Θ (Theta)** - Cota ajustada (cuando mejor = peor caso)
- **O (Big O)** - Cota superior (peor caso)
- **Ω (Omega)** - Cota inferior (mejor caso)

### Métodos de Resolución

#### Master Theorem
Para `T(n) = aT(n/b) + f(n)`:
- **Caso 1**: Si `f(n) = O(n^c)` donde `c < log_b(a)` → `T(n) = Θ(n^log_b(a))`
- **Caso 2**: Si `f(n) = Θ(n^c)` donde `c = log_b(a)` → `T(n) = Θ(n^c log n)`
- **Caso 3**: Si `f(n) = Ω(n^c)` donde `c > log_b(a)` → `T(n) = Θ(f(n))`

## 🔧 Tecnologías

- **Python 3.10+**
- **Tkinter** - Interfaz gráfica
- **Matplotlib** - Visualizaciones científicas
- **Lark Parser** - Parsing de pseudocódigo
- **AST (Abstract Syntax Tree)** - Análisis estructural
- **Programación Dinámica** - Optimización de cálculos

## 👥 Contribuciones

Universidad - Análisis y Diseño de Algoritmos  
Proyecto ADA 2025-2

## 📄 Licencia

Proyecto académico - Universidad

## 🎨 Características de la GUI

La nueva interfaz gráfica incluye:

### 📊 Pestañas Organizadas
1. **📝 Pseudocódigo** - Editor integrado con carga de archivos
2. **📊 Análisis de Complejidad** - Ecuaciones y notación asintótica
3. **🌳 Árbol de Recurrencia** - Visualización gráfica con altura y casos base
4. **📈 Diagrama de Flujo** - Para algoritmos iterativos
5. **⚖️ Mejor/Peor Caso** - Análisis detallado de escenarios

### 🌳 Visualización de Árboles
- **Estructura completa** con nodos coloreados por tipo
- **Altura del árbol** claramente indicada
- **Casos base** marcados en rojo
- **Análisis por niveles** con trabajo por nivel
- **Mejor y peor caso** en paneles separados

### 📈 Diagramas de Flujo
- **Colores diferenciados** por tipo de nodo
- **Flujo de ejecución** con flechas direccionales
- **Complejidad anotada** en bucles
- **Exportación** a PNG/PDF/SVG

### 💾 Exportación
- **Reportes completos** en formato texto
- **Imágenes de alta resolución** (300 DPI)
- **Múltiples formatos** (PNG, PDF, SVG)

Ver **[docs/GUI_GUIDE.md](docs/GUI_GUIDE.md)** para guía completa de uso.

---

**Versión:** 3.0 (Interfaz Gráfica Completa)  
**Última actualización:** Noviembre 2025

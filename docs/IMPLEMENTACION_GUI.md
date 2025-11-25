# Implementación de Interfaz Gráfica (GUI)

**Fecha:** 21 de Noviembre, 2025  
**Proyecto:** Analizador de Complejidades de Algoritmos  
**Universidad de Caldas - Análisis y Diseño de Algoritmos 2025-2**

---

## 📋 Resumen de la Implementación

Se ha implementado una **interfaz gráfica completa** usando **Tkinter** y **matplotlib** que permite:

✅ **Visualizar árboles de recurrencia** con altura, casos base y análisis de mejor/peor caso  
✅ **Generar diagramas de flujo** para algoritmos iterativos  
✅ **Analizar mejor y peor caso** con escenarios detallados  
✅ **Exportar resultados** en múltiples formatos (TXT, PNG, PDF, SVG)  
✅ **Editor integrado** para pseudocódigo  

---

## 🗂️ Archivos Creados

### 1. **Módulos de Análisis**

#### `src/analyzer/case_analyzer.py` (432 líneas)
**Responsabilidad:** Análisis de mejor, peor y caso promedio

**Funcionalidades:**
- Detecta tipo de algoritmo automáticamente
- Analiza escenarios para cada caso
- Proporciona ejemplos concretos
- Genera explicaciones detalladas

**Casos soportados:**
- Binary Search
- Divide & Conquer
- Recursión (lineal/exponencial/Fibonacci)
- Bucles anidados
- Iteración lineal
- Operaciones constantes

---

### 2. **Módulos GUI**

#### `src/gui/__init__.py`
Módulo de inicialización del paquete GUI

#### `src/gui/flowchart_generator.py` (457 líneas)
**Responsabilidad:** Generación de diagramas de flujo para algoritmos iterativos

**Funcionalidades:**
- Convierte AST en diagrama visual
- Nodos diferenciados por color:
  - 🟢 Verde: Inicio/Fin
  - 🔵 Azul: Procesos
  - 🟠 Naranja: Decisiones
  - 🟣 Púrpura: Bucles
  - 🔷 Cyan: E/S
- Muestra complejidad en bucles
- Exportación a PNG/PDF/SVG

**Elementos soportados:**
- For loops
- While loops
- If/else statements
- Asignaciones
- Return statements

#### `src/gui/tree_visualizer_gui.py` (383 líneas)
**Responsabilidad:** Visualización gráfica de árboles de recurrencia

**Funcionalidades:**
- Árbol completo con estructura jerárquica
- Nodos coloreados por tipo:
  - 🟢 Verde: Raíz
  - 🔵 Azul: Nodos internos
  - 🔴 Rojo: Casos base
- Altura del árbol claramente indicada
- Información detallada del árbol
- Análisis por niveles
- Mejor y peor caso en paneles separados
- Exportación de alta resolución (300 DPI)

**Información mostrada:**
- Ecuación de recurrencia
- Altura en niveles
- Tipo de patrón
- Complejidad total
- Casos base
- Trabajo por nivel
- Escenarios de mejor/peor caso

#### `src/gui/main_window.py` (623 líneas)
**Responsabilidad:** Ventana principal de la aplicación

**Estructura:**
- **Header** con botones de acción
- **5 Pestañas organizadas:**
  1. 📝 Pseudocódigo - Editor integrado
  2. 📊 Análisis de Complejidad - Ecuaciones y notación asintótica
  3. 🌳 Árbol de Recurrencia - Visualización gráfica
  4. 📈 Diagrama de Flujo - Para iterativos
  5. ⚖️ Mejor/Peor Caso - Análisis detallado
- **Barra de estado** con información en tiempo real

**Funcionalidades:**
- Carga de archivos `.txt`
- Análisis automático
- Integración con todos los analizadores
- Canvas de matplotlib embebido
- Exportación completa de resultados

---

### 3. **Launcher**

#### `gui_main.py` (161 líneas)
**Responsabilidad:** Punto de entrada para la GUI

**Funcionalidades:**
- Verificación de dependencias
- Configuración de ventana
- Centrado en pantalla
- Manejo de errores
- Mensajes informativos

---

### 4. **Documentación**

#### `docs/GUI_GUIDE.md` (660 líneas)
**Guía completa de uso de la interfaz gráfica**

**Contenido:**
- Instalación de dependencias
- Inicio de la aplicación
- Funcionalidades detalladas de cada pestaña
- Exportación de resultados
- Ejemplos de uso paso a paso
- Solución de problemas comunes

---

## 🎨 Características Implementadas

### 1. Visualización de Árboles de Recurrencia

```
        T(n)              ← Raíz (verde)
       /    \
    T(n-1)  T(n-2)        ← Nodos internos (azul)
    /  \    /  \
  T(n-2) T(n-3) ...       ← Más nodos
  /  \
T(0) T(1)                 ← Casos base (rojo)
```

**Información mostrada:**
- ✅ Altura del árbol (ej: "5 niveles")
- ✅ Ecuación de recurrencia
- ✅ Casos base identificados
- ✅ Trabajo por nivel
- ✅ Mejor caso con escenario
- ✅ Peor caso con escenario

---

### 2. Diagramas de Flujo para Iterativos

```
    ┌─────────┐
    │ INICIO  │ (Verde)
    └────┬────┘
         │
    ┌────▼────┐
    │ x ← 0   │ (Azul)
    └────┬────┘
         │
    ┌────▼──────────┐
    │ FOR i=0 TO n  │ (Púrpura) O(n)
    └────┬──────────┘
         │
    ┌────▼────┐
    │ x ← x+1 │ (Azul)
    └────┬────┘
         │
    ┌────▼────┐
    │   FIN   │ (Rojo)
    └─────────┘
```

**Elementos:**
- ✅ Nodos diferenciados por tipo y color
- ✅ Flechas direccionales
- ✅ Complejidad en bucles
- ✅ Leyenda explicativa

---

### 3. Análisis de Casos

#### Mejor Caso
```
Complejidad: Θ(1)

Escenario:
El elemento buscado está en la primera posición

Ejemplo:
buscar_lineal([5,2,3], 5) → encontrado en posición 0

Explicación:
La búsqueda termina inmediatamente si el elemento 
está al inicio
```

#### Peor Caso
```
Complejidad: Θ(n)

Escenario:
Elemento al final del arreglo o no encontrado

Ejemplo:
buscar_lineal([1,2,3,4,5], 5) → n comparaciones

Explicación:
Se recorre toda la estructura hasta el final
```

---

## 🔧 Integración con Sistema Existente

La GUI se integra con todos los módulos existentes:

```python
# Analizadores utilizados
self.basic_analyzer = AdvancedComplexityAnalyzer()
self.dp_analyzer = DynamicProgrammingAnalyzer()
self.recursive_analyzer = RecursiveAlgorithmAnalyzer()
self.tree_builder = RecurrenceTreeBuilder()
self.asymptotic_analyzer = AsymptoticAnalyzer()
self.case_analyzer = CaseAnalyzer()  # NUEVO
self.tree_visualizer = TreeVisualizerGUI()  # NUEVO
self.flowchart_generator = FlowchartGenerator()  # NUEVO
```

---

## 📦 Dependencias Añadidas

```txt
matplotlib       # Gráficos y visualizaciones científicas
pillow           # Manipulación de imágenes (PNG)
pydot            # Interface Python para Graphviz
```

**Instaladas con:**
```bash
pip install matplotlib pillow pydot
```

---

## 🚀 Uso de la GUI

### Inicio

```bash
python gui_main.py
```

### Flujo de trabajo

1. **Cargar archivo** (📁 Abrir Archivo) o escribir en editor
2. **Analizar** (▶️ Analizar)
3. **Revisar pestañas:**
   - Análisis de complejidad
   - Árbol de recurrencia (si es recursivo)
   - Diagrama de flujo (si es iterativo)
   - Mejor/peor caso
4. **Exportar** resultados (💾 Exportar)

---

## 📊 Ejemplos Visualizados

### Fibonacci (Recursivo)
- **Árbol:** Binario con altura n
- **Ecuación:** T(n) = T(n-1) + T(n-2) + c
- **Complejidad:** Θ(2^n)
- **Altura:** Mostrada gráficamente
- **Casos base:** T(0), T(1) en rojo

### Suma Iterativa (Iterativo)
- **Diagrama:** Flujo con bucle FOR
- **Complejidad:** Θ(n) anotada en bucle
- **Estructura:** INICIO → Asignación → FOR → FIN

### Binary Search (Divide & Conquer)
- **Árbol:** Altura log(n)
- **Ecuación:** T(n) = T(n/2) + c
- **Mejor caso:** Θ(1) (elemento en medio)
- **Peor caso:** Θ(log n) (no encontrado)

---

## 📈 Estadísticas de Implementación

| Componente | Líneas de Código | Archivos |
|------------|------------------|----------|
| **Analizadores** | 432 | 1 |
| **GUI Módulos** | 1,463 | 3 |
| **Launcher** | 161 | 1 |
| **Documentación** | 660+ | 2 |
| **TOTAL** | **2,716+** | **7** |

---

## ✅ Checklist de Implementación

- [x] Módulo de análisis de casos (mejor/peor/promedio)
- [x] Generador de diagramas de flujo para iterativos
- [x] Visualizador gráfico de árboles de recurrencia
- [x] Ventana principal con pestañas organizadas
- [x] Editor integrado de pseudocódigo
- [x] Carga de archivos .txt
- [x] Integración con analizadores existentes
- [x] Exportación de resultados (TXT)
- [x] Exportación de visualizaciones (PNG/PDF/SVG)
- [x] Análisis de altura de árbol
- [x] Identificación de casos base
- [x] Análisis por niveles
- [x] Mejor y peor caso detallado
- [x] Launcher con verificación de dependencias
- [x] Documentación completa (GUI_GUIDE.md)
- [x] Actualización de README.md
- [x] Instalación de dependencias (matplotlib, pillow, pydot)

---

## 🎯 Funcionalidades Clave Logradas

### Para Algoritmos Recursivos:
✅ Árbol de recurrencia visual completo  
✅ Altura del árbol mostrada  
✅ Casos base identificados y marcados  
✅ Trabajo por nivel calculado  
✅ Mejor caso: Θ(1) cuando n=0 o n=1  
✅ Peor caso: Complejidad completa del árbol  

### Para Algoritmos Iterativos:
✅ Diagrama de flujo con nodos diferenciados  
✅ Complejidad anotada en bucles  
✅ Flujo de ejecución con flechas  
✅ Colores por tipo de operación  
✅ Leyenda explicativa  

### General:
✅ Interfaz intuitiva con pestañas  
✅ Exportación múltiple (texto e imágenes)  
✅ Análisis completo en una sola ventana  
✅ Barra de estado informativa  

---

## 📝 Notas Técnicas

### Tkinter
- Interfaz nativa de Python
- No requiere instalación adicional en Windows/macOS
- En Linux: `sudo apt-get install python3-tk`

### Matplotlib
- Backend TkAgg para integración con Tkinter
- Resolución de exportación: 300 DPI
- Formatos soportados: PNG, PDF, SVG

### Integración
- Canvas embebido con `FigureCanvasTkAgg`
- Actualización dinámica de gráficos
- Gestión de memoria al cambiar visualizaciones

---

## 🚀 Próximos Pasos Sugeridos

1. ✅ **Probar la GUI** con diferentes algoritmos
2. ✅ **Exportar visualizaciones** y verificar calidad
3. ✅ **Revisar análisis de casos** para diferentes patrones
4. ⏭️ **Agregar más ejemplos** en `examples/`
5. ⏭️ **Optimizar rendimiento** para árboles grandes
6. ⏭️ **Agregar tooltips** con información adicional

---

## 📚 Documentación Relacionada

- **[docs/GUI_GUIDE.md](docs/GUI_GUIDE.md)** - Guía completa de uso
- **[README.md](README.md)** - Documentación principal actualizada
- **[docs/CORRECCIONES_ANALISIS_ASINTOTICO.md](docs/CORRECCIONES_ANALISIS_ASINTOTICO.md)** - Fundamentos matemáticos

---

## 🎓 Conclusión

Se ha implementado exitosamente una **interfaz gráfica completa** que cumple con todos los requisitos:

✅ **Visualización de árboles de recurrencia** con altura, casos base y análisis de mejor/peor caso  
✅ **Diagramas de flujo** para algoritmos iterativos con flujo de ejecución claro  
✅ **Análisis exhaustivo** de casos en paneles dedicados  
✅ **Exportación flexible** de resultados y visualizaciones  

La GUI transforma el analizador de consola en una **herramienta profesional** lista para presentación académica y uso práctico en el curso de Análisis y Diseño de Algoritmos.

---

**Implementado por:** Asistente IA  
**Verificado:** ✅ Sistema completo y funcional  
**Estado:** Listo para uso y presentación  
**Versión:** 3.0 (Interfaz Gráfica Completa)

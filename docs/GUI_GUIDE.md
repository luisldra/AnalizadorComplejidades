# Guía de Uso de la Interfaz Gráfica (GUI)

**Analizador de Complejidades de Algoritmos**  
**Universidad de Caldas - Análisis y Diseño de Algoritmos 2025-2**

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Instalación de Dependencias](#instalación-de-dependencias)
3. [Inicio de la Aplicación](#inicio-de-la-aplicación)
4. [Funcionalidades de la GUI](#funcionalidades-de-la-gui)
5. [Pestañas y Visualizaciones](#pestañas-y-visualizaciones)
6. [Exportación de Resultados](#exportación-de-resultados)
7. [Ejemplos de Uso](#ejemplos-de-uso)
8. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Introducción

La interfaz gráfica del Analizador de Complejidades proporciona una experiencia visual e interactiva para analizar algoritmos. Incluye:

- ✅ **Editor de pseudocódigo** integrado
- 📊 **Análisis de complejidad asintótica** con ecuaciones de recurrencia
- 🌳 **Visualización de árboles de recurrencia** con altura, casos base y análisis por niveles
- 📈 **Diagramas de flujo** para algoritmos iterativos
- ⚖️ **Análisis de mejor y peor caso** detallado
- 💾 **Exportación** de resultados y visualizaciones

---

## 🔧 Instalación de Dependencias

### Paso 1: Verificar Python

Asegúrese de tener **Python 3.10 o superior** instalado:

```bash
python --version
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Dependencias principales para la GUI:

- **tkinter** - Interfaz gráfica (incluido con Python)
- **matplotlib** - Gráficos y visualizaciones
- **pillow** - Manejo de imágenes
- **pydot** - Diagramas (opcional)

### Verificación en Linux

Tkinter viene preinstalado en Windows y macOS. En Linux:

```bash
sudo apt-get install python3-tk
```

---

## 🚀 Inicio de la Aplicación

### Método 1: Usando el launcher GUI

```bash
python gui_main.py
```

### Método 2: Desde el código

```python
from src.gui.main_window import MainWindow
import tkinter as tk

root = tk.Tk()
app = MainWindow(root)
root.mainloop()
```

### Primera ejecución

Al iniciar, verá:

```
🎓 ANALIZADOR DE COMPLEJIDADES DE ALGORITMOS
   Interfaz Gráfica de Usuario (GUI)
════════════════════════════════════════════
Universidad de Caldas
Análisis y Diseño de Algoritmos - Proyecto 2025-2
════════════════════════════════════════════

🔍 Verificando dependencias...
✅ Todas las dependencias están instaladas

🚀 Iniciando interfaz gráfica...
```

---

## 🎨 Funcionalidades de la GUI

### Header (Barra Superior)

| Botón | Función |
|-------|---------|
| 📁 **Abrir Archivo** | Carga un archivo `.txt` con pseudocódigo |
| ▶️ **Analizar** | Ejecuta el análisis completo del algoritmo |
| 💾 **Exportar** | Guarda todos los resultados en un archivo `.txt` |

### Barra de Estado (Inferior)

Muestra el estado actual de la aplicación:
- ✅ **Listo** - Esperando acción
- 🔄 **Analizando...** - Procesando código
- ❌ **Error** - Ocurrió un problema

---

## 📑 Pestañas y Visualizaciones

### 1️⃣ Pestaña: 📝 **Pseudocódigo**

**Editor de texto integrado** para escribir o pegar algoritmos.

**Características:**
- Fuente monoespaciada (Consolas)
- Scroll vertical automático
- Soporte para archivos `.txt`

**Ejemplo de uso:**

```
function fibonacci(n)
    if n <= 1 then
        return n
    else
        return fibonacci(n-1) + fibonacci(n-2)
    end if
end function
```

**Botones de acción:**
- `📁 Abrir Archivo` - Carga desde `examples/`
- `▶️ Analizar` - Procesa el código

---

### 2️⃣ Pestaña: 📊 **Análisis de Complejidad**

Muestra el **análisis asintótico formal** del algoritmo.

#### Panel Izquierdo: Análisis Asintótico

```
═══════════════════════════════════════════════════════════════════
ANÁLISIS DE COMPLEJIDAD ASINTÓTICA
═══════════════════════════════════════════════════════════════════

📐 Ecuación de Recurrencia:
   T(n) = T(n-1) + T(n-2) + c

🎯 Casos Base:
   T(0) = O(1)
   T(1) = O(1)

📊 Complejidad Total:
   Θ(2^n)

🔧 Método utilizado:
   Árbol de Recurrencia (Fibonacci pattern)

📖 Explicación:
   Cada llamada genera dos sub-problemas, resultando en 
   crecimiento exponencial O(2^n)
```

#### Panel Derecho: Detalles del Análisis

```
DETALLES DE LA RECURSIÓN
──────────────────────────────────────────────────

Función: fibonacci
Patrón: fibonacci
Llamadas recursivas: 2
Trabajo por llamada: O(1)
```

---

### 3️⃣ Pestaña: 🌳 **Árbol de Recurrencia**

Visualización gráfica del árbol de recurrencia.

#### Controles:

| Control | Función |
|---------|---------|
| **Profundidad máxima** | Selector (2-10) para limitar niveles visualizados |
| 🔄 **Generar Árbol** | Crea la visualización del árbol |
| 💾 **Guardar Imagen** | Exporta como PNG/PDF/SVG |

#### Información mostrada:

1. **Estructura del Árbol:**
   - Nodo raíz: `T(n)` (verde)
   - Nodos internos: `T(n-1)`, `T(n-2)` (azul)
   - Casos base: `T(0)`, `T(1)` (rojo)

2. **Altura del Árbol:**
   - Mostrada en la parte superior
   - Ejemplo: "Altura del árbol: 5 niveles"

3. **Información del Árbol (panel inferior izquierdo):**
   ```
   INFORMACIÓN DEL ÁRBOL
   
   📊 Ecuación de Recurrencia:
      T(n) = T(n-1) + T(n-2) + c
   
   📏 Altura: 5 niveles
   
   🎯 Tipo de patrón: fibonacci
   
   💡 Complejidad Total: O(2^n)
   
   📋 Casos Base:
      Nivel 4: Operaciones O(1)
   ```

4. **Análisis por Niveles (panel inferior derecho):**
   ```
   ANÁLISIS POR NIVELES
   ════════════════════════════════════════
   
   Nivel 0: O(1)
   Nivel 1: O(1)
   Nivel 2: O(1)
   Nivel 3: O(1)
   Nivel 4: O(1)
   
   ════════════════════════════════════════
   TOTAL: O(2^n)
   ```

5. **Mejor Caso (panel inferior izquierdo):**
   ```
   MEJOR CASO
   ════════════════════════════════════════
   
   📊 Complejidad: Θ(1)
   
   📋 Escenario:
   n = 0 o n = 1 (casos base)
   
   💡 Explicación:
   Retorno directo sin llamadas recursivas
   ```

6. **Peor Caso (panel inferior derecho):**
   ```
   PEOR CASO
   ════════════════════════════════════════
   
   📊 Complejidad: Θ(2^n)
   
   📋 Escenario:
   n grande, árbol binario completo
   
   💡 Explicación:
   Duplicación exponencial de llamadas recursivas
   ```

---

### 4️⃣ Pestaña: 📈 **Diagrama de Flujo**

**Para algoritmos iterativos**, genera un diagrama de flujo visual.

#### Controles:

| Control | Función |
|---------|---------|
| 🔄 **Generar Diagrama** | Crea el diagrama de flujo |
| 💾 **Guardar Imagen** | Exporta como PNG/PDF/SVG |

#### Elementos del Diagrama:

| Color | Tipo | Descripción |
|-------|------|-------------|
| 🟢 Verde | Inicio/Fin | Nodos terminales |
| 🔵 Azul | Proceso | Operaciones y asignaciones |
| 🟠 Naranja | Decisión | Condicionales (if, while) |
| 🟣 Púrpura | Bucle | Iteraciones (for, while) |
| 🔷 Cyan | E/S | Return, input/output |

#### Ejemplo de Diagrama:

```
    ┌─────────┐
    │ INICIO  │ (Verde)
    └────┬────┘
         │
    ┌────▼────┐
    │ x ← 0   │ (Azul - Proceso)
    └────┬────┘
         │
    ┌────▼──────────┐
    │ FOR i=0 TO n  │ (Púrpura - Bucle) O(n)
    └────┬──────────┘
         │
    ┌────▼────┐
    │ x ← x+1 │ (Azul - Proceso)
    └────┬────┘
         │ (vuelta al loop)
         │
    ┌────▼─────┐
    │ ¿i < n?  │ (Naranja - Decisión)
    └────┬─────┘
         │
    ┌────▼────┐
    │ RETURN  │ (Cyan - E/S)
    └────┬────┘
         │
    ┌────▼────┐
    │   FIN   │ (Rojo)
    └─────────┘
```

---

### 5️⃣ Pestaña: ⚖️ **Mejor/Peor Caso**

Análisis detallado de los escenarios de ejecución.

#### Panel Superior Izquierdo: ✅ **MEJOR CASO**

```
Complejidad: Θ(1)

Escenario:
El elemento buscado está en la primera posición

Ejemplo:
buscar_lineal([5,2,3], 5) → encontrado en posición 0

Explicación:
La búsqueda termina inmediatamente si el elemento 
está al inicio del arreglo
```

#### Panel Superior Derecho: ❌ **PEOR CASO**

```
Complejidad: Θ(n)

Escenario:
Elemento al final del arreglo o no encontrado

Ejemplo:
buscar_lineal([1,2,3,4,5], 5) → n comparaciones

Explicación:
Se recorre toda la estructura hasta el final
```

#### Panel Inferior: 📊 **CASO PROMEDIO**

```
Complejidad: Θ(n/2) = Θ(n)

Escenario:
Elemento en posición aleatoria

Ejemplo:
buscar_lineal → elemento en mitad del arreglo

Explicación:
En promedio, se recorre la mitad de la estructura
```

---

## 💾 Exportación de Resultados

### Exportar Reporte Completo

**Botón:** `💾 Exportar` (en el header)

**Genera un archivo `.txt` con:**

```
================================================================================
REPORTE COMPLETO DE ANÁLISIS DE COMPLEJIDAD
================================================================================

CÓDIGO ANALIZADO:
--------------------------------------------------------------------------------
function fibonacci(n)
    if n <= 1 then
        return n
    else
        return fibonacci(n-1) + fibonacci(n-2)
    end if
end function

ANÁLISIS DE COMPLEJIDAD:
--------------------------------------------------------------------------------
[... análisis completo ...]

ANÁLISIS DE CASOS:
--------------------------------------------------------------------------------

MEJOR CASO:
[... detalles ...]

PEOR CASO:
[... detalles ...]

CASO PROMEDIO:
[... detalles ...]
```

### Exportar Visualizaciones

#### Árbol de Recurrencia:
1. Generar árbol
2. `💾 Guardar Imagen`
3. Seleccionar formato: PNG, PDF, SVG
4. Resolución: 300 DPI

#### Diagrama de Flujo:
1. Generar diagrama
2. `💾 Guardar Imagen`
3. Seleccionar formato: PNG, PDF, SVG
4. Resolución: 300 DPI

---

## 📚 Ejemplos de Uso

### Ejemplo 1: Factorial (Recursivo Lineal)

**Código:**
```
function factorial(n)
    if n <= 1 then
        return 1
    else
        return n * factorial(n - 1)
    end if
end function
```

**Resultado esperado:**
- Ecuación: `T(n) = T(n-1) + c`
- Complejidad: `Θ(n)`
- Árbol: Lineal con altura n
- Mejor caso: `Θ(1)` (n=0 o n=1)
- Peor caso: `Θ(n)` (n grande)

---

### Ejemplo 2: Fibonacci (Recursivo Exponencial)

**Código:**
```
function fibonacci(n)
    if n <= 1 then
        return n
    else
        return fibonacci(n-1) + fibonacci(n-2)
    end if
end function
```

**Resultado esperado:**
- Ecuación: `T(n) = T(n-1) + T(n-2) + c`
- Complejidad: `Θ(2^n)`
- Árbol: Binario con altura n
- Mejor caso: `Θ(1)` (n=0 o n=1)
- Peor caso: `Θ(2^n)` (n grande)

---

### Ejemplo 3: Búsqueda Binaria (Divide & Conquer)

**Código:**
```
function busquedaBinaria(arr, target, left, right)
    if left > right then
        return -1
    end if
    
    mid = (left + right) / 2
    
    if arr[mid] == target then
        return mid
    else if arr[mid] > target then
        return busquedaBinaria(arr, target, left, mid - 1)
    else
        return busquedaBinaria(arr, target, mid + 1, right)
    end if
end function
```

**Resultado esperado:**
- Ecuación: `T(n) = T(n/2) + c`
- Complejidad: `Θ(log n)`
- Árbol: Altura log₂(n)
- Mejor caso: `Θ(1)` (elemento en medio)
- Peor caso: `Θ(log n)` (no encontrado)

---

### Ejemplo 4: Suma Iterativa (Lineal)

**Código:**
```
function sumaIterativa(arr, n)
    suma = 0
    for i = 0 to n - 1 do
        suma = suma + arr[i]
    end for
    return suma
end function
```

**Resultado esperado:**
- Complejidad: `Θ(n)`
- Diagrama de flujo con bucle for
- Mejor caso: `Θ(n)` (siempre recorre todo)
- Peor caso: `Θ(n)`

---

## 🛠️ Solución de Problemas

### Problema 1: "Tkinter no está instalado"

**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS/Windows:** Tkinter viene incluido con Python

---

### Problema 2: "matplotlib no se encuentra"

```bash
pip install matplotlib
```

---

### Problema 3: "Error al parsear el código"

**Causa:** Sintaxis incorrecta del pseudocódigo

**Solución:**
1. Revisar que tenga estructura válida
2. Ver ejemplos en `examples/`
3. Verificar `end if`, `end for`, `end function`

---

### Problema 4: "No se puede generar árbol de recurrencia"

**Causa:** El algoritmo no es recursivo

**Solución:**
- Los árboles solo funcionan para algoritmos recursivos
- Use **Diagrama de Flujo** para algoritmos iterativos

---

### Problema 5: Ventana muy pequeña o demasiado grande

**Solución:**
Editar en `gui_main.py`:
```python
window_width = 1400  # Ajustar según pantalla
window_height = 900
```

---

## 📞 Soporte y Contacto

**Proyecto:** Analizador de Complejidades  
**Universidad:** Universidad de Caldas  
**Curso:** Análisis y Diseño de Algoritmos  
**Año:** 2025-2

**Documentación adicional:**
- `README.md` - Guía principal
- `docs/` - Documentación técnica
- `examples/` - Ejemplos de algoritmos

---

## 🎯 Características Clave de la GUI

✅ **Interfaz intuitiva** con pestañas organizadas  
✅ **Visualización interactiva** de árboles de recurrencia  
✅ **Diagramas de flujo automáticos** para iterativos  
✅ **Análisis completo** de mejor/peor/promedio caso  
✅ **Exportación** de resultados y gráficos  
✅ **Editor integrado** con carga de archivos  
✅ **Cálculos formales** con Theta, Big O, Omega  

---

**¡Disfrute analizando algoritmos con nuestra GUI! 🚀**

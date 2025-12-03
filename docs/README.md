# Documentación General

Guía completa del proyecto: cómo se instala, se ejecuta, qué hace cada módulo, cómo se generan los reportes y cómo interactúa la capa LLM opcional.

## 1. Instalación y requisitos mínimos
- **Python 3.10+** (tkinter incluido en Windows/macOS; en Linux: `sudo apt-get install python3-tk`).
- Dependencias: `pip install -r requirements.txt` (Sympy, Lark, matplotlib, networkx, pillow, pytest, python-dotenv, google-generativeai opcional).
- Opcional LLM: crear `.env` con `GEMINI_API_KEY=tu_api_key` si quieres usar la ventana IA.

## 2. Cómo se ejecuta
### GUI (recomendada)
```bash
python gui_main.py
```
Al abrir la GUI:
- Se cargan los ejemplos de `examples/` y se analizan (verás tiempos por archivo en consola).
- Pestañas: Reporte (análisis completo), Código (pseudocódigo), Árbol (si recursivo) o Flujo (si iterativo).
- Ventana IA opcional: botón “Asistente IA (Generar)” abre `LLMWindow` si hay API key.

### CLI
```bash
python src/main.py
```
Se pide la ruta del `.txt` (usa `examples/factorial.txt` por defecto) y muestra un menú para elegir el tipo de análisis.

## 3. Qué pasa internamente (flujo)
1) **Entrada**: pseudocódigo desde archivo/editor o descripción NL→LLM (opcional).
2) **Parser Lark** (`src/parser/*`): convierte el pseudocódigo en AST (nodos en `src/ast/nodes.py`).
3) **Orquestador** (`src/logic/analysis_orchestrator.py`):
   - Detecta recursión (`recurrence_solver.py`).
   - Calcula expresión/recurrencia y Big-O con `math_analyzer.py`.
   - Genera ecuación formal y cota Θ con `asymptotic_analyzer.py`.
   - Construye árbol de recurrencia y costos por nivel (`recurrence_tree_builder.py`).
   - Analiza mejor/peor/promedio (`case_analyzer.py`).
   - Tiempo de análisis por algoritmo (`elapsed_ms` en `AnalysisResult`).
   - En GUI: render árbol o flujo, y muestra reporte.
4) **Salida**:
   - CLI: imprime resultados en consola.
   - GUI: reporte con todos los datos, árbol (recursivos), flujo (iterativos), mejores/peores casos.
   - Consola de la GUI: tiempos por archivo en la carga inicial.

## 4. Reportes (GUI/CLI)
- **Motor matemático**: expresión de costo y Big-O.
- **Heurístico**: ecuación de recurrencia, cota (Θ/O/Ω) y explicación.
- **Costos por nivel** (recursivos): resumen por nivel para patrones comunes (T(n/2)+c, 2T(n/2)+n, T(n-1)+T(n-2)+c…).
- **Casos**: mejor, peor y promedio con escenarios y ejemplos.
- **Árbol de recurrencia**: altura, casos base, estructura simbólica.
- **Flujo** (iterativos): diagrama generado con networkx+matplotlib.

## 5. Integración LLM (opcional)
- Archivos: `src/llm/system_prompt.py`, `src/llm/gemini_service.py`, `src/gui/llm_window.py`.
- Funciones: traducir lenguaje natural→pseudocódigo, opinión de complejidad, razonamiento, validación, traza.
- Sin API key: el proyecto funciona igual (solo se desactiva la ventana IA).

## 6. Errores comunes y cómo resolver
- **Tkinter/matplotlib no instalados (Linux)**: `sudo apt-get install python3-tk`, `pip install matplotlib`.
- **Símbolos raros/encoding**: ejecutar con UTF-8 (`PYTHONIOENCODING=utf-8`) o usar una consola/fuente con soporte.
- **LLM 429/cuota**: esperar el cooldown o aumentar cuota (no afecta el análisis principal).
- **Parser falla**: revisar sintaxis (uso de `begin/end`, `call`, etc.); ver ejemplos en `examples/`.
- **No se muestra pestaña Árbol**: el algoritmo no es recursivo; se muestra pestaña Flujo en su lugar.

## 7. Estructura de la documentación
- `flow_cli.md`: flujo y menú de `src/main.py`.
- `flow_gui.md`: GUI, pestañas y tiempos iniciales.
- `parser.md`: gramática y AST.
- `orchestrator.md`: coordinación de analizadores y campos de `AnalysisResult`.
- `analyzers.md`: motores matemático, asintótico, casos, recurrencias, DP.
- `visuals.md`: árbol de recurrencia y diagrama de flujo.
- `config_examples.md`: configuración, `.env`, ejemplos cargados.
- `llm.md`: integración opcional con Gemini.

## 8. Tests
```bash
python -m pytest tests/
```

## 9. Consejos de uso
- Arranca por la GUI para ver reportes completos y visualizaciones.
- Si editas la gramática, ajusta `transformer.py` y `ast/nodes.py`.
- Para medir rendimiento, revisa la consola en la carga inicial de la GUI (tiempo por algoritmo). 

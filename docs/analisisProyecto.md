# Análisis del Proyecto y Archivos Clave

Visión detallada de lo que hace cada módulo y por qué es relevante.

## Entradas
- **gui_main.py**: arranca la GUI, verifica dependencias, lanza `MainWindow` y muestra el tiempo total al cerrar.
- **src/main.py**: modo consola con menú. Usa `AnalizadorCompleto` (wrapper de los analizadores) para ejecutar opciones: análisis formal, DP, recursión, árbol, reporte.

## Parser / AST
- **src/parser/grammar.lark**: define la sintaxis soportada (functions, if/else, while/for/repeat, arrays/matrices, `call`, return).
- **src/parser/parser.py**: expone `parse_code`, carga la gramática (Earley).
- **src/parser/transformer.py**: transforma el árbol de Lark a nodos Python.
- **src/ast/nodes.py**: clases de nodos (Program, Function, For, While, If, Repeat, Return, Call, BinOp, Var, Number, Array/MatrixAccess, etc.).

## Orquestación
- **src/logic/analysis_orchestrator.py**: coordina todo el pipeline.
  - Detecta recursión (`RecursiveAlgorithmAnalyzer`).
  - Motor matemático (`math_analyzer.py`) → expresión/recurrencia + Big-O.
  - Motor asintótico (`asymptotic_analyzer.py`) → ecuación formal + cota (Θ/O/Ω) y costos por nivel.
  - Árbol de recurrencia (`recurrence_tree_builder.py`) → estructura simbólica.
  - Casos mejor/peor/promedio (CaseAnalyzer en GUI).
  - LLM opcional (clasificación, razonamiento, validación, traza).
  - Tiempo de análisis por algoritmo (`elapsed_ms`).
  - Cachea resultados por archivo para evitar reprocesar en GUI.

## Analizadores
- **math_analyzer.py**: recorre el AST, arma funciones/recurrencias Sympy, resuelve Big-O. Normaliza logs/Max y tiene fallbacks (divide & conquer, lineal).
- **asymptotic_analyzer.py**: construye RecurrenceEquation, aplica Master/Sustitución/árbol, devuelve AsymptoticBound. Estima costos por nivel para patrones comunes y corrige binaria/quick sort por nombre.
- **case_analyzer.py**: heurística de mejor/peor/promedio usando AST + nombre + complejidad/recurrencia. Patrones: binary_search, prime_test, fibonacci, divide_conquer, nested loops, lineal.
- **advanced_complexity.py**: combina complejidad por nodos (bucles, condicionales, recursión básica) en O/Ω/Θ.
- **dp_analyzer.py**: capa de memoización/patrones + árbol de recurrencia (usa solver/builder/visualizer).
- **recurrence_solver.py**: detecta patrón de llamadas, deriva `T(n)`; reglas por nombre para binaria/quick sort.
- **recurrence_tree_builder.py**: extrae términos recursivos, estima altura, genera topología y valores por nivel.
- **recurrence_visualizer.py**: representación textual del árbol.

## GUI
- **src/gui/main_window.py**: ventana principal.
  - Lista de algoritmos (carga `examples` al iniciar, muestra tiempos por archivo en consola una sola vez).
  - Pestañas: Reporte (análisis completo + costos por nivel + casos), Código, Árbol (si recursivo), Flujo (si iterativo).
  - Usa `AnalysisOrchestrator`, `TreeVisualizerGUI`, `FlowchartGenerator`, `CaseAnalyzer`.
- **src/gui/tree_visualizer_gui.py**: render del árbol de recurrencia.
- **src/gui/flowchart_generator.py**: genera diagrama de flujo (networkx + matplotlib).
- **src/gui/llm_window.py**: ventana IA (si hay API key) para traducir NL→pseudocódigo y auditar complejidad.

## LLM (opcional)
- **src/llm/system_prompt.py**: prompts para pseudocódigo, razonamiento, clasificación, validación y trazas.
- **src/llm/gemini_service.py**: wrapper Gemini (selección de modelo, uso de tokens, funciones de traducción/auditoría).
- Uso: opcional; el análisis principal no depende del LLM.

## Config y ejemplos
- **src/config.py**: BASE_DIR, lista de ejemplos, carga `.env` (`GEMINI_API_KEY`).
- **examples/**: factorial, fibonacci, merge_sort, busqueda_binaria, algoritmo_cubico, bubble_sort, quick_sort, suma_iterativa, es_primo, torres_hanoi.

## Resultado de análisis (AnalysisResult)
- Campos principales: expresión/cota matemática, ecuación/cota heurística, casos base, patrón de recursión, costos por nivel (si recursivo), árbol de recurrencia, casos mejor/peor/promedio.
- Campos LLM opcionales: clasificación, razonamiento, validación, traza, tokens/costo.
- Tiempo de análisis por algoritmo (`elapsed_ms`).

## Cómo se muestran los tiempos
- GUI imprime en consola los tiempos de análisis de los ejemplos al cargar (solo una vez) y el total.
- Cada `AnalysisResult` guarda `elapsed_ms` por si necesitas reportarlo en otro flujo.

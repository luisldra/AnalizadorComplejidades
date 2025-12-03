# Orquestador (`src/logic/analysis_orchestrator.py`)

Coordina todos los analizadores y empaqueta resultados para GUI/CLI.

## Responsabilidades
- Ejecutar el pipeline sobre un AST o texto:
  1) Parsear (si se recibe codigo).
  2) Detectar recursión (`RecursiveAlgorithmAnalyzer`).
  3) Analisis matematico (`MathematicalAnalyzer`).
  4) Analisis asintotico formal (`AsymptoticAnalyzer`).
  5) Construir arbol de recurrencia (`TreeStructure`).
  6) Analisis de casos (CaseAnalyzer en GUI).
- Cache global por archivo para evitar reprocesar.
- Traduccion desde lenguaje natural (LLM) opcional via `process_natural_description`.
- Enriquecimiento LLM opcional (clasificacion, razonamiento, validacion, traza).
- Registro de tiempo de analisis por algoritmo (`elapsed_ms`).

## Salida
- Retorna `AnalysisResult` con:
  - Expresion matematica y Big-O.
  - Ecuacion/cota heuristica (Theta u otra).
  - Arbol de recurrencia (estructura) y costos por nivel (si recursivo).
  - Casos base, patron de recursion, flag `is_recursive`.
  - Campos LLM opcionales y tiempo de analisis en ms.

## Uso
- GUI: `MainWindow._load_initial_data` llama `process_file` y guarda en cache.
- CLI: `src/main.py` usa `AnalizadorCompleto` (wrapper sobre los mismos analizadores).

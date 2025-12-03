# Analizadores principales

## MathematicalAnalyzer (`src/analyzer/math_analyzer.py`)
- Recorre el AST y construye expresiones/recurrencias simbólicas (Sympy).
- Simplifica a Big-O (`solve`, `solve_recurrence`).
- Normaliza términos (log, Max) y tiene fallbacks para patrones comunes.
- Provee `last_raw_results` para inspección.

## AsymptoticAnalyzer (`src/analyzer/asymptotic_analyzer.py`)
- Construye ecuación formal (a, b, f(n), casos base, método usado).
- Resuelve recurrencia (Master, sustitución, árbol).
- Entrega `AsymptoticBound` (complexity + notation).
- Estima costos por nivel para patrones básicos y corrige patrones conocidos (binaria, quick sort).

## CaseAnalyzer (`src/analyzer/case_analyzer.py`)
- Deriva mejor/peor/promedio combinando: AST, nombre de función, ecuación/complexidad.
- Patrones específicos: binary search, prime test, Fibonacci, divide & conquer, loops, etc.
- Retorna `CaseAnalysis` por caso (complexity, escenario, ejemplo, explicación).

## AdvancedComplexityAnalyzer (`src/analyzer/advanced_complexity.py`)
- Combina complejidad para nodos (asignaciones, bucles, condicionales, recursión básica).
- Produce `ComplexityResult` con O, Ω y Θ (cuando coinciden).

## DynamicProgrammingAnalyzer (`src/analyzer/dp_analyzer.py`)
- Capa coordinadora para memoización, patrones de recurrencia y visualización.
- Usa `RecurrenceSolver`, `TreeStructure`, `RecurrenceTreeVisualizer`.

## RecurrenceSolver (`src/analyzer/recurrence_solver.py`)
- Detecta patrón de llamadas recursivas y deriva ecuación (lineal, binary, divide & conquer).
- Tabla de patrones conocidos (T(n/2)+c, 2T(n/2)+n, etc.) y soluciones cerradas.
- Enriquecido con reglas por nombre (binary search, quick sort).

## RecurrenceTreeBuilder (`src/analyzer/recurrence_tree_builder.py`)
- Parsea la ecuación y genera topología simbólica del árbol.
- Calcula altura estimada y estructura por niveles.

## RecurrenceTreeVisualizer (`src/analyzer/recurrence_visualizer.py`)
- Convierte la estructura del árbol en texto (o datos) para mostrar en consola/GUI.

## LLM (opcional) (`src/llm/*`)
- Prompts y servicio Gemini para: traducción NL→pseudocódigo, razonamiento, clasificación, validación, traza.
- No es obligatorio para el análisis base.

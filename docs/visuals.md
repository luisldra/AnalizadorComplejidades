# Visualizaciones

## FlowchartGenerator (`src/gui/flowchart_generator.py`)
- Usa `networkx` + `matplotlib` para generar un diagrama de flujo desde el AST.
- Colorea nodos por tipo (inicio/fin, proceso, decisión, bucle, E/S).
- Devuelve una figura (Figure) que la GUI inserta en la pestaña Flujo.

## TreeVisualizerGUI (`src/gui/tree_visualizer_gui.py`)
- Renderiza la estructura de árbol de recurrencia (`TreeStructure`) en la pestaña Árbol.
- Muestra nodos, altura y casos base; integra con el builder/visualizer de análisis.

## RecurrenceTreeVisualizer (`src/analyzer/recurrence_visualizer.py`)
- Genera una representación textual (o datos) del árbol de recurrencia.
- Se usa en CLI y como base para la GUI.

## Costos por nivel en el reporte
- Se calculan en `AsymptoticAnalyzer.estimate_level_costs` para patrones conocidos y se muestran en el reporte GUI cuando el algoritmo es recursivo.

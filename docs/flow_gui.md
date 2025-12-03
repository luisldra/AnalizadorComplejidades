# Flujo GUI (`gui_main.py` y `src/gui/main_window.py`)

Entrada grafica sobre Tkinter.

## gui_main.py
- Prepara el entorno (TkAgg) y verifica dependencias.
- Configura la ventana principal y lanza `MainWindow`.
- Al cerrar, imprime el tiempo total de ejecucion de la app.

## src/gui/main_window.py
- Construye la interfaz:
  - Lista de algoritmos (carga inicial desde `examples`).
  - Boton “Asistente IA” (opcional).
  - Pestañas: Reporte, Codigo, Arbol (si recursivo) o Flujo (si iterativo).
- `AnalysisOrchestrator` procesa cada archivo y cachea resultados.
- Reporte muestra: expresion matematica, ecuacion/cota Theta, costos por nivel (recursivos), casos mejor/peor/promedio.
- Visualizadores:
  - `TreeVisualizerGUI` para arboles de recurrencia.
  - `FlowchartGenerator` para diagramas de flujo (iterativos).

## Medicion de tiempo
- En la carga inicial imprime en consola el tiempo por archivo y total de los ejemplos (`_load_initial_data`).

## Relevancia
Interfaz principal para usuarios no tecnicos; concentra reporte, codigo y visualizaciones en un mismo lugar.

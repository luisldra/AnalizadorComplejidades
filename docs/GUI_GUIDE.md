# Guía de Uso de la Interfaz Gráfica (GUI)

**Analizador de Complejidades de Algoritmos** — Universidad de Caldas  

## Contenido
1. Requisitos e instalación
2. Inicio rápido
3. Flujo de uso
4. Pestañas y visualizaciones
5. Costos por nivel (recursivos)
6. Problemas frecuentes

## 1. Requisitos e instalación
```bash
pip install -r requirements.txt   # Python 3.10+
```
Dependencias clave GUI: tkinter, matplotlib, pillow.

## 2. Inicio rápido
```bash
python gui_main.py       # Lanza la GUI
```
Al abrir se cargan los ejemplos de `examples/` en la lista de la izquierda.

## 3. Flujo de uso
1. Selecciona un algoritmo o abre un `.txt`.
2. Pestaña “Reporte”: lee el análisis matemático y heurístico.
3. Si es recursivo, revisa el bloque “Costos por nivel (recursivo)”.
4. Pestaña “Código”: muestra el pseudocódigo.
5. Pestaña “Árbol” (recursivos) o “Flujo” (iterativos) según aplique.

## 4. Pestañas y visualizaciones
- **Reporte**:  
  - Expresión de costo (motor matemático) + Big-O.  
  - Ecuación de recurrencia y cota Θ (heurístico).  
  - Costos por nivel si es recursivo.  
  - Mejor/peor/promedio (CaseAnalyzer).
- **Código**: pseudocódigo original.
- **Árbol** (solo recursivos): visualización de árbol de recurrencia con altura y casos base.
- **Flujo** (iterativos): diagrama de flujo generado.

## 5. Costos por nivel (recursivos)
Se muestran en el reporte cuando existe recurrencia reconocible. Ejemplos:
- `T(n)=T(n/2)+c`: Nivel k → 1 nodo tamaño n/2^k; costo nivel ≈ c; altura ≈ log n.
- `T(n)=2T(n/2)+n`: Nivel k → 2^k nodos tamaño n/2^k; costo nivel ≈ n; altura ≈ log n.
- `T(n)=T(n-1)+T(n-2)+c`: Nivel k → ~2^k nodos; costo nivel ≈ 2^k; altura ≈ n.

## 6. Problemas frecuentes
- **No aparece la pestaña Árbol**: el algoritmo no es recursivo. Usa la pestaña Flujo.
- **Símbolos raros**: ejecutar con UTF-8 (`PYTHONIOENCODING=utf-8`) o usar fuente con soporte.
- **LLM no disponible**: la app funciona sin LLM; solo se desactiva la ventana de IA.

## Notas
- El LLM (Gemini) es opcional para traducir lenguaje natural o auditar; no afecta el análisis principal.
- Patrones conocidos ajustados: búsqueda binaria (Θ(log n)), quick sort (Θ(n log n), peor n²).

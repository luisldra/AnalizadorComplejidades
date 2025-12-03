# Config y ejemplos

## config.py
- Define `BASE_DIR` (`examples/`) y la lista de archivos de ejemplo.
- Carga `.env` con `python-dotenv`; se usa `GEMINI_API_KEY` si activas el LLM.

## examples/
- Archivos `.txt` de referencia: factorial, fibonacci, merge_sort, busqueda_binaria, algoritmo_cubico, bubble_sort, quick_sort, suma_iterativa, es_primo, torres_hanoi.
- El GUI carga estos archivos al iniciar; CLI usa `examples/factorial.txt` por defecto si no se especifica otro.

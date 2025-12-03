# Integracion LLM (opcional)

## Archivos
- `src/llm/system_prompt.py`: prompts para pseudocodigo, razonamiento paso a paso, clasificacion, validacion y trazas.
- `src/llm/gemini_service.py`: wrapper Gemini (seleccion de modelo, conteo de tokens, funciones de traduccion NL→pseudocodigo, opinion de complejidad, razonamiento, etc.).
- `src/gui/llm_window.py`: ventana IA en la GUI para generar pseudocodigo y auditar complejidad contra los motores internos.

## Flujo
- Si se provee `GEMINI_API_KEY` en `.env`, la ventana IA se habilita.
- `AnalysisOrchestrator.process_natural_description` usa el LLM para generar pseudocodigo y luego ejecuta el pipeline normal.
- En `process_code`, si `use_llm=True`, se agregan campos de clasificacion/razonamiento/validacion/traza al `AnalysisResult`.

## Notas
- El LLM no es requerido para el analisis base; si no hay API key, el proyecto sigue funcionando (solo se desactiva la ventana IA).
- Dependencia: `google-generativeai` (opcional).

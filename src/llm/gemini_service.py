from typing import Dict, Optional, Tuple
import google.generativeai as genai
from src.config import GEMINI_API_KEY
from src.llm.system_prompt import (
    PSEUDOCODE_GRAMMAR_PROMPT,
    NATURAL_TO_PSEUDOCODE_PROMPT,
    REASONING_PROMPT,
    PATTERN_CLASSIFICATION_PROMPT,
    VALIDATION_PROMPT,
    TRACE_PROMPT,
)


class GeminiService:
    """
    Capa de conveniencia para centralizar todas las llamadas al LLM.
    Guarda la metrica de tokens de la ultima llamada para estimar costos.
    """

    def __init__(self):
        self.model = None
        self.last_token_usage: Optional[Dict[str, int]] = None

        if not GEMINI_API_KEY:
            raise ValueError("No se encontro la GEMINI_API_KEY en el archivo .env")

        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = self._find_best_model()
        except Exception as e:
            print(f"Error fatal configurando Gemini: {e}")
            self.model = None

    def _find_best_model(self):
        """
        Busca en la API los modelos disponibles y selecciona el mejor.
        Prioridad: Flash -> 1.5 Pro -> 1.0 Pro -> pro
        """
        try:
            print(">> Buscando modelos disponibles en tu cuenta...")
            available_models = []
            for m in genai.list_models():
                if "generateContent" in m.supported_generation_methods:
                    available_models.append(m.name)

            priorities = [
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-1.0-pro",
                "gemini-pro",
            ]

            selected_name = None
            for priority in priorities:
                for avail in available_models:
                    if priority in avail:
                        selected_name = avail
                        break
                if selected_name:
                    break

            if not selected_name and available_models:
                selected_name = available_models[0]
            if not selected_name:
                selected_name = "gemini-pro"

            print(f">> Modelo seleccionado: {selected_name}")
            return genai.GenerativeModel(selected_name)

        except Exception as e:
            print(f"Advertencia: error listando modelos ({e}), usando 'gemini-pro'.")
            return genai.GenerativeModel("gemini-pro")

    # ----------------- Utilidades internas -----------------

    def _clean_code_block(self, text: str) -> str:
        if not text:
            return ""
        cleaned = (
            text.replace("```javascript", "")
            .replace("```python", "")
            .replace("```txt", "")
            .replace("```", "")
            .strip()
        )
        return cleaned

    def _capture_usage(self, response) -> Optional[Dict[str, int]]:
        usage = getattr(response, "usage_metadata", None)
        if not usage:
            return None
        return {
            "prompt_tokens": getattr(usage, "prompt_token_count", None),
            "candidates_tokens": getattr(usage, "candidates_token_count", None),
            "total_tokens": getattr(usage, "total_token_count", None),
        }

    def _generate(self, prompt: str) -> Tuple[str, Optional[Dict[str, int]]]:
        """
        Envia un prompt y devuelve (texto, uso_de_tokens)
        """
        if not self.model:
            return "Error: No hay conexion con el modelo de IA.", None

        try:
            response = self.model.generate_content(prompt)
            text = getattr(response, "text", "") or ""
            usage = self._capture_usage(response)
            return text.strip(), usage
        except Exception as e:
            return f"Error generando contenido: {e}", None

    # ----------------- Funciones publicas -----------------

    def generate_algorithm_code(self, user_request: str) -> str:
        """
        Compatibilidad hacia atras: genera pseudocodigo desde lenguaje natural.
        Guarda metrica de tokens en self.last_token_usage.
        """
        code = self.translate_natural_language(user_request)
        return code

    def translate_natural_language(self, description: str) -> str:
        prompt = (
            f"{PSEUDOCODE_GRAMMAR_PROMPT}\n"
            f"{NATURAL_TO_PSEUDOCODE_PROMPT}\n"
            f"DESCRIPCION DEL USUARIO:\n{description}\n\n"
            f"CODIGO GENERADO:"
        )
        text, usage = self._generate(prompt)
        self.last_token_usage = usage
        return self._clean_code_block(text)

    def get_complexity_opinion(self, code: str) -> str:
        """
        Opinion rapida de complejidad con cota fuerte.
        """
        prompt = (
            "Analiza el siguiente pseudocodigo y da su complejidad temporal "
            "usando notacion Theta y una breve justificacion de 1 linea.\n\n"
            f"CODIGO:\n{code}\n\nFORMATO:\nTheta(...) - Justificacion"
        )
        text, usage = self._generate(prompt)
        self.last_token_usage = usage
        return text.strip()

    def explain_steps(self, code: str) -> str:
        """
        Devuelve pasos de razonamiento estructurado para el analisis.
        """
        prompt = f"{REASONING_PROMPT}\n\nPSEUDOCODIGO:\n{code}\n"
        text, usage = self._generate(prompt)
        self.last_token_usage = usage
        return text

    def classify_pattern(self, code: str) -> str:
        prompt = f"{PATTERN_CLASSIFICATION_PROMPT}\n\nPSEUDOCODIGO:\n{code}\n"
        text, usage = self._generate(prompt)
        self.last_token_usage = usage
        return text.strip()

    def validate_recurrence(self, code: str, equation: str, complexity: str) -> str:
        prompt = (
            f"{VALIDATION_PROMPT}\n\nCODIGO:\n{code}\n\n"
            f"ECUACION PROPUESTA: {equation}\n"
            f"COMPLEJIDAD PROPUESTA: {complexity}\n"
        )
        text, usage = self._generate(prompt)
        self.last_token_usage = usage
        return text.strip()

    def generate_trace_diagram(self, code: str) -> str:
        prompt = f"{TRACE_PROMPT}\n\nPSEUDOCODIGO:\n{code}\n"
        text, usage = self._generate(prompt)
        self.last_token_usage = usage
        return text.strip()

    def estimate_cost_us(self, tokens: Optional[Dict[str, int]], cost_per_token_us: int = 10) -> Optional[int]:
        """
        Estima el costo aproximado en microsegundos para la llamada LLM.
        No es un costo real de facturacion, solo una metrica local configurable.
        """
        if not tokens or not tokens.get("total_tokens"):
            return None
        return tokens["total_tokens"] * cost_per_token_us

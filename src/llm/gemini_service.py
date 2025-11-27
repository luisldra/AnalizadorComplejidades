import google.generativeai as genai
from src.config import GEMINI_API_KEY
from src.llm.system_prompt import PSEUDOCODE_GRAMMAR_PROMPT

class GeminiService:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("No se encontró la GEMINI_API_KEY en el archivo .env")
        
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            
            # --- SELECCIÓN DINÁMICA DEL MEJOR MODELO ---
            self.model = self._find_best_model()
            
        except Exception as e:
            print(f"Error fatal configurando Gemini: {e}")
            # Fallback de emergencia para no romper la app al iniciar
            self.model = None 

    def _find_best_model(self):
        """
        Busca en la API los modelos disponibles y selecciona el mejor.
        Prioridad: Flash -> 1.5 Pro -> 1.0 Pro
        """
        try:
            print("🔍 Buscando modelos disponibles en tu cuenta...")
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            # Lista de prioridad (del más rápido al más estándar)
            priorities = [
                'gemini-1.5-flash',
                'gemini-1.5-pro',
                'gemini-1.0-pro',
                'gemini-pro'
            ]
            
            selected_name = None
            
            # 1. Intentar coincidencia exacta o parcial
            for priority in priorities:
                for avail in available_models:
                    if priority in avail:
                        selected_name = avail
                        break
                if selected_name: break
            
            # 2. Si no encuentra ninguno de la lista, toma el primero disponible
            if not selected_name and available_models:
                selected_name = available_models[0]
            
            # 3. Fallback final (hardcoded)
            if not selected_name:
                selected_name = 'gemini-pro'

            print(f"✅ Modelo seleccionado: {selected_name}")
            return genai.GenerativeModel(selected_name)

        except Exception as e:
            print(f"⚠️ Error listando modelos ({e}), intentando 'gemini-pro' por defecto.")
            return genai.GenerativeModel('gemini-pro')

    def generate_algorithm_code(self, user_request: str) -> str:
        """
        Solicita a Gemini que genere un algoritmo basado en la descripción del usuario.
        """
        if not self.model:
            return "Error: No hay conexión con el modelo de IA."

        full_prompt = f"{PSEUDOCODE_GRAMMAR_PROMPT}\n\nSOLICITUD DEL USUARIO: {user_request}\n\nCÓDIGO GENERADO:"
        
        try:
            response = self.model.generate_content(full_prompt)
            
            if not response.text:
                return "Error: Gemini generó una respuesta vacía."
                
            code = response.text
            # Limpieza básica de markdown
            code = code.replace("```javascript", "").replace("```python", "").replace("```", "").strip()
            return code
            
        except Exception as e:
            return f"Error Generando Código: {str(e)}\nVerifica tu API Key o cuota."

    def get_complexity_opinion(self, code: str) -> str:
        """
        Consulta la complejidad al LLM.
        """
        if not self.model:
            return "Error de conexión IA."

        prompt = f"""
        Analiza el siguiente pseudocódigo y dime cuál es su complejidad temporal usando la notación con una cota fuerte (Theta) y una breve justificación de 1 línea.
        
        CÓDIGO:
        {code}
        
        FORMATO RESPUESTA:
        Θ(...) - Justificación
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return "No se pudo obtener opinión."
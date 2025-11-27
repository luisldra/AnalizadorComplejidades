import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

# Imports del proyecto
from src.llm.gemini_service import GeminiService
from src.logic.analysis_orchestrator import AnalysisOrchestrator

class LLMWindow(tk.Toplevel):
    def __init__(self, parent, orchestrator: AnalysisOrchestrator):
        super().__init__(parent)
        self.title("🤖 Asistente IA - Generador y Auditor")
        self.geometry("1100x750")
        
        self.orchestrator = orchestrator
        self.gemini = None # Se inicializa lazy
        self.generated_code = ""
        
        self._setup_ui()
        
        # Inicializar servicio en hilo separado para no congelar UI
        threading.Thread(target=self._init_service, daemon=True).start()

    def _init_service(self):
        try:
            self.gemini = GeminiService()
            # Actualizar UI de forma segura desde otro hilo
            self.after(0, lambda: self.status_lbl.config(text="✅ Conectado a Gemini AI", foreground="green"))
            self.after(0, lambda: self.btn_generate.config(state=tk.NORMAL))
        except Exception as e:
            self.after(0, lambda: self.status_lbl.config(text=f"❌ Error API: {e}", foreground="red"))

    def _setup_ui(self):
        # Panel Superior: Entrada
        top_frame = ttk.LabelFrame(self, text="1. Describe el algoritmo que necesitas", padding=10)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.txt_prompt = tk.Entry(top_frame, font=('Arial', 12))
        self.txt_prompt.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.txt_prompt.bind("<Return>", lambda e: self._generate())
        
        self.btn_generate = ttk.Button(top_frame, text="✨ Generar Código", command=self._generate, state=tk.DISABLED)
        self.btn_generate.pack(side=tk.RIGHT)

        # Panel Central: Código y Análisis
        center_frame = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        center_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Izquierda: Código Generado
        self.frame_code = ttk.LabelFrame(center_frame, text="2. Código Generado por IA (Editable)", padding=5)
        center_frame.add(self.frame_code, weight=1)
        
        self.txt_code = scrolledtext.ScrolledText(self.frame_code, font=('Consolas', 11), height=15)
        self.txt_code.pack(fill=tk.BOTH, expand=True)
        
        # Botón de acción central
        action_frame = ttk.Frame(self.frame_code)
        action_frame.pack(fill=tk.X, pady=5)
        self.status_lbl = ttk.Label(action_frame, text="Conectando...", font=('Arial', 9))
        self.status_lbl.pack(side=tk.LEFT)
        ttk.Button(action_frame, text="🔍 Auditar Código (Comparar)", command=self._audit_code).pack(side=tk.RIGHT)

        # Derecha: Auditoría
        self.frame_audit = ttk.LabelFrame(center_frame, text="3. Auditoría Técnica: Máquina vs IA", padding=5)
        center_frame.add(self.frame_audit, weight=1)
        
        self.txt_audit = scrolledtext.ScrolledText(self.frame_audit, font=('Segoe UI', 10), height=15)
        self.txt_audit.pack(fill=tk.BOTH, expand=True)
        # Tags para colores
        self.txt_audit.tag_config("match", foreground="green", font=('Segoe UI', 11, 'bold'))
        self.txt_audit.tag_config("diverge", foreground="red", font=('Segoe UI', 11, 'bold'))
        self.txt_audit.tag_config("title", font=('Segoe UI', 12, 'bold'), foreground="#1565C0")

    def _generate(self):
        prompt = self.txt_prompt.get().strip()
        if not prompt: return
        
        self.btn_generate.config(state=tk.DISABLED, text="Generando...")
        self.txt_code.delete('1.0', tk.END)
        self.txt_code.insert('1.0', "⏳ Gemini está pensando...\nEsto puede tomar unos segundos.")
        
        threading.Thread(target=self._generate_thread, args=(prompt,), daemon=True).start()

    def _generate_thread(self, prompt):
        code = self.gemini.generate_algorithm_code(prompt)
        # Actualizar UI en hilo principal
        self.after(0, lambda: self._show_code(code))

    def _show_code(self, code):
        self.txt_code.delete('1.0', tk.END)
        self.txt_code.insert('1.0', code)
        self.generated_code = code
        self.btn_generate.config(state=tk.NORMAL, text="✨ Generar Código")

    def _audit_code(self):
        code = self.txt_code.get('1.0', tk.END).strip()
        if not code or "⏳" in code: return
        
        self.txt_audit.delete('1.0', tk.END)
        self.txt_audit.insert('1.0', "🕵️ Realizando Auditoría Cruzada...\n\n")
        
        threading.Thread(target=self._audit_thread, args=(code,), daemon=True).start()

    def _audit_thread(self, code):
        ai_opinion = self.gemini.get_complexity_opinion(code)
        real_result = self.orchestrator.process_code(code, "IA_Snippet")
        self.after(0, lambda: self._show_audit(ai_opinion, real_result))

    def _show_audit(self, ai_opinion, real_res):
        t = self.txt_audit
        t.delete('1.0', tk.END)
        
        if real_res.error:
            t.insert(tk.END, "❌ ERROR DE SINTAXIS:\n", "diverge")
            t.insert(tk.END, "El código generado no es válido.\n")
            t.insert(tk.END, f"Detalle: {real_res.error}\n")
            return

        t.insert(tk.END, "RESULTADOS DEL DUELO\n", "title")
        t.insert(tk.END, "="*40 + "\n\n")
        
        t.insert(tk.END, "🤖 OPINIÓN DE GEMINI:\n", "title")
        t.insert(tk.END, f"{ai_opinion}\n\n")
        
        t.insert(tk.END, "📏 MOTOR HEURÍSTICO:\n", "title")
        
        # Mostrar notación completa Θ(n)
        display_comp = real_res.heur_complexity 
        if display_comp == "N/A": display_comp = "Θ(?)"
        
        t.insert(tk.END, f"Complejidad: {display_comp}\n") 
        t.insert(tk.END, f"Ecuación: {real_res.heur_equation}\n\n")

        t.insert(tk.END, "🧮 MOTOR MATEMÁTICO:\n", "title")
        t.insert(tk.END, f"Expresión: {real_res.math_expression}\n")
        t.insert(tk.END, f"Cálculo: {real_res.math_complexity}\n\n")
        
        # t.insert(tk.END, "⚖️ VEREDICTO:\n", "title")
        
        # # --- LÓGICA DE COMPARACIÓN ---
        # def normalize(text):
        #     # Limpieza extrema para comparación justa
        #     if not text: return ""
        #     return text.lower().replace("θ", "").replace("o", "").replace("(", "").replace(")", "").replace(" ", "").strip()

        # ai_raw = ai_opinion.split("-")[0] # Tomar solo la parte "Θ(n)" antes del guion
        
        # ai_clean = normalize(ai_raw)
        # motor_clean = normalize(real_res.heur_notation) 
        
        # match = False
        
        # # 1. Coincidencia exacta
        # if ai_clean == motor_clean: 
        #     match = True
        # # 2. Inclusión (ej: "n" dentro de "linear")
        # elif motor_clean and motor_clean in ai_clean and len(motor_clean) > 1: 
        #     match = True
        # elif ai_clean and ai_clean in motor_clean and len(ai_clean) > 1:
        #     match = True
            
        # # 3. Casos especiales de lenguaje natural
        # if motor_clean == "n" and ("lineal" in ai_opinion.lower() or "linear" in ai_opinion.lower()):
        #     match = True
        # if "2^n" in motor_clean and "exponencial" in ai_opinion.lower():
        #     match = True
            
        # # 4. Regla de oro: Evitar falso positivo de "1" vs "n"
        # if "1" in motor_clean and "n" in ai_clean: match = False
        # if "n" in motor_clean and "1" in ai_clean: match = False

        # if match:
        #      t.insert(tk.END, "✅ CONCORDANCIA DETECTADA\n", "match")
        #      t.insert(tk.END, "La IA y el Motor Heurístico coinciden.")
        # else:
        #      t.insert(tk.END, "⚠️ DIVERGENCIA DETECTADA\n", "diverge")
        #      t.insert(tk.END, f"Motor: {real_res.heur_complexity} vs IA: {ai_raw}\n")
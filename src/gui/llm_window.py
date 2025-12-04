import tkinter as tk
from tkinter import ttk, scrolledtext
import threading

from src.llm.gemini_service import GeminiService
from src.logic.analysis_orchestrator import AnalysisOrchestrator


class LLMWindow(tk.Toplevel):
    """
    Ventana de asistencia IA:
    - Traduce lenguaje natural a pseudocodigo compatible.
    - Audita complejidad cruzando motor heuristico, matematico y LLM.
    - Muestra razonamiento, validacion y trazas generadas por el LLM.
    """

    def __init__(self, parent, orchestrator: AnalysisOrchestrator):
        super().__init__(parent)
        self.title("AI - Asistente IA - Generador y Auditor")
        self.state('zoomed')  # Maximizar ventana (Windows)

        self.orchestrator = orchestrator
        self.gemini = None  # Inicializacion lazy
        self.generated_code = ""

        self._setup_ui()
        threading.Thread(target=self._init_service, daemon=True).start()

    # ----------------- Inicializacion -----------------
    def _init_service(self):
        try:
            self.gemini = GeminiService()
            self.after(0, lambda: self.status_lbl.config(text="Conectado a Gemini AI", foreground="green"))
            self.after(0, lambda: self.btn_generate.config(state=tk.NORMAL))
        except Exception as e:
            self.after(0, lambda: self.status_lbl.config(text=f"Error API: {e}", foreground="red"))

    # ----------------- UI -----------------
    def _setup_ui(self):
        top_frame = ttk.LabelFrame(self, text="1. Describe el algoritmo que necesitas", padding=10)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        self.txt_prompt = tk.Entry(top_frame, font=("Arial", 12))
        self.txt_prompt.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.txt_prompt.bind("<Return>", lambda e: self._generate())

        self.btn_generate = ttk.Button(top_frame, text="Generar Codigo", command=self._generate, state=tk.DISABLED)
        self.btn_generate.pack(side=tk.RIGHT)

        center_frame = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        center_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Columna izquierda: codigo generado
        self.frame_code = ttk.LabelFrame(center_frame, text="2. Codigo Generado por IA (Editable)", padding=5)
        center_frame.add(self.frame_code, weight=1)

        self.txt_code = scrolledtext.ScrolledText(self.frame_code, font=("Consolas", 11), height=15)
        self.txt_code.pack(fill=tk.BOTH, expand=True)

        action_frame = ttk.Frame(self.frame_code)
        action_frame.pack(fill=tk.X, pady=5)
        self.status_lbl = ttk.Label(action_frame, text="Conectando...", font=("Arial", 9))
        self.status_lbl.pack(side=tk.LEFT)
        ttk.Button(action_frame, text="Auditar Codigo (Comparar)", command=self._audit_code).pack(side=tk.RIGHT)

        # Columna derecha: auditoria
        self.frame_audit = ttk.LabelFrame(center_frame, text="3. Auditoria Tecnica: Motor vs IA", padding=5)
        center_frame.add(self.frame_audit, weight=1)

        self.txt_audit = scrolledtext.ScrolledText(self.frame_audit, font=("Segoe UI", 10), height=15)
        self.txt_audit.pack(fill=tk.BOTH, expand=True)
        self.txt_audit.tag_config("match", foreground="green", font=("Segoe UI", 11, "bold"))
        self.txt_audit.tag_config("diverge", foreground="red", font=("Segoe UI", 11, "bold"))
        self.txt_audit.tag_config("title", font=("Segoe UI", 12, "bold"), foreground="#1565C0")
        self.txt_audit.tag_config("label", font=("Segoe UI", 10, "bold"))
        self.txt_audit.tag_config("warn", foreground="#C62828", font=("Segoe UI", 10, "bold"))

    # ----------------- Generacion -----------------
    def _generate(self):
        prompt = self.txt_prompt.get().strip()
        if not prompt:
            return

        self.btn_generate.config(state=tk.DISABLED, text="Generando...")
        self.txt_code.delete("1.0", tk.END)
        self.txt_code.insert("1.0", "Gemini esta pensando...\nEsto puede tomar unos segundos.")

        threading.Thread(target=self._generate_thread, args=(prompt,), daemon=True).start()

    def _generate_thread(self, prompt):
        if not self.gemini:
            code = "Error: servicio LLM no disponible."
        else:
            code = self.gemini.translate_natural_language(prompt)
        self.after(0, lambda: self._show_code(code))

    def _show_code(self, code):
        self.txt_code.delete("1.0", tk.END)
        self.txt_code.insert("1.0", code)
        self.generated_code = code
        self.btn_generate.config(state=tk.NORMAL, text="Generar Codigo")

    # ----------------- Auditoria -----------------
    def _audit_code(self):
        code = self.txt_code.get("1.0", tk.END).strip()
        if not code or "Gemini esta pensando" in code:
            return

        self.txt_audit.delete("1.0", tk.END)
        self.txt_audit.insert("1.0", ">> Realizando Auditoria Cruzada...\n\n")

        threading.Thread(target=self._audit_thread, args=(code,), daemon=True).start()

    def _audit_thread(self, code):
        ai_opinion = self.gemini.get_complexity_opinion(code) if self.gemini else "LLM no disponible"
        real_result = self.orchestrator.process_code(
            code,
            "IA_Snippet",
            use_llm=True,
            llm_service=self.gemini,
        )
        self.after(0, lambda: self._show_audit(ai_opinion, real_result))

    def _show_audit(self, ai_opinion, real_res):
        t = self.txt_audit
        t.delete("1.0", tk.END)

        if real_res.error:
            t.insert(tk.END, "ERROR DE SINTAXIS:\n", "diverge")
            t.insert(tk.END, "El codigo generado no es valido.\n")
            t.insert(tk.END, f"Detalle: {real_res.error}\n")
            return

        def _clean(text: str) -> str:
            if not text:
                return ""
            # eliminar marcadores markdown simples
            return text.replace("***", "").replace("**", "").strip()

        def _short_error(text: str) -> str:
            if not text:
                return ""
            lower = text.lower()
            if "error generando contenido" in lower or "quota" in lower or "429" in lower:
                return "LLM sin respuesta (cuota/limite alcanzado, reintente luego)."
            return text

        def _section(title, body, tag=None):
            if not body:
                return
            t.insert(tk.END, f"{title}\n", tag or "title")
            t.insert(tk.END, f"{body}\n\n")

        t.insert(tk.END, "RESULTADOS DEL DUELO\n", "title")
        t.insert(tk.END, "========================================\n\n")

        _section("IA - OPINION DE GEMINI:", _clean(ai_opinion))

        display_comp = real_res.heur_complexity or "Theta(?)"
        heur_body = f"Complejidad: {display_comp}\nEcuacion: {real_res.heur_equation}"
        _section("MOTOR HEURISTICO:", heur_body)

        math_body = f"Expresion: {real_res.math_expression}\nCalculo: {real_res.math_complexity}"
        _section("MOTOR MATEMATICO:", math_body)

        if real_res.llm_pattern:
            _section("CLASIFICACION LLM:", _clean(real_res.llm_pattern))

        if real_res.llm_reasoning:
            _section("RAZONAMIENTO LLM:", _clean(real_res.llm_reasoning))

        if real_res.llm_validation:
            _section("VALIDACION LLM:", _short_error(_clean(real_res.llm_validation)), "warn" if "LLM sin respuesta" in _short_error(real_res.llm_validation) else "title")

        if real_res.llm_trace:
            _section("TRAZA LLM:", _short_error(_clean(real_res.llm_trace)), "warn" if "LLM sin respuesta" in _short_error(real_res.llm_trace) else "title")

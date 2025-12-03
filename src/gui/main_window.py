import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
import time

# Imports del sistema
from src.gui.llm_window import LLMWindow
from src.config import get_algorithm_files
from src.logic.analysis_orchestrator import AnalysisOrchestrator
from src.gui.tree_visualizer_gui import TreeVisualizerGUI
from src.gui.flowchart_generator import FlowchartGenerator
from src.analyzer.case_analyzer import CaseAnalyzer

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Algoritmos")
        self.root.geometry("1400x900")
        
        self.orchestrator = AnalysisOrchestrator()
        self.flowchart_gen = FlowchartGenerator()
        self.case_analyzer = CaseAnalyzer()
        
        self.gui_cache = {} 
        self._timing_printed = False
        
        self._setup_ui()
        self.root.after(100, self._load_initial_data)

    def _setup_ui(self):
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=('Segoe UI', 10))
        style.configure("Bold.TLabel", font=('Segoe UI', 10, 'bold'))
        
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Izquierda
        left_frame = ttk.LabelFrame(paned, text="Algoritmos", width=300)
        paned.add(left_frame, weight=1)
        
        # BOTÓN IA 
        btn_ai = ttk.Button(left_frame, text="✨ ASISTENTE IA (Generar)", command=self._open_ai_window)
        btn_ai.pack(fill=tk.X, padx=5, pady=5)
        
        self.tree_list = ttk.Treeview(left_frame, columns=("status", "comp"), show="headings")
        self.tree_list.heading("status", text="Archivo")
        self.tree_list.heading("comp", text="Complejidad")
        self.tree_list.column("status", width=180)
        self.tree_list.column("comp", width=100)
        self.tree_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree_list.bind("<<TreeviewSelect>>", self._on_item_selected)
        
        ttk.Button(left_frame, text="🔄 Recargar", command=self._load_initial_data).pack(fill=tk.X, padx=5, pady=5)

        # Derecha
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=4)
        
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestañas
        self.txt_report = self._create_tab_content("📊 Reporte", "text")
        self.txt_code = self._create_tab_content("📝 Código", "text")
        
        # Frames para gráficos (se inicializan pero no se agregan al notebook aún)
        self.frame_tree = ttk.Frame(self.notebook)
        self.tree_viz = TreeVisualizerGUI(self.frame_tree)
        self.tree_viz.pack(fill=tk.BOTH, expand=True)
        
        self.frame_flow = ttk.Frame(self.notebook)
        self.flow_container = ttk.Frame(self.frame_flow)
        self.flow_container.pack(fill=tk.BOTH, expand=True)
        self.current_fig_canvas = None
        
    def _open_ai_window(self):
        LLMWindow(self.root, self.orchestrator)

    def _create_tab_content(self, title, type):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        if type == "text":
            txt = scrolledtext.ScrolledText(frame, font=('Consolas', 10), padx=10, pady=10)
            txt.pack(fill=tk.BOTH, expand=True)
            # Estilos de texto
            txt.tag_config("h1", foreground="#1565C0", font=('Consolas', 12, 'bold'))
            txt.tag_config("box", foreground="#E65100", font=('Consolas', 10, 'bold'))
            txt.tag_config("success", foreground="#2E7D32")
            txt.tag_config("error", foreground="#C62828")
            txt.tag_config("info", foreground="#0277BD")
            return txt
        return frame

    def _load_initial_data(self):
        files = get_algorithm_files()
        for item in self.tree_list.get_children():
            self.tree_list.delete(item)
        
        total_start = time.perf_counter()
        timing_rows = []
            
        for file_path in files:
            result = self.orchestrator.process_file(file_path)
            self.gui_cache[result.filename] = result
            
            if result.error:
                self.tree_list.insert("", tk.END, iid=result.filename, values=(result.filename, "ERROR"))
            else:
                self.tree_list.insert("", tk.END, iid=result.filename, values=(result.filename, result.heur_complexity))
            
            timing_ms = result.elapsed_ms
            if timing_ms is None:
                timing_ms = (time.perf_counter() - total_start) * 1000
            timing_rows.append((result.filename, timing_ms))

        # Imprimir tiempos de análisis por archivo y total (solo al cargar una vez)
        if not getattr(self, "_timing_printed", False):
            total_ms = (time.perf_counter() - total_start) * 1000
            print("\nTiempos de análisis inicial:")
            for fname, ms in timing_rows:
                print(f"   - {fname}: {ms:.2f} ms")
            print(f"   Total: {total_ms:.2f} ms\n")
            self._timing_printed = True

    def _on_item_selected(self, event):
        selection = self.tree_list.selection()
        if not selection: return
        
        filename = selection[0]
        if filename not in self.gui_cache: return
        
        res = self.gui_cache[filename]
        
        # 1. Código
        self.txt_code.delete('1.0', tk.END)
        self.txt_code.insert('1.0', res.code)
        
        # 2. Reporte
        self._fill_report_detailed(res)
        
        # 3. Gestión de Pestañas
        self._update_tabs_visibility(res)

    def _fill_report_detailed(self, res):
        t = self.txt_report
        t.delete('1.0', tk.END)
        
        def w(text, tag=None): t.insert(tk.END, text + "\n", tag)

        # Header
        w("╔" + "═"*90 + "╗", "h1")
        w(f"║ {'ANÁLISIS DEL ALGORITMO: ' + res.name:<88} ║", "h1")
        w("╚" + "═"*90 + "╝\n", "h1")

        # 1. Matemático
        w("┌─ 🔢 RESULTADOS DEL MOTOR MATEMÁTICO " + "─"*58 + "┐", "box")
        w(f"  • Función: {res.name}")
        
        # Lógica para mostrar "Expresión de Costo" o "Ecuación" según corresponda
        if "T(n)" in res.math_expression:
            w(f"  • Ecuación de Recurrencia: {res.math_expression}")
        else:
            w(f"  • Expresión de costo: {res.math_expression}")
            
        w(f"  • Complejidad Derivada: {res.math_complexity}")
        w("└" + "─"*90 + "┘\n")

        # 2. Heurístico
        w("┌─ 📐 ECUACIÓN DE RECURRENCIA Y COMPLEJIDAD ASINTÓTICA (HEURÍSTICO) " + "─"*34 + "┐", "box")
        w(f"  Ecuación de Recurrencia GENERAL:")
        w(f"    {res.heur_equation}\n")
        
        if res.heur_base_cases != "N/A":
            w(f"  Casos Base:")
            w(f" {res.heur_base_cases}\n")
            
        w(f"  Complejidad Asintótica:")
        w(f"    {res.heur_complexity}  [Cota ajustada]\n")
        
        w(f"  Método de Análisis:")
        w(f"    {res.heur_method}\n")
        
        w(f"  Explicación:")
        w(f"    {res.heur_explanation}")
        w("└" + "─"*90 + "┘\n")

        # Costos por nivel (solo si es recursivo)
        if getattr(res, "is_recursive", False) and getattr(res, "level_costs", []):
            w("┌─ Costos por nivel (recursivo) " + "─"*54 + "┐", "box")
            for line in res.level_costs:
                w(f"  - {line}")
            w("└" + "─"*90 + "┘\n")

        # 3. Escenarios
        w("┌─ 🔍 ANÁLISIS DE MEJOR, PEOR Y CASO PROMEDIO " + "─"*50 + "┐", "box")
        
        try:
            # Analizar casos en tiempo real para obtener ejemplos y explicaciones
            cases = self.case_analyzer.analyze_all_cases(
                res.ast_node, 
                recurrence_eq=res.heur_equation,
                complexity=res.heur_complexity
            )
            
            # MEJOR CASO
            w("  ╭─ ✅ MEJOR CASO " + "─"*68 + "╮", "success")
            w(f"  │ Complejidad: {cases['best'].complexity}", "success")
            w(f"  │ Escenario: {cases['best'].scenario}", "success")
            w(f"  │ Ejemplo: {cases['best'].ejemplo}", "success")
            w(f"  │ Explicación: {cases['best'].explanation}", "success")
            w("  ╰" + "─"*86 + "╯\n", "success")

            # PEOR CASO
            w("  ╭─ ❌ PEOR CASO " + "─"*69 + "╮", "error")
            w(f"  │ Complejidad: {cases['worst'].complexity}", "error")
            w(f"  │ Escenario: {cases['worst'].scenario}", "error")
            w(f"  │ Ejemplo: {cases['worst'].ejemplo}", "error")
            w(f"  │ Explicación: {cases['worst'].explanation}", "error")
            w("  ╰" + "─"*86 + "╯\n", "error")

            # PROMEDIO
            w("  ╭─ 📊 CASO PROMEDIO " + "─"*65 + "╮", "info")
            w(f"  │ Complejidad: {cases['average'].complexity}", "info")
            w(f"  │ Escenario: {cases['average'].scenario}", "info")
            w(f"  │ Explicación: {cases['average'].explanation}", "info")
            w("  ╰" + "─"*86 + "╯", "info")

        except Exception as e:
            w(f"  [!] Error detallando casos: {e}")

        w("└" + "─"*90 + "┘")

    def _update_tabs_visibility(self, res):
        # Ocultar todo primero
        if self.frame_tree in self.notebook.tabs(): self.notebook.forget(self.frame_tree)
        if self.frame_flow in self.notebook.tabs(): self.notebook.forget(self.frame_flow)
        
        if res.is_recursive:
            self.notebook.add(self.frame_tree, text="🌳 Árbol")
            if res.tree_structure_data:
                self.tree_viz.draw_tree(res.tree_structure_data)
        else:
            self.notebook.add(self.frame_flow, text="📈 Flujo")
            self._draw_flowchart(res)

    def _draw_flowchart(self, res):
        for widget in self.flow_container.winfo_children():
            widget.destroy()
        
        if not res.ast_node: return
        
        try:
            # Generar figura (ahora devuelve un objeto Figure independiente)
            fig = self.flowchart_gen.generate_flowchart(res.ast_node, title="")
            
            canvas = FigureCanvasTkAgg(fig, master=self.flow_container)
            canvas.draw()
            
            widget = canvas.get_tk_widget()
            widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except Exception as e:
            tk.Label(self.flow_container, text=f"Error visualizando flujo: {e}").pack()

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

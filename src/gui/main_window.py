"""
Main Window GUI
===============

Ventana principal de la interfaz gráfica del analizador de complejidades.

Esta ventana integra todas las funcionalidades del analizador:
- Carga de archivos de pseudocódigo
- Análisis de complejidad asintótica
- Visualización de árboles de recurrencia
- Diagramas de flujo para algoritmos iterativos
- Análisis de mejor/peor caso

Classes:
- MainWindow: Ventana principal de la aplicación
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os
import sympy as sp

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.parser.parser import parse_code
from src.analyzer.advanced_complexity import AdvancedComplexityAnalyzer
from src.analyzer.dp_analyzer import DynamicProgrammingAnalyzer
from src.analyzer.recurrence_solver import RecursiveAlgorithmAnalyzer
from src.analyzer.recurrence_tree_builder import TreeStructure
from src.analyzer.asymptotic_analyzer import AsymptoticAnalyzer
from src.analyzer.case_analyzer import CaseAnalyzer
from src.analyzer.math_analyzer import MathematicalAnalyzer # IMPORT THE NEW ANALYZER
from src.gui.tree_visualizer_gui import TreeVisualizerGUI
from src.gui.flowchart_generator import FlowchartGenerator


class MainWindow:
    """
    Ventana principal del Analizador de Complejidades.
    
    Proporciona una interfaz gráfica completa para analizar algoritmos.
    """
    
    def __init__(self, root):
        """Inicializa la ventana principal."""
        self.root = root
        self.root.title("Analizador de Complejidades - Universidad de Caldas")
        self.root.geometry("1400x900")
        
        # Variables
        self.current_file = None
        self.current_ast = None
        self.current_code = ""
        self.math_raw_results = None 
        
        # Analizadores
        self.basic_analyzer = AdvancedComplexityAnalyzer()
        self.dp_analyzer = DynamicProgrammingAnalyzer()
        self.recursive_analyzer = RecursiveAlgorithmAnalyzer()
        
        # CORRECCIÓN: Iniciamos el builder vacío
        self.tree_builder = TreeStructure(None) 
        
        self.asymptotic_analyzer = AsymptoticAnalyzer()
        self.case_analyzer = CaseAnalyzer()
        self.math_analyzer = MathematicalAnalyzer()
        
        # GUI Components (se inicializan en _create_tree_tab)
        self.tree_visualizer = None 
        self.flowchart_generator = FlowchartGenerator()
        
        self._setup_ui()
        self._setup_styles()
    
    def _setup_styles(self):
        """Configura los estilos de la interfaz."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores corporativos
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#1976D2')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#424242')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#616161')
        style.configure('Success.TLabel', font=('Arial', 10), foreground='#4CAF50')
        style.configure('Error.TLabel', font=('Arial', 10), foreground='#F44336')
        
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
    
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        self._create_header(main_frame)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Tabs
        self._create_code_tab()
        self._create_complete_analysis_tab()  # NUEVO: Análisis completo integrado
        self._create_tree_tab()
        self._create_flowchart_tab()
        
        # Status bar
        self._create_status_bar(main_frame)
    
    def _create_header(self, parent):
        """Crea el header de la aplicación."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Título
        title = ttk.Label(header_frame, text="🎓 Analizador de Complejidades de Algoritmos",
                         style='Title.TLabel')
        title.grid(row=0, column=0, sticky=tk.W)
        
        subtitle = ttk.Label(header_frame, text="Universidad de Caldas - Análisis y Diseño de Algoritmos 2025-2",
                           style='Info.TLabel')
        subtitle.grid(row=1, column=0, sticky=tk.W)
        
        # Botones de acción
        btn_frame = ttk.Frame(header_frame)
        btn_frame.grid(row=0, column=1, rowspan=2, sticky=tk.E, padx=10)
        
        ttk.Button(btn_frame, text="📁 Abrir Archivo", command=self.load_file,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="▶️ Analizar", command=self.analyze_code,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="💾 Exportar", command=self.export_results,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        
        header_frame.columnconfigure(0, weight=1)
    
    def _create_code_tab(self):
        """Crea la pestaña de código."""
        code_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(code_frame, text="📝 Pseudocódigo")
        
        # Frame para el editor
        editor_frame = ttk.LabelFrame(code_frame, text="Editor de Pseudocódigo", padding="10")
        editor_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        code_frame.columnconfigure(0, weight=1)
        code_frame.rowconfigure(0, weight=1)
        
        # Editor de texto
        self.code_editor = scrolledtext.ScrolledText(editor_frame, width=80, height=30,
                                                     font=('Consolas', 11), wrap=tk.WORD)
        self.code_editor.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)
        
        # Placeholder text - ejemplo válido de factorial
        self.code_editor.insert('1.0', """function factorial(n)
begin
    if n <= 1
    begin
        return 1
    end
    else
    begin
        return n * call factorial(n - 1)
    end
end
""")
    
    def _create_analysis_tab(self):
        """Crea la pestaña de análisis - DEPRECATED, usar _create_complete_analysis_tab."""
        pass
    
    def _create_complete_analysis_tab(self):
        """Crea la pestaña de análisis completo e integrado."""
        analysis_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(analysis_frame, text="📊 Análisis Completo")
        
        # Área de texto única con scroll para todo el análisis
        complete_frame = ttk.LabelFrame(analysis_frame, text="Análisis Integrado del Algoritmo", padding="10")
        complete_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        analysis_frame.columnconfigure(0, weight=1)
        analysis_frame.rowconfigure(0, weight=1)
        
        # Área de texto con formato
        self.complete_analysis_text = scrolledtext.ScrolledText(
            complete_frame, width=140, height=45,
            font=('Consolas', 10), wrap=tk.WORD
        )
        self.complete_analysis_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        complete_frame.columnconfigure(0, weight=1)
        complete_frame.rowconfigure(0, weight=1)
    
    def _create_tree_tab(self):
        """Crea la pestaña de árboles de recurrencia con el nuevo visualizador."""
        tree_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tree_frame, text="🌳 Árbol de Recurrencia")
        
        # Frame para controles superiores
        control_frame = ttk.Frame(tree_frame)
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(control_frame, text="Visualización Simbólica de la Recurrencia").pack(side=tk.LEFT, padx=5)
        
        # Botón manual por si acaso
        ttk.Button(control_frame, text="🔄 Redibujar", 
                   command=self.generate_tree).pack(side=tk.RIGHT, padx=5)
        
        # Frame contenedor del visualizador
        container = ttk.Frame(tree_frame, relief="sunken", borderwidth=1)
        container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Instanciar el visualizador GUI correctamente
        self.tree_visualizer = TreeVisualizerGUI(container)
        self.tree_visualizer.pack(fill=tk.BOTH, expand=True)
        
        # Configurar pesos del grid
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(1, weight=1)
    
    def _create_flowchart_tab(self):
        """Crea la pestaña de diagramas de flujo."""
        flow_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(flow_frame, text="📈 Diagrama de Flujo")
        
        # Frame para controles
        control_frame = ttk.Frame(flow_frame)
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="🔄 Generar Diagrama",
                  command=self.generate_flowchart).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="💾 Guardar Imagen",
                  command=self.save_flowchart).pack(side=tk.LEFT, padx=5)
        
        # Frame para el canvas
        self.flow_canvas_frame = ttk.Frame(flow_frame)
        self.flow_canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        flow_frame.columnconfigure(0, weight=1)
        flow_frame.rowconfigure(1, weight=1)
        
        # Canvas placeholder
        self.flow_canvas = None
        self.flow_figure = None
    
    def _create_cases_tab(self):
        """Crea la pestaña de análisis de casos."""
        cases_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(cases_frame, text="⚖️ Mejor/Peor Caso")
        
        # Mejor caso
        best_frame = ttk.LabelFrame(cases_frame, text="✅ MEJOR CASO", padding="10")
        best_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.best_case_text = scrolledtext.ScrolledText(best_frame, width=45, height=15,
                                                       font=('Consolas', 10), wrap=tk.WORD)
        self.best_case_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        best_frame.columnconfigure(0, weight=1)
        best_frame.rowconfigure(0, weight=1)
        
        # Peor caso
        worst_frame = ttk.LabelFrame(cases_frame, text="❌ PEOR CASO", padding="10")
        worst_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.worst_case_text = scrolledtext.ScrolledText(worst_frame, width=45, height=15,
                                                        font=('Consolas', 10), wrap=tk.WORD)
        self.worst_case_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        worst_frame.columnconfigure(0, weight=1)
        worst_frame.rowconfigure(0, weight=1)
        
        # Caso promedio
        avg_frame = ttk.LabelFrame(cases_frame, text="📊 CASO PROMEDIO", padding="10")
        avg_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.avg_case_text = scrolledtext.ScrolledText(avg_frame, width=90, height=15,
                                                      font=('Consolas', 10), wrap=tk.WORD)
        self.avg_case_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        avg_frame.columnconfigure(0, weight=1)
        avg_frame.rowconfigure(0, weight=1)
        
        cases_frame.columnconfigure(0, weight=1)
        cases_frame.columnconfigure(1, weight=1)
        cases_frame.rowconfigure(0, weight=1)
        cases_frame.rowconfigure(1, weight=1)
    
    def _create_status_bar(self, parent):
        """Crea la barra de estado."""
        status_frame = ttk.Frame(parent, relief=tk.SUNKEN, padding="2")
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Listo", style='Info.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        self.file_label = ttk.Label(status_frame, text="", style='Info.TLabel')
        self.file_label.pack(side=tk.RIGHT)
    
    def load_file(self):
        """Carga un archivo de pseudocódigo."""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de pseudocódigo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialdir="examples"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.code_editor.delete('1.0', tk.END)
                self.code_editor.insert('1.0', content)
                
                self.current_file = filename
                self.file_label.config(text=f"Archivo: {os.path.basename(filename)}")
                self.status_label.config(text="✅ Archivo cargado correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
                self.status_label.config(text="❌ Error al cargar archivo")
    
    def analyze_code(self):
        """Analiza el código actual de manera integrada."""
        self.current_code = self.code_editor.get('1.0', tk.END).strip()
        
        if not self.current_code:
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return
        
        try:
            self.status_label.config(text="🔄 Analizando...")
            self.root.update()
            
            # Parsear código
            self.current_ast = parse_code(self.current_code)
            
            # Realizar análisis completo integrado
            self._perform_complete_analysis()
            
            # Generar árbol automáticamente si es recursivo
            if hasattr(self.current_ast, 'functions') and self.current_ast.functions:
                for func in self.current_ast.functions:
                    rec_analysis = self.recursive_analyzer.analyze_recursive_algorithm(func)
                    if rec_analysis['has_recursion']:
                        # Generar árbol automáticamente
                        try:
                            self.generate_tree()
                        except Exception as e:
                            print(f"Error al generar árbol: {e}")
                        break
            
            # Cambiar a la pestaña de análisis completo
            self.notebook.select(1)
            
            self.status_label.config(text="✅ Análisis completado")
            
        except Exception as e:
            messagebox.showerror("Error de análisis", f"Error al analizar el código:\n{str(e)}")
            self.status_label.config(text="❌ Error en el análisis")
            import traceback
            traceback.print_exc()
    
    def _perform_complete_analysis(self):
        """Realiza el análisis completo e integrado del algoritmo."""
        # Limpiar texto
        self.complete_analysis_text.delete('1.0', tk.END)
        
        result = ""
        
        # --- NEW MATHEMATICAL ANALYSIS ---
        result += "╔" + "═" * 118 + "╗\n"
        result += "║" + " " * 35 + "ANÁLISIS MATEMÁTICO REAL (NUEVO MOTOR)" + " " * 44 + "║\n"
        result += "╚" + "═" * 118 + "╝\n\n"
        try:
            solved_results = self.math_analyzer.analyze(self.current_ast)
            # Store raw equations for tree builder and textual analysis
            self.math_raw_results = self.math_analyzer.last_raw_results
            
            result += "┌─ 🔢 RESULTADOS DEL MOTOR MATEMÁTICO " + "─" * 80 + "┐\n\n"
            if self.math_raw_results:
                for func_name, raw_value in self.math_raw_results.items():
                    solved = solved_results.get(func_name)
                    result += f"  Función: {func_name}\n"
                    if isinstance(raw_value, sp.Eq):
                        result += f"    • Ecuación de Recurrencia: {raw_value}\n"
                        result += f"    • Complejidad Derivada: {solved}\n\n"
                    else:
                        result += f"    • Expresión de costo: {raw_value}\n"
                        result += f"    • Complejidad Derivada: {solved}\n\n"
            else:
                result += "  No se encontraron resultados matemáticos.\n\n"
            result += "└" + "─" * 118 + "┘\n\n"
        except Exception as e:
            self.math_raw_results = None
            result += f"  ❌ Error en el nuevo motor matemático: {e}\n\n"
            import traceback
            traceback.print_exc()
        # --- END NEW ANALYSIS ---

        result += "╔" + "═" * 118 + "╗\n"
        result += "║" + " " * 38 + "ANÁLISIS HEURÍSTICO (MOTOR ANTIGUO)" + " " * 45 + "║\n"
        result += "╚" + "═" * 118 + "╝\n\n"
        
        # 1. ANÁLISIS ASINTÓTICO (OLD ENGINE)
        result += "┌─ 📐 ECUACIÓN DE RECURRENCIA Y COMPLEJIDAD ASINTÓTICA " + "─" * 62 + "┐\n\n"
        
        recursive_info = None
        if hasattr(self.current_ast, 'functions') and self.current_ast.functions:
            for func in self.current_ast.functions:
                rec_analysis = self.recursive_analyzer.analyze_recursive_algorithm(func)
                if rec_analysis['has_recursion']:
                    recursive_info = rec_analysis
                    break
        
        recurrence, bound = self.asymptotic_analyzer.analyze(self.current_ast, recursive_info)
        
        result += f"  Ecuación de Recurrencia GENERAL:\n"
        result += f"    {recurrence.equation}\n\n"
        
        if recurrence.base_cases:
            result += f"  Casos Base:\n"
            for case, value in recurrence.base_cases.items():
                result += f"    • {case} = {value}\n"
            result += "\n"
        
        # Determinar si es tight bound o weak bound
        bound_type = self._determine_bound_type(bound, recursive_info)
        
        result += f"  Complejidad Asintótica:\n"
        if bound_type == "tight":
            result += f"    Θ({bound.complexity})  [Cota ajustada]\n\n"
        elif bound_type == "upper":
            result += f"    O({bound.complexity})  [Cota superior]\n\n"
        else:
            result += f"    Ω({bound.complexity})  [Cota inferior]\n\n"
        
        result += f"  Método de Análisis:\n"
        result += f"    {recurrence.method_used}\n\n"
        result += f"  Explicación:\n"
        for line in bound.explanation.split('\n'):
            result += f"    {line}\n"
        
        result += "\n└" + "─" * 118 + "┘\n\n"
        
        # 2. ANÁLISIS DE CASOS (con validación de coherencia)
        # Pasar la ecuación y complejidad para validar coherencia
        cases = self.case_analyzer.analyze_all_cases(
            self.current_ast, 
            recurrence_eq=recurrence.equation,
            complexity=bound.complexity
        )
        
        result += "┌─ 🔍 ANÁLISIS DE MEJOR, PEOR Y CASO PROMEDIO " + "─" * 71 + "┐\n\n"
        
        # Mejor caso
        best = cases['best']
        result += "  ╭─ ✅ MEJOR CASO " + "─" * 100 + "╮\n"
        result += f"  │ Complejidad: {best.complexity}\n"
        result += f"  │\n"
        result += f"  │ Escenario:\n"
        for line in best.scenario.split('\n'):
            result += f"  │   {line}\n"
        result += f"  │\n"
        result += f"  │ Ejemplo:\n"
        for line in best.ejemplo.split('\n'):
            result += f"  │   {line}\n"
        result += f"  │\n"
        result += f"  │ Explicación:\n"
        for line in best.explanation.split('\n'):
            result += f"  │   {line}\n"
        result += "  ╰" + "─" * 116 + "╯\n\n"
        
        # Peor caso
        worst = cases['worst']
        result += "  ╭─ ❌ PEOR CASO " + "─" * 101 + "╮\n"
        result += f"  │ Complejidad: {worst.complexity}\n"
        result += f"  │\n"
        result += f"  │ Escenario:\n"
        for line in worst.scenario.split('\n'):
            result += f"  │   {line}\n"
        result += f"  │\n"
        result += f"  │ Ejemplo:\n"
        for line in worst.ejemplo.split('\n'):
            result += f"  │   {line}\n"
        result += f"  │\n"
        result += f"  │ Explicación:\n"
        for line in worst.explanation.split('\n'):
            result += f"  │   {line}\n"
        result += "  ╰" + "─" * 116 + "╯\n\n"
        
        # Caso promedio
        avg = cases['average']
        result += "  ╭─ 📊 CASO PROMEDIO " + "─" * 97 + "╮\n"
        result += f"  │ Complejidad: {avg.complexity}\n"
        result += f"  │\n"
        result += f"  │ Escenario:\n"
        for line in avg.scenario.split('\n'):
            result += f"  │   {line}\n"
        result += f"  │\n"
        result += f"  │ Ejemplo:\n"
        for line in avg.ejemplo.split('\n'):
            result += f"  │   {line}\n"
        result += f"  │\n"
        result += f"  │ Explicación:\n"
        for line in avg.explanation.split('\n'):
            result += f"  │   {line}\n"
        result += "  ╰" + "─" * 116 + "╯\n\n"
        
        result += "└" + "─" * 118 + "┘\n\n"
        
        # 3. ANÁLISIS TEXTUAL DEL ÁRBOL DE RECURRENCIA (si es recursivo)
        if recursive_info:
            result += "┌─ 🌳 ESTRUCTURA DEL ÁRBOL DE RECURRENCIA " + "─" * 75 + "┐\n\n"
            
            # Generar análisis de árbol textual desde el motor matemático
            if self.math_raw_results:
                eq_found = None
                for res in self.math_raw_results.values():
                    if isinstance(res, sp.Eq):
                        eq_found = res
                        break
                
                if eq_found is not None:
                    tree_analysis = self.math_analyzer._generate_tree_textual_analysis(eq_found)
                    result += tree_analysis
                    tree_builder = TreeStructure(str(eq_found))
                    tree_data = tree_builder.get_structure()

                    self.tree_visualizer.draw_tree(tree_data)

                else:
                    result += "  No se pudo generar el análisis del árbol a partir de la ecuación de recurrencia."
            else:
                result += "  Análisis matemático no disponible para generar el árbol."

            result += "\n└" + "─" * 118 + "┘\n\n"
        
        # 4. DETALLES ADICIONALES
        if recursive_info:
            result += "┌─ 📚 DETALLES DE LA RECURSIÓN " + "─" * 86 + "┐\n\n"
            result += f"  Función analizada: {recursive_info['function_name']}\n"
            result += f"  Patrón detectado: {recursive_info['pattern_type']}\n"
            result += f"  Número de llamadas recursivas: {len(recursive_info['recursive_calls'])}\n"
            result += f"  Trabajo por llamada: {recursive_info['work_per_call']}\n"
            result += f"  \n"
            result += f"  Llamadas recursivas encontradas:\n"
            for i, call in enumerate(recursive_info['recursive_calls'], 1):
                result += f"    {i}. {call}\n"
            result += "\n└" + "─" * 118 + "┘\n\n"
        
        result += "\n" + "═" * 120 + "\n"
        result += "NOTA: Para algoritmos recursivos, consultar el tab 'Árbol de Recurrencia' para visualizar\n"
        result += "      la estructura general de las llamadas recursivas y ambientes.\n"
        result += "      Para algoritmos iterativos, consultar el tab 'Diagrama de Flujo'.\n"
        result += "═" * 120 + "\n"
        
        self.complete_analysis_text.insert('1.0', result)
    
    def _determine_bound_type(self, bound, recursive_info):
        """Determina si la cota es ajustada (Θ), superior (O) o inferior (Ω)."""
        # Por ahora, asumimos que si tenemos información completa, es tight bound
        # En el futuro, se puede mejorar con análisis más detallado
        if recursive_info and bound.complexity:
            # Si tenemos recursión bien analizada, probablemente es tight
            return "tight"
        elif bound.complexity and "O(" in str(bound.notation):
            return "upper"
        elif bound.complexity and "Ω(" in str(bound.notation):
            return "lower"
        else:
            return "tight"  # Por defecto asumimos tight

    def _format_eq_for_tree_builder(self, eq: 'sp.Eq') -> str:
        """
        Converts a sympy recurrence equation into the string format
        expected by the old RecurrenceTreeBuilder.
        Example: Eq(T(n), 2*T(n/2) + n) -> "T(n) = 2*T(n/2) + O(n)"
        """
        from sympy import O, Add, oo
        
        lhs = eq.lhs
        rhs = eq.rhs
        
        # Separate recursive and non-recursive parts of the RHS
        recursive_terms = []
        non_recursive_terms = []
        
        for term in Add.make_args(rhs):
            if term.has(self.math_analyzer.T):
                recursive_terms.append(term)
            else:
                non_recursive_terms.append(term)
                
        # Format the non-recursive part as O(...)
        non_recursive_work = sum(non_recursive_terms) if non_recursive_terms else sp.Integer(0)

        work_str = ""
        # Defensive check for None and check for free_symbols
        if non_recursive_work is None:
            work_str = "O(1)" # Assume constant work if something went wrong
        elif hasattr(non_recursive_work, 'free_symbols') and non_recursive_work.free_symbols:
            work_str = str(O(non_recursive_work, (self.math_analyzer.n, oo)))
        else: # It's a constant
            work_str = f"O({non_recursive_work})"

        # Format the final string
        if not recursive_terms:
             return f"{lhs} = {work_str}"
        
        rhs_str = " + ".join(map(str, recursive_terms))
        if work_str:
            rhs_str += f" + {work_str}"
        
        return f"{lhs} = {rhs_str}"

    def _perform_complexity_analysis(self):
        """DEPRECATED - Realiza el análisis de complejidad."""
        # Este método ya no se usa, ver _perform_complete_analysis()
        pass
    
    def _perform_case_analysis(self):
        """DEPRECATED - Realiza el análisis de mejor/peor caso."""
        # Este método ya no se usa, ver _perform_complete_analysis()
        pass
    
    def generate_tree(self):
        """Genera el árbol simbólico basado en la ecuación matemática encontrada."""
        if not self.math_raw_results:
            # Intentar analizar si no hay resultados
            if self.current_ast:
                self.math_raw_results = self.math_analyzer.analyze(self.current_ast)
            else:
                return

        # Buscar una ecuación en los resultados (Eq object)
        eq_found = None
        for res in self.math_raw_results.values():
            if isinstance(res, sp.Eq):
                eq_found = res
                break
        
        if eq_found is not None:
            try:
                # 1. Pasar la ecuación al constructor de estructura
                self.tree_builder.analyze_equation(str(eq_found))
                
                # 2. Obtener datos limpios
                tree_data = self.tree_builder.get_structure()
                
                # 3. Dibujar
                self.tree_visualizer.draw_tree(tree_data)
                
                self.status_label.config(text=f"✅ Árbol generado para: {eq_found}")
            except Exception as e:
                print(f"Error dibujando árbol: {e}")
                self.status_label.config(text="❌ Error visualizando árbol")
        else:
            # Limpiar si no es recursivo
            self.tree_visualizer.canvas.delete("all")
            self.tree_visualizer.canvas.create_text(
                400, 200, text="Este algoritmo no parece ser recursivo\n(No hay ecuación de recurrencia)", 
                font=("Arial", 14), fill="#B0BEC5"
            )
    
    def save_tree(self):
        """Guarda el árbol de recurrencia."""
        if self.tree_figure is None:
            messagebox.showwarning("Advertencia", "Primero debe generar un árbol")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")]
        )
        
        if filename:
            self.tree_figure.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Éxito", f"Árbol guardado en:\n{filename}")
    
    def generate_flowchart(self):
        """Genera y muestra el diagrama de flujo."""
        if self.current_ast is None:
            messagebox.showwarning("Advertencia", "Primero debe analizar el código")
            return
        
        try:
            self.status_label.config(text="🔄 Generando diagrama...")
            self.root.update()
            
            # Generar diagrama
            self.flow_figure = self.flowchart_generator.generate_flowchart(
                self.current_ast, "Diagrama de Flujo del Algoritmo"
            )
            
            # Limpiar canvas anterior
            if self.flow_canvas:
                self.flow_canvas.get_tk_widget().destroy()
            
            # Crear nuevo canvas
            self.flow_canvas = FigureCanvasTkAgg(self.flow_figure, self.flow_canvas_frame)
            self.flow_canvas.draw()
            self.flow_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.status_label.config(text="✅ Diagrama generado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar diagrama:\n{str(e)}")
            self.status_label.config(text="❌ Error generando diagrama")
            import traceback
            traceback.print_exc()
    
    def save_flowchart(self):
        """Guarda el diagrama de flujo."""
        if self.flow_figure is None:
            messagebox.showwarning("Advertencia", "Primero debe generar un diagrama")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")]
        )
        
        if filename:
            self.flow_figure.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Éxito", f"Diagrama guardado en:\n{filename}")
    
    def export_results(self):
        """Exporta todos los resultados a un archivo."""
        if self.current_ast is None:
            messagebox.showwarning("Advertencia", "Primero debe analizar el código")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write("REPORTE COMPLETO DE ANÁLISIS DE COMPLEJIDAD\n")
                    f.write("=" * 80 + "\n\n")
                    
                    f.write("CÓDIGO ANALIZADO:\n")
                    f.write("-" * 80 + "\n")
                    f.write(self.current_code + "\n\n")
                    
                    f.write("ANÁLISIS DE COMPLEJIDAD:\n")
                    f.write("-" * 80 + "\n")
                    f.write(self.complete_analysis_text.get('1.0', tk.END) + "\n")
                    
                    f.write("\nANÁLISIS DE CASOS:\n")
                    f.write("-" * 80 + "\n")
                    f.write("\nMEJOR CASO:\n")
                    f.write(self.best_case_text.get('1.0', tk.END) + "\n")
                    f.write("\nPEOR CASO:\n")
                    f.write(self.worst_case_text.get('1.0', tk.END) + "\n")
                    f.write("\nCASO PROMEDIO:\n")
                    f.write(self.avg_case_text.get('1.0', tk.END) + "\n")
                
                messagebox.showinfo("Éxito", f"Reporte exportado a:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")


def main():
    """Función principal para lanzar la GUI."""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()

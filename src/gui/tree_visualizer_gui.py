import tkinter as tk
from tkinter import ttk

class TreeVisualizerGUI(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Estilos
        self.node_radius = 25
        self.level_height = 70 # Distancia vertical entre niveles
        self.color_root = "#BBDEFB"
        self.color_node = "#E1F5FE"
        self.color_leaf = "#C8E6C9"
        self.font_main = ("Segoe UI", 9, "bold")

    def draw_tree(self, data):
        self.canvas.delete("all")
        self.update_idletasks()
        w = self.canvas.winfo_width()
        if w < 50: w = 800
        
        root_node = data.get("tree_topology", {"val": "n", "children": []})
        height_str = data.get("height", "?")
        
        # Dibujar recursivamente comenzando desde el centro, arriba
        max_depth_to_draw = 2 # Dibujamos Raiz, Hijos, Nietos
        
        self._draw_recursive(root_node, w/2, 50, w/2, 0, max_depth_to_draw)
        
        # Dibujar la abstracción (...) y casos base después del último nivel dibujado
        last_y = 50 + (max_depth_to_draw * self.level_height)
        self._draw_footer(w/2, last_y, height_str)

    def _draw_recursive(self, node, x, y, available_width, depth, max_depth):
        """
        Dibuja un nodo y llama recursivamente a sus hijos.
        x, y: Centro del nodo actual
        available_width: Ancho disponible para distribuir a los hijos
        """
        # Determinar color
        color = self.color_root if depth == 0 else self.color_node
        
        # Dibujar el nodo actual
        self._draw_circle(x, y, node["val"], color)
        
        # Si llegamos al límite de profundidad, no dibujamos hijos (aunque existan)
        if depth >= max_depth:
            return

        children = node.get("children", [])
        num_children = len(children)
        
        if num_children == 0:
            return

        # Calcular posiciones de los hijos
        # Dividimos el ancho disponible entre los hijos
        next_y = y + self.level_height
        
        # Lógica de espaciado:
        # Si es el nivel 0, damos mucho espacio. Si es nivel 1, menos espacio.
        width_per_child = available_width / num_children
        
        # Ajuste para que no queden muy separados si hay pocos hijos
        if width_per_child > 150: width_per_child = 150
        
        total_span = width_per_child * (num_children - 1)
        start_x = x - (total_span / 2)

        for i, child in enumerate(children):
            child_x = start_x + (i * width_per_child)
            
            # Dibujar línea conectora
            self.canvas.create_line(x, y + self.node_radius, child_x, next_y - self.node_radius, fill="#546E7A", width=2)
            
            # Llamada recursiva
            self._draw_recursive(child, child_x, next_y, width_per_child, depth + 1, max_depth)

    def _draw_footer(self, cx, start_y, height_str):
        # Dibujar puntos suspensivos
        dots_y = start_y + 30
        self.canvas.create_text(cx, dots_y, text="⋮\n(Expansión)\n⋮", font=("Arial", 12, "bold"), fill="#90A4AE")
        
        # Dibujar Hojas (Casos Base)
        leaves_y = dots_y + 60
        
        # Dibujamos 2 hojas representativas
        leaf_spacing = 60
        self._draw_circle(cx - leaf_spacing, leaves_y, "T(1)", self.color_leaf)
        self._draw_circle(cx + leaf_spacing, leaves_y, "T(1)", self.color_leaf)
        
        # Conectores fantasma
        self.canvas.create_line(cx, dots_y + 20, cx - leaf_spacing, leaves_y - self.node_radius, dash=(4,4), fill="#B0BEC5")
        self.canvas.create_line(cx, dots_y + 20, cx + leaf_spacing, leaves_y - self.node_radius, dash=(4,4), fill="#B0BEC5")

        # Indicador de Altura
        self.canvas.create_line(50, 50, 50, leaves_y, width=2, fill="#FF5722", arrow=tk.BOTH)
        self.canvas.create_text(60, (50 + leaves_y)/2, text=f"Altura h ≈ {height_str}", anchor="w", fill="#D84315", font=("Arial", 10, "bold"))

    def _draw_circle(self, x, y, text, color):
        r = self.node_radius
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="#455A64", width=2)
        self.canvas.create_text(x, y, text=text, font=self.font_main)
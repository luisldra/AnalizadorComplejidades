import networkx as nx
import textwrap
from matplotlib.figure import Figure

class FlowchartGenerator:
    """
    Genera diagramas de flujo visuales a partir del AST.
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.pos = {}
        self.labels = {}
        self.node_colors = {}
        self.counter = 0
        
        self.colors = {
            'start_end': '#81C784',  # Verde suave
            'process': '#64B5F6',    # Azul suave
            'decision': '#FFB74D',   # Naranja suave
            'io': '#4DD0E1',         # Cyan suave
            'loop': '#BA68C8'        # Morado suave
        }

    # --- UTILIDADES DE TEXTO ---

    def _wrap_text(self, text, width=20):
        """Divide el texto en varias líneas para que quepa en la caja."""
        if not text or str(text).strip() == "": return ""
        return "\n".join(textwrap.wrap(str(text), width=width))

    def _get_safe_list(self, obj, attrs):
        """Obtiene una lista de atributos de forma segura."""
        for attr in attrs:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if isinstance(val, list):
                    return val
        return []

    def _extract_value_from_object(self, node):
        """
        Intenta extraer el valor primitivo de un objeto nodo.
        Busca atributos comunes donde se suelen guardar los valores.
        """
        common_value_attrs = ['value', 'name', 'id', 'op', 'operator']
        for attr in common_value_attrs:
            if hasattr(node, attr):
                val = getattr(node, attr)
                if val is not None and val is not node:
                    return val
        return None

    def _get_node_text(self, node):
        """
        Extrae texto legible de CUALQUIER nodo AST buscando sus atributos de valor.
        Esta función es la clave para arreglar los textos '<object at...>'
        """
        if node is None:
            return "?"
            
        # 1. Si ya es un dato primitivo, devolverlo como string
        if isinstance(node, (int, float, str, bool)):
            return str(node)
            
        # 2. Obtener el nombre de la clase para decisiones estructurales
        cls_name = type(node).__name__
        
        # --- ESTRUCTURAS COMPLEJAS (Tienen prioridad) ---
        
        # Operaciones Binarias (suma, resta, comparaciones)
        if hasattr(node, 'left') and hasattr(node, 'right'):
            left = self._get_node_text(node.left)
            right = self._get_node_text(node.right)
            op_obj = getattr(node, 'op', getattr(node, 'operator', '+'))
            op = self._get_node_text(op_obj) if not isinstance(op_obj, str) else op_obj
            return f"{left} {op} {right}"

        # Llamadas a Función
        if cls_name in ['Call', 'FunctionCall'] or hasattr(node, 'func_name'):
            func_obj = getattr(node, 'func_name', getattr(node, 'name', 'call'))
            func_name = self._get_node_text(func_obj)
            
            args_list = self._get_safe_list(node, ['arguments', 'args', 'params'])
            args = ", ".join([self._get_node_text(arg) for arg in args_list])
            return f"{func_name}({args})"

        # Sentencias de Asignación
        if cls_name in ['AssignStmt', 'Assign']:
            target = self._get_node_text(getattr(node, 'name', getattr(node, 'target', '?')))
            val = self._get_node_text(getattr(node, 'value', getattr(node, 'expr', '?')))
            return f"{target} ← {val}"

        # Estructuras de Control (If, While)
        if hasattr(node, 'condition'):
            cond = self._get_node_text(node.condition)
            if "While" in cls_name:
                return f"Mientras {cond}"
            return f"¿{cond}?" 

        # Bucle For
        if cls_name in ['ForStmt', 'For']:
            var = self._get_node_text(getattr(node, 'variable', getattr(node, 'var', 'i')))
            start = self._get_node_text(getattr(node, 'start', getattr(node, 'begin', '0')))
            end = self._get_node_text(getattr(node, 'end', getattr(node, 'limit', 'n')))
            return f"Para {var} = {start} hasta {end}"

        # Return
        if cls_name in ['ReturnStmt', 'Return']:
            val = self._get_node_text(getattr(node, 'value', getattr(node, 'expr', '')))
            return f"Retornar {val}"

        # --- NODOS HOJA (Variables, Números) ---
        # Buscamos contenido recursivamente
        val = self._extract_value_from_object(node)
        if val is not None:
            # Recursión para limpiar el valor (ej. si 'value' es otro objeto nodo)
            return self._get_node_text(val)
        
        return f"[{cls_name}]"

    # --- GENERACIÓN DEL GRAFO ---

    def generate_flowchart(self, ast, title="Diagrama de Flujo"):
        self.graph = nx.DiGraph()
        self.counter = 0
        self.labels = {}
        self.node_colors = {}
        
        start_id = self._add_node("INICIO", 'start_end')
        last_id = start_id
        
        # Buscar dónde están las funciones o instrucciones
        functions = self._get_safe_list(ast, ['functions', 'body'])
        
        if functions:
            # Caso 1: Es una lista de funciones (Program node) -> Tomamos la primera
            if hasattr(functions[0], 'body') or hasattr(functions[0], 'statements'):
                func = functions[0]
                
                # Extraer parámetros de entrada
                func_args = self._get_safe_list(func, ['arguments', 'args', 'parameters'])
                if func_args:
                    args_text = [self._get_node_text(arg) for arg in func_args]
                    params_node_text = f"Entrada: {', '.join(args_text)}"
                    param_id = self._add_node(params_node_text, 'io')
                    self.graph.add_edge(last_id, param_id)
                    last_id = param_id
                
                body = self._get_safe_list(func, ['body', 'statements'])
                last_id = self._process_block(body, last_id)
            
            # Caso 2: Es una lista de instrucciones directas (Script)
            else:
                 last_id = self._process_block(functions, last_id)
            
        end_id = self._add_node("FIN", 'start_end')
        self.graph.add_edge(last_id, end_id)
        
        return self._draw_graph(title)

    def _process_block(self, statements, parent_id):
        current_id = parent_id
        if not statements: return current_id
        
        if not isinstance(statements, list):
            statements = [statements]

        for stmt in statements:
            cls_name = type(stmt).__name__
            
            if "If" in cls_name:
                current_id = self._process_if(stmt, current_id)
            elif "For" in cls_name or "While" in cls_name:
                current_id = self._process_loop(stmt, current_id)
            elif "Return" in cls_name:
                text = self._get_node_text(stmt)
                node_id = self._add_node(text, 'start_end')
                self.graph.add_edge(current_id, node_id)
                current_id = node_id
            else:
                # Proceso genérico (Asignación, Llamada)
                text = self._get_node_text(stmt)
                node_id = self._add_node(text, 'process')
                self.graph.add_edge(current_id, node_id)
                current_id = node_id
                
        return current_id

    def _process_if(self, stmt, parent_id):
        cond_text = self._get_node_text(getattr(stmt, 'condition', getattr(stmt, 'test', None)))
        decision_id = self._add_node(cond_text, 'decision')
        self.graph.add_edge(parent_id, decision_id)
        
        # Rama Verdadera
        true_start = self._add_node("V", 'process', size=0.1)
        self.graph.add_edge(decision_id, true_start)
        
        true_body = self._get_safe_list(stmt, ['true_body', 'body', 'then_body'])
        true_end = self._process_block(true_body, true_start)
        
        # Rama Falsa
        false_start = self._add_node("F", 'process', size=0.1)
        self.graph.add_edge(decision_id, false_start)
        
        false_body = self._get_safe_list(stmt, ['false_body', 'else_body', 'orelse'])
        false_end = self._process_block(false_body, false_start)
        
        # Nodo de unión
        join_id = self._add_node("", 'process', size=0.01)
        self.graph.add_edge(true_end, join_id)
        self.graph.add_edge(false_end, join_id)
        
        return join_id

    def _process_loop(self, stmt, parent_id):
        loop_text = self._get_node_text(stmt)
        decision_id = self._add_node(loop_text, 'loop')
        self.graph.add_edge(parent_id, decision_id)
        
        # Cuerpo del ciclo
        body_start = self._add_node("Hacer", 'process', size=0.1)
        self.graph.add_edge(decision_id, body_start, label="Ciclo")
        
        body = self._get_safe_list(stmt, ['body', 'statements'])
        body_end = self._process_block(body, body_start)
        
        # Cierre del ciclo (retorno)
        self.graph.add_edge(body_end, decision_id)
        
        # Salida
        exit_id = self._add_node("Fin Ciclo", 'process', size=0.1)
        self.graph.add_edge(decision_id, exit_id, label="Salir")
        
        return exit_id

    def _add_node(self, label, type_key, size=None, shape='s'):
        node_id = self.counter
        self.graph.add_node(node_id)
        # Limpieza final extrema: quitar referencias de memoria
        label_str = str(label)
        if "object at" in label_str:
            try:
                label_str = label_str.split(" ")[0].split(".")[-1].replace("<", "").replace(">", "")
            except:
                label_str = "Obj"
        
        self.labels[node_id] = label_str
        self.node_colors[node_id] = self.colors.get(type_key, '#FFFFFF')
        self.counter += 1
        return node_id

    # --- ALGORITMO DE LAYOUT JERÁRQUICO (Árbol) ---

    def _hierarchy_pos(self, G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
        """
        Coloca los nodos en una estructura jerárquica (padre arriba, hijos abajo).
        Si hay ciclos, intenta convertir a árbol BFS primero.
        """
        if not nx.is_tree(G):
            try:
                # Convertir grafo cíclico en árbol de expansión para el layout
                roots = [n for n, d in G.in_degree() if d == 0]
                actual_root = roots[0] if roots else 0
                tree = nx.bfs_tree(G, actual_root)
                return self._hierarchy_pos(tree, actual_root, width, vert_gap, vert_loc, xcenter)
            except:
                # Fallback a Kamada Kawai si falla la conversión
                return nx.kamada_kawai_layout(G)

        pos = {root: (xcenter, vert_loc)}
        children = list(G.neighbors(root))
        if not children:
            return pos
            
        dx = width / len(children) 
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos.update(self._hierarchy_pos(G, root=child, width=dx, vert_gap=vert_gap, 
                                         vert_loc=vert_loc-vert_gap, xcenter=nextx))
        return pos

    def _draw_graph(self, title):
        # Lienzo alto para permitir crecimiento vertical
        fig = Figure(figsize=(10, 18)) 
        ax = fig.add_subplot(111)
        
        # Selección de Layout
        try:
            pos = nx.nx_agraph.graphviz_layout(self.graph, prog='dot')
        except:
            try:
                pos = self._hierarchy_pos(self.graph, root=0)
            except:
                pos = nx.kamada_kawai_layout(self.graph)
            
        # Dibujar Nodos
        nx.draw_networkx_nodes(
            self.graph, pos, 
            node_color=[self.node_colors[n] for n in self.graph.nodes()],
            node_size=2000,
            alpha=0.95,
            node_shape='s', # Cuadrados
            ax=ax
        )
        
        # Dibujar Bordes Curvos
        nx.draw_networkx_edges(
            self.graph, pos,
            edge_color='#455A64',
            arrows=True,
            arrowsize=15,
            connectionstyle='arc3,rad=0.1',
            ax=ax
        )
        
        # Dibujar Etiquetas de Nodos
        labels_formatted = {k: self._wrap_text(v) for k, v in self.labels.items()}
        nx.draw_networkx_labels(
            self.graph, pos,
            labels=labels_formatted,
            font_size=8,
            font_weight="bold",
            font_family="sans-serif",
            ax=ax
        )
        
        # Dibujar Etiquetas de Bordes (Si/No/Ciclo)
        edge_labels = nx.get_edge_attributes(self.graph, 'label')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=7, label_pos=0.7, ax=ax)
        
        ax.set_title(title, fontsize=14)
        ax.set_axis_off()
        fig.tight_layout()
        
        return fig
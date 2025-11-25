import matplotlib.pyplot as plt
import networkx as nx
import textwrap

class FlowchartGenerator:
    """
    Genera diagramas de flujo visuales a partir del AST.
    Versión: LAYOUT JERÁRQUICO (TIPO ÁRBOL) + Limpieza de texto.
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.pos = {}
        self.labels = {}
        self.node_colors = {}
        self.counter = 0
        self.levels = {} # Para guardar el nivel (Y) de cada nodo
        
        self.colors = {
            'start_end': '#81C784',  # Verde
            'process': '#64B5F6',    # Azul
            'decision': '#FFB74D',   # Naranja
            'io': '#4DD0E1',         # Cyan
            'loop': '#BA68C8'        # Morado
        }

    # ... (TUS MÉTODOS DE LIMPIEZA DE TEXTO SE MANTIENEN IGUAL, COPIAR DE ARRIBA) ...
    # Para ahorrar espacio aquí, asumo que usas el método _get_node_text robusto que ya tenías.
    # Si lo necesitas completo dímelo, pero es el mismo _get_node_text de la respuesta anterior.
    
    def _wrap_text(self, text, width=20):
        if not text or str(text).strip() == "": return ""
        return "\n".join(textwrap.wrap(str(text), width=width))

    def _get_safe_list(self, obj, attrs):
        for attr in attrs:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if isinstance(val, list): return val
        return []
    
    def _extract_value_from_object(self, node):
        for attr in ['value', 'name', 'id', 'op', 'operator']:
            if hasattr(node, attr):
                val = getattr(node, attr)
                if val is not None and val is not node: return val
        return None

    def _get_node_text(self, node):
        # ... (PEGA AQUÍ EL MÉTODO _get_node_text DE LA RESPUESTA ANTERIOR) ...
        # ... (Es vital para que el texto salga limpio) ...
        # Si no quieres copiar/pegar, avísame y te pongo el archivo entero otra vez.
        if node is None: return "?"
        if isinstance(node, (int, float, str, bool)): return str(node)
        cls_name = type(node).__name__
        
        if cls_name in ['Var', 'Variable', 'Name', 'Identifier']:
            val = getattr(node, 'name', getattr(node, 'id', getattr(node, 'value', None)))
            if val is not None and val is not node: return self._get_node_text(val)
            return str(val) if val is not None else "?"
            
        if cls_name in ['Number', 'Num', 'Int', 'Float']:
            return str(getattr(node, 'value', getattr(node, 'n', 0)))
            
        if hasattr(node, 'left') and hasattr(node, 'right'):
            left = self._get_node_text(node.left)
            right = self._get_node_text(node.right)
            op_obj = getattr(node, 'op', getattr(node, 'operator', '+'))
            op = op_obj if isinstance(op_obj, str) else self._get_node_text(op_obj)
            return f"{left} {op} {right}"

        if cls_name in ['Call', 'FunctionCall']:
            func = getattr(node, 'func_name', getattr(node, 'name', 'call'))
            func_name = self._get_node_text(func)
            args = self._get_safe_list(node, ['arguments', 'args'])
            args_str = ", ".join([self._get_node_text(arg) for arg in args])
            return f"{func_name}({args_str})"

        if cls_name in ['AssignStmt', 'Assign']:
            target = self._get_node_text(getattr(node, 'name', getattr(node, 'target', None)))
            val = self._get_node_text(getattr(node, 'value', getattr(node, 'expr', None)))
            return f"{target} ← {val}"

        if hasattr(node, 'condition'):
            cond = self._get_node_text(node.condition)
            return f"¿{cond}?" if "If" in cls_name else f"Mientras {cond}"

        if cls_name in ['ForStmt', 'For']:
            var = self._get_node_text(getattr(node, 'variable', getattr(node, 'var', None)))
            start = self._get_node_text(getattr(node, 'start', getattr(node, 'begin', '0')))
            end = self._get_node_text(getattr(node, 'end', getattr(node, 'limit', 'n')))
            return f"Para {var} = {start} hasta {end}"
            
        if cls_name in ['ReturnStmt', 'Return']:
            val = self._get_node_text(getattr(node, 'value', ''))
            return f"Retornar {val}"

        val = self._extract_value_from_object(node)
        if val is not None: return self._get_node_text(val)
        return f"[{cls_name}]"

    # --- GENERACIÓN CON LAYOUT JERÁRQUICO ---

    def generate_flowchart(self, ast, title="Diagrama de Flujo"):
        self.graph = nx.DiGraph()
        self.counter = 0
        self.labels = {}
        self.node_colors = {}
        
        # Limpiar contadores
        start_id = self._add_node("INICIO", 'start_end')
        last_id = start_id
        
        functions = self._get_safe_list(ast, ['functions', 'body'])
        if functions:
            func = functions[0]
            args = self._get_safe_list(func, ['arguments', 'args'])
            if args:
                args_txt = ", ".join([self._get_node_text(a) for a in args])
                io_id = self._add_node(f"Entrada: {args_txt}", 'io')
                self.graph.add_edge(last_id, io_id)
                last_id = io_id
            
            body = self._get_safe_list(func, ['body', 'statements'])
            last_id = self._process_block(body, last_id)
        elif isinstance(ast, list):
             last_id = self._process_block(ast, last_id)
            
        end_id = self._add_node("FIN", 'start_end')
        self.graph.add_edge(last_id, end_id)
        
        return self._draw_graph(title)

    # ... (MÉTODOS _process_block, _process_if, _process_loop IGUALES A LA RESPUESTA ANTERIOR) ...
    # Asegúrate de copiarlos aquí si estás reemplazando el archivo completo.
    # Por brevedad, asumo que los tienes, son los que crean la estructura lógica del grafo.
    
    def _process_block(self, statements, parent_id):
        current_id = parent_id
        if not statements: return current_id
        if not isinstance(statements, list): statements = [statements]
        for stmt in statements:
            cls_name = type(stmt).__name__
            if "If" in cls_name: current_id = self._process_if(stmt, current_id)
            elif "For" in cls_name or "While" in cls_name: current_id = self._process_loop(stmt, current_id)
            elif "Return" in cls_name:
                text = self._get_node_text(stmt)
                node_id = self._add_node(text, 'start_end')
                self.graph.add_edge(current_id, node_id)
                current_id = node_id
            else:
                text = self._get_node_text(stmt)
                node_id = self._add_node(text, 'process')
                self.graph.add_edge(current_id, node_id)
                current_id = node_id
        return current_id

    def _process_if(self, stmt, parent_id):
        cond_text = self._get_node_text(getattr(stmt, 'condition', getattr(stmt, 'test', None)))
        decision_id = self._add_node(cond_text, 'decision')
        self.graph.add_edge(parent_id, decision_id)
        true_node = self._add_node("V", 'process', size=0.1)
        self.graph.add_edge(decision_id, true_node)
        true_body = self._get_safe_list(stmt, ['true_body', 'body', 'then_body'])
        true_end = self._process_block(true_body, true_node)
        false_node = self._add_node("F", 'process', size=0.1)
        self.graph.add_edge(decision_id, false_node)
        false_body = self._get_safe_list(stmt, ['false_body', 'else_body', 'orelse'])
        false_end = self._process_block(false_body, false_node)
        join_id = self._add_node("", 'process', size=0.01)
        self.graph.add_edge(true_end, join_id)
        self.graph.add_edge(false_end, join_id)
        return join_id

    def _process_loop(self, stmt, parent_id):
        loop_text = self._get_node_text(stmt)
        decision_id = self._add_node(loop_text, 'loop')
        self.graph.add_edge(parent_id, decision_id)
        body_start = self._add_node("Hacer", 'process', size=0.1)
        self.graph.add_edge(decision_id, body_start, label="Ciclo")
        body = self._get_safe_list(stmt, ['body', 'statements'])
        body_end = self._process_block(body, body_start)
        self.graph.add_edge(body_end, decision_id) # Retorno
        exit_id = self._add_node("Fin Ciclo", 'process', size=0.1)
        self.graph.add_edge(decision_id, exit_id, label="Salir")
        return exit_id

    def _add_node(self, label, type_key, size=None, shape='s'):
        node_id = self.counter
        self.graph.add_node(node_id)
        # Limpieza final
        label_str = str(label)
        if "object at" in label_str:
            label_str = label_str.split(" ")[0].split(".")[-1].replace("<", "").replace(">", "")
        self.labels[node_id] = label_str
        self.node_colors[node_id] = self.colors.get(type_key, '#FFFFFF')
        self.counter += 1
        return node_id

    # --- AQUÍ ESTÁ LA MAGIA DEL ÁRBOL VERTICAL ---

    def _hierarchy_pos(self, G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
        """
        Si no tienes Graphviz, esto simula un layout de árbol.
        Coloca el nodo raíz arriba y sus sucesores abajo recursivamente.
        """
        if not nx.is_tree(G):
            # Si hay ciclos (bucles), convertimos a árbol temporalmente para el layout
            # usando una búsqueda en anchura (BFS) desde la raíz.
            # Esto rompe los ciclos visualmente pero mantiene la estructura vertical.
            try:
                # Encontrar raíz (nodo con grado de entrada 0, o el 0 si no hay)
                roots = [n for n, d in G.in_degree() if d == 0]
                actual_root = roots[0] if roots else 0
                tree = nx.bfs_tree(G, actual_root)
                return self._hierarchy_pos(tree, actual_root, width, vert_gap, vert_loc, xcenter)
            except:
                # Fallback si falla la conversión
                return nx.spring_layout(G)

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
        # Hacemos el lienzo MUY ALTO para permitir scroll vertical "virtual"
        # y que los nodos no se aplasten.
        fig = plt.figure(figsize=(10, 18)) 
        ax = fig.add_subplot(111)
        
        # Intentamos usar Graphviz (dot) que es el REY de los árboles
        try:
            pos = nx.nx_agraph.graphviz_layout(self.graph, prog='dot')
        except:
            # Si no hay graphviz, usamos nuestro layout jerárquico manual
            # Buscamos el nodo INICIO (id 0 normalmente)
            try:
                pos = self._hierarchy_pos(self.graph, root=0)
            except:
                 pos = nx.kamada_kawai_layout(self.graph) # Último recurso

        nx.draw_networkx_nodes(
            self.graph, pos, 
            node_color=[self.node_colors[n] for n in self.graph.nodes()],
            node_size=2000,
            alpha=0.95,
            node_shape='s', # Cuadrados
            ax=ax
        )
        
        # Bordes curvos para que las flechas de retorno (ciclos) se vean bien
        nx.draw_networkx_edges(
            self.graph, pos,
            edge_color='#455A64',
            arrows=True,
            arrowsize=15,
            connectionstyle='arc3,rad=0.1', # Curvatura suave
            ax=ax
        )
        
        labels_formatted = {k: self._wrap_text(v) for k, v in self.labels.items()}
        nx.draw_networkx_labels(
            self.graph, pos,
            labels=labels_formatted,
            font_size=8,
            font_weight="bold",
            font_family="sans-serif",
            ax=ax
        )
        
        edge_labels = nx.get_edge_attributes(self.graph, 'label')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=7, label_pos=0.7)
        
        plt.title(title, fontsize=14)
        plt.axis('off')
        plt.tight_layout()
        
        return fig
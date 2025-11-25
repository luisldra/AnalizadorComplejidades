import re

class TreeStructure:
    """
    Analiza una ecuación de recurrencia y genera la estructura lógica
    para dibujar un árbol simbólico profundo.
    """
    def __init__(self, equation_str=None):
        self.equation_str = str(equation_str) if equation_str else ""
        
        # Estructura por defecto
        self.structure = {
            "val": "n",
            "children": []
        }
        self.base_case = "T(1)"
        self.height_str = "?"
        self.recursive_terms = [] # Lista de términos recursivos hijos
        
        if self.equation_str:
            self.analyze_equation(self.equation_str)

    def analyze_equation(self, equation_str):
        """Procesa la ecuación y construye el árbol."""
        self.equation_str = str(equation_str)
        if not self.equation_str: return
        
        self._parse_equation_terms()
        self._calculate_height()
        self._build_deep_tree_topology()

    def _parse_equation_terms(self):
        """Extrae los términos recursivos de la ecuación (RHS)."""
        s = self.equation_str.strip()
        
        # 1. Extraer el Lado Derecho (RHS) de forma segura
        # Si viene como Eq(T(n), ...), quitamos el envoltorio
        if s.startswith("Eq("):
            s = s[3:-1] # Quitar Eq( y el último )
        
        # Separar por la coma principal: "T(n), 2*T(n/2) + n"
        parts = s.split(",")
        if len(parts) >= 2:
            rhs = parts[1].strip()
        else:
            rhs = s # Fallback por si no es un objeto Eq
            
        # 2. Limpieza de espacios para facilitar Regex
        rhs_clean = rhs.replace(" ", "")
        
        # 3. Regex para encontrar llamadas a T(...)
        # Busca: (coeficiente opcional *) T ( contenido )
        # Ejemplos que captura: "2*T(n/2)", "T(n-1)", "T(n-2)"
        matches = re.findall(r'(?:(\d+)\*)?T\(([^)]+)\)', rhs_clean)
        
        self.recursive_terms = []
        for coef, arg in matches:
            count = int(coef) if coef else 1
            # Si es 2*T(n/2), agregamos "n/2" dos veces a la lista
            for _ in range(count):
                self.recursive_terms.append(arg)

    def _calculate_height(self):
        """Calcula la altura aproximada basada en los términos."""
        if not self.recursive_terms:
            self.height_str = "0"
            return

        # Tomamos el primer término para estimar (asumiendo homogeneidad principal)
        term = self.recursive_terms[0]
        
        if "/2" in term: 
            self.height_str = "log_2(n)"
        elif "/" in term:
            # Extraer divisor n/3 -> log_3(n)
            match = re.search(r'/(\d+)', term)
            base = match.group(1) if match else "b"
            self.height_str = f"log_{base}(n)"
        elif "-1" in term and "-2" in term: # Fibonacci específico
             self.height_str = "n"
        elif "-1" in term: 
            self.height_str = "n"
        elif "-" in term:
             self.height_str = "n/k"
        else:
            self.height_str = "log(n)"

    def _apply_transformation(self, current_val, rule):
        """
        Calcula el valor de un nodo hijo aplicando la regla al padre.
        Ej: Padre="n/2", Regla="n/2" -> Hijo="n/4"
        Ej: Padre="n-1", Regla="n-2" -> Hijo="n-3"
        """
        try:
            # Lógica para División (Merge Sort, Binary Search)
            if "/" in rule:
                # Extraer divisor de la regla (ej: 2 de n/2)
                div_match = re.search(r'/(\d+)', rule)
                divisor = int(div_match.group(1)) if div_match else 2
                
                # Analizar el padre
                if current_val == "n":
                    return f"n/{divisor}"
                elif "/2" in current_val and divisor == 2:
                    return "n/4"
                elif "/4" in current_val and divisor == 2:
                    return "n/8"
                elif "/" in current_val:
                    # Fallback genérico: n/x -> n/(x*div)
                    prev_div_match = re.search(r'/(\d+)', current_val)
                    prev_div = int(prev_div_match.group(1)) if prev_div_match else 1
                    return f"n/{prev_div * divisor}"
                
            # Lógica para Resta (Fibonacci, Factorial)
            elif "-" in rule:
                # Extraer sustraendo de la regla (ej: 1 de n-1)
                sub_match = re.search(r'-(\d+)', rule)
                subtrahend = int(sub_match.group(1)) if sub_match else 0
                
                if current_val == "n":
                    return rule # n-1 o n-2
                elif "-" in current_val:
                    # Padre es "n-1", Regla es "n-2" -> Resultado "n-(1+2)" -> "n-3"
                    prev_sub_match = re.search(r'-(\d+)', current_val)
                    prev_sub = int(prev_sub_match.group(1)) if prev_sub_match else 0
                    total_sub = prev_sub + subtrahend
                    return f"n-{total_sub}"
            
            return rule # Si no sabemos transformar, devolvemos la regla tal cual
            
        except:
            return "?"

    def _build_deep_tree_topology(self):
        """Construye la topología del árbol hasta los nietos (Nivel 2)."""
        
        # Nivel 0: Raíz
        self.structure = {
            "val": "n",
            "children": []
        }
        
        if not self.recursive_terms:
            return

        # Nivel 1: Hijos directos
        # Para Fibonacci: recursive_terms = ["n-1", "n-2"]
        for term in self.recursive_terms:
            child_node = {
                "val": term, 
                "children": []
            }
            
            # Nivel 2: Nietos (Aplicar las mismas reglas a este hijo)
            # Esto mostrará la asimetría. 
            # Si es Fibonacci: Al hijo (n-1) le aplicamos (n-1) y (n-2) -> nietos: (n-2), (n-3)
            for sub_rule in self.recursive_terms:
                grandchild_val = self._apply_transformation(term, sub_rule)
                child_node["children"].append({
                    "val": grandchild_val,
                    "children": [] # Paramos aquí para no saturar
                })
            
            self.structure["children"].append(child_node)

    def get_structure(self):
        """Interfaz para la GUI."""
        # Fallback si no se detectó nada
        if not self.structure["children"]:
             return {
                "tree_topology": {"val": "n", "children": []},
                "height": "0",
                "base_case": "T(1)"
            }

        return {
            "tree_topology": self.structure,
            "height": self.height_str,
            "base_case": self.base_case
        }
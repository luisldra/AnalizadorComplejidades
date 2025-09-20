# 📊 Analizador de Complejidades

Proyecto académico para **Análisis y Diseño de Algoritmos**.  
Implementa un **parser de pseudocódigo** con generación de AST (Árbol de Sintaxis Abstracta) y cálculo de **complejidad temporal**.

---

## 🚀 Tecnologías
- Python 3.10+
- [Lark](https://github.com/lark-parser/lark) (parser)
- Pytest (pruebas unitarias)

---

## 📂 Estructura del proyecto
AnalizadorComplejidades/
├── src/
│ ├── ast/ # Definiciones de nodos del AST
│ ├── parser/ # Gramática y transformador
│ └── ...
├── tests/ # Pruebas unitarias con pytest
├── README.md
└── .gitignore

---

## ⚡ Ejecución de pruebas
Para correr los tests:
```bash
pytest -s
Ejemplo de salida:

tests/test_complexity_suma.py Complejidad: O(n)
.
tests/test_parser.py <src.ast.nodes.Program object at 0x...>
.
```
---

## 📌 Ejemplos de pseudocódigo soportado
Asignación
function identidad(n)
begin
    x 🡨 n
    return x
end
Bucle for
function suma(n)
begin
    s 🡨 0
    for i 🡨 1 to n do
    begin
        s 🡨 s + i
    end
    return s
end
Condicional if-else
function maximo(a, b)
begin
    if (a > b) then
    begin
        return a
    end
    else
    begin
        return b
    end
end
---
##👨‍💻 Autores
Luis Rodríguez – Proyecto académico para la materia Análisis y Diseño de Algoritmos.
Yonier

---




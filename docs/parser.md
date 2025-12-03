# Parser y AST

## Archivos
- `src/parser/grammar.lark`: gramatica Lark del pseudocodigo (funciones, asignaciones, arrays/matrices, if/while/for/repeat, llamados con `call`, return).
- `src/parser/parser.py`: carga la gramatica y expone `parse_code(code)`.
- `src/parser/transformer.py`: convierte el arbol de Lark en nodos Python.
- `src/ast/nodes.py`: definicion de nodos AST (Program, Function, Assignment, For, While, If, Repeat, Return, Call, BinOp, Var, Number, Array/MatrixAccess, etc.).

## Flujo
1) `parse_code` llama a Lark (Earley) con `grammar.lark`.
2) El `ASTTransformer` recibe el arbol y construye instancias de `nodes.py`.
3) El AST resultante se pasa a los analizadores.

## Relevancia
El parser es la entrada formal al sistema; garantiza que el pseudocodigo tenga una estructura consistente para el analisis matematico y heuristico.

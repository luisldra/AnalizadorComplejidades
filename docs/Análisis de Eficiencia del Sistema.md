Análisis de Eficiencia del Sistema

Este apartado describe la complejidad algorítmica interna del analizador de complejidades, sus funciones de coste aproximadas, así como los límites prácticos en cuanto al tamaño y tipo de entrada que puede procesar.

Parámetro de Tamaño de Entrada

A diferencia de un algoritmo clásico que trabaja sobre un arreglo de tamaño n, el tamaño de entrada de nuestro analizador se mide en función del pseudocódigo que recibe:

* L: número de líneas de pseudocódigo.
* T: número de tokens (palabras clave, identificadores, símbolos).
* N: número de nodos del AST (árbol de sintaxis abstracta) que se construye a partir del seudocódigo.

En la práctica, N es aproximadamente proporcional a T y a L, por lo que podemos considerar:

n = N = número de nodos del AST

Como veremos en las secciones siguientes, el tiempo de ejecución del analizador crece de forma aproximadamente lineal con N.

Pipeline General y Funciones de Coste

El recorrido completo de una entrada típica pasa por las siguientes etapas:

1. Parsing léxico/sintáctico ? parseCode + nodes
1. Análisis de recursividad y modelo de recurrencia ? recurrenceSolver, dpAnalyzer
1. Construcción simbólica del árbol de recurrencia ? recurrenceTreeBuilder
1. Análisis matemático y asintótico ? mathAnalyzer, asymptoticAnalyzer
1. Análisis de casos (mejor, peor, promedio) ? caseAnalyzer
1. Análisis avanzado y resumen final ? advancedComplexity, AnalysisResult

A continuación, se detalla la complejidad aproximada de cada etapa.

Parsing y construcción del AST (parseCode + nodes)

Esta fase realiza:

* Análisis léxico.
* Análisis sintáctico usando la gramática LARK.
* Construcción del AST con nodos como Function, For, While, If, Call, etc.

Cada token/línea del seudocódigo se procesa una vez, por lo que el coste es proporcional al número de nodos del árbol.

* Función de coste: $T\_{parse}(N) = a \cdot N$
* Complejidad: $T\_{parse}(N) \in \Theta(N)$

8\.2.2. Análisis recursivo y deducción de recurrencias (recurrenceSolver, dpAnalyzer)

En esta fase se:

* Recorre el AST buscando llamadas recursivas a la misma función.
* Se analiza cómo cambia el parámetro de tamaño en cada llamada ($n-1$, $n/2$, $n-1$ y $n-2$, etc.).
* Se estima el trabajo no recursivo de cada nivel.

Este análisis consiste en uno o varios recorridos adicionales sobre el AST, sin bucles anidados que crezcan con N.

* Función de coste: $T\_{recurrence}(N) = b \cdot N$
* Complejidad: $T\_{recurrence}(N) \in \Theta(N)$

Construcción del árbol de recurrencia (recurrenceTreeBuilder)

Aquí se construye una representación simbólica de la recurrencia:

* Niveles de recursión (por ejemplo, $\log\_2(n)$ niveles para $T(n)=2T(n/2)+n$).
* Trabajo por nivel.

Importante: no se genera un árbol real con n nodos, sino una estructura pequeña dependiente del patrón de la ecuación, no del valor concreto de n.

* Función de coste (en función de niveles simbólicos k): $T\_{tree}(k) = c \cdot k$, con k muy pequeño.
* Complejidad práctica: $T\_{tree} \in O(1)$ respecto a N (constante para los patrones soportados).

Análisis matemático y asintótico (mathAnalyzer, asymptoticAnalyzer)

En esta fase se:

* Generan expresiones simbólicas de coste y ecuaciones de recurrencia utilizando SymPy.
* Se aplican reglas cerradas (Teorema Maestro, sustitución, análisis de bucles) para obtener la complejidad en notación $O$, $\Omega$, $\Theta$.

Hay dos componentes:

1. Generación de la ecuación: lineal en el número de nodos o términos de coste.
1. Resolución simbólica: coste casi constante mientras se trate de las recurrencias estándar soportadas ($T(n)=T(n-1)+c$, $T(n)=aT(n/b)+f(n)$, etc.).
* Función de coste: $T\_{math}(N) = d \cdot N + K$ (donde K refleja el coste simbólico de SymPy).
* Complejidad: $T\_{math}(N) \in \Theta(N)$

Análisis de casos: mejor, peor y promedio (caseAnalyzer)

caseAnalyzer recorre nuevamente el AST y utiliza la información anterior para:

* Detectar el tipo de algoritmo: recursive, fibonacci, binary\_search, divide\_conquer, nested\_loops, linear\_search, etc.
* Generar descripciones del mejor caso, peor caso y caso promedio, ajustadas al tipo de algoritmo y a la recurrencia encontrada.

El núcleo del análisis es otro recorrido del AST más consultas sobre tablas de reglas.

* Función de coste: $T\_{case}(N) = e \cdot N$
* Complejidad: $T\_{case}(N) \in \Theta(N)$

Análisis avanzado y resumen final (advancedComplexity, AnalysisResult)

En esta fase se integran:

* Datos matemáticos ($O$, $\Omega$, $\Theta$, ecuaciones de recurrencia).
* Escenarios de casos (mejor, peor, promedio).
* Árbol de recurrencia y observaciones adicionales.

El coste depende principalmente del tamaño del informe generado (texto), que crece linealmente con la cantidad de información a presentar. En la práctica, para algoritmos típicos el coste es muy bajo:

* Función de coste aproximada: $T\_{advanced}(N) \approx f \cdot N$ con f pequeño.
* Complejidad: $T\_{advanced}(N) \in \Theta(N)$

Complejidad global del analizador

Sumando todas las fases dependientes de N:

$$\begin{aligned} T\_{total}(N) &= T\_{parse}(N) + T\_{recurrence}(N) + T\_{math}(N) + T\_{case}(N) + T\_{advanced}(N) + overhead\_{UI} \\ \text{Sustituyendo las funciones lineales:} \\ T\_{total}(N) &= (a + b + d + e + f) \cdot N + K \end{aligned}$$

Por tanto:

Complejidad global del analizador:

$$T\_{total}(N) \in \Theta(N)$$

Es decir, el tiempo de análisis crece de forma lineal con el tamaño del seudocódigo (número de nodos del AST).

La constante oculta en $\Theta(N)$ es relativamente alta debido al uso de SymPy y a la generación de informes detallados, pero la escala sigue siendo lineal.

Límites Prácticos del Sistema

Más allá de la notación asintótica, el analizador presenta ciertos límites prácticos, tanto por la gramática y modelos soportados como por el tamaño máximo razonable de entrada.

Límites por tipo de algoritmos

El analizador funciona especialmente bien cuando:

* El algoritmo puede describirse con un único parámetro de tamaño principal ($n$).
* Las llamadas recursivas siguen patrones estándar:
- $n - k$ (ej. $n - 1$)
- $n / b$
- $n - 1$ y $n - 2$ (patrón Fibonacci).
* Los bucles tienen límites claros y lineales/cuadráticos en $n$:
- for i = 1 to n
- for i = 1 to n - 1
- for i = 1 to n do for j = 1 to n do ...
* No se usan estructuras dinámicas extremadamente complejas ni construcciones fuera de la gramática definida.

El sistema empieza a perder precisión o a volverse genérico cuando:

* Existen dos o más parámetros de tamaño independientes ($m, n$) y la recurrencia natural sería $T(m, n)$.
* Los límites de los bucles dependen de condiciones muy complejas o de datos cuya distribución no se modela explícitamente.
* La recurrencia deducida no encaja en ninguno de los modelos implementados en recurrenceModels.
* SymPy recibe expresiones simbólicas demasiado complejas, lo que puede generar tiempos de cómputo altos o errores de expansión/series.

Resumen de limitación importante:

El analizador asume que los algoritmos pueden modelarse con un único parámetro de tamaño $n$ y con patrones de recurrencia estándar. Algoritmos con múltiples parámetros, estructuras fuertemente dinámicas o recursiones no estructuradas pueden no ser analizados con precisión.

Límites por tamaño de entrada y rendimiento

Se midieron tiempos para varios algoritmos de prueba:

Plaintext

Tiempos de análisis inicial:

- factorial.txt:          289.49 ms
- fibonacci.txt:          412.16 ms
- merge\_sort.txt:          88.62 ms
- busqueda\_binaria.txt:    45.86 ms
- algoritmo\_cubico.txt:    82.67 ms
- bubble\_sort.txt:         73.31 ms
- quick\_sort.txt:          27.98 ms
- suma\_iterativa.txt:      28.48 ms
- es\_primo.txt:           164.66 ms
- torres\_hanoi.txt:        94.68 ms

\------------------------------------------------

Total:                 1314.64 ms  (? 1.3 s)

Observaciones:

* Para algoritmos pequeños/medianos (decenas de líneas), el tiempo se mantiene en el rango de 30–100 ms.
* Para algoritmos recursivos más complejos (Fibonacci, factorial, Torres de Hanoi), el coste aumenta hasta los 300–400 ms, principalmente por:
- Generación y manipulación simbólica de recurrencias.
- Construcción y formateo del informe.
* Si se duplica el tamaño del pseudocódigo (más líneas pero mismo patrón de algoritmo), se espera que el tiempo de análisis aproximadamente se duplique, consistente con la complejidad lineal $\Theta(N)$.

En la práctica, el límite razonable está dado por:

1. El tiempo de respuesta aceptable para el usuario (p.ej. 1–3 segundos).
1. La capacidad de SymPy para manejar expresiones simbólicas sin explotar en tiempo o memoria.

#!/usr/bin/env python3
"""
GUÍA DE USO DEL SISTEMA PRINCIPAL
==================================

Esta guía explica cómo usar el sistema completo de análisis de complejidades.
"""

print("""
🎓 ANALIZADOR DE COMPLEJIDADES - GUÍA DE USO
============================================

## PASO 1: Ejecutar el programa principal
   python src/main.py

## PASO 2: Cargar pseudocódigo
   - Ingrese la ruta a un archivo .txt con pseudocódigo
   - O presione Enter para usar examples/factorial.txt

## PASO 3: Seleccionar tipo de análisis
   1. 🔍 Análisis básico de complejidad
   2. 🧠 Análisis con Dynamic Programming  
   3. 🔄 Análisis de algoritmos recursivos
   4. 🌳 Análisis con árboles de recurrencia
   5. 📊 Todos los análisis
   6. 📋 Reporte completo integrado

## ARCHIVOS DE EJEMPLO DISPONIBLES:
   - examples/factorial.txt      → Recursión lineal O(n)
   - examples/fibonacci.txt      → Recursión exponencial O(2^n)
   - examples/suma_iterativa.txt → Iterativo lineal O(n)
   - examples/merge_sort.txt     → Divide y vencerás O(n log n)
   - examples/busqueda_binaria.txt → Búsqueda binaria O(log n)
   - examples/algoritmo_cubico.txt → Triple bucle O(n³)

## FUNCIONALIDADES PRINCIPALES:
✅ Parser completo de pseudocódigo
✅ Análisis de complejidad O, Ω, Θ
✅ Detección automática de recursión
✅ Árboles de recurrencia con visualización
✅ Dynamic Programming con cache
✅ Estadísticas de rendimiento
✅ Arquitectura SOLID modular

## SINTAXIS DEL PSEUDOCÓDIGO:
   function nombre(params)
   begin
       if condicion
       begin
           // statements
       end
       else
       begin
           // statements  
       end
       
       for i = 1 to n do
           // statements
       end
       
       return call funcion(args)
   end

¡Pruebe diferentes algoritmos y explore todas las capacidades!
""")
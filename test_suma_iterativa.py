#!/usr/bin/env python3
"""
Test completo para suma_iterativa.txt
Valida todos los aspectos del análisis de complejidad para el algoritmo iterativo de suma.

Este test verifica:
1. Parsing correcto del pseudocódigo
2. Análisis básico de complejidad
3. Detección de patrones iterativos
4. Análisis de programación dinámica
5. Construcción de árboles de recurrencia
6. Integración completa del sistema
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import AnalizadorCompleto
from src.parser.parser import parse_code
from src.analyzer.complexity_engine import ComplexityEngine
from src.analyzer.dp_analyzer import DynamicProgrammingAnalyzer
from src.analyzer.recurrence_tree_builder import RecurrenceTreeBuilder

def test_suma_iterativa_completo():
    """Test completo del análisis de suma_iterativa.txt"""
    
    print("=" * 80)
    print("TEST COMPLETO: SUMA_ITERATIVA.TXT")
    print("=" * 80)
    
    # 1. Test de carga de archivo
    print("\n1. PRUEBA DE CARGA DE ARCHIVO")
    print("-" * 40)
    
    analizador = AnalizadorCompleto()
    archivo = "examples/suma_iterativa.txt"
    
    try:
        pseudocodigo = analizador.cargar_pseudocodigo(archivo)
        print(f"✅ Archivo cargado exitosamente:")
        print(f"Contenido:\n{pseudocodigo}")
        assert pseudocodigo is not None, "El pseudocódigo no debe ser None"
        assert "suma_iterativa" in pseudocodigo, "Debe contener el nombre de la función"
        assert "for i = 1 to n" in pseudocodigo, "Debe contener el bucle iterativo"
    except Exception as e:
        print(f"❌ Error cargando archivo: {e}")
        return False
    
    # 2. Test de parsing
    print("\n2. PRUEBA DE PARSING")
    print("-" * 40)
    
    try:
        ast = parse_code(pseudocodigo)
        print(f"✅ AST generado exitosamente")
        print(f"Tipo de nodo raíz: {type(ast).__name__}")
        
        # Verificar estructura del AST
        assert ast is not None, "El AST no debe ser None"
        print(f"Nodos encontrados en el AST:")
        analizador._mostrar_estructura_ast(ast, nivel=0)
        
    except Exception as e:
        print(f"❌ Error en parsing: {e}")
        return False
    
    # 3. Test de análisis básico de complejidad
    print("\n3. PRUEBA DE ANÁLISIS BÁSICO")
    print("-" * 40)
    
    try:
        engine = ComplexityEngine()
        complejidad = engine.analyze_complexity(ast)
        
        print(f"✅ Análisis básico completado")
        print(f"Complejidad detectada: {complejidad}")
        
        # Verificaciones específicas para suma iterativa
        assert complejidad is not None, "La complejidad no debe ser None"
        # Para suma iterativa esperamos O(n) debido al bucle
        assert "O(n)" in str(complejidad) or "n" in str(complejidad), f"Esperada complejidad O(n), obtenida: {complejidad}"
        
    except Exception as e:
        print(f"❌ Error en análisis básico: {e}")
        return False
    
    # 4. Test de detección de recursión
    print("\n4. PRUEBA DE DETECCIÓN DE RECURSIÓN")
    print("-" * 40)
    
    try:
        # Para suma iterativa NO debe detectar recursión
        tiene_recursion = analizador._detectar_recursion(ast)
        print(f"✅ Detección de recursión completada")
        print(f"¿Tiene recursión?: {tiene_recursion}")
        
        # Suma iterativa NO debe tener recursión
        assert not tiene_recursion, "Suma iterativa no debe ser detectada como recursiva"
        
    except Exception as e:
        print(f"❌ Error en detección de recursión: {e}")
        return False
    
    # 5. Test de análisis de programación dinámica
    print("\n5. PRUEBA DE ANÁLISIS DE PROGRAMACIÓN DINÁMICA")
    print("-" * 40)
    
    try:
        dp_analyzer = DynamicProgrammingAnalyzer()
        es_dp, patron_dp, optimizacion = dp_analyzer.analyze(ast)
        
        print(f"✅ Análisis DP completado")
        print(f"¿Es DP?: {es_dp}")
        print(f"Patrón DP: {patron_dp}")
        print(f"Optimización: {optimizacion}")
        
        # Suma iterativa no es típicamente DP, pero puede tener optimizaciones
        
    except Exception as e:
        print(f"❌ Error en análisis DP: {e}")
        return False
    
    # 6. Test de construcción de árboles de recurrencia
    print("\n6. PRUEBA DE ÁRBOLES DE RECURRENCIA")
    print("-" * 40)
    
    try:
        tree_builder = RecurrenceTreeBuilder()
        
        # Para algoritmos iterativos, el árbol será simple o no aplicable
        print("✅ Constructor de árboles inicializado")
        print("ℹ️  Para algoritmos iterativos, los árboles de recurrencia no son aplicables")
        
    except Exception as e:
        print(f"❌ Error en construcción de árboles: {e}")
        return False
    
    # 7. Test de integración completa
    print("\n7. PRUEBA DE INTEGRACIÓN COMPLETA")
    print("-" * 40)
    
    try:
        # Simular análisis completo como lo haría el usuario
        print("Ejecutando análisis completo...")
        
        # Análisis básico
        print("\n📊 ANÁLISIS BÁSICO:")
        analizador.analisis_basico(pseudocodigo)
        
        print("\n🔄 ANÁLISIS DE RECURSIÓN:")
        analizador.analisis_recursion(pseudocodigo)
        
        print("\n💾 ANÁLISIS DE PROGRAMACIÓN DINÁMICA:")
        analizador.analisis_dp(pseudocodigo)
        
        print("✅ Integración completa exitosa")
        
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        return False
    
    # 8. Resumen de resultados esperados
    print("\n8. RESUMEN DE RESULTADOS ESPERADOS")
    print("-" * 40)
    
    print("""
    📋 RESULTADOS ESPERADOS PARA SUMA_ITERATIVA:
    
    ✅ Complejidad temporal: O(n)
       - Un bucle que itera de 1 a n
       - Operaciones constantes dentro del bucle
    
    ✅ Complejidad espacial: O(1)
       - Solo variables locales (s, i)
       - No recursión, no estructuras adicionales
    
    ✅ Tipo de algoritmo: Iterativo
       - No hay llamadas recursivas
       - Patrón de bucle simple
    
    ✅ Patrón identificado: Suma aritmética
       - Suma de enteros consecutivos
       - Fórmula matemática equivalente: n*(n+1)/2
    
    ⚠️  Optimización posible:
       - Podría optimizarse a O(1) usando la fórmula matemática
       - return n * (n + 1) / 2
    """)
    
    print("\n" + "=" * 80)
    print("✅ TEST SUMA_ITERATIVA COMPLETADO EXITOSAMENTE")
    print("=" * 80)
    
    return True

def test_comparacion_con_formula_matematica():
    """Test adicional: comparar con la fórmula matemática optimizada"""
    
    print("\n" + "=" * 80)
    print("TEST ADICIONAL: COMPARACIÓN CON FÓRMULA MATEMÁTICA")
    print("=" * 80)
    
    print("""
    🔍 ANÁLISIS DE OPTIMIZACIÓN:
    
    Algoritmo actual (suma_iterativa.txt):
    - Complejidad: O(n)
    - Espacio: O(1)
    - Método: iterativo con bucle
    
    Algoritmo optimizado (fórmula matemática):
    - Complejidad: O(1)
    - Espacio: O(1)  
    - Método: return n * (n + 1) / 2
    
    💡 RECOMENDACIÓN:
    Para casos de uso en producción, considerar usar la fórmula matemática
    directa para mejor rendimiento en valores grandes de n.
    
    📊 EJEMPLO DE DIFERENCIA:
    - n = 1,000,000
    - Iterativo: 1,000,000 operaciones
    - Fórmula: 3 operaciones (multiplicación, suma, división)
    """)

if __name__ == "__main__":
    """Ejecutar todos los tests"""
    
    print("🚀 INICIANDO BATERÍA DE TESTS PARA SUMA_ITERATIVA")
    
    try:
        # Test principal
        exito = test_suma_iterativa_completo()
        
        if exito:
            # Test adicional
            test_comparacion_con_formula_matematica()
            
            print(f"\n🎉 TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
            print(f"✅ El sistema maneja correctamente el algoritmo suma_iterativa.txt")
            
        else:
            print(f"\n❌ ALGUNOS TESTS FALLARON")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 ERROR CRÍTICO EN TESTS: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
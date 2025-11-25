#!/usr/bin/env python3
"""
ANALIZADOR DE COMPLEJIDADES DE ALGORITMOS
==========================================

Sistema completo para análisis de complejidad computacional de algoritmos
implementados en pseudocódigo. Incluye:

- ✅ Análisis básico de complejidad (O, Ω, Θ)
- ✅ Técnicas de Dynamic Programming
- ✅ Árboles de recurrencia para algoritmos recursivos
- ✅ Visualización de patrones de recurrencia
- ✅ Cache inteligente con memoización
- ✅ Arquitectura SOLID refactorizada

Desarrollado por: Universidad - Análisis y Diseño de Algoritmos
Proyecto 2025-2
"""

import sys
import os
from typing import Optional, Dict, Any
from pathlib import Path

# Add the root directory to the path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code
from src.analyzer.advanced_complexity import AdvancedComplexityAnalyzer
from src.analyzer.dp_analyzer import DynamicProgrammingAnalyzer
from src.analyzer.recurrence_solver import RecursiveAlgorithmAnalyzer
from src.analyzer.recurrence_tree_builder import RecurrenceTreeBuilder
from src.analyzer.recurrence_visualizer import RecurrenceTreeVisualizer
from src.analyzer.asymptotic_analyzer import AsymptoticAnalyzer


class AnalizadorCompleto:
    """
    Clase principal que integra todos los sistemas de análisis.
    """
    
    def __init__(self):
        """Inicializa todos los analizadores."""
        print("🚀 Inicializando Analizador de Complejidades...")
        
        # Analizadores principales
        self.basic_analyzer = AdvancedComplexityAnalyzer()
        self.dp_analyzer = DynamicProgrammingAnalyzer()
        self.recursive_analyzer = RecursiveAlgorithmAnalyzer()
        self.tree_builder = RecurrenceTreeBuilder()
        self.tree_visualizer = RecurrenceTreeVisualizer()
        self.asymptotic_analyzer = AsymptoticAnalyzer()
        
        print("✅ Todos los sistemas cargados correctamente")
    
    def cargar_pseudocodigo(self, archivo_path: str) -> Optional[str]:
        """
        Carga pseudocódigo desde un archivo .txt
        
        Args:
            archivo_path: Ruta al archivo .txt
            
        Returns:
            Contenido del archivo o None si hay error
        """
        try:
            with open(archivo_path, 'r', encoding='utf-8') as file:
                contenido = file.read().strip()
                
            if not contenido:
                print(f"⚠️  El archivo {archivo_path} está vacío")
                return None
                
            print(f"✅ Pseudocódigo cargado desde: {archivo_path}")
            return contenido
            
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo {archivo_path}")
            return None
        except Exception as e:
            print(f"❌ Error leyendo archivo: {e}")
            return None
    
    def mostrar_pseudocodigo(self, codigo: str):
        """Muestra el pseudocódigo de forma formateada."""
        print("\n" + "="*60)
        print("📝 PSEUDOCÓDIGO A ANALIZAR")
        print("="*60)
        print(codigo)
        print("="*60)
    
    def analisis_basico(self, ast) -> Dict[str, Any]:
        """Realiza análisis asintótico formal de complejidad."""
        print("\n🔍 ANÁLISIS DE COMPLEJIDAD")
        print("-" * 50)
        
        try:
            # Primero detectar si hay recursión
            recursive_info = None
            if hasattr(ast, 'functions') and ast.functions:
                for func in ast.functions:
                    rec_analysis = self.recursive_analyzer.analyze_recursive_algorithm(func)
                    if rec_analysis['has_recursion']:
                        recursive_info = rec_analysis
                        break
            
            # Realizar análisis asintótico formal
            recurrence, bound = self.asymptotic_analyzer.analyze(ast, recursive_info)
            
            print(f"Ecuación: {recurrence.equation}")
            if recurrence.base_cases:
                base_str = ", ".join([f"{k} = {v}" for k, v in recurrence.base_cases.items()])
                print(f"Casos base: {base_str}")
            print(f"\nComplejidad: {bound.notation}({bound.complexity})")
            
            return {
                'tipo': 'formal',
                'ecuacion': recurrence.equation,
                'complejidad': f"{bound.notation}({bound.complexity})",
                'metodo': recurrence.method_used,
                'explicacion': bound.explanation
            }
            
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def analisis_con_dp(self, ast) -> Dict[str, Any]:
        """Realiza análisis con técnicas de Dynamic Programming."""
        print("\n🧠 ANÁLISIS CON DYNAMIC PROGRAMMING")
        print("-" * 50)
        
        try:
            resultado = self.dp_analyzer.analyze_with_dp(ast)
            stats = self.dp_analyzer.get_dp_statistics()
            
            print(f"📊 Resultados con DP:")
            print(f"   • Big O optimizado:      {resultado.big_o}")
            print(f"   • Omega optimizado:      {resultado.omega}")
            print(f"   • Theta optimizado:      {resultado.theta}")
            descripcion = getattr(resultado, 'description', 'Análisis con Dynamic Programming')
            print(f"   • Descripción: {descripcion}")
            
            print(f"\n🧠 Estadísticas de Cache DP:")
            print(f"   • Cache hits:   {stats['cache_hits']}")
            print(f"   • Cache misses: {stats['cache_misses']}")
            print(f"   • Hit rate:     {stats['hit_rate_percentage']}%")
            
            return {
                'tipo': 'dp',
                'big_o': resultado.big_o,
                'omega': resultado.omega,
                'theta': resultado.theta,
                'descripcion': descripcion,
                'cache_stats': stats
            }
            
        except Exception as e:
            print(f"❌ Error en análisis DP: {e}")
            return {}
    
    def analisis_recursion(self, ast) -> Dict[str, Any]:
        """Analiza algoritmos recursivos."""
        print("\n🔄 ANÁLISIS DE RECURSIÓN")
        print("-" * 50)
        
        try:
            # Buscar funciones recursivas
            funciones_recursivas = []
            
            if hasattr(ast, 'functions'):
                for func in ast.functions:
                    resultado = self.recursive_analyzer.analyze_recursive_algorithm(func)
                    if resultado['has_recursion']:
                        funciones_recursivas.append((func, resultado))
            
            if not funciones_recursivas:
                print("ℹ️  No se detectaron algoritmos recursivos")
                return {'tipo': 'recursion', 'recursivo': False}
            
            print(f"✅ Se encontraron {len(funciones_recursivas)} función(es) recursiva(s)")
            
            resultados = []
            for func, analisis in funciones_recursivas:
                print(f"\n📍 Función: {analisis['function_name']}")
                print(f"   • Llamadas recursivas: {len(analisis['recursive_calls'])}")
                print(f"   • Patrón detectado: {analisis['pattern_type']}")
                print(f"   • Relación: {analisis['recurrence_relation']}")
                print(f"   • Complejidad estimada: {analisis['estimated_complexity']}")
                print(f"   • Trabajo por llamada: {analisis['work_per_call']}")
                
                resultados.append(analisis)
            
            return {
                'tipo': 'recursion',
                'recursivo': True,
                'funciones': resultados
            }
            
        except Exception as e:
            print(f"❌ Error en análisis de recursión: {e}")
            return {}
    
    def analisis_arboles_recurrencia(self, ast) -> Dict[str, Any]:
        """Genera y visualiza árboles de recurrencia."""
        print("\n🌳 ANÁLISIS CON ÁRBOLES DE RECURRENCIA")
        print("-" * 50)
        
        try:
            resultado, arbol = self.dp_analyzer.analyze_with_recurrence_tree(ast)
            
            if arbol is None:
                print("ℹ️  No se pudo generar árbol de recurrencia - algoritmo no recursivo")
                return {'tipo': 'arbol', 'tiene_arbol': False}
            
            print("✅ Árbol de recurrencia generado exitosamente")
            print(f"\n📊 Complejidad calculada: {resultado.big_o}")
            
            # Mostrar visualización del árbol
            print(f"\n🌳 Visualización del Árbol:")
            print(self.tree_visualizer.visualize(arbol))
            
            # Mostrar análisis por niveles
            print(f"\n📊 Análisis por Niveles:")
            print(arbol.get_level_summary())
            
            return {
                'tipo': 'arbol',
                'tiene_arbol': True,
                'complejidad': resultado.big_o,
                'niveles': arbol.levels if hasattr(arbol, 'levels') else 4
            }
            
        except Exception as e:
            print(f"❌ Error en análisis de árboles: {e}")
            return {}
    
    def reporte_completo(self, ast) -> str:
        """Genera un reporte completo combinando todos los análisis."""
        print("\n📋 GENERANDO REPORTE COMPLETO")
        print("-" * 50)
        
        try:
            reporte = self.dp_analyzer.generate_recurrence_report(ast)
            return reporte
        except Exception as e:
            print(f"❌ Error generando reporte completo: {e}")
            return f"Error: {e}"
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de opciones."""
        print("\n" + "="*60)
        print("🎯 MENÚ PRINCIPAL - ANALIZADOR DE COMPLEJIDADES")
        print("="*60)
        print("1. 🔍 Análisis de complejidad (notación asintótica formal)")
        print("2. 🧠 Análisis con Dynamic Programming")
        print("3. 🔄 Análisis de algoritmos recursivos")
        print("4. 🌳 Análisis con árboles de recurrencia") 
        print("5. 📊 Análisis completo (complejidad + árbol)")
        print("6. 📋 Reporte completo integrado")
        print("7. 📝 Cargar nuevo archivo")
        print("8. ❌ Salir")
        print("-" * 60)
    
    def ejecutar_opcion(self, opcion: str, ast) -> bool:
        """
        Ejecuta la opción seleccionada por el usuario.
        
        Returns:
            True si debe continuar, False si debe salir
        """
        
        if opcion == '1':
            self.analisis_basico(ast)
        elif opcion == '2':
            self.analisis_con_dp(ast)
        elif opcion == '3':
            self.analisis_recursion(ast)
        elif opcion == '4':
            self.analisis_arboles_recurrencia(ast)
        elif opcion == '5':
            print("\n🚀 ANÁLISIS COMPLETO")
            print("="*60)
            self.analisis_basico(ast)
            self.analisis_arboles_recurrencia(ast)
        elif opcion == '6':
            print("\n📋 REPORTE COMPLETO INTEGRADO")
            print("="*60)
            reporte = self.reporte_completo(ast)
            print(reporte)
        elif opcion == '7':
            return 'reload'  # Señal especial para recargar archivo
        elif opcion == '8':
            print("\n👋 ¡Gracias por usar el Analizador de Complejidades!")
            return False
        else:
            print("❌ Opción no válida. Por favor seleccione una opción del 1-8.")
        
        return True


def main():
    """Función principal del programa."""
    print("🎓 ANALIZADOR DE COMPLEJIDADES DE ALGORITMOS")
    print("=" * 60)
    print("Universidad de Caldas- Análisis y Diseño de Algoritmos")
    print("Proyecto ADA 2025-2")
    print("=" * 60)
    
    # Inicializar el analizador
    analizador = AnalizadorCompleto()
    
    while True:
        # Solicitar archivo de entrada
        print(f"\n📁 Ingrese la ruta del archivo .txt con el pseudocódigo:")
        print(f"   (o presione Enter para usar 'examples/factorial.txt')")
        
        archivo_path = input("📁 Archivo: ").strip()
        
        # Usar archivo por defecto si no se especifica
        if not archivo_path:
            archivo_path = "examples/factorial.txt"
        
        # Cargar pseudocódigo
        codigo = analizador.cargar_pseudocodigo(archivo_path)
        if codigo is None:
            continuar = input("\n¿Desea intentar con otro archivo? (s/n): ").lower()
            if continuar != 's':
                break
            continue
        
        # Mostrar pseudocódigo
        analizador.mostrar_pseudocodigo(codigo)
        
        # Parsear código
        try:
            print("\n🔄 Parseando pseudocódigo...")
            ast = parse_code(codigo)
            print("✅ Pseudocódigo parseado correctamente")
        except Exception as e:
            print(f"❌ Error parseando pseudocódigo: {e}")
            print("⚠️  Verifique que el pseudocódigo tenga la sintaxis correcta")
            continue
        
        # Bucle principal del menú
        while True:
            analizador.mostrar_menu_principal()
            opcion = input("🎯 Seleccione una opción (1-8): ").strip()
            
            resultado = analizador.ejecutar_opcion(opcion, ast)
            
            if resultado == 'reload':
                break  # Salir del bucle de menú para cargar nuevo archivo
            elif resultado == False:
                return  # Salir completamente del programa
            
            # Pausa para que el usuario pueda leer los resultados
            input("\n⏸️  Presione Enter para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Programa interrumpido por el usuario!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("📧 Por favor reporte este error al equipo de desarrollo")

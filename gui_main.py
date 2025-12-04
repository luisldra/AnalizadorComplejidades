#!/usr/bin/env python3
"""
GUI Launcher
============

Punto de entrada principal para la interfaz gráfica del
Analizador de Complejidades.

Uso:
    python gui_main.py

O directamente desde línea de comandos si tiene permisos de ejecución:
    ./gui_main.py
"""

import sys
import os

# Add the root directory to the path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

# Verificar dependencias
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    print("❌ Error: Tkinter no está instalado.")
    print("Tkinter viene preinstalado con Python en Windows y macOS.")
    print("En Linux, instale con: sudo apt-get install python3-tk")
    sys.exit(1)

try:
    import matplotlib
    matplotlib.use('TkAgg')  # Backend para Tkinter
except ImportError:
    print("❌ Error: matplotlib no está instalado.")
    print("Instale con: pip install matplotlib")
    sys.exit(1)

try:
    from src.gui.main_window import MainWindow
except ImportError as e:
    print(f"❌ Error al importar módulos de la GUI: {e}")
    print("Asegúrese de que todos los archivos estén en su lugar.")
    import traceback
    traceback.print_exc()
    sys.exit(1)


def check_dependencies():
    """Verifica que todas las dependencias estén instaladas."""
    missing = []
    
    dependencies = {
        'lark': 'lark-parser',
        'sympy': 'sympy',
        'networkx': 'networkx',
        'matplotlib': 'matplotlib',
        'PIL': 'pillow'
    }
    
    for module, package in dependencies.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("⚠️  Advertencia: Faltan las siguientes dependencias:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nInstale con: pip install " + " ".join(missing))
        
        response = input("\n¿Desea continuar de todas formas? (s/n): ")
        if response.lower() != 's':
            sys.exit(1)
    
    return True

def main():
    """Función principal que lanza la GUI."""
    
    print("=" * 60)
    print("ANALIZADOR DE COMPLEJIDADES DE ALGORITMOS")
    print("   Interfaz Gráfica de Usuario (GUI)")
    print("=" * 60)
    print("Universidad de Caldas")
    print("Análisis y Diseño de Algoritmos - Proyecto 2025-2")
    print("=" * 60)
    print()
    
    # Verificar dependencias
    print("Verificando dependencias...")
    if not check_dependencies():
        return
    
    print("Todas las dependencias están instaladas")
    print()
    print("Iniciando interfaz gráfica...")
    print()
    
    try:
        # Crear ventana principal
        root = tk.Tk()
        
        # Configuración de la ventana
        root.title("Analizador de Complejidades - LDRA UCaldas")
        root.state('zoomed')  # Maximizar ventana (Windows)
        
        # Crear aplicación
        app = MainWindow(root)
        
        print("Interfaz gráfica iniciada correctamente")
        print("   1. Haga clic en los archivos para ver los reportes")
        print("   2. O escriba directamente en el editor")
        print("   3. Puede analizar un codigo diferente con IA, presionando el boton 'Analizar con IA'")
        print()
        
        # Iniciar loop de eventos
        root.mainloop()
        
        print("\n Aplicación cerrada correctamente")
        
    except Exception as e:
        print(f"\n Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        
        # Mostrar error en ventana si es posible
        try:
            messagebox.showerror("Error Fatal", 
                               f"Error al iniciar la aplicación:\n\n{str(e)}\n\n"
                               f"Consulte la consola para más detalles.")
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Aplicación interrumpida por el usuario")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

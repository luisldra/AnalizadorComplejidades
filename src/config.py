import os
from dotenv import load_dotenv

load_dotenv()


# Ruta base donde están tus txt
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")
print(os.getenv("GEMINI_API_KEY"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_algorithm_files():
    
    # Lista de archivos a procesar
    ALGORITHMS = [
        os.path.join(BASE_DIR, "factorial.txt"),
        os.path.join(BASE_DIR, "fibonacci.txt"),
        os.path.join(BASE_DIR, "merge_sort.txt"),
        os.path.join(BASE_DIR, "busqueda_binaria.txt"),
        os.path.join(BASE_DIR, "algoritmo_cubico.txt"), 
        os.path.join(BASE_DIR, "bubble_sort.txt"),
        os.path.join(BASE_DIR, "quick_sort.txt"),
        os.path.join(BASE_DIR, "suma_iterativa.txt"),
        # os.path.join(BASE_DIR, "es_primo.txt"),
        # os.path.join(BASE_DIR, "torres_hanoi.txt"),
        os.path.join(BASE_DIR, "mochila.txt"),
        os.path.join(BASE_DIR, "lcs.txt"),
    ]
    
    return ALGORITHMS
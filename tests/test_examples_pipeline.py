import os
from pathlib import Path

import pytest

from src.logic.analysis_orchestrator import AnalysisOrchestrator


EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


@pytest.mark.parametrize(
    "filename,expected_fragment",
    [
        ("busqueda_binaria.txt", "Θ(log n)"),
        ("merge_sort.txt", "Θ(n log n)"),
        ("quick_sort.txt", "Θ(n log n)"),
        ("torres_hanoi.txt", "Θ(2^n)"),
        ("fibonacci.txt", "Θ(2^n)"),
        ("factorial.txt", "Θ(n)"),
        ("bubble_sort.txt", "Θ(n^2)"),
    ],
)
def test_examples_heuristic_complexity(filename: str, expected_fragment: str):
    """Verifica que los ejemplos clave se analicen sin error y con la cota esperada."""
    orch = AnalysisOrchestrator()
    file_path = EXAMPLES_DIR / filename
    assert file_path.exists(), f"Falta el ejemplo {filename}"

    result = orch.process_file(str(file_path))
    assert not result.error, f"Error al analizar {filename}: {result.error}"
    assert expected_fragment in result.heur_complexity, (
        f"{filename} deberia contener {expected_fragment}, obtuvo {result.heur_complexity}"
    )


def test_examples_no_errors():
    """Todos los archivos en examples/ deben analizarse sin errores."""
    orch = AnalysisOrchestrator()
    for file_path in sorted(EXAMPLES_DIR.glob("*.txt")):
        result = orch.process_file(str(file_path))
        assert not result.error, f"Error en {file_path.name}: {result.error}"
        assert result.heur_equation, f"Sin ecuacion heuristica para {file_path.name}"
        assert result.heur_complexity.startswith("Θ"), f"Complejidad no normalizada en {file_path.name}"


def test_stress_nested_loops_depth_four():
    """Estresa el analizador con 4 bucles anidados (esperamos n^4)."""
    code = """
    function stress_loops(n)
    begin
        s = 0
        for i = 1 to n do
        begin
            for j = 1 to n do
            begin
                for k = 1 to n do
                begin
                    for t = 1 to n do
                    begin
                        s = s + 1
                    end
                end
            end
        end
        return s
    end
    """
    orch = AnalysisOrchestrator()
    result = orch.process_code(code, name_hint="stress_loops")
    assert not result.error, f"Error en stress_loops: {result.error}"
    assert "n^4" in result.heur_complexity, f"Esperado n^4, obtuvo {result.heur_complexity}"
    assert "cn^4" in result.heur_equation, f"Ecuacion inesperada: {result.heur_equation}"

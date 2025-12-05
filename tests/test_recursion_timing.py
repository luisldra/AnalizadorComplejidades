from src.logic.analysis_orchestrator import AnalysisOrchestrator


def _make_padded_code(body_lines: int, name: str, recursive_body: str) -> str:
    """
    Construye pseudocódigo con la cantidad de líneas deseada.
    Se rellena con asignaciones triviales para alcanzar el tamaño mínimo.
    """
    header = [
        f"function {name}(n)",
        "begin",
        "    x = 0",
        "    if n <= 0",
        "    begin",
        "        return 0",
        "    end",
    ]
    footer = [
        "    return x",
        "end",
    ]
    core = [line for line in recursive_body.splitlines() if line.strip()]
    # Rellenar con líneas triviales hasta alcanzar el mínimo
    total_current = len(header) + len(core) + len(footer)
    filler_needed = max(0, body_lines - total_current)
    filler = [f"    x = x + {i}" for i in range(1, filler_needed + 1)]
    code_lines = header + core + filler + footer
    assert len(code_lines) >= body_lines, "No se alcanzó el número de líneas requerido"
    return "\n".join(code_lines)


def _analyze(code: str, hint: str):
    orch = AnalysisOrchestrator()
    return orch.process_code(code, name_hint=hint)


def test_recursion_depth_linear_20_lines():
    """Recursión lineal con al menos 20 líneas y medición de tiempo."""
    recursive_body = """
    x = x + 1
    call rec20(n - 1)
    """
    code = _make_padded_code(20, "rec20", recursive_body)
    result = _analyze(code, "rec20")
    assert not result.error
    assert "Θ" in result.heur_complexity
    assert result.elapsed_ms >= 0
    assert "T(n-1)" in result.heur_equation


def test_recursion_binary_30_lines():
    """Recursión binaria (tipo Fibonacci) con al menos 30 líneas y medición de tiempo."""
    recursive_body = """
    x = x + 1
    call rec30(n - 1)
    call rec30(n - 2)
    """
    code = _make_padded_code(30, "rec30", recursive_body)
    result = _analyze(code, "rec30")
    assert not result.error
    assert "Θ" in result.heur_complexity
    assert result.elapsed_ms >= 0
    assert "T(n-2)" in result.heur_equation


def test_recursion_divide_conquer_40_lines():
    """Divide y vencerás con al menos 40 líneas y medición de tiempo."""
    recursive_body = """
    mid = n / 2
    call rec40(mid)
    call rec40(mid)
    x = x + mid
    """
    code = _make_padded_code(40, "rec40", recursive_body)
    result = _analyze(code, "rec40")
    assert not result.error
    assert "Θ" in result.heur_complexity
    assert result.elapsed_ms >= 0
    assert "T(n/2)" in result.heur_equation

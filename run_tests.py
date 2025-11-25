# run_tests.py
import pytest
import sys

# Add project root to path to allow imports
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

if __name__ == "__main__":
    # Exit with the result of pytest.main
    sys.exit(pytest.main(["-v", "tests/test_math_analyzer.py"]))

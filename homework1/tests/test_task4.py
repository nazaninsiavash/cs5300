import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task4 import calculate_discount

def test_with_integers():
    result = calculate_discount(100, 20)
    assert result == 80.0

def test_with_floats():
    result = calculate_discount(50.0, 10.0)
    assert result == 45.0

def test_mixed_types():
    result = calculate_discount(100, 25.0)
    assert result == 75.0

def test_no_discount():
    result = calculate_discount(100, 0)
    assert result == 100.0

def test_full_discount():
    result = calculate_discount(50, 100)
    assert result == 0.0

def test_negative_price():
    with pytest.raises(ValueError):
        calculate_discount(-10, 20)

def test_invalid_discount():
    with pytest.raises(ValueError):
        calculate_discount(100, 150)

def test_non_numeric():
    with pytest.raises(TypeError):
        calculate_discount("abc", 20)

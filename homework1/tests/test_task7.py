import sys
from pathlib import Path
import pytest
import numpy as np
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task7 import calculate_statistics, matrix_operations, normalize_array

def test_calculate_statistics():
    data = [1, 2, 3, 4, 5]
    result = calculate_statistics(data)
    
    assert result is not None
    assert result['mean'] == 3.0
    assert result['median'] == 3.0
    assert result['min'] == 1
    assert result['max'] == 5
    assert pytest.approx(result['std'], 0.01) == 1.414

def test_calculate_statistics_with_invalid_data():
    result = calculate_statistics([])
    assert result is None

def test_matrix_operations():
    matrix_a = [[1, 2], [3, 4]]
    matrix_b = [[5, 6], [7, 8]]
    result = matrix_operations(matrix_a, matrix_b)
    
    expected = [[19, 22], [43, 50]]
    assert result == expected

def test_matrix_operations_invalid_dimensions():
    matrix_a = [[1, 2], [3, 4]]
    matrix_b = [[5, 6, 7]]
    
    with pytest.raises(Exception) as excinfo:
        matrix_operations(matrix_a, matrix_b)
    assert "Matrix multiplication failed" in str(excinfo.value)

def test_normalize_array():
    data = [0, 5, 10]
    result = normalize_array(data)
    
    assert result[0] == 0.0
    assert result[1] == 0.5
    assert result[2] == 1.0

def test_normalize_array_same_values():
    data = [5, 5, 5]
    result = normalize_array(data)
    
    assert all(x == 0.0 for x in result)

def test_numpy_imported():
    # Verify numpy is available
    import numpy
    assert numpy is not None
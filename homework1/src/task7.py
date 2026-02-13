"""
Task 7: Using the numpy package
Demonstrating how to use an external package - numpy for numerical operations
"""
import numpy as np

def calculate_statistics(data):
    """Calculate basic statistics for a dataset"""
    try:
        arr = np.array(data)
        stats = {
            'mean': np.mean(arr),
            'median': np.median(arr),
            'std': np.std(arr),
            'min': np.min(arr),
            'max': np.max(arr)
        }
        return stats
    except:
        return None

def matrix_operations(matrix_a, matrix_b):
    """Perform matrix multiplication"""
    try:
        a = np.array(matrix_a)
        b = np.array(matrix_b)
        result = np.dot(a, b)
        return result.tolist()
    except:
        raise Exception("Matrix multiplication failed - check dimensions")

def normalize_array(data):
    """Normalize an array to range [0, 1]"""
    arr = np.array(data)
    min_val = np.min(arr)
    max_val = np.max(arr)
    if max_val == min_val:
        return np.zeros_like(arr).tolist()
    normalized = (arr - min_val) / (max_val - min_val)
    return normalized.tolist()

if __name__ == "__main__":
    print("Testing numpy package...")
    
    # Test statistics
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    stats = calculate_statistics(data)
    if stats:
        print(f"\nStatistics for {data}:")
        print(f"Mean: {stats['mean']:.2f}")
        print(f"Median: {stats['median']:.2f}")
        print(f"Std Dev: {stats['std']:.2f}")
        print(f"Min: {stats['min']}, Max: {stats['max']}")
    
    # Test matrix multiplication
    matrix_a = [[1, 2], [3, 4]]
    matrix_b = [[5, 6], [7, 8]]
    result = matrix_operations(matrix_a, matrix_b)
    print(f"\nMatrix multiplication result:")
    print(result)
    
    # Test normalization
    data = [10, 20, 30, 40, 50]
    normalized = normalize_array(data)
    print(f"\nNormalized {data}:")
    print([f"{x:.2f}" for x in normalized])
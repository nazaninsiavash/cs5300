import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task3 import number_checker, check_if_prime, get_first_primes, sum_to_n

def test_positive_number():
    assert number_checker(10) == "positive"
    
def test_negative_number():
    assert number_checker(-5) == "negative"
    
def test_zero():
    assert number_checker(0) == "zero"

def test_prime_numbers():
    assert check_if_prime(2) == True
    assert check_if_prime(7) == True
    assert check_if_prime(4) == False
    assert check_if_prime(1) == False

def test_ten_primes():
    primes = get_first_primes(10)
    assert primes == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_sum_function():
    assert sum_to_n(100) == 5050
    assert sum_to_n(10) == 55
    assert sum_to_n(1) == 1

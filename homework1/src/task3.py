"""
Task 3: Working with if statements, loops, etc
- Check if numbers are positive/negative/zero
- Find first 10 prime numbers
- Add up numbers from 1 to 100
"""

def number_checker(num):
    """Checks whether a number is positive, negative, or zero"""
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    else:
        return "zero"

def check_if_prime(number):
    """Figured out if a number is prime or not"""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    
    # Only check odd numbers up to sqrt
    # I believe this is way faster than checking every number
    for i in range(3, int(number**0.5) + 1, 2):
        if number % i == 0:
            return False
    return True

def get_first_primes(count):
    """Gets the first 'count' prime numbers using a for loop"""
    primes = []
    num = 2
    
    for _ in range(count):
        while not check_if_prime(num):
            num += 1
        primes.append(num)
        num += 1
    
    return primes

def sum_to_n(n):
    """Adds all numbers from 1 to n using while loop"""
    total = 0
    current = 1
    while current <= n:
        total += current
        current += 1
    return total

if __name__ == "__main__":
    # Testing the if statement
    print(f"5 is {number_checker(5)}") #should get positive
    print(f"-3 is {number_checker(-3)}") #should get negative
    print(f"0 is {number_checker(0)}") #should get zero
    
    # Testing for loop with primes
    print(f"\nFirst 10 primes: {get_first_primes(10)}")
    
    # Testing while loop
    print(f"\nSum from 1 to 100: {sum_to_n(100)}")

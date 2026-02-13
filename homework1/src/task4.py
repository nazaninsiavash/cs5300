"""
Task 4: Duck typing example with a discount calculator
The function accepts different number types , if it acts like a number, we'll use it!
"""

def calculate_discount(price, discount):
    """
    Calculate final price after discount
    Works with integers, floats, whatever acts like a number
    
    price: original price
    discount: discount percent (0-100)
    """
    # Duck typing - just try to use them as numbers
    # If it quacks like a duck...
    try:
        price = float(price) #whatever
        discount = float(discount) #something
    except:
        raise TypeError("Need numeric values for price and discount!!")
    
    # Quick validation
    if price < 0:
        raise ValueError("Price can't be negative!!")
    if discount < 0 or discount > 100:
        raise ValueError("Discount should be between 0 and 100!!")
    
    # Calculate it
    final = price - (price * discount / 100)
    return final

if __name__ == "__main__":
    # Try with different types
    print(f"Int example: ${calculate_discount(100, 20)}")
    print(f"Float example: ${calculate_discount(50.99, 15.5)}")
    print(f"Mixed: ${calculate_discount(75, 10.0)}")

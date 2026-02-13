"""
Task 2: Playing around with different data types
Testing out integers, floats, strings, and booleans
"""

# Different examples of data types I'm using
my_age = 25  # integer
pi_value = 3.14  # float  
my_string = "Adv Software is a core course"  # string
is_student = True  # boolean

def show_integer():
    return my_age

def show_float():
    return pi_value

def show_string():
    return my_string

def show_boolean():
    return is_student

def display_all_types():
    """Just showing all the types"""
    print(f"Integer example: {my_age}")
    print(f"Float example: {pi_value}")
    print(f"String example: {my_string}")
    print(f"Boolean example: {is_student}")

if __name__ == "__main__":
    display_all_types()

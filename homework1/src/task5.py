"""
Task 5: Lists and dictionaries practice
Using lists for book collection and dict for student records
"""

# My book list : title and author

books = [
    ("Atomic Habits", "James Clear"),
    ("The 7 Habits of Highly Effective People", "Stephen R. Covey"),
    ("Mindset", "Carol S. Dweck"),
    ("Deep Work", "Cal Newport"),
    ("Write It Down, Make It Happen", "Henriette Klauser"),
]

# Student records
students = {
    "Naz Siavash": "STU001",
    "Sarah Marion": "STU002",
    "Mike Williams": "STU003",
    "Emma Davis": "STU004",
}

def get_books():
    return books

def first_three():
    """Using slice to get first 3 books"""
    return books[:3]

def get_students():
    return students

def find_student(name):
    """Look up student by name"""
    return students.get(name)

if __name__ == "__main__":
    print("All books:")
    for title, author in books:
        print(f"  {title} by {author}")
    
    print("\nFirst 3 books:")
    for title, author in first_three():
        print(f"  {title} by {author}")
    
    print("\nStudent database:")
    for name, id in students.items():
        print(f"  {name}: {id}")

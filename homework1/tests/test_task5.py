import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task5 import get_books, first_three, get_students, find_student

def test_books_list():
    books = get_books()
    assert len(books) > 0
    assert type(books) == list

def test_first_three_slice():
    three_books = first_three()
    assert len(three_books) == 3

def test_students_dict():
    students = get_students()
    assert type(students) == dict
    assert len(students) > 0

def test_find_existing_student():
    result = find_student("Naz Siavash")
    assert result == "STU001"

def test_find_missing_student():
    result = find_student("Nobody")
    assert result == None

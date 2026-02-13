import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task2 import show_integer, show_float, show_string, show_boolean

def test_integer():
    result = show_integer()
    assert type(result) == int
    
def test_float():
    result = show_float()
    assert type(result) == float
    
def test_string():
    result = show_string()
    assert type(result) == str
    
def test_boolean():
    result = show_boolean()
    assert type(result) == bool

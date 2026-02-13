import sys
from pathlib import Path
import tempfile
import os
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task6 import count_words

def test_word_counting():
    # Create my temp file with known word count
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("hello naz test")
        temp_file = f.name
    
    count = count_words(temp_file)
    os.remove(temp_file)
    assert count == 3

def test_empty_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        temp_file = f.name
    
    count = count_words(temp_file)
    os.remove(temp_file)
    assert count == 0

def test_actual_readme():
    # Test the actual file
    readme_path = Path(__file__).parent.parent / "task6_read_me.txt"
    if readme_path.exists():
        count = count_words(str(readme_path))
        assert count == 104  # actual count from the lorem ipsum text

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task1 import print_greeting

def test_greeting_output(capsys):
    """Make sure hello world prints correctly"""
    print_greeting()
    output = capsys.readouterr()
    assert output.out == "Hello, World!\n"

"""
Task 6: Reading files and counting words
"""
import os

def count_words(filename):
    """Read file and count how many words it has"""
    try:
        with open(filename, 'r') as f:
            text = f.read()
            words = text.split()
            return len(words)
    except FileNotFoundError:
        print(f"Can't find file: {filename}")
        return 0

if __name__ == "__main__":
    # Get path to the text file
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, "task6_read_me.txt")
    
    word_count = count_words(file_path)
    print(f"Total words in file: {word_count}")

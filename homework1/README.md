# Homework 1 - Python Basics


## What's in here

```
homework1/
├── src/           # All the task files
├── tests/         # Test files
└── task6_read_me.txt  # Sample text file
```

## Setup

First, making a virtual environment:
```bash
python3 -m venv hw1 --system-site-packages
source hw1/bin/activate
```

Install what you need:
```bash
cd ~/cs5300/homework1
pip install -r requirements.txt
```

## Running stuff

Run individual tasks:
```bash
python3 src/task1.py
python3 src/task2.py
# etc...
```

Run all tests:
```bash
pytest
```

Run specific test:
```bash
pytest tests/test_task1.py -v
```

## The Tasks

**Task 1** - Basic hello world with test  
**Task 2** - Playing with different data types  
**Task 3** - If statements, for loops, while loops. Made prime number finder and sum calculator  
**Task 4** - Duck typing with a discount calculator  
**Task 5** - Lists (book collection) and dicts (student database)  
**Task 6** - Reading files and counting words  
**Task 7** - Using library numpy

All tests should pass. If something doesn't work, make sure you're in the right directory and have activated the virtual environment.

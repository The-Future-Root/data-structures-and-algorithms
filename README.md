# Data Structures and Algorithms

How to store data so it's quick to work with, and how to write code that stays fast as the data grows. You'll build the classic data structures yourself in Python, see how each one is laid out, and learn to judge how fast code is before you even run it.

This is the material behind technical job interviews, but it's not only for interviews. It's the difference between a search that takes a millisecond and one that takes a minute, and between a program that handles ten users and one that handles ten million.

## Who this is for

You're comfortable with Python, including functions, lists, dictionaries and classes. If you need a refresher, see [Python Basics](https://github.com/The-Future-Root/python-basics) and [Python OOP](https://github.com/The-Future-Root/python-oop).

## What you need

- **Python 3.10 or newer**, from [python.org](https://www.python.org/downloads/). Check with `python3 --version` (on Windows, `python --version`).
- **A text editor**, such as VS Code.

## Lessons

| # | Lesson | You'll learn | Real-world use in the exercise |
|---|---|---|---|
| 1 | [Big O](./01-big-o/) | Measuring how code slows down as data grows | Finding duplicate orders quickly |
| 2 | [Arrays and lists](./02-arrays-and-lists/) | How Python lists work, and what's fast or slow | Running sales totals and rotas |
| 3 | [Linked lists](./03-linked-lists/) | Chains of nodes, and when they beat lists | A music playlist |
| 4 | [Stacks and queues](./04-stacks-and-queues/) | Last in first out, first in first out | Undo history and a support queue |
| 5 | [Hash tables](./05-hash-tables/) | How dictionaries find things instantly | Building your own dictionary |
| 6 | [Searching](./06-searching/) | Linear search and binary search | Searching a log by timestamp |
| 7 | [Sorting](./07-sorting/) | Bubble, insertion and merge sort | Ranking products |
| 8 | [Trees](./08-trees/) | Binary search trees | A fast product index |
| 9 | [Graphs](./09-graphs/) | Networks, breadth-first and depth-first search | Finding routes on a metro map |

## How the exercises work

Each lesson folder has `exercise.py`, where you write your code, and `test_exercise.py`, which checks it. Run the tests from the lesson's folder:

```bash
cd 01-big-o
python3 -m unittest -v
```

Some tests also check **speed**: they give your code a large input and fail if it takes too long. That's deliberate. In this subject, an answer that's correct but slow isn't finished.

Hints are at the end of each lesson, and full solutions are in [solutions/](./solutions/).

## About the diagrams

Each lesson draws its data structure so you can see its shape. The colours keep the same meaning throughout: **blue** for the structure itself, **green** for the item you're looking for or the result, **amber** for the part currently being worked on, and **red** for "empty", "missing" or "too slow".

## License

The code in this repository is released under the [MIT License](./LICENSE). The lesson text and diagrams are released under [Creative Commons Attribution 4.0](./LICENSE-CONTENT) (CC BY 4.0): you may share and adapt them, including for your own teaching, as long as you credit The Future Root.

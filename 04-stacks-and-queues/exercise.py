# Lesson 4: stacks and queues
#
# Use a Python list as a stack, and collections.deque as a queue.
# Test with:  python3 -m unittest -v

from collections import deque

PAIRS = {")": "(", "]": "[", "}": "{"}


class UndoHistory:
    """The undo and redo history of a text editor, using two stacks."""

    def __init__(self):
        """Start with nothing to undo or redo."""
        pass

    def do(self, action):
        """Record a new action. Doing something new clears the redo history."""
        pass

    def undo(self):
        """Undo the most recent action and return it, or return None if there's nothing to undo."""
        pass

    def redo(self):
        """Redo the most recently undone action and return it, or return None if there's nothing to redo."""
        pass


def is_balanced(text):
    """Return True if every bracket in text is closed in the right order. Other characters are ignored."""
    pass


class SupportQueue:
    """Support tickets, served first come first served, with urgent tickets ahead of normal ones."""

    def __init__(self):
        """Start with no tickets waiting."""
        pass

    def add(self, ticket, urgent=False):
        """Add a ticket to the back of its queue, in O(1)."""
        pass

    def next_ticket(self):
        """Remove and return the next ticket to work on, in O(1), or return None if there are none."""
        pass

    def peek(self):
        """Return the next ticket without removing it, or None."""
        pass

    def __len__(self):
        """Return how many tickets are waiting."""
        pass


if __name__ == "__main__":
    history = UndoHistory()
    history.do("type 'Dear Sam'")
    history.do("make bold")
    print(history.undo())
    print(history.redo())

    print(is_balanced("total = prices[0] * (1 + rate)"))
    print(is_balanced("print(items[0)]"))

    queue = SupportQueue()
    queue.add("T-101 password reset")
    queue.add("T-102 invoice question")
    queue.add("T-103 site is down", urgent=True)
    print(queue.next_ticket())
    print(queue.next_ticket())
    print(len(queue))

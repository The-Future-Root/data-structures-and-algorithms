# Solution to lesson 4: stacks and queues

from collections import deque

PAIRS = {")": "(", "]": "[", "}": "{"}


class UndoHistory:
    """The undo and redo history of a text editor, using two stacks."""

    def __init__(self):
        """Start with nothing to undo or redo."""
        self._done = []
        self._undone = []

    def do(self, action):
        """Record a new action. Doing something new clears the redo history."""
        self._done.append(action)
        self._undone.clear()

    def undo(self):
        """Undo the most recent action and return it, or return None if there's nothing to undo."""
        if not self._done:
            return None
        action = self._done.pop()
        self._undone.append(action)
        return action

    def redo(self):
        """Redo the most recently undone action and return it, or return None if there's nothing to redo."""
        if not self._undone:
            return None
        action = self._undone.pop()
        self._done.append(action)
        return action


def is_balanced(text):
    """Return True if every bracket in text is closed in the right order. Other characters are ignored."""
    stack = []
    for character in text:
        if character in "([{":
            stack.append(character)
        elif character in PAIRS:
            if not stack or stack.pop() != PAIRS[character]:
                return False
    return not stack


class SupportQueue:
    """Support tickets, served first come first served, with urgent tickets ahead of normal ones."""

    def __init__(self):
        """Start with no tickets waiting."""
        self._urgent = deque()
        self._normal = deque()

    def add(self, ticket, urgent=False):
        """Add a ticket to the back of its queue, in O(1)."""
        if urgent:
            self._urgent.append(ticket)
        else:
            self._normal.append(ticket)

    def next_ticket(self):
        """Remove and return the next ticket to work on, in O(1), or return None if there are none."""
        if self._urgent:
            return self._urgent.popleft()
        if self._normal:
            return self._normal.popleft()
        return None

    def peek(self):
        """Return the next ticket without removing it, or None."""
        if self._urgent:
            return self._urgent[0]
        if self._normal:
            return self._normal[0]
        return None

    def __len__(self):
        """Return how many tickets are waiting."""
        return len(self._urgent) + len(self._normal)


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

import time
import unittest

from exercise import SupportQueue, UndoHistory, is_balanced

BIG = 200_000


class TestUndoHistory(unittest.TestCase):
    def test_undo_most_recent_first(self):
        history = UndoHistory()
        history.do("type 'Dear Sam'")
        history.do("make bold")
        history.do("delete line")
        self.assertEqual(history.undo(), "delete line")
        self.assertEqual(history.undo(), "make bold")
        self.assertEqual(history.undo(), "type 'Dear Sam'")
        self.assertIsNone(history.undo(), "With nothing left to undo, return None")

    def test_redo(self):
        history = UndoHistory()
        history.do("a")
        history.do("b")
        history.undo()
        history.undo()
        self.assertEqual(history.redo(), "a")
        self.assertEqual(history.redo(), "b")
        self.assertIsNone(history.redo())
        self.assertEqual(history.undo(), "b", "A redone action can be undone again")

    def test_new_action_clears_redo(self):
        history = UndoHistory()
        history.do("a")
        history.do("b")
        history.undo()
        history.do("c")
        self.assertIsNone(history.redo(), "Doing something new should clear the redo history")
        self.assertEqual(history.undo(), "c")
        self.assertEqual(history.undo(), "a")

    def test_empty(self):
        history = UndoHistory()
        self.assertIsNone(history.undo())
        self.assertIsNone(history.redo())


class TestIsBalanced(unittest.TestCase):
    def test_balanced(self):
        self.assertTrue(is_balanced("total = prices[0] * (1 + rate)"))
        self.assertTrue(is_balanced("{'items': [1, (2, 3)]}"))
        self.assertTrue(is_balanced(""))
        self.assertTrue(is_balanced("no brackets at all"))

    def test_wrong_order(self):
        self.assertFalse(is_balanced("print(items[0)]"))
        self.assertFalse(is_balanced("(]"))

    def test_unclosed_or_extra(self):
        self.assertFalse(is_balanced("(("), "Brackets still open at the end mean it isn't balanced")
        self.assertFalse(is_balanced("())"), "A closing bracket with nothing open isn't balanced")
        self.assertFalse(is_balanced(")("))

    def test_long(self):
        self.assertTrue(is_balanced("([{" * 50_000 + "}])" * 50_000))


class TestSupportQueue(unittest.TestCase):
    def test_first_come_first_served(self):
        queue = SupportQueue()
        queue.add("T-101")
        queue.add("T-102")
        queue.add("T-103")
        self.assertEqual(queue.next_ticket(), "T-101")
        self.assertEqual(queue.next_ticket(), "T-102")
        self.assertEqual(queue.next_ticket(), "T-103")
        self.assertIsNone(queue.next_ticket(), "With no tickets left, return None")

    def test_urgent_first(self):
        queue = SupportQueue()
        queue.add("T-101")
        queue.add("T-102", urgent=True)
        queue.add("T-103")
        queue.add("T-104", urgent=True)
        self.assertEqual([queue.next_ticket() for _ in range(4)], ["T-102", "T-104", "T-101", "T-103"])

    def test_peek_and_len(self):
        queue = SupportQueue()
        self.assertEqual(len(queue), 0)
        self.assertIsNone(queue.peek())
        queue.add("T-101")
        queue.add("T-102", urgent=True)
        self.assertEqual(queue.peek(), "T-102")
        self.assertEqual(len(queue), 2, "peek shouldn't remove the ticket")
        queue.next_ticket()
        self.assertEqual(queue.peek(), "T-101")
        self.assertEqual(len(queue), 1)

    def test_fast(self):
        queue = SupportQueue()
        for i in range(BIG):
            queue.add(i)
        start = time.perf_counter()
        for i in range(BIG):
            self.assertEqual(queue.next_ticket(), i)
        self.assertLess(time.perf_counter() - start, 1.5, "Too slow: list.pop(0) is O(n). Use collections.deque and popleft()")


if __name__ == "__main__":
    unittest.main()

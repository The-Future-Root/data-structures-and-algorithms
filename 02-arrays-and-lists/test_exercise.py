import ast
import pathlib
import random
import time
import unittest

from exercise import best_window, merge_sorted, remove_all, rotate, running_totals

SOURCE = pathlib.Path(__file__).with_name("exercise.py").read_text()
BIG = 200_000


def timed(function, *args):
    start = time.perf_counter()
    result = function(*args)
    return result, time.perf_counter() - start


class TestRunningTotals(unittest.TestCase):
    def test_totals(self):
        self.assertEqual(running_totals([120, 80, 200]), [120, 200, 400])
        self.assertEqual(running_totals([]), [])

    def test_new_list(self):
        sales = [1, 2]
        running_totals(sales)
        self.assertEqual(sales, [1, 2], "Return a new list; don't change the one you were given")


class TestRotate(unittest.TestCase):
    def test_rotate(self):
        days = ["Mon", "Tue", "Wed", "Thu"]
        self.assertEqual(rotate(days, 1), ["Thu", "Mon", "Tue", "Wed"])
        self.assertEqual(rotate(days, 2), ["Wed", "Thu", "Mon", "Tue"])

    def test_big_k_and_zero(self):
        self.assertEqual(rotate([1, 2, 3], 4), [3, 1, 2])
        self.assertEqual(rotate([1, 2, 3], 0), [1, 2, 3])
        self.assertEqual(rotate([1, 2, 3], 3), [1, 2, 3])

    def test_empty(self):
        self.assertEqual(rotate([], 5), [])


class TestRemoveAll(unittest.TestCase):
    def test_removes_in_place(self):
        items = [3, 0, 1, 0, 0, 2]
        self.assertEqual(remove_all(items, 0), 3)
        self.assertEqual(items, [3, 1, 2], "Change the list you were given")

    def test_nothing_to_remove(self):
        items = ["a", "b"]
        self.assertEqual(remove_all(items, "z"), 0)
        self.assertEqual(items, ["a", "b"])

    def test_fast(self):
        items = [0, 1] * (BIG // 2)
        count, seconds = timed(remove_all, items, 0)
        self.assertEqual(count, BIG // 2)
        self.assertEqual(len(items), BIG // 2)
        self.assertLess(seconds, 1.0, "Too slow: calling remove() in a loop is O(n^2); use two pointers")


class TestMergeSorted(unittest.TestCase):
    def test_merge(self):
        self.assertEqual(merge_sorted([1, 4, 9], [2, 3, 10, 11]), [1, 2, 3, 4, 9, 10, 11])

    def test_duplicates_and_empty(self):
        self.assertEqual(merge_sorted([1, 2, 2], [2, 3]), [1, 2, 2, 2, 3])
        self.assertEqual(merge_sorted([], [5, 6]), [5, 6])
        self.assertEqual(merge_sorted([5], []), [5])

    def test_no_sorting_functions(self):
        names = {getattr(n.func, "id", getattr(n.func, "attr", None)) for n in ast.walk(ast.parse(SOURCE)) if isinstance(n, ast.Call)}
        self.assertFalse({"sorted", "sort"} & names, "Don't use sorted() or .sort() in this exercise")

    def test_fast(self):
        a = list(range(0, BIG, 2))
        b = list(range(1, BIG, 2))
        result, seconds = timed(merge_sorted, a, b)
        self.assertEqual(result, list(range(BIG)))
        self.assertLess(seconds, 1.0, "Too slow: walk through both lists once, with an index into each")


class TestBestWindow(unittest.TestCase):
    def test_window(self):
        self.assertEqual(best_window([3, 8, 2, 9, 4], 2), 13)
        self.assertEqual(best_window([3, 8, 2, 9, 4], 3), 19)
        self.assertEqual(best_window([5], 1), 5)

    def test_too_short(self):
        self.assertIsNone(best_window([1, 2], 3))

    def test_negative_numbers(self):
        self.assertEqual(best_window([-5, -2, -8], 2), -7)

    def test_matches_brute_force(self):
        rng = random.Random(2)
        values = [rng.randint(-50, 100) for _ in range(3000)]
        expected = max(sum(values[i:i + 40]) for i in range(len(values) - 40 + 1))
        self.assertEqual(best_window(values, 40), expected)

    def test_fast(self):
        rng = random.Random(3)
        values = [rng.randint(0, 100) for _ in range(BIG)]
        result, seconds = timed(best_window, values, 1000)
        self.assertIsNotNone(result)
        self.assertLess(seconds, 1.0, "Too slow: keep a running total and slide the window along")


if __name__ == "__main__":
    unittest.main()

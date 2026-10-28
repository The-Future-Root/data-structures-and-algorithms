import ast
import pathlib
import random
import time
import unittest

from exercise import binary_search, count_between, first_after, first_at_or_after, linear_search, read_log

HERE = pathlib.Path(__file__).parent
SOURCE = (HERE / "exercise.py").read_text()
SEARCHES = ["binary_search", "first_at_or_after", "first_after", "count_between"]
BIG = list(range(0, 2_000_000, 2))


def runs_fast(test, function, make_args, limit=0.25, times=300):
    """Call function `times` times, failing as soon as the total goes over `limit` seconds."""
    start = time.perf_counter()
    for i in range(times):
        function(*make_args(i))
        if time.perf_counter() - start > limit:
            test.fail(f"Too slow: {function.__name__} should halve the search range each step, O(log n)")


class TestLinearSearch(unittest.TestCase):
    def test_found(self):
        self.assertEqual(linear_search(["Mon", "Tue", "Wed"], "Wed"), 2)
        self.assertEqual(linear_search([5, 3, 5], 5), 0, "Return the first match")

    def test_missing(self):
        self.assertEqual(linear_search([5, 3], 9), -1)
        self.assertEqual(linear_search([], 9), -1)


class TestBinarySearch(unittest.TestCase):
    def test_found(self):
        items = [3, 8, 12, 19, 23, 31, 40, 47, 52, 58, 64, 71, 77, 85, 90, 96]
        for index, value in enumerate(items):
            self.assertEqual(binary_search(items, value), index)

    def test_missing(self):
        items = [3, 8, 12, 19]
        for value in [0, 4, 13, 20, 100]:
            self.assertEqual(binary_search(items, value), -1)
        self.assertEqual(binary_search([], 5), -1)
        self.assertEqual(binary_search([5], 5), 0)

    def test_strings(self):
        times = ["09:00:22", "09:00:48", "09:14:07", "09:35:06"]
        self.assertEqual(binary_search(times, "09:14:07"), 2)

    def test_random(self):
        rng = random.Random(6)
        for _ in range(200):
            items = sorted(rng.sample(range(1000), rng.randint(0, 40)))
            target = rng.randint(0, 999)
            expected = items.index(target) if target in items else -1
            self.assertEqual(binary_search(items, target), expected, f"Searching {items} for {target}")

    def test_fast(self):
        runs_fast(self, binary_search, lambda i: (BIG, 1_999_998 - i))


class TestBoundaries(unittest.TestCase):
    times = ["09:00", "09:05", "09:05", "09:05", "09:10", "09:20"]

    def test_first_at_or_after(self):
        self.assertEqual(first_at_or_after(self.times, "09:05"), 1, "With repeats, return the first one")
        self.assertEqual(first_at_or_after(self.times, "09:06"), 4)
        self.assertEqual(first_at_or_after(self.times, "08:00"), 0)
        self.assertEqual(first_at_or_after(self.times, "09:30"), 6, "If none is late enough, return len(timestamps)")
        self.assertEqual(first_at_or_after([], "09:00"), 0)

    def test_first_after(self):
        self.assertEqual(first_after(self.times, "09:05"), 4, "Skip past every repeat of end")
        self.assertEqual(first_after(self.times, "08:00"), 0)
        self.assertEqual(first_after(self.times, "09:20"), 6)
        self.assertEqual(first_after([], "09:00"), 0)

    def test_count_between(self):
        self.assertEqual(count_between(self.times, "09:05", "09:10"), 4, "Both ends are included")
        self.assertEqual(count_between(self.times, "09:06", "09:09"), 0)
        self.assertEqual(count_between(self.times, "00:00", "23:59"), 6)

    def test_random_against_brute_force(self):
        rng = random.Random(7)
        for _ in range(300):
            items = sorted(rng.choices(range(30), k=rng.randint(0, 25)))
            low, high = sorted([rng.randint(-2, 32), rng.randint(-2, 32)])
            self.assertEqual(first_at_or_after(items, low), len([x for x in items if x < low]))
            self.assertEqual(first_after(items, high), len([x for x in items if x <= high]))
            self.assertEqual(count_between(items, low, high), len([x for x in items if low <= x <= high]))

    def test_fast(self):
        runs_fast(self, first_at_or_after, lambda i: (BIG, 1_999_990 - i))
        runs_fast(self, first_after, lambda i: (BIG, 1_999_990 - i))
        runs_fast(self, count_between, lambda i: (BIG, 1_999_000 - i, 1_999_990))


class TestTheLog(unittest.TestCase):
    def test_read_log(self):
        log = read_log(HERE / "server.log")
        self.assertEqual(len(log), 87)
        self.assertEqual(log[0], ("2026-03-14T08:58:47", "POST /checkout 201"))

    def test_checkout_incident(self):
        log = read_log(HERE / "server.log")
        timestamps = [timestamp for timestamp, _ in log]
        start = first_at_or_after(timestamps, "2026-03-14T09:35:00")
        end = first_after(timestamps, "2026-03-14T09:35:59")
        self.assertEqual([message for _, message in log[start:end]], ["POST /checkout 500", "POST /login 401", "POST /checkout 500", "POST /checkout 500"])


class TestRules(unittest.TestCase):
    def test_no_shortcuts(self):
        tree = ast.parse(SOURCE)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name for alias in node.names] + [getattr(node, "module", None)]
                self.assertNotIn("bisect", names, "Write the searches yourself instead of using bisect")
        for function in tree.body:
            if isinstance(function, ast.FunctionDef) and function.name in SEARCHES:
                for node in ast.walk(function):
                    if isinstance(node, ast.Compare):
                        self.assertFalse(any(isinstance(op, (ast.In, ast.NotIn)) for op in node.ops), f"Don't use `in` inside {function.name}: it's a linear search")
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                        self.assertNotEqual(node.func.attr, "index", f"Don't use .index() inside {function.name}: it's a linear search")


if __name__ == "__main__":
    unittest.main()

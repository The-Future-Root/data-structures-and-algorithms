import ast
import copy
import pathlib
import random
import time
import unittest

from exercise import PRODUCTS, cheapest, insertion_sort, merge, merge_sort, rank_products

SOURCE = pathlib.Path(__file__).with_name("exercise.py").read_text()
HAND_WRITTEN = ["insertion_sort", "merge", "merge_sort"]


def timed(function, *args):
    start = time.perf_counter()
    result = function(*args)
    return result, time.perf_counter() - start


class TestInsertionSort(unittest.TestCase):
    def test_sorts_in_place(self):
        prices = [24.99, 6.50, 89.00, 18.00, 54.99]
        insertion_sort(prices)
        self.assertEqual(prices, [6.50, 18.00, 24.99, 54.99, 89.00], "Sort the list you were given")

    def test_edge_cases(self):
        for items in [[], [1], [2, 1], [1, 2], [3, 3, 1, 3], [5, 4, 3, 2, 1]]:
            expected = sorted(items)
            insertion_sort(items)
            self.assertEqual(items, expected)

    def test_random(self):
        rng = random.Random(7)
        for _ in range(100):
            items = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
            expected = sorted(items)
            insertion_sort(items)
            self.assertEqual(items, expected)

    def test_fast_on_sorted_input(self):
        items = list(range(10_000))
        _, seconds = timed(insertion_sort, items)
        self.assertLess(seconds, 0.2, "Insertion sort should be O(n) on a list that's already sorted: stop shifting as soon as the item is in place")


class TestMerge(unittest.TestCase):
    def test_merge(self):
        self.assertEqual(merge([3, 27, 38, 43], [9, 10, 82]), [3, 9, 10, 27, 38, 43, 82])
        self.assertEqual(merge([], [1, 2]), [1, 2])
        self.assertEqual(merge([1, 2], []), [1, 2])

    def test_left_first_when_equal(self):
        result = merge([1], [1.0])
        self.assertIs(type(result[0]), int, "When two items are equal, take the one from the left first: that keeps merge sort stable")


class TestMergeSort(unittest.TestCase):
    def test_sorts(self):
        self.assertEqual(merge_sort([38, 27, 43, 3, 9, 82, 10]), [3, 9, 10, 27, 38, 43, 82])
        self.assertEqual(merge_sort(["mocha", "chai", "latte"]), ["chai", "latte", "mocha"])

    def test_edge_cases(self):
        for items in [[], [1], [2, 1], [3, 3, 1, 3]]:
            self.assertEqual(merge_sort(items), sorted(items))

    def test_does_not_change_input(self):
        items = [3, 1, 2]
        merge_sort(items)
        self.assertEqual(items, [3, 1, 2], "merge_sort should return a new list and leave the original alone")

    def test_random(self):
        rng = random.Random(8)
        for _ in range(100):
            items = [rng.randint(-50, 50) for _ in range(rng.randint(0, 60))]
            self.assertEqual(merge_sort(items), sorted(items))

    def test_fast(self):
        rng = random.Random(9)
        items = [rng.random() for _ in range(10_000)]
        result, seconds = timed(merge_sort, items)
        self.assertEqual(result, sorted(items))
        self.assertLess(seconds, 0.5, "Too slow for merge sort: is it O(n^2)? Split in half, sort each half, then merge")


class TestRankProducts(unittest.TestCase):
    def test_order(self):
        names = [product["name"] for product in rank_products(PRODUCTS)]
        self.assertEqual(names, ["Coffee scale", "Pour-over kettle", "Burr grinder", "Travel mug", "Paper filters", "Milk frother"])

    def test_does_not_change_input(self):
        before = copy.deepcopy(PRODUCTS)
        rank_products(PRODUCTS)
        self.assertEqual(PRODUCTS, before, "Return a new list; don't sort PRODUCTS itself")

    def test_cheapest(self):
        self.assertEqual(cheapest(PRODUCTS, 3), ["Paper filters", "Travel mug", "Milk frother"])
        self.assertEqual(cheapest(PRODUCTS, 0), [])
        self.assertEqual(len(cheapest(PRODUCTS, 10)), 6)


class TestRules(unittest.TestCase):
    def test_no_built_in_sorting_in_your_sorts(self):
        for function in ast.parse(SOURCE).body:
            if isinstance(function, ast.FunctionDef) and function.name in HAND_WRITTEN:
                for node in ast.walk(function):
                    if isinstance(node, ast.Call):
                        name = getattr(node.func, "id", getattr(node.func, "attr", None))
                        self.assertNotIn(name, ("sorted", "sort"), f"Don't use sorted() or .sort() inside {function.name}")


if __name__ == "__main__":
    unittest.main()

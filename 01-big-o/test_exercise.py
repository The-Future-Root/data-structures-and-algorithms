import random
import time
import unittest

from exercise import common_customers, first_repeat, has_duplicates, has_pair_with_sum

BIG = 30_000


def timed(function, *args):
    start = time.perf_counter()
    result = function(*args)
    return result, time.perf_counter() - start


class TestHasDuplicates(unittest.TestCase):
    def test_small(self):
        self.assertIs(has_duplicates(["A12", "B7", "A12"]), True)
        self.assertIs(has_duplicates(["A12", "B7", "C3"]), False)
        self.assertIs(has_duplicates([]), False)

    def test_fast(self):
        result, seconds = timed(has_duplicates, list(range(BIG)))
        self.assertIs(result, False)
        self.assertLess(seconds, 1.0, "Too slow for 30,000 items: use a set instead of a loop inside a loop")


class TestCommonCustomers(unittest.TestCase):
    def test_small(self):
        january = ["Alex", "Sam", "Priya", "Sam"]
        february = ["Jo", "Priya", "Alex", "Priya"]
        self.assertEqual(common_customers(january, february), ["Alex", "Priya"])

    def test_none_in_common(self):
        self.assertEqual(common_customers(["A"], ["B"]), [])

    def test_fast(self):
        a = [f"customer{i}" for i in range(BIG)]
        b = [f"customer{i}" for i in range(BIG // 2, BIG + BIG // 2)]
        result, seconds = timed(common_customers, a, b)
        self.assertEqual(len(result), BIG // 2)
        self.assertLess(seconds, 2.0, "Too slow: turn one list into a set first")


class TestFirstRepeat(unittest.TestCase):
    def test_small(self):
        self.assertEqual(first_repeat(["A12", "B7", "C3", "B7", "A12"]), "B7")
        self.assertIsNone(first_repeat(["A", "B", "C"]))
        self.assertIsNone(first_repeat([]))

    def test_fast(self):
        items = list(range(BIG)) + [BIG - 1]
        result, seconds = timed(first_repeat, items)
        self.assertEqual(result, BIG - 1)
        self.assertLess(seconds, 1.0, "Too slow for 30,000 items: keep a set of what you've seen")


class TestPairWithSum(unittest.TestCase):
    def test_small(self):
        self.assertIs(has_pair_with_sum([12, 38, 7, 20], 50), True)
        self.assertIs(has_pair_with_sum([12, 38, 7, 20], 100), False)

    def test_two_different_items(self):
        self.assertIs(has_pair_with_sum([25, 10], 50), False, "One $25 item can't be used twice")
        self.assertIs(has_pair_with_sum([25, 10, 25], 50), True, "Two separate $25 items do count")

    def test_fast(self):
        prices = list(range(1, BIG + 1))
        random.Random(1).shuffle(prices)
        result, seconds = timed(has_pair_with_sum, prices, 3 * BIG)
        self.assertIs(result, False)
        self.assertLess(seconds, 1.0, "Too slow for 30,000 prices: for each price, check a set for budget - price")


if __name__ == "__main__":
    unittest.main()

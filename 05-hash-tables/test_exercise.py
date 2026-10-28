import ast
import pathlib
import time
import unittest

from exercise import HashMap

SOURCE = pathlib.Path(__file__).with_name("exercise.py").read_text()
BIG = 30_000


class TestPutAndGet(unittest.TestCase):
    def test_put_get(self):
        stock = HashMap()
        stock.put("latte", 40)
        stock.put("scone", 12)
        self.assertEqual(stock.get("latte"), 40)
        self.assertEqual(stock.get("scone"), 12)

    def test_replace(self):
        stock = HashMap()
        stock.put("latte", 40)
        stock.put("latte", 38)
        self.assertEqual(stock.get("latte"), 38)
        self.assertEqual(len(stock), 1, "Putting an existing key again should replace the value, not add a second pair")

    def test_missing_key(self):
        stock = HashMap()
        self.assertIsNone(stock.get("muffin"))
        self.assertEqual(stock.get("muffin", 0), 0)

    def test_other_key_types(self):
        table = HashMap()
        table.put(1042, "oat milk")
        table.put(("Leeds", "LS1"), "north")
        self.assertEqual(table.get(1042), "oat milk")
        self.assertEqual(table.get(("Leeds", "LS1")), "north")

    def test_pairs_are_in_the_right_buckets(self):
        table = HashMap()
        for word in ["latte", "scone", "mocha", "chai"]:
            table.put(word, len(word))
        for index, bucket in enumerate(table._buckets):
            for key, _ in bucket:
                self.assertEqual(hash(key) % len(table._buckets), index, f"{key!r} is in the wrong bucket: use self._bucket(key)")


class TestCollisions(unittest.TestCase):
    def test_same_bucket(self):
        # With 8 buckets, hash(1), hash(9) and hash(17) all land in bucket 1.
        table = HashMap()
        table.put(1, "a")
        table.put(9, "b")
        table.put(17, "c")
        self.assertEqual([table.get(1), table.get(9), table.get(17)], ["a", "b", "c"])
        self.assertTrue(table.remove(9))
        self.assertEqual(table.get(1), "a")
        self.assertIsNone(table.get(9))
        self.assertEqual(table.get(17), "c")


class TestRemoveContainsLen(unittest.TestCase):
    def test_remove(self):
        stock = HashMap()
        stock.put("latte", 40)
        self.assertTrue(stock.remove("latte"))
        self.assertFalse("latte" in stock)
        self.assertFalse(stock.remove("latte"), "Removing a missing key should return False")
        self.assertEqual(len(stock), 0)

    def test_contains(self):
        stock = HashMap()
        stock.put("scone", 0)
        self.assertTrue("scone" in stock, "A key with a value of 0 is still in the table")
        self.assertFalse("muffin" in stock)

    def test_len_and_keys(self):
        stock = HashMap()
        self.assertEqual(len(stock), 0)
        for name in ["latte", "scone", "chai"]:
            stock.put(name, 1)
        self.assertEqual(len(stock), 3)
        self.assertCountEqual(stock.keys(), ["latte", "scone", "chai"])


class TestResize(unittest.TestCase):
    def test_grows(self):
        table = HashMap()
        self.assertEqual(table.bucket_count(), 8)
        for i in range(6):
            table.put(i, i)
        self.assertEqual(table.bucket_count(), 8, "6 keys in 8 buckets is a load of 0.75: no need to grow yet")
        table.put(6, 6)
        self.assertEqual(table.bucket_count(), 16, "Over 0.75 keys per bucket, double the number of buckets")

    def test_everything_survives_a_resize(self):
        table = HashMap()
        for i in range(100):
            table.put(f"item-{i}", i)
        self.assertEqual(len(table), 100)
        for i in range(100):
            self.assertEqual(table.get(f"item-{i}"), i)

    def test_fast(self):
        table = HashMap()
        start = time.perf_counter()
        for i in range(BIG):
            table.put(f"order-{i}", i)
        for i in range(BIG):
            table.get(f"order-{i}")
        self.assertLess(time.perf_counter() - start, 1.0, "Too slow: the buckets are getting long. Resize when the table is over 0.75 full")


class TestNoDict(unittest.TestCase):
    def test_no_dict_or_set(self):
        for node in ast.walk(ast.parse(SOURCE)):
            self.assertFalse(isinstance(node, (ast.Dict, ast.Set, ast.DictComp, ast.SetComp)), "Don't use a dict or set: build the table from the buckets")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, ("dict", "set", "frozenset"), "Don't use a dict or set: build the table from the buckets")


if __name__ == "__main__":
    unittest.main()

import random
import time
import unittest

from exercise import ProductIndex, TreeNode

CATALOGUE = [(50, "Travel mug"), (30, "Paper filters"), (70, "Burr grinder"), (20, "Coffee scoop"),
             (40, "Milk jug"), (60, "Pour-over kettle"), (80, "Espresso machine")]


def build(pairs=CATALOGUE):
    index = ProductIndex()
    for key, value in pairs:
        index.insert(key, value)
    return index


class TestInsert(unittest.TestCase):
    def test_shape(self):
        index = build()
        self.assertIsInstance(index.root, TreeNode)
        self.assertEqual(index.root.key, 50, "The first key inserted becomes the root")
        self.assertEqual(index.root.left.key, 30, "Smaller keys go to the left")
        self.assertEqual(index.root.right.key, 70, "Bigger keys go to the right")
        self.assertEqual(index.root.left.right.key, 40)
        self.assertEqual(index.root.right.left.key, 60)
        self.assertIsNone(index.root.left.left.left)

    def test_replace(self):
        index = build()
        index.insert(60, "Gooseneck kettle")
        self.assertEqual(index.get(60), "Gooseneck kettle")
        self.assertEqual(len(index), 7, "Inserting an existing key replaces its value")

    def test_no_list_or_dict_inside(self):
        index = build()
        for name, value in vars(index).items():
            self.assertNotIsInstance(value, (list, tuple, dict, set), f"Don't store the products in self.{name}; link TreeNode objects")


class TestLookups(unittest.TestCase):
    def test_get(self):
        index = build()
        self.assertEqual(index.get(60), "Pour-over kettle")
        self.assertEqual(index.get(20), "Coffee scoop")
        self.assertIsNone(index.get(65))
        self.assertEqual(index.get(65, "not found"), "not found")
        self.assertIsNone(ProductIndex().get(1))

    def test_contains_and_len(self):
        index = build()
        self.assertTrue(50 in index)
        self.assertTrue(80 in index)
        self.assertFalse(55 in index)
        self.assertEqual(len(index), 7)
        self.assertEqual(len(ProductIndex()), 0)
        self.assertFalse(1 in ProductIndex())

    def test_string_keys(self):
        index = build([("MUG-018", "Travel mug"), ("FIL-100", "Paper filters"), ("SCL-002", "Coffee scale")])
        self.assertEqual(index.get("SCL-002"), "Coffee scale")
        self.assertEqual(index.smallest(), "FIL-100")


class TestOrder(unittest.TestCase):
    def test_smallest_largest(self):
        index = build()
        self.assertEqual(index.smallest(), 20)
        self.assertEqual(index.largest(), 80)
        self.assertIsNone(ProductIndex().smallest())
        self.assertIsNone(ProductIndex().largest())

    def test_in_order(self):
        index = build()
        self.assertEqual(index.in_order(), sorted(CATALOGUE))
        self.assertEqual(ProductIndex().in_order(), [])

    def test_between(self):
        index = build()
        self.assertEqual(index.between(35, 65), [40, 50, 60])
        self.assertEqual(index.between(40, 60), [40, 50, 60], "Both ends are included")
        self.assertEqual(index.between(81, 99), [])
        self.assertEqual(index.between(0, 100), [20, 30, 40, 50, 60, 70, 80])

    def test_random_against_sorted(self):
        rng = random.Random(8)
        keys = rng.sample(range(10_000), 500)
        index = build([(key, str(key)) for key in keys])
        self.assertEqual([key for key, _ in index.in_order()], sorted(keys))
        self.assertEqual(index.between(2000, 3000), sorted(key for key in keys if 2000 <= key <= 3000))


class TestHeight(unittest.TestCase):
    def test_height(self):
        self.assertEqual(ProductIndex().height(), 0)
        self.assertEqual(build([(5, "a")]).height(), 1)
        self.assertEqual(build().height(), 3)

    def test_sorted_input_makes_a_tall_tree(self):
        index = build([(key, "x") for key in range(1, 301)])
        self.assertEqual(index.height(), 300, "Inserting keys in order gives one long chain: every node only has a right child")


class TestSpeed(unittest.TestCase):
    def test_fast(self):
        rng = random.Random(9)
        keys = rng.sample(range(10_000_000), 30_000)
        message = "Too slow: insert and get should go down one path, turning left or right at each node"
        start = time.perf_counter()
        index = ProductIndex()
        for key in keys:
            index.insert(key, key)
            if time.perf_counter() - start > 1.5:
                self.fail(message)
        for key in keys:
            index.get(key)
            if time.perf_counter() - start > 1.5:
                self.fail(message)
        self.assertLess(index.height(), 60, "A tree of random keys should be fairly bushy")

if __name__ == "__main__":
    unittest.main()

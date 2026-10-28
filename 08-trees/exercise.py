# Lesson 8: a product index as a binary search tree
#
# TreeNode and ProductIndex.__init__ are written for you. Build the tree
# from TreeNode objects: don't keep the products in a list or dict.
# Test with:  python3 -m unittest -v


class TreeNode:
    """One entry in the tree: a key, its value, and links to the left and right children."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class ProductIndex:
    """A binary search tree of products, keyed by product code."""

    def __init__(self):
        """Start with an empty tree."""
        self.root = None
        self._size = 0

    def insert(self, key, value):
        """Add a product, or replace the value if the key is already there."""
        pass

    def get(self, key, default=None):
        """Return the value for key, or default if it isn't in the tree."""
        pass

    def __contains__(self, key):
        """Support `key in index`."""
        pass

    def __len__(self):
        """Return the number of products."""
        pass

    def smallest(self):
        """Return the smallest key, or None if the tree is empty."""
        pass

    def largest(self):
        """Return the largest key, or None if the tree is empty."""
        pass

    def in_order(self):
        """Return a list of (key, value) pairs, smallest key first."""
        pass

    def _in_order(self, node, pairs):
        """Add the pairs under node to the list, in order."""
        pass

    def between(self, low, high):
        """Return a list of the keys from low to high, both included, smallest first."""
        pass

    def _between(self, node, low, high, keys):
        """Add the keys under node that are between low and high, skipping branches that can't contain any."""
        pass

    def height(self):
        """Return the number of levels in the tree: 0 when empty, 1 for just a root."""
        pass

    def _height(self, node):
        """Return the height of the tree below node."""
        pass


if __name__ == "__main__":
    index = ProductIndex()
    for code, name in [(50, "Travel mug"), (30, "Paper filters"), (70, "Burr grinder"), (20, "Coffee scoop"),
                       (40, "Milk jug"), (60, "Pour-over kettle"), (80, "Espresso machine")]:
        index.insert(code, name)
    print(index.get(60), len(index), index.height())
    print(index.smallest(), index.largest())
    print(index.between(35, 65))
    print([code for code, _ in index.in_order()])

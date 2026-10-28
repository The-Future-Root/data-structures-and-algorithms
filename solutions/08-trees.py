# Solution to lesson 8: a product index as a binary search tree


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
        if self.root is None:
            self.root = TreeNode(key, value)
            self._size += 1
            return
        node = self.root
        while True:
            if key == node.key:
                node.value = value
                return
            if key < node.key:
                if node.left is None:
                    node.left = TreeNode(key, value)
                    self._size += 1
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = TreeNode(key, value)
                    self._size += 1
                    return
                node = node.right

    def get(self, key, default=None):
        """Return the value for key, or default if it isn't in the tree."""
        node = self.root
        while node is not None:
            if key == node.key:
                return node.value
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return default

    def __contains__(self, key):
        """Support `key in index`."""
        node = self.root
        while node is not None:
            if key == node.key:
                return True
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return False

    def __len__(self):
        """Return the number of products."""
        return self._size

    def smallest(self):
        """Return the smallest key, or None if the tree is empty."""
        if self.root is None:
            return None
        node = self.root
        while node.left is not None:
            node = node.left
        return node.key

    def largest(self):
        """Return the largest key, or None if the tree is empty."""
        if self.root is None:
            return None
        node = self.root
        while node.right is not None:
            node = node.right
        return node.key

    def in_order(self):
        """Return a list of (key, value) pairs, smallest key first."""
        pairs = []
        self._in_order(self.root, pairs)
        return pairs

    def _in_order(self, node, pairs):
        """Add the pairs under node to the list, in order."""
        if node is None:
            return
        self._in_order(node.left, pairs)
        pairs.append((node.key, node.value))
        self._in_order(node.right, pairs)

    def between(self, low, high):
        """Return a list of the keys from low to high, both included, smallest first."""
        keys = []
        self._between(self.root, low, high, keys)
        return keys

    def _between(self, node, low, high, keys):
        """Add the keys under node that are between low and high, skipping branches that can't contain any."""
        if node is None:
            return
        if low < node.key:
            self._between(node.left, low, high, keys)
        if low <= node.key <= high:
            keys.append(node.key)
        if node.key < high:
            self._between(node.right, low, high, keys)

    def height(self):
        """Return the number of levels in the tree: 0 when empty, 1 for just a root."""
        return self._height(self.root)

    def _height(self, node):
        """Return the height of the tree below node."""
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))


if __name__ == "__main__":
    index = ProductIndex()
    for code, name in [(50, "Travel mug"), (30, "Paper filters"), (70, "Burr grinder"), (20, "Coffee scoop"),
                       (40, "Milk jug"), (60, "Pour-over kettle"), (80, "Espresso machine")]:
        index.insert(code, name)
    print(index.get(60), len(index), index.height())
    print(index.smallest(), index.largest())
    print(index.between(35, 65))
    print([code for code, _ in index.in_order()])

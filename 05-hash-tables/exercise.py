# Lesson 5: a hash table
#
# __init__, _bucket and bucket_count are written for you.
# Don't use a dict or a set anywhere in this class: the point is to build one.
# Test with:  python3 -m unittest -v


class HashMap:
    """A hash table using separate chaining: each bucket is a list of [key, value] pairs."""

    def __init__(self, capacity=8):
        """Start empty, with `capacity` buckets."""
        self._buckets = []
        for _ in range(capacity):
            self._buckets.append([])
        self._size = 0

    def _bucket(self, key):
        """Return the bucket that key belongs in."""
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        """Store value under key, replacing any old value. Grow when the table gets too full."""
        pass

    def get(self, key, default=None):
        """Return the value stored under key, or default if the key isn't there."""
        pass

    def remove(self, key):
        """Remove key and its value. Return True, or False if the key wasn't there."""
        pass

    def __contains__(self, key):
        """Support `key in table`."""
        pass

    def __len__(self):
        """Return the number of keys, in O(1)."""
        pass

    def keys(self):
        """Return a list of all the keys, in no particular order."""
        pass

    def bucket_count(self):
        """Return how many buckets the table has right now."""
        return len(self._buckets)

    def _resize(self, capacity):
        """Move every pair into a new, bigger set of buckets."""
        pass


if __name__ == "__main__":
    stock = HashMap()
    stock.put("latte", 40)
    stock.put("scone", 12)
    stock.put("latte", 38)
    print(stock.get("latte"), stock.get("muffin", 0))
    print("scone" in stock, len(stock))
    for i in range(20):
        stock.put(f"item-{i}", i)
    print(len(stock), stock.bucket_count())

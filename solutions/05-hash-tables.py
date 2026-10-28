# Solution to lesson 5: a hash table


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
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > len(self._buckets) * 0.75:
            self._resize(len(self._buckets) * 2)

    def get(self, key, default=None):
        """Return the value stored under key, or default if the key isn't there."""
        for stored_key, value in self._bucket(key):
            if stored_key == key:
                return value
        return default

    def remove(self, key):
        """Remove key and its value. Return True, or False if the key wasn't there."""
        bucket = self._bucket(key)
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        """Support `key in table`."""
        for stored_key, _ in self._bucket(key):
            if stored_key == key:
                return True
        return False

    def __len__(self):
        """Return the number of keys, in O(1)."""
        return self._size

    def keys(self):
        """Return a list of all the keys, in no particular order."""
        result = []
        for bucket in self._buckets:
            for key, _ in bucket:
                result.append(key)
        return result

    def bucket_count(self):
        """Return how many buckets the table has right now."""
        return len(self._buckets)

    def _resize(self, capacity):
        """Move every pair into a new, bigger set of buckets."""
        old_buckets = self._buckets
        self._buckets = []
        for _ in range(capacity):
            self._buckets.append([])
        for bucket in old_buckets:
            for key, value in bucket:
                self._bucket(key).append([key, value])


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

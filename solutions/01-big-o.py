# Solution to lesson 1: make it fast


def has_duplicates_slow(items):
    """The O(n^2) version from the lesson, for comparison. Don't change it."""
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False


def has_duplicates(items):
    """Return True if any item appears more than once. O(n)."""
    seen = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False


def common_customers(list_a, list_b):
    """Return the names in both lists, sorted, with no repeats. O(n)."""
    in_b = set(list_b)
    both = set()
    for name in list_a:
        if name in in_b:
            both.add(name)
    return sorted(both)


def first_repeat(items):
    """Return the first item that appears for a second time, or None. O(n)."""
    seen = set()
    for item in items:
        if item in seen:
            return item
        seen.add(item)
    return None


def has_pair_with_sum(prices, budget):
    """Return True if two different items in prices add up exactly to budget. O(n)."""
    seen = set()
    for price in prices:
        if budget - price in seen:
            return True
        seen.add(price)
    return False

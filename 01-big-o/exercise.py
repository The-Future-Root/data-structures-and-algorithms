# Lesson 1: make it fast
#
# Each function has an obvious O(n^2) solution with a loop inside a loop.
# Write O(n) versions instead. The tests try them on large inputs.
# Test with:  python3 -m unittest -v


def has_duplicates_slow(items):
    """The O(n^2) version from the lesson, for comparison. Don't change it."""
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False


def has_duplicates(items):
    """Return True if any item appears more than once. O(n)."""
    pass


def common_customers(list_a, list_b):
    """Return the names in both lists, sorted, with no repeats. O(n)."""
    pass


def first_repeat(items):
    """Return the first item that appears for a second time, or None. O(n)."""
    pass


def has_pair_with_sum(prices, budget):
    """Return True if two different items in prices add up exactly to budget. O(n)."""
    pass

# Solution to lesson 2: list algorithms


def running_totals(sales):
    """Return a new list of totals so far: [120, 80, 200] gives [120, 200, 400]."""
    totals = []
    total = 0
    for amount in sales:
        total += amount
        totals.append(total)
    return totals


def rotate(items, k):
    """Return a new list with every item moved k places to the right, wrapping round."""
    if not items:
        return []
    k = k % len(items)
    if k == 0:
        return list(items)
    return items[-k:] + items[:-k]


def remove_all(items, value):
    """Remove every `value` from items in place, in O(n). Return how many were removed."""
    write = 0
    for read in range(len(items)):
        if items[read] != value:
            items[write] = items[read]
            write += 1
    removed = len(items) - write
    del items[write:]
    return removed


def merge_sorted(a, b):
    """Merge two already-sorted lists into one sorted list, in O(n + m)."""
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result


def best_window(values, k):
    """Return the largest total of any k items in a row, in O(n), or None if there are fewer than k."""
    if len(values) < k:
        return None
    total = sum(values[:k])
    best = total
    for i in range(k, len(values)):
        total += values[i] - values[i - k]
        best = max(best, total)
    return best

# Solution to lesson 6: searching a log


def linear_search(items, target):
    """Return the index of target in items by checking each one in turn, or -1 if it isn't there."""
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1


def binary_search(items, target):
    """items is sorted. Return the index of target, or -1 if it isn't there, in O(log n)."""
    low = 0
    high = len(items) - 1
    while low <= high:
        middle = (low + high) // 2
        if items[middle] == target:
            return middle
        if items[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def first_at_or_after(timestamps, start):
    """timestamps is sorted. Return the index of the first one >= start, or len(timestamps) if there's none, in O(log n)."""
    low = 0
    high = len(timestamps)
    while low < high:
        middle = (low + high) // 2
        if timestamps[middle] < start:
            low = middle + 1
        else:
            high = middle
    return low


def first_after(timestamps, end):
    """timestamps is sorted. Return the index of the first one > end, or len(timestamps) if there's none, in O(log n)."""
    low = 0
    high = len(timestamps)
    while low < high:
        middle = (low + high) // 2
        if timestamps[middle] <= end:
            low = middle + 1
        else:
            high = middle
    return low


def count_between(timestamps, start, end):
    """timestamps is sorted. Return how many are between start and end, inclusive, in O(log n)."""
    return first_after(timestamps, end) - first_at_or_after(timestamps, start)


def read_log(path):
    """Read a log file where each line is 'timestamp message'. Return a list of (timestamp, message) pairs."""
    log = []
    with open(path) as file:
        for line in file:
            line = line.strip()
            if line:
                timestamp, message = line.split(" ", 1)
                log.append((timestamp, message))
    return log


if __name__ == "__main__":
    log = read_log("server.log")
    timestamps = [timestamp for timestamp, _ in log]
    print(len(log), "entries")
    start = first_at_or_after(timestamps, "2026-03-14T09:35:00")
    end = first_after(timestamps, "2026-03-14T09:35:59")
    for timestamp, message in log[start:end]:
        print(timestamp, message)
    print(count_between(timestamps, "2026-03-14T09:00:00", "2026-03-14T09:59:59"), "entries between 9 and 10")

# Lesson 6: searching a log
#
# read_log is written for you. Don't use `in`, .index(), or the bisect
# module in the search functions: the point is to write the searches.
# Test with:  python3 -m unittest -v


def linear_search(items, target):
    """Return the index of target in items by checking each one in turn, or -1 if it isn't there."""
    pass


def binary_search(items, target):
    """items is sorted. Return the index of target, or -1 if it isn't there, in O(log n)."""
    pass


def first_at_or_after(timestamps, start):
    """timestamps is sorted. Return the index of the first one >= start, or len(timestamps) if there's none, in O(log n)."""
    pass


def first_after(timestamps, end):
    """timestamps is sorted. Return the index of the first one > end, or len(timestamps) if there's none, in O(log n)."""
    pass


def count_between(timestamps, start, end):
    """timestamps is sorted. Return how many are between start and end, inclusive, in O(log n)."""
    pass


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

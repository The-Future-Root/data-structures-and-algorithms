# Solution to lesson 7: sorting and ranking products


def insertion_sort(items):
    """Sort items in place, smallest first, using insertion sort."""
    for i in range(1, len(items)):
        value = items[i]
        j = i - 1
        while j >= 0 and items[j] > value:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = value


def merge(left, right):
    """Merge two sorted lists into one new sorted list. Take from left when they're equal."""
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(items):
    """Return a new sorted list, using merge sort. Don't change items."""
    if len(items) <= 1:
        return list(items)
    middle = len(items) // 2
    return merge(merge_sort(items[:middle]), merge_sort(items[middle:]))


def rank_products(products):
    """Return a new list of products: highest rating first, then most reviews, then name A to Z."""
    return sorted(products, key=lambda product: (-product["rating"], -product["reviews"], product["name"]))


def cheapest(products, count):
    """Return the names of the `count` cheapest products, cheapest first."""
    by_price = sorted(products, key=lambda product: product["price"])
    names = []
    for product in by_price[:count]:
        names.append(product["name"])
    return names


PRODUCTS = [
    {"name": "Travel mug", "rating": 4.6, "reviews": 1280, "price": 18.00},
    {"name": "Pour-over kettle", "rating": 4.8, "reviews": 312, "price": 54.99},
    {"name": "Burr grinder", "rating": 4.6, "reviews": 2045, "price": 89.00},
    {"name": "Paper filters", "rating": 4.4, "reviews": 870, "price": 6.50},
    {"name": "Coffee scale", "rating": 4.8, "reviews": 312, "price": 32.00},
    {"name": "Milk frother", "rating": 4.1, "reviews": 1990, "price": 24.99},
]


if __name__ == "__main__":
    prices = [24.99, 6.50, 89.00, 18.00, 54.99]
    insertion_sort(prices)
    print(prices)
    print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
    for product in rank_products(PRODUCTS):
        print(f"{product['rating']}  {product['reviews']:>5}  {product['name']}")
    print(cheapest(PRODUCTS, 3))

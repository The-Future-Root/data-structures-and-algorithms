# Lesson 7: sorting and ranking products
#
# Write insertion_sort, merge and merge_sort without sorted() or .sort().
# For rank_products and cheapest, use sorted() with a key, the way you would in real code.
# Test with:  python3 -m unittest -v


def insertion_sort(items):
    """Sort items in place, smallest first, using insertion sort."""
    pass


def merge(left, right):
    """Merge two sorted lists into one new sorted list. Take from left when they're equal."""
    pass


def merge_sort(items):
    """Return a new sorted list, using merge sort. Don't change items."""
    pass


def rank_products(products):
    """Return a new list of products: highest rating first, then most reviews, then name A to Z."""
    pass


def cheapest(products, count):
    """Return the names of the `count` cheapest products, cheapest first."""
    pass


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

import pathlib
import random
import time
import unittest

from exercise import MetroMap, load_map

HERE = pathlib.Path(__file__).parent


def city():
    return load_map(HERE / "metro.txt")


def grid(size):
    """A size x size grid of stations, each connected to the ones beside, above and below it."""
    metro = MetroMap()
    for row in range(size):
        for column in range(size):
            if column + 1 < size:
                metro.connect((row, column), (row, column + 1))
            if row + 1 < size:
                metro.connect((row, column), (row + 1, column))
    return metro


class TestBuilding(unittest.TestCase):
    def test_add_line(self):
        metro = MetroMap()
        metro.add_line(["A", "B", "C"])
        self.assertEqual(metro.stations(), ["A", "B", "C"])
        self.assertEqual(metro.neighbours("B"), ["A", "C"], "Each station connects to the next, in both directions")
        self.assertEqual(metro.neighbours("A"), ["B"])

    def test_city(self):
        metro = city()
        self.assertEqual(len(metro.stations()), 12)
        self.assertEqual(metro.neighbours("Central"), ["Market Street", "Old Town", "Park Lane", "University"])
        self.assertEqual(metro.neighbours("Hospital"), ["Riverside"])


class TestFewestStops(unittest.TestCase):
    def test_routes(self):
        metro = city()
        self.assertEqual(metro.fewest_stops("Northgate", "Stadium"), ["Northgate", "University", "Central", "Old Town", "Stadium"])
        self.assertEqual(metro.fewest_stops("Airport", "Hospital"), ["Airport", "Park Lane", "Central", "Old Town", "Riverside", "Hospital"])
        self.assertEqual(metro.fewest_stops("Harbour", "Market Street"), ["Harbour", "Market Street"])

    def test_same_station(self):
        self.assertEqual(city().fewest_stops("Museum", "Museum"), ["Museum"])

    def test_no_route(self):
        metro = city()
        metro.add_line(["Depot", "Sidings"])
        self.assertIsNone(metro.fewest_stops("Central", "Depot"))
        self.assertIsNone(metro.fewest_stops("Central", "Nowhere"), "A station that isn't on the map has no route")

    def test_shortest_not_first_found(self):
        metro = MetroMap()
        metro.add_line(["A", "B", "C", "D", "E"])
        metro.connect("A", "Z")
        metro.connect("Z", "E")
        self.assertEqual(metro.fewest_stops("A", "E"), ["A", "Z", "E"], "Breadth-first search finds the fewest stops, even if another route was explored first")

    def test_grid(self):
        metro = grid(30)
        route = metro.fewest_stops((0, 0), (29, 29))
        self.assertEqual(len(route), 59, "Corner to corner on a 30 x 30 grid takes 58 stops")
        for a, b in zip(route, route[1:]):
            self.assertIn(b, metro.neighbours(a), "Each step of the route must be one stop")

    def test_fast(self):
        metro = grid(100)
        start = time.perf_counter()
        route = metro.fewest_stops((0, 0), (99, 99))
        self.assertEqual(len(route), 199)
        self.assertLess(time.perf_counter() - start, 1.0, "Too slow: use a set or dict to remember visited stations, and a deque for the queue")


class TestReachable(unittest.TestCase):
    def test_everything_open(self):
        metro = city()
        self.assertEqual(metro.reachable("Harbour"), set(metro.stations()))

    def test_closed_station(self):
        metro = city()
        self.assertEqual(metro.reachable("Harbour", closed={"Central"}), {"Harbour", "Market Street"})
        self.assertEqual(metro.reachable("Stadium", closed={"Old Town"}), {"Stadium"})
        cut_off = metro.reachable("Northgate", closed={"Central", "Riverside"})
        self.assertEqual(cut_off, {"Northgate", "University", "Museum", "Old Town", "Stadium"})

    def test_start_closed_or_missing(self):
        metro = city()
        self.assertEqual(metro.reachable("Central", closed={"Central"}), set())
        self.assertEqual(metro.reachable("Nowhere"), set())

    def test_big_random(self):
        rng = random.Random(9)
        metro = grid(60)
        closed = {(rng.randrange(60), rng.randrange(60)) for _ in range(300)}
        closed.discard((0, 0))
        reached = metro.reachable((0, 0), closed)
        self.assertFalse(reached & closed)
        for station in reached:
            if station != (0, 0):
                self.assertTrue(any(n in reached for n in metro.neighbours(station)))

    def test_fast(self):
        metro = grid(100)
        start = time.perf_counter()
        self.assertEqual(len(metro.reachable((0, 0))), 10_000)
        self.assertLess(time.perf_counter() - start, 1.0, "Too slow: use a set to remember which stations you've seen")


if __name__ == "__main__":
    unittest.main()

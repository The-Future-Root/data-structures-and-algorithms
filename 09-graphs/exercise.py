# Lesson 9: routes on a metro map
#
# __init__, add_station, connect, stations and load_map are written for you.
# Test with:  python3 -m unittest -v

from collections import deque


class MetroMap:
    """An undirected graph of metro stations, stored as an adjacency list."""

    def __init__(self):
        """Start with no stations."""
        self._links = {}

    def add_station(self, station):
        """Add a station with no connections, if it isn't there already."""
        if station not in self._links:
            self._links[station] = set()

    def connect(self, a, b):
        """Connect two stations in both directions, adding them if needed."""
        self.add_station(a)
        self.add_station(b)
        self._links[a].add(b)
        self._links[b].add(a)

    def add_line(self, stations):
        """Connect each station in the list to the next one."""
        pass

    def stations(self):
        """Return a sorted list of every station."""
        return sorted(self._links)

    def neighbours(self, station):
        """Return a sorted list of the stations one stop away."""
        pass

    def fewest_stops(self, start, goal):
        """Return the route with the fewest stops as a list of stations, or None if there's no route.
        Explore neighbours in alphabetical order."""
        pass

    def reachable(self, start, closed=()):
        """Return the set of stations you can reach from start without passing through a closed station."""
        pass


def load_map(path):
    """Read a file of lines like 'Red: Northgate, University, Central' and return a MetroMap."""
    metro = MetroMap()
    with open(path) as file:
        for line in file:
            if ":" in line:
                _, stops = line.split(":", 1)
                names = []
                for name in stops.split(","):
                    names.append(name.strip())
                metro.add_line(names)
    return metro


if __name__ == "__main__":
    metro = load_map("metro.txt")
    print(len(metro.stations()), "stations")
    print(metro.neighbours("Central"))
    print(" -> ".join(metro.fewest_stops("Northgate", "Stadium")))
    print(" -> ".join(metro.fewest_stops("Airport", "Hospital")))
    print(sorted(metro.reachable("Harbour", closed={"Central"})))

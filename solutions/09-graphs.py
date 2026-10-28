# Solution to lesson 9: routes on a metro map

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
        for i in range(len(stations) - 1):
            self.connect(stations[i], stations[i + 1])

    def stations(self):
        """Return a sorted list of every station."""
        return sorted(self._links)

    def neighbours(self, station):
        """Return a sorted list of the stations one stop away."""
        return sorted(self._links[station])

    def fewest_stops(self, start, goal):
        """Return the route with the fewest stops as a list of stations, or None if there's no route.
        Explore neighbours in alphabetical order."""
        if start not in self._links or goal not in self._links:
            return None
        came_from = {start: None}
        queue = deque([start])
        while queue:
            station = queue.popleft()
            if station == goal:
                route = []
                while station is not None:
                    route.append(station)
                    station = came_from[station]
                route.reverse()
                return route
            for neighbour in self.neighbours(station):
                if neighbour not in came_from:
                    came_from[neighbour] = station
                    queue.append(neighbour)
        return None

    def reachable(self, start, closed=()):
        """Return the set of stations you can reach from start without passing through a closed station."""
        if start not in self._links or start in closed:
            return set()
        seen = {start}
        stack = [start]
        while stack:
            station = stack.pop()
            for neighbour in self._links[station]:
                if neighbour not in seen and neighbour not in closed:
                    seen.add(neighbour)
                    stack.append(neighbour)
        return seen


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

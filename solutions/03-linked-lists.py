# Solution to lesson 3: a playlist as a linked list


class Node:
    """One song in the playlist: a title, and a link to the next node."""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Playlist:
    """A singly linked list of song titles."""

    def __init__(self):
        """Start empty: head and tail are None, and the size is 0."""
        self.head = None
        self.tail = None
        self._size = 0

    def add(self, title):
        """Add a song at the end, in O(1)."""
        node = Node(title)
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self._size += 1

    def play_next(self, title):
        """Add a song at the front, in O(1)."""
        self.head = Node(title, self.head)
        if self.tail is None:
            self.tail = self.head
        self._size += 1

    def remove(self, title):
        """Remove the first song with this title. Return True, or False if it isn't there."""
        if self.head is None:
            return False
        if self.head.value == title:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self._size -= 1
            return True
        previous = self.head
        current = self.head.next
        while current is not None:
            if current.value == title:
                previous.next = current.next
                if current is self.tail:
                    self.tail = previous
                self._size -= 1
                return True
            previous = current
            current = current.next
        return False

    def contains(self, title):
        """Return True if the song is in the playlist."""
        node = self.head
        while node is not None:
            if node.value == title:
                return True
            node = node.next
        return False

    def __len__(self):
        """Return the number of songs, in O(1)."""
        return self._size

    def __iter__(self):
        """Go through the titles in order."""
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def to_list(self):
        """Return a normal Python list of the titles, in order."""
        titles = []
        for title in self:
            titles.append(title)
        return titles

    def reverse(self):
        """Reverse the playlist in place by relinking the nodes."""
        previous = None
        node = self.head
        while node is not None:
            following = node.next
            node.next = previous
            previous = node
            node = following
        self.head, self.tail = self.tail, self.head


if __name__ == "__main__":
    playlist = Playlist()
    playlist.add("Blue Monday")
    playlist.add("Hey Jude")
    playlist.add("Clocks")
    playlist.play_next("Yellow")
    playlist.remove("Hey Jude")
    print(playlist.to_list())
    playlist.reverse()
    print(playlist.to_list(), len(playlist))

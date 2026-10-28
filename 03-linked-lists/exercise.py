# Lesson 3: a playlist as a linked list
#
# The Node class is written for you. Build Playlist out of nodes:
# don't keep the songs in a Python list inside it.
# Test with:  python3 -m unittest -v


class Node:
    """One song in the playlist: a title, and a link to the next node."""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Playlist:
    """A singly linked list of song titles."""

    def __init__(self):
        """Start empty: head and tail are None, and the size is 0."""
        pass

    def add(self, title):
        """Add a song at the end, in O(1)."""
        pass

    def play_next(self, title):
        """Add a song at the front, in O(1)."""
        pass

    def remove(self, title):
        """Remove the first song with this title. Return True, or False if it isn't there."""
        pass

    def contains(self, title):
        """Return True if the song is in the playlist."""
        pass

    def __len__(self):
        """Return the number of songs, in O(1)."""
        pass

    def __iter__(self):
        """Go through the titles in order."""
        pass

    def to_list(self):
        """Return a normal Python list of the titles, in order."""
        pass

    def reverse(self):
        """Reverse the playlist in place by relinking the nodes."""
        pass


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

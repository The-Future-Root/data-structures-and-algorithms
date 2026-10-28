import time
import unittest

from exercise import Node, Playlist

BIG = 20_000


def make(*titles):
    playlist = Playlist()
    for title in titles:
        playlist.add(title)
    return playlist


def walk(playlist):
    """Follow the links from head, so the tests check the real nodes."""
    titles = []
    node = playlist.head
    while node is not None:
        titles.append(node.value)
        node = node.next
    return titles


class TestEmpty(unittest.TestCase):
    def test_empty(self):
        playlist = Playlist()
        self.assertIsNone(playlist.head)
        self.assertIsNone(playlist.tail)
        self.assertEqual(len(playlist), 0)
        self.assertEqual(playlist.to_list(), [])


class TestAdd(unittest.TestCase):
    def test_add_links_nodes(self):
        playlist = make("Blue Monday", "Hey Jude", "Clocks")
        self.assertIsInstance(playlist.head, Node, "head should be a Node")
        self.assertEqual(walk(playlist), ["Blue Monday", "Hey Jude", "Clocks"])
        self.assertEqual(playlist.tail.value, "Clocks")
        self.assertIsNone(playlist.tail.next, "The last node's next should be None")

    def test_play_next(self):
        playlist = make("Blue Monday", "Hey Jude")
        playlist.play_next("Yellow")
        self.assertEqual(walk(playlist), ["Yellow", "Blue Monday", "Hey Jude"])
        self.assertEqual(playlist.tail.value, "Hey Jude")

    def test_play_next_on_empty(self):
        playlist = Playlist()
        playlist.play_next("Yellow")
        playlist.add("Clocks")
        self.assertEqual(walk(playlist), ["Yellow", "Clocks"])
        self.assertEqual(playlist.tail.value, "Clocks")

    def test_no_python_list_inside(self):
        playlist = make("a", "b", "c")
        for name, value in vars(playlist).items():
            self.assertNotIsInstance(value, (list, tuple, dict), f"Don't store the songs in self.{name}; link Node objects")


class TestLenAndIter(unittest.TestCase):
    def test_len(self):
        playlist = make("a", "b")
        playlist.play_next("c")
        self.assertEqual(len(playlist), 3)
        playlist.remove("a")
        self.assertEqual(len(playlist), 2)
        playlist.remove("zzz")
        self.assertEqual(len(playlist), 2)

    def test_iter(self):
        playlist = make("a", "b", "c")
        self.assertEqual([title for title in playlist], ["a", "b", "c"])
        self.assertEqual(playlist.to_list(), ["a", "b", "c"])

    def test_contains(self):
        playlist = make("Blue Monday", "Clocks")
        self.assertTrue(playlist.contains("Clocks"))
        self.assertFalse(playlist.contains("Yellow"))
        self.assertFalse(Playlist().contains("Yellow"))


class TestRemove(unittest.TestCase):
    def test_remove_middle(self):
        playlist = make("Blue Monday", "Hey Jude", "Clocks")
        self.assertTrue(playlist.remove("Hey Jude"))
        self.assertEqual(walk(playlist), ["Blue Monday", "Clocks"])

    def test_remove_head(self):
        playlist = make("Blue Monday", "Hey Jude")
        self.assertTrue(playlist.remove("Blue Monday"))
        self.assertEqual(walk(playlist), ["Hey Jude"])

    def test_remove_tail_updates_tail(self):
        playlist = make("Blue Monday", "Hey Jude", "Clocks")
        self.assertTrue(playlist.remove("Clocks"))
        self.assertEqual(playlist.tail.value, "Hey Jude")
        playlist.add("Yellow")
        self.assertEqual(walk(playlist), ["Blue Monday", "Hey Jude", "Yellow"], "After removing the last song, tail must point at the new last node")

    def test_remove_only_song(self):
        playlist = make("Clocks")
        self.assertTrue(playlist.remove("Clocks"))
        self.assertIsNone(playlist.head)
        self.assertIsNone(playlist.tail)
        playlist.add("Yellow")
        self.assertEqual(walk(playlist), ["Yellow"])

    def test_remove_first_match_only(self):
        playlist = make("a", "b", "a")
        playlist.remove("a")
        self.assertEqual(walk(playlist), ["b", "a"])

    def test_remove_missing(self):
        self.assertFalse(make("a", "b").remove("z"))
        self.assertFalse(Playlist().remove("z"))


class TestReverse(unittest.TestCase):
    def test_reverse(self):
        playlist = make("a", "b", "c", "d")
        head_node = playlist.head
        playlist.reverse()
        self.assertEqual(walk(playlist), ["d", "c", "b", "a"])
        self.assertIs(playlist.tail, head_node, "Reverse by relinking the same nodes, not by making new ones")
        self.assertIsNone(playlist.tail.next)
        playlist.add("e")
        self.assertEqual(walk(playlist), ["d", "c", "b", "a", "e"])

    def test_reverse_small(self):
        empty = Playlist()
        empty.reverse()
        self.assertEqual(walk(empty), [])
        one = make("a")
        one.reverse()
        self.assertEqual(walk(one), ["a"])


class TestSpeed(unittest.TestCase):
    def test_add_and_play_next_are_fast(self):
        playlist = Playlist()
        start = time.perf_counter()
        for i in range(BIG):
            playlist.add(i)
            playlist.play_next(-i)
        seconds = time.perf_counter() - start
        self.assertEqual(len(playlist), 2 * BIG)
        self.assertLess(seconds, 2.0, "Too slow: add and play_next should be O(1). Use the tail reference instead of walking to the end")

    def test_len_is_fast(self):
        playlist = make(*range(20_000))
        start = time.perf_counter()
        for _ in range(5_000):
            len(playlist)
        self.assertLess(time.perf_counter() - start, 1.0, "Too slow: keep a size counter instead of counting the nodes")


if __name__ == "__main__":
    unittest.main()

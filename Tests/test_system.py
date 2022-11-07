import unittest
from Interperter.mouse_interperter import main


class TestInterperter(unittest.TestCase):
    def test_interperter_marco(self):
        self.assertEqual(main(
            "10 N = #A N . 1 - N = N . ! N . [ @ ] ~A @ $ $$")[0], "9 8 7 6 5 4 3 2 1 0 ")

    def test_interperter_basic(self):
        self.assertEqual(main("1 2 3 + + ! $$")[0], "6 ")
        self.assertEqual(main("\"Hello World.\" $$")[0], "Hello World. ")

    def test_interperter_loop(self):
        self.assertEqual(main(
            "10 to_do = ( to_do . ! to_do . 1 - to_do = to_do . [ ^ ] ) \"Done\" $$")[0], "10 9 8 7 6 5 4 3 2 1 Done ")

    def test_interperter_fib(self):
        self.assertEqual(main("\"Printing first 10 in fibonacci:\" 19 todo = 1 1 \"0\" #A to_save = to_print = to_save . to_save . to_print . + to_print . ! todo . 1 - todo = todo . [ @ ] ~A @ $ $$")[
                         0], "Printing first 10 in fibonacci: 0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 ")

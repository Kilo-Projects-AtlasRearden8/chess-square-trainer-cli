"""Tests for chess board square parsing and color logic."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from board import DARK, LIGHT, all_squares, parse_square, square_color, square_name


class TestParseSquare(unittest.TestCase):
    def test_valid_squares(self):
        cases = {
            "a1": (0, 0),
            "h1": (7, 0),
            "a8": (0, 7),
            "h8": (7, 7),
            "e4": (4, 3),
            "d5": (3, 4),
        }
        for square, expected in cases.items():
            self.assertEqual(parse_square(square), expected)

    def test_invalid_squares(self):
        invalid = ["", "i9", "a", "a11", "e4extra", " ", "A1", "a0", "a9", None, 5, 3.14]
        for square in invalid:
            self.assertIsNone(parse_square(square))

    def test_lowercase_only(self):
        # Square notation is lowercase in this module.
        self.assertIsNone(parse_square("E4"))
        self.assertIsNone(parse_square("E4"))


class TestSquareName(unittest.TestCase):
    def test_round_trip_all_squares(self):
        for file_index in range(8):
            for rank_index in range(8):
                name = square_name(file_index, rank_index)
                self.assertEqual(parse_square(name), (file_index, rank_index))

    def test_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            square_name(8, 0)
        with self.assertRaises(ValueError):
            square_name(0, 8)


class TestSquareColor(unittest.TestCase):
    def test_corners(self):
        # a1 is dark from White's perspective; colors alternate.
        self.assertEqual(square_color(0, 0), DARK)
        self.assertEqual(square_color(7, 0), LIGHT)
        self.assertEqual(square_color(0, 7), LIGHT)
        self.assertEqual(square_color(7, 7), DARK)

    def test_alternation(self):
        self.assertEqual(square_color(4, 3), LIGHT)  # e4
        self.assertEqual(square_color(3, 4), LIGHT)  # d5
        self.assertEqual(square_color(4, 4), DARK)   # e5
        self.assertEqual(square_color(3, 3), DARK)   # d4

    def test_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            square_color(8, 0)


class TestAllSquares(unittest.TestCase):
    def test_count_and_uniqueness(self):
        squares = all_squares()
        self.assertEqual(len(squares), 64)
        self.assertEqual(len(set(squares)), 64)


if __name__ == "__main__":
    unittest.main()

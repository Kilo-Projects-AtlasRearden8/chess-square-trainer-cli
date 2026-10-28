"""Tests for local JSON accuracy tracking."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stats import (
    DEFAULT_STATS_FILE,
    accuracy,
    empty_stats,
    load_stats,
    record,
    save_stats,
    square_accuracy,
)


class TestStats(unittest.TestCase):
    def test_empty_stats_structure(self):
        data = empty_stats()
        self.assertEqual(data, {"squares": {}, "total": {"correct": 0, "wrong": 0}})

    def test_accuracy_no_data(self):
        self.assertEqual(accuracy(empty_stats()), 0.0)

    def test_record_updates_square_and_total(self):
        data = empty_stats()
        record(data, "e4", True)
        record(data, "e4", True)
        record(data, "e4", False)
        record(data, "d5", True)

        self.assertEqual(data["squares"]["e4"], {"correct": 2, "wrong": 1})
        self.assertEqual(data["squares"]["d5"], {"correct": 1, "wrong": 0})
        self.assertEqual(data["total"], {"correct": 3, "wrong": 1})

    def test_accuracy_after_records(self):
        data = empty_stats()
        record(data, "e4", True)
        record(data, "e4", True)
        record(data, "e4", False)
        self.assertAlmostEqual(accuracy(data), 2 / 3)

    def test_square_accuracy_untracked_is_none(self):
        self.assertIsNone(square_accuracy(empty_stats(), "e4"))

    def test_save_and_load_round_trip(self):
        data = empty_stats()
        record(data, "a1", True)
        record(data, "a1", False)

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "stats.json")
            save_stats(path, data)
            with open(path, "r", encoding="utf-8") as handle:
                reloaded = json.load(handle)
            self.assertEqual(reloaded["total"], {"correct": 1, "wrong": 1})
            loaded = load_stats(path)
            self.assertEqual(loaded["total"], {"correct": 1, "wrong": 1})
            self.assertEqual(loaded["squares"]["a1"], {"correct": 1, "wrong": 1})

    def test_load_missing_file_returns_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "missing.json")
            data = load_stats(path)
            self.assertEqual(data, empty_stats())

    def test_default_stats_file_constant(self):
        self.assertEqual(DEFAULT_STATS_FILE, "chess_stats.json")


if __name__ == "__main__":
    unittest.main()

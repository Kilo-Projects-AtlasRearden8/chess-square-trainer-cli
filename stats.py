"""Local JSON accuracy tracking for the chess square trainer.

All training history stays on the user's machine in a plain JSON file.
No accounts, no network, no personal data.
"""

import json
import os

DEFAULT_STATS_FILE = "chess_stats.json"


class StatsError(Exception):
    """Raised when the stats file cannot be read or written."""


def empty_stats():
    """Return a fresh stats document."""
    return {"squares": {}, "total": {"correct": 0, "wrong": 0}}


def load_stats(path):
    """Load stats from ``path``.

    Missing or unreadable files yield a fresh stats document so training can
    start without any setup.
    """
    if not os.path.exists(path):
        return empty_stats()
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError) as exc:
        raise StatsError("cannot read stats file %s: %s" % (path, exc))
    if not isinstance(data, dict):
        raise StatsError("stats file %s does not contain a JSON object" % path)
    squares = data.get("squares", {})
    total = data.get("total", {})
    if not isinstance(squares, dict) or not isinstance(total, dict):
        raise StatsError("stats file %s has an unexpected structure" % path)
    total.setdefault("correct", 0)
    total.setdefault("wrong", 0)
    cleaned = {"squares": {}, "total": total}
    for square, entry in squares.items():
        if not isinstance(entry, dict):
            continue
        entry = dict(entry)
        entry.setdefault("correct", 0)
        entry.setdefault("wrong", 0)
        cleaned["squares"][square] = entry
    return cleaned


def save_stats(path, data):
    """Persist stats to ``path`` atomically."""
    directory = os.path.dirname(os.path.abspath(path))
    try:
        tmp_path = path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(tmp_path, path)
    except OSError as exc:
        raise StatsError("cannot write stats file %s: %s" % (path, exc))


def record(data, square, correct):
    """Record one answered drill question in ``data`` (mutates in place)."""
    squares = data.setdefault("squares", {})
    entry = squares.setdefault(square, {"correct": 0, "wrong": 0})
    total = data.setdefault("total", {"correct": 0, "wrong": 0})
    if correct:
        entry["correct"] = int(entry.get("correct", 0)) + 1
        total["correct"] = int(total.get("correct", 0)) + 1
    else:
        entry["wrong"] = int(entry.get("wrong", 0)) + 1
        total["wrong"] = int(total.get("wrong", 0)) + 1


def accuracy(data):
    """Return overall accuracy as a float in [0, 1], or 0.0 with no data."""
    total = data.get("total", {})
    correct = int(total.get("correct", 0))
    wrong = int(total.get("wrong", 0))
    count = correct + wrong
    if count == 0:
        return 0.0
    return correct / count


def square_accuracy(data, square):
    """Return accuracy for a single square, or None if never drilled."""
    entry = data.get("squares", {}).get(square)
    if not entry:
        return None
    correct = int(entry.get("correct", 0))
    wrong = int(entry.get("wrong", 0))
    count = correct + wrong
    if count == 0:
        return None
    return correct / count

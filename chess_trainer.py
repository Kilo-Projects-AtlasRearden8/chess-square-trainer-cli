"""Chess square trainer CLI.

Drill chess board coordinates and square colors. Accuracy is tracked in a
local JSON file. No accounts, no network, no game assets.

Usage:
    python chess_trainer.py drill --count 10 --mode color
    python chess_trainer.py quiz --count 20 --mode mixed
    python chess_trainer.py stats --stats-file chess_stats.json

Run as a module: python -m chess_trainer
"""

import argparse
import random
import sys

from board import (
    DARK,
    LIGHT,
    NUM_FILES,
    NUM_RANKS,
    all_squares,
    parse_square,
    square_color,
    square_name,
)
from stats import DEFAULT_STATS_FILE, accuracy, load_stats, record, save_stats

QUIT_COMMANDS = {"q", "quit", "exit"}


def normalize_color(answer):
    """Map a user answer to ``"light"``/``"dark"`` or None if unrecognized."""
    answer = answer.strip().lower()
    if answer in {"light", "l"}:
        return LIGHT
    if answer in {"dark", "d"}:
        return DARK
    return None


def prompt(prompt_text):
    """Read one line from stdin, returning None on EOF or a quit command."""
    try:
        line = input(prompt_text)
    except EOFError:
        print()
        return None
    if line.strip().lower() in QUIT_COMMANDS:
        return None
    return line


def drill_color(square_name_str):
    """Run one color drill question. Returns True if the user answered correctly."""
    expected = square_color(*parse_square(square_name_str))
    answer = prompt("What color is %s? (light/dark) " % square_name_str)
    if answer is None:
        return None
    guess = normalize_color(answer)
    if guess is None:
        print("  Unrecognized answer. It was %s." % expected)
        return False
    if guess == expected:
        print("  Correct!")
        return True
    print("  Incorrect. %s is %s." % (square_name_str, expected))
    return False


def drill_coordinate(expected_color):
    """Run one coordinate drill question. Returns True if answered correctly."""
    answer = prompt("Name a %s square: " % expected_color)
    if answer is None:
        return None
    parsed = parse_square(answer)
    if parsed is None:
        print("  Not a valid square (like e4). It should have been %s." % expected_color)
        return False
    actual = square_color(*parsed)
    if actual == expected_color:
        print("  Correct! %s is %s." % (answer, actual))
        return True
    print("  Incorrect. %s is %s, not %s." % (answer, actual, expected_color))
    return False


def run_drill(args):
    """Run an interactive drill session and persist accuracy to JSON."""
    data = load_stats(args.stats_file)
    squares = all_squares()
    rng = random.Random(args.seed)

    count = args.count
    done = 0
    session_correct = 0
    session_total = 0

    print("Chess square trainer - drill mode")
    print("Squares: %d | Mode: %s | Questions: %d" % (len(squares), args.mode, count))
    print("Stats file: %s" % args.stats_file)
    print("Type 'q' to quit at any time.\n")

    try:
        while done < count:
            file_index, rank_index = rng.choice(squares)
            name = square_name(file_index, rank_index)

            if args.mode == "color":
                question_color = square_color(file_index, rank_index)
                prompt_text = "[%d/%d] What color is %s? (light/dark) " % (
                    done + 1,
                    count,
                    name,
                )
                answer = prompt(prompt_text)
                if answer is None:
                    break
                guess = normalize_color(answer)
                if guess is None:
                    print("    Unrecognized answer. It was %s." % question_color)
                    correct = False
                else:
                    correct = guess == question_color
                    if correct:
                        print("    Correct!")
                    else:
                        print("    Incorrect. %s is %s." % (name, question_color))
            elif args.mode == "coordinate":
                expected_color = rng.choice([LIGHT, DARK])
                prompt_text = "[%d/%d] Name a %s square: " % (
                    done + 1,
                    count,
                    expected_color,
                )
                answer = prompt(prompt_text)
                if answer is None:
                    break
                parsed = parse_square(answer)
                if parsed is None:
                    print("    Not a valid square (like e4).")
                    correct = False
                else:
                    actual = square_color(*parsed)
                    correct = actual == expected_color
                    if correct:
                        print("    Correct! %s is %s." % (answer, actual))
                    else:
                        print(
                            "    Incorrect. %s is %s, not %s."
                            % (answer, actual, expected_color)
                        )
            else:  # mixed
                if rng.random() < 0.5:
                    question_color = square_color(file_index, rank_index)
                    prompt_text = "[%d/%d] What color is %s? (light/dark) " % (
                        done + 1,
                        count,
                        name,
                    )
                    answer = prompt(prompt_text)
                    if answer is None:
                        break
                    guess = normalize_color(answer)
                    if guess is None:
                        print("    Unrecognized answer. It was %s." % question_color)
                        correct = False
                    else:
                        correct = guess == question_color
                        if correct:
                            print("    Correct!")
                        else:
                            print(
                                "    Incorrect. %s is %s." % (name, question_color)
                            )
                else:
                    expected_color = rng.choice([LIGHT, DARK])
                    prompt_text = "[%d/%d] Name a %s square: " % (
                        done + 1,
                        count,
                        expected_color,
                    )
                    answer = prompt(prompt_text)
                    if answer is None:
                        break
                    parsed = parse_square(answer)
                    if parsed is None:
                        print("    Not a valid square (like e4).")
                        correct = False
                    else:
                        actual = square_color(*parsed)
                        correct = actual == expected_color
                        if correct:
                            print("    Correct! %s is %s." % (answer, actual))
                        else:
                            print(
                                "    Incorrect. %s is %s, not %s."
                                % (answer, actual, expected_color)
                            )

            record(data, name, correct)
            done += 1
            session_total += 1
            if correct:
                session_correct += 1
            save_stats(args.stats_file, data)
            acc = accuracy(data)
            print(
                "    Session: %d/%d | Overall accuracy: %.0f%%\n"
                % (session_correct, session_total, acc * 100)
            )
    except KeyboardInterrupt:
        print("\nInterrupted.")

    print("Session complete: %d/%d correct." % (session_correct, session_total))
    print("Overall accuracy: %.0f%% (%s)" % (accuracy(data) * 100, args.stats_file))
    return 0


def run_stats(args):
    """Print an accuracy summary from the stats file."""
    try:
        data = load_stats(args.stats_file)
    except Exception as exc:  # StatsError or file issues
        print("Error loading stats: %s" % exc)
        return 1

    total = data.get("total", {})
    correct = int(total.get("correct", 0))
    wrong = int(total.get("wrong", 0))
    count = correct + wrong

    print("Chess square trainer - stats")
    print("Stats file: %s" % args.stats_file)
    print("Total questions: %d" % count)
    print("Correct: %d" % correct)
    print("Wrong:   %d" % wrong)
    if count:
        print("Accuracy: %.1f%%" % (accuracy(data) * 100))
    else:
        print("Accuracy: n/a (no questions answered yet)")

    squares = data.get("squares", {})
    if squares and args.worst:
        ranked = []
        for square, entry in squares.items():
            c = int(entry.get("correct", 0))
            w = int(entry.get("wrong", 0))
            n = c + w
            if n:
                ranked.append((c / n, n, c, square))
        ranked.sort()
        print("\nSquares needing the most work:")
        for acc, n, c, square in ranked[: args.worst]:
            print("  %s: %.0f%% (%d correct / %d total)" % (square, acc * 100, c, n))
    elif squares:
        print("\nTracked squares: %d" % len(squares))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="chess_trainer.py",
        description="Drill chess board coordinates and square colors. "
        "Accuracy is tracked in a local JSON file.",
    )
    parser.add_argument(
        "--stats-file",
        default=DEFAULT_STATS_FILE,
        help="Path to the JSON stats file (default: %s)" % DEFAULT_STATS_FILE,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    drill_parser = subparsers.add_parser("drill", help="Run an interactive drill session")
    drill_parser.add_argument(
        "--count", type=int, default=10, help="Number of questions (default: 10)"
    )
    drill_parser.add_argument(
        "--mode",
        choices=["color", "coordinate", "mixed"],
        default="mixed",
        help="Drill mode: color, coordinate, or mixed (default: mixed)",
    )
    drill_parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for repeatable sessions"
    )
    drill_parser.set_defaults(func=run_drill)

    quiz_parser = subparsers.add_parser("quiz", help="Alias for drill (quiz mode)")
    quiz_parser.add_argument("--count", type=int, default=10)
    quiz_parser.add_argument(
        "--mode", choices=["color", "coordinate", "mixed"], default="mixed"
    )
    quiz_parser.add_argument("--seed", type=int, default=None)
    quiz_parser.set_defaults(func=run_drill)

    stats_parser = subparsers.add_parser("stats", help="Show accuracy summary")
    stats_parser.add_argument(
        "--worst", type=int, default=0, help="Show N squares with the lowest accuracy"
    )
    stats_parser.set_defaults(func=run_stats)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

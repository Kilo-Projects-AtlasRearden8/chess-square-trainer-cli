# Chess Square Trainer CLI

A small, local-first Python command-line tool for drilling chess board
coordinates and square colors. Accuracy is tracked in a local JSON file.

**No game assets. No accounts. No internet. No secrets.** Uses only the
Python standard library, so there is nothing to install and nothing leaves
your machine.

Built by **Dylan Asdale** for **Asdale Dynamics, LLC** (Indiana, formed
October 2026), author of *The Massive AI Manual* and founder of
dylanasdale.github.io. This is a fan project shared in the same clear,
step-by-step, never-condescending style as the LLC's beginner-friendly AI
education and practical tools.

## What it does

- **Color drill** — you are shown a square such as `e4` and answer
  `light` or `dark`.
- **Coordinate drill** — you are told a color and must name *any* square of
  that color (for example, `a1` is dark).
- **Mixed drill** — alternates between the two question types.
- **Accuracy tracking** — every answer is recorded per square and overall in
  a plain `chess_stats.json` file, saved after each question so a quick
  quit never loses your progress.
- **Stats review** — see your overall percentage, or list the squares you
  struggle with most.

## Requirements

Python 3 (developed on 3.13). No dependencies.

## Quick start

```bash
# 10 mixed questions (great first drill)
python3 chess_trainer.py drill --count 10 --mode mixed

# 20 color-only questions
python3 chess_trainer.py drill --count 20 --mode color

# 20 coordinate-only questions ("name a dark square")
python3 chess_trainer.py drill --count 20 --mode coordinate

# "quiz" is a friendly alias for "drill"
python3 chess_trainer.py quiz --count 10 --mode mixed

# Review your accuracy
python3 chess_trainer.py stats

# Review your 5 weakest squares
python3 chess_trainer.py stats --worst 5

# Type 'q' (or quit / exit) at any prompt to stop and save your progress
```

You can also run it as a module:

```bash
python3 -m chess_trainer drill --count 10 --mode color
```

### Using a different stats file

The `--stats-file` option is global, so it comes *before* the subcommand.

```bash
python3 chess_trainer.py --stats-file my_stats.json drill --count 10
python3 chess_trainer.py --stats-file my_stats.json stats --worst 5
```

Stats files are plain JSON. The default, `chess_stats.json`, is created next
to wherever you run the tool. It is ignored by git via `.gitignore`.

## Tips for low-energy / ADHD-friendly use

- Start with `--count 5` or even `--count 3` and quit any time. Progress
  is always saved.
- Use `--seed 1` for a repeatable sequence when you want to re-drill the
  same squares.
- `--mode color` keeps the cognitive load lowest; work up to `mixed`.
- `stats --worst 5` makes review fast: just fix a handful of trouble squares
  per session.

## How accuracy is scored

From White's perspective, `a1` is a dark square. For a square whose file
index is `f` (0–7 for a–h) and rank index is `r` (0–7 for 1–8), the color is
`light` when `(f + r)` is odd and `dark` when it is even.

## Testing

```bash
python3 -m unittest discover -s tests
```

Tests cover square parsing (valid and invalid inputs, case sensitivity),
square colors, naming round-trips across all 64 squares, full enumeration,
and JSON accuracy tracking (records, overall accuracy, save/load round trip,
missing-file handling).

## Files

| File | Purpose |
| --- | --- |
| `board.py` | Square parsing, naming, and light/dark color logic |
| `stats.py` | Local JSON accuracy tracking with atomic saves |
| `chess_trainer.py` | Command-line interface (`drill`, `quiz`, `stats`) |
| `tests/test_board.py` | Tests for square parsing and colors |
| `tests/test_stats.py` | Tests for JSON accuracy tracking |
| `STATUS.md` | Build/run/verification notes |
| `LICENSE` | MIT License |

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See [LICENSE](LICENSE).

## Credit

Created by **Dylan Asdale** for **Asdale Dynamics, LLC**. Learn about
beginner-friendly AI, books, and practical tools at
[dylanasdale.github.io](https://dylanasdale.github.io) and in *The Massive
AI Manual*.

This is an unofficial fan project. It is not affiliated with any chess
organization.

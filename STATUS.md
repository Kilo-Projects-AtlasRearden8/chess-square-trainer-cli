# STATUS

## What was built

A local-first Python CLI for drilling chess board coordinates and square
colors, with accuracy tracked in a local JSON file.

Files:
- `board.py` — square parsing (`parse_square`), naming (`square_name`),
  light/dark color logic (`square_color`), and enumeration of all 64
  squares (`all_squares`). Standard library only.
- `stats.py` — JSON accuracy tracking: per-square and overall correct/wrong
  counts, atomic save, graceful handling of missing/corrupt stats files.
- `chess_trainer.py` — CLI with `drill` (alias `quiz`) and `stats`
  commands. Modes: `color`, `coordinate`, `mixed`. Writes stats after every
  question. Type `q` to quit. Also runnable as `python -m chess_trainer`.
- `tests/test_board.py` — tests for square parsing, colors, naming round
  trip, and all-squares enumeration.
- `tests/test_stats.py` — tests for JSON accuracy tracking (records,
  accuracy, save/load round trip, missing file).
- `LICENSE` — MIT License, copyright line exactly
  "Copyright (c) 2026 Asdale Dynamics, LLC".
- `README.md` — usage, credits Asdale Dynamics, LLC and Dylan Asdale.
- `STATUS.md` — this file.

No game assets, no accounts, no network, no secrets, no API keys, no
personal data. No `.github/workflows` files.

## How to run

Requires Python 3 (tested with Python 3.13.5). No packages to install.

```bash
# Drill 10 mixed questions
python3 chess_trainer.py drill --count 10 --mode mixed

# Color drill
python3 chess_trainer.py drill --count 20 --mode color

# Coordinate drill ("Name a dark square")
python3 chess_trainer.py drill --count 20 --mode coordinate

# Quiz mode (alias for drill)
python3 chess_trainer.py quiz --count 10

# Stats summary
python3 chess_trainer.py stats

# Worst 5 squares
python3 chess_trainer.py stats --worst 5

# Custom stats file
python3 chess_trainer.py drill --count 10 --stats-file my_stats.json

# Module entrypoint
python3 -m chess_trainer drill --count 10
```

Stats live in `chess_stats.json` (or `--stats-file`) next to the tool. Type
`q` to quit a drill session.

## Verification results

- `python3 -m unittest discover -s tests`: 17 tests, OK
- CLI smoke tests: drill (color/coordinate), stats, `--worst`, custom
  stats file, `python -m chess_trainer` all run correctly
- JSON stats written atomically and reloaded correctly
- MIT LICENSE copyright line verified exactly:
  "Copyright (c) 2026 Asdale Dynamics, LLC"
- README credits Asdale Dynamics, LLC

## Known gaps

- `stats --worst` prints tracked-square count but the worst-squares list
  only shows when `--worst` is given (intentional, minimal CLI).
- Drill questions are fully random; no spaced-repetition prioritization of
  weak squares.
- No persistent player name or profile (by design: no personal data).
- Color is from White's perspective (a1 dark).
- Not packaged for PyPI; run from source.

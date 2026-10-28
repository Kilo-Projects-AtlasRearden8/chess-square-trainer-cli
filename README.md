# Chess Square Trainer CLI

A small, local-first Python CLI for drilling chess board coordinates and
square colors, with accuracy tracked in a local JSON file. A fan project
built by Dylan Asdale for Asdale Dynamics, LLC.

No game assets, no accounts, no network, no secrets. Standard library only.

## Who this is for

Dylan Asdale is a registered nurse turned AI author and founder of
ASDALE DYNAMICS, LLC (Indiana, formed October 2026). His book *The Massive
AI Manual* and hub site dylanasdale.github.io explain AI "like a friend
would": plain English, step by step, never condescending.

The LLC focuses on beginner-friendly AI education, books and guides, and
practical tools it can publish or sell. This chess trainer is one of the
fun extras — a gaming/chess tool built in the same local-first, tested,
accessible style as the LLC's other projects.

## Features

- Drill square **colors**: shown a square like `e4`, answer `light` or `dark`
- Drill **coordinates**: told a color, name a square of that color
- **Mixed mode**: alternates between the two question types
- Accuracy tracked per square and overall in a plain JSON file
- Stats summary, including worst squares
- No external dependencies — Python 3 standard library only

## Requirements

Python 3. No packages to install.

## Usage

Run from the project folder:

```bash
# Drill 10 mixed questions
python chess_trainer.py drill --count 10 --mode mixed

# Drill colors only
python chess_trainer.py drill --count 20 --mode color

# Drill coordinates only
python chess_trainer.py drill --count 20 --mode coordinate

# Quiz mode is an alias for drill
python chess_trainer.py quiz --count 10

# Show accuracy summary
python chess_trainer.py stats

# Show the 5 squares needing the most work
python chess_trainer.py stats --worst 5

# Use a different stats file
python chess_trainer.py drill --count 10 --stats-file my_chess_stats.json

# Run as a module
python -m chess_trainer drill --count 10
```

Type `q` to quit a drill session at any time. Progress is saved after every
question, so quitting early never loses your accuracy history.

Stats are stored in `chess_stats.json` (or your `--stats-file` path) next to
where you run the tool. Everything stays on your machine.

## Tests

```bash
python -m unittest discover -s tests
```

Tests cover square parsing (valid/invalid), square colors, round-trip naming,
and JSON accuracy tracking.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## Credit

Built by Dylan Asdale for **Asdale Dynamics, LLC** — Indiana, formed October
2026. Beginner-friendly AI education, books, guides, and practical tools.
Learn more at dylanasdale.github.io.

This is a fan project. Not affiliated with any chess organization.

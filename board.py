"""Chess board square parsing and color logic.

No external dependencies. Standard library only.
"""

FILES = "abcdefgh"
RANKS = "12345678"
NUM_FILES = 8
NUM_RANKS = 8

LIGHT = "light"
DARK = "dark"


def parse_square(square):
    """Parse a chess square like ``"e4"``.

    Returns a ``(file_index, rank_index)`` tuple of zero-based integers, or
    ``None`` if the input is not a valid square.

    Files are ``a`` through ``h`` (0..7), ranks are ``1`` through ``8`` (0..7).
    """
    if not isinstance(square, str):
        return None
    if len(square) != 2:
        return None
    file_char = square[0]
    rank_char = square[1]
    if file_char not in FILES:
        return None
    if rank_char not in RANKS:
        return None
    return FILES.index(file_char), RANKS.index(rank_char)


def square_name(file_index, rank_index):
    """Return the algebraic name (e.g. ``"e4"``) for zero-based indices."""
    if not (0 <= file_index < NUM_FILES and 0 <= rank_index < NUM_RANKS):
        raise ValueError("square indices out of range")
    return FILES[file_index] + RANKS[rank_index]


def square_color(file_index, rank_index):
    """Return ``"light"`` or ``"dark"`` for the given square.

    From White's perspective, ``a1`` is a dark square, so squares where the
    file index plus rank index is even are dark, and odd sums are light.
    """
    if not (0 <= file_index < NUM_FILES and 0 <= rank_index < NUM_RANKS):
        raise ValueError("square indices out of range")
    return LIGHT if (file_index + rank_index) % 2 == 1 else DARK


def all_squares():
    """Return a list of every (file_index, rank_index) on the board."""
    return [
        (file_index, rank_index)
        for file_index in range(NUM_FILES)
        for rank_index in range(NUM_RANKS)
    ]


def opposite_color(color):
    """Return the opposite of ``"light"``/``"dark"``."""
    if color == LIGHT:
        return DARK
    if color == DARK:
        return LIGHT
    raise ValueError("unknown color: %r" % color)

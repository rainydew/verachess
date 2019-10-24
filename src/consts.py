# coding: utf-8
from typing import List, Any, Tuple

Pieces = {
    "k": "♚",
    "K": "♔",
    "q": "♛",
    "Q": "♕",
    "b": "♝",
    "B": "♗",
    "n": "♞",
    "N": "♘",
    "r": "♜",
    "R": "♖",
    "p": "♟",
    "P": "♙",
}


class Promotions:
    white = [Pieces[x] for x in "QRNB"]
    black = [Pieces[x] for x in "qrnb"]
    white_rev = {Pieces[c]: c for c in "QRNB"}
    black_rev = {Pieces[c]: c for c in "qrnb"}


class Stats:
    common_stats = "w KQkq - 0 1"


class Positions:
    common_startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    common_start_fen = common_startpos + " " + Stats.common_stats
    blank = "8/8/8/8/8/8/8/8"


class Color:
    cyan_light = "#a8f3ff"
    cyan_dark = "#9ee4ef"
    pink_light = "#f0b3ff"
    pink_dark = "#efa1ff"
    lemon_dark = "#88d600"
    lemon_light = "#bbd66f"
    black = "#000000"
    white = "#ffffff"
    red = "#ff0000"
    blue = "#0000ff"
    green_dark = "#00d100"
    cell_sel_light = "#f7f786"
    cell_sel_dark = "#f0d58c"


class Font:
    font_24 = "-family {Times New Roman} -size 24 -weight normal -slant roman -underline 0 -overstrike 0"
    font_14 = "-family {Times New Roman} -size 14 -weight normal -slant roman -underline 0 -overstrike 0"


class Role:
    human = 0
    computer = 1
    remote = 2


class CastleCells:
    white_long = ((7 ,4), (7, 3), (7, 2))
    white_short = ((7 ,4), (7, 5), (7, 6))
    black_long = ((0 ,4), (0, 3), (0, 2))
    black_short = ((0 ,4), (0, 5), (0, 6))
    white_l_p, white_s_p, black_l_p, black_s_p = map(lambda x: x[1:], (
        white_long, white_short, black_long, black_short))  # type: Tuple[Tuple[int, int]]
    white_l_arrive, white_s_arrive, black_l_arrive, black_s_arrive = map(lambda x: x[-1], (
        white_long, white_short, black_long, black_short))  # type: Tuple[int, int]
    # todo: c960 support


class MenuStatNames:
    flip = "Flip"


def gen_empty_board(init_value=None) -> List[List[Any]]:
    return [[init_value for _ in range(8)] for _ in range(8)]

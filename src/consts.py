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


class Positions:
    common_startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    blank = "8/8/8/8/8/8/8/8"


class Stats:
    common_stats = "w KQkq - 0 1"


class Color:
    cyan_light = "#a8f3ff"
    cyan_dark = "#9ee4ef"
    pink_light = "#f0b3ff"
    pink_dark = "#efa1ff"
    lemon_dark = "#88d600"
    lemon_light = "#bbd66f"
    black = "#000000"
    red = "#ff0000"


class Font:
    font_24 = "-family {Times New Roman} -size 24 -weight normal -slant roman -underline 0 -overstrike 0"


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


def gen_empty_board(init_value=None) -> List[List[Any]]:
    return [[init_value for _ in range(8)] for _ in range(8)]

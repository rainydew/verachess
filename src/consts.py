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
    magenta = "#ff00ff"     # check


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


class Winner:
    white = 1.0
    black = 0.0
    draw = 0.5
    unknown = -1.0


Winner_Dict = {Winner.white: "1-0", Winner.draw: "1/2-1/2", Winner.black: "0-1"}


class EndType:
    unterminated = 0
    checkmate = -1
    resign = -2
    time_forfeit = -3
    engine_stall = -4
    adjunction_win = -5  # by user or FICS
    table_base_win = -6
    score_rule_win = -7
    illegal_move = -8
    break_rule = -9  # e.g. memory overflow
    skip_win = -15
    other_win = -16
    stalemate = 1
    three_fold = 2
    fifty_rule = 3
    insufficient_material = 4
    adjunction_draw = 5
    table_base_draw = 6
    score_rule_draw = 7
    mutual_agreement = 8
    tournament_cancel = 14
    skip_draw = 15
    other_draw = 16





def gen_empty_board(init_value=None) -> List[List[Any]]:
    return [[init_value for _ in range(8)] for _ in range(8)]

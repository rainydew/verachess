# coding: utf-8
from typing import List, Any, Tuple, Dict
import easygui
import sys


def _get_bin_path():
    filepath = sys.argv[0]  # type: str
    if filepath.replace("\\", "/").split("/")[-2] == "src":
        binpath = filepath + "/../../bin"
    else:
        binpath = filepath + "/.."
    return binpath


def _gen_eco_dict() -> Dict[str, str]:
    eco = {" ".join(Positions.common_start_fen.split()[:4]): "A00 Start Position"}
    try:
        f = open("verachess.eco", encoding="utf-8")
    except:
        easygui.msgbox("开局库文件verachess.eco被损坏，请从https://github.com/rainydew/verachess下载文件")
    else:
        for line in f:
            if line:
                eco_name, eco_fen, eco_move = line.split("\t")  # type: str
                eco_fen = " ".join(eco_fen.split()[:4])
                eco[eco_fen] = eco_name
        f.close()
    return eco


Pieces = {
    "K": "♔",
    "k": "♚",
    "Q": "♕",
    "q": "♛",
    "B": "♗",
    "b": "♝",
    "N": "♘",
    "n": "♞",
    "R": "♖",
    "r": "♜",
    "P": "♙",
    "p": "♟",
}       # type: Dict[str, str]


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
    name_normal_startpos = "startpos"


class Color:
    cyan_light = "#a8f3ff"
    cyan_dark = "#9ee4ef"
    pink_light = "#f0b3ff"
    pink_dark = "#efa1ff"
    cell_sel_light = "#9eb55e"
    cell_sel_dark = "#6aa800"
    black = "#000000"
    white = "#ffffff"
    red = "#ff0000"
    blue = "#0000ff"
    orange = "#ff3f00"
    green_dark = "#00d100"
    yellow_light = "#ffefad"
    yellow_dark = "#dbc27f"
    magenta = "#ff00ff"     # check
    clock_inactive = "#24b6ff"
    clock_active = "#d0fffc"
    clock_disabled = "#c0c0c0"
    clock_enabled = "#dddddd"
    move_normal = "#ffd5ab"
    move_highlight = "#9999ff"


class Style:
    move_list_slider = "Slicder.Vertical.TScale"    # must ended with .Vertical.TScale (the widget name and orient)


class Font:
    font_24 = "-family {Times New Roman} -size 24 -weight normal -slant roman"
    font_18 = "-family {Times New Roman} -size 18 -weight normal -slant roman"
    font_14 = "-family {Times New Roman} -size 14 -weight normal -slant roman"
    font_9 = "-family {Times New Roman} -size 9 -weight normal -slant roman"
    font_clock = "-family Digiface -size 16 -weight bold -slant roman"
    font_move = "-family Roboto -size 9 -weight normal -slant roman"
    add_blackbold = "-family 黑体"
    add_bold = "-weight bold"


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


class MenuStatNames:
    flip = "Flip"
    clock = "Clock"


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
    withdraw = -14
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
    single_king_with_opp_violate = 9
    tournament_cancel = 14
    skip_draw = 15
    other_draw = 16


class Termination:
    unterminated = "未结束"
    normal = "常规结束"
    time_forfeit = "超时"
    rule_infraction = "犯规或故障"
    adjunction = "裁判裁定"
    abandon = "比赛取消"
    all_type = (unterminated, normal, time_forfeit, rule_infraction, adjunction, abandon)


class EndTypeToTermination:
    unterminated = Termination.unterminated
    checkmate = Termination.normal
    resign = Termination.normal
    time_forfeit = Termination.time_forfeit
    engine_stall = Termination.rule_infraction
    adjunction_win = Termination.adjunction  # by user or FICS
    table_base_win = Termination.adjunction
    score_rule_win = Termination.adjunction
    illegal_move = Termination.rule_infraction
    break_rule = Termination.rule_infraction  # e.g. memory overflow
    withdraw = Termination.abandon
    skip_win = Termination.abandon
    other_win = Termination.adjunction
    stalemate = Termination.normal
    three_fold = Termination.normal
    fifty_rule = Termination.normal
    insufficient_material = Termination.normal
    adjunction_draw = Termination.adjunction
    table_base_draw = Termination.adjunction
    score_rule_draw = Termination.adjunction
    mutual_agreement = Termination.normal
    single_king_with_opp_violate = Termination.adjunction
    tournament_cancel = Termination.abandon
    skip_draw = Termination.abandon
    other_draw = Termination.adjunction


class CpuMoveConf:
    use_depth = 0
    use_timer = 1
    use_node = 2


class Paths:
    binpath = _get_bin_path()
    flag = "flags/"
    music = "music/"



class InfoTypes:
    time_use = "time"
    time_remain = "remain"
    nodes = "nodes"
    depth = "depth"
    nps = "nps"
    tbhits = "tbhits"
    score = "score"
    main_pv = "pv"


EcoBook = _gen_eco_dict()   # type: Dict[str, str]


def gen_empty_board(init_value=None) -> List[List[Any]]:
    return [[init_value for _ in range(8)] for _ in range(8)]


if __name__ == '__main__':
    print("book load success")

# coding: utf-8
# 只有这里的全局变量，被其他模块导入，才能有共同的id，才可以共享通信
from typing import List, Dict, Tuple, Union, Any
from consts import Positions, Role, EndType, CpuMoveConf, Winner as ConstWinner
from match import today, now

if (lambda: None)():
    import verachess


def calc_fen_hash(fen: str) -> int:
    return hash(" ".join(fen.split(" ")[:4]))


def gen_init_game_info() -> Dict[str, Any]:
    return {'WPlayer': '', 'BPlayer': '', 'WElo': '', 'BElo': '', 'WType': Role.human, 'BType': Role.human,
            'Event': '', 'Site': 'verachess 5.0', 'Round': '', 'Result': ConstWinner.unknown, 'Date': today(),
            'MTime': now(), 'TCMin': 5.0, 'TCSec': 3.0, 'Termination': '未结束', 'TDetail': '', 'SScore': 1,
            'SDepth': 1, 'STime': 1, 'SNodes': 1, 'SNps': 1, 'STb': 1, 'SPv': 1}


class Globals:
    Cell_names = None  # type: List[List[str]]  # r, c -> tk cell name
    Reverse_cell_names = None  # type: Dict[str, Tuple[int, int]]   # tk cell name -> r, c
    MoveNames = None  # type: List[str]   # index -> tk label name
    MoveRows = None  # type: List[int]   # index -> the label row position
    ReverseMoveNames = None  # type: Dict[str, int]  # tk label name -> index
    Row_names = []  # type: List[str]  # r -> tk row name
    Column_names = []  # type: List[str]  # c -> tk column name
    Main = None  # type: verachess.MainWindow
    Selection = None  # type: Tuple[int, int]  # place, None shows no selection
    Check = None  # type: Tuple[int, int]  # place, None shows no check
    Highlights = []  # type: List[Tuple[int, int]]  # place, None shows no selection
    GameFen = Positions.common_start_fen  # type: str  # ep and so on
    White = True  # white=True, real mover
    Game_role = {"w": Role.human, "b": Role.human}  # false if human can click
    WName = ""
    BName = ""
    Game_end = EndType.unterminated  # type: int  # !0 to lock board, >0 means draw, <0 means win/lose
    TerminationInfo = ""    # todo: async info after engine supported
    Chess_960_Columns = (None, None, None)  # type: Tuple[int, int, int]
    LastMove = None  # type: Tuple[int, int]  # place, None shows no lastmove
    Models = False  # true when promotions and so on, all the main window will block
    History = [GameFen]  # type: List[str]   # fen history, history[0] shows start position
    AlphabetMovelist = []  # type: List[str]
    PGNMovelist = []  # type: List[str]
    History_hash = [hash(calc_fen_hash(GameFen))]  # type: List[int]
    InfoHistory = []  # type: List[Dict[str, Any]] # map clock_remain, time_use, score, depth, nps, tbhits, nodes, pv
    # hash_full cpu_load and cpu temperature will not be saved by move
    Start_pos = Positions.name_normal_startpos  # in c960 it will change
    SunkenCell = None  # type: Tuple[int, int]  # place to record which
    Winner = ConstWinner.unknown  # type: float
    Wtime = 300000  # total ms
    Btime = 300000
    Wremain = 300000  # now ms
    Bremain = 300000
    Wuse = 0
    Buse = 0
    Winc = 3000
    Binc = 3000
    ClockConf = {'WhiteMinEntry': 5, 'WhiteSecEntry': 0, 'WhiteIncEntry': 3, 'CpuSet': 16.0, 'CpuRebal': 1.0, 'Sync':
        True, 'Cmv': 'UseDepth'}
    # todo: tick logic separate from computer play and fics
    CpuSet = 16  # type: Union[int, float]
    CpuRebal = 1.0
    Cmv = CpuMoveConf.use_depth
    MoveSlider = -1  # the last one
    GameInfo = gen_init_game_info()


class ModelLock:
    def __enter__(self):
        Globals.Models = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        Globals.Models = False


def release_model_lock():
    Globals.Models = False

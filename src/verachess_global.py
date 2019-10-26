# coding: utf-8
# 只有这里的全局变量，被其他模块导入，才能有共同的id，才可以共享通信
from typing import List, Dict, Tuple
from consts import Positions, Role, EndType

if (lambda: None)():
    import verachess


def calc_fen_hash(fen: str) -> int:
    return hash(" ".join(fen.split(" ")[:4]))


class Globals:
    Cell_names = None  # type: List[List[str]]  # r, c -> tk cell name
    Reverse_cell_names = None  # type: Dict[str, Tuple[int, int]]   # tk cell name -> r, c
    Row_names = []  # type: List[str]  # r -> tk row name
    Column_names = []  # type: List[str]  # c -> tk row name
    Main = None  # type: verachess.MainWindow
    Selection = None  # type: Tuple[int, int]  # place, None shows no selection
    Check = None    # type: Tuple[int, int]  # place, None shows no check
    Highlights = []  # type: List[Tuple[int, int]]  # place, None shows no selection
    Game_fen = Positions.common_start_fen # type: str  # ep and so on
    Game_role = {"w": Role.human, "b": Role.human}  # false if human can click
    Game_end = EndType.unterminated    # type: int  # !0 to lock board, >0 means draw, <0 means win/lose
    Chess_960_Columns = (None, None, None)  # type: Tuple[int, int, int]
    LastMove = None  # type: Tuple[int, int]  # place, None shows no lastmove
    Models = False  # true when promotions and so on, all the main window will block
    History = [Game_fen]    # type: List[str]   # fen history
    History_hash = [hash(calc_fen_hash(Game_fen))]    # type: List[int]
    SunkenCell = None  # type: Tuple[int, int]  # place to record which
    Winner = -1.0   # type: float


class ModelLock:
    def __enter__(self):
        Globals.Models = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        Globals.Models = False


def release_model_lock():
    Globals.Models = False

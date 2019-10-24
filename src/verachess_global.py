# coding: utf-8
# 只有这里的全局变量，被其他模块导入，才能有共同的id，才可以共享通信
from typing import List, Dict, Tuple
from consts import Positions, Role
from time import sleep

if (lambda: None)():
    import verachess


class Globals:
    Cell_names = None  # type: List[List[str]]  # r, c -> tk cell name
    Reverse_cell_names = None  # type: Dict[str, Tuple[int, int]]   # tk cell name -> r, c
    Row_names = []  # type: List[str]  # r -> tk row name
    Column_names = []  # type: List[str]  # c -> tk row name
    Main = None  # type: verachess.MainWindow
    Selection = None  # type: Tuple[int, int]  # place, None shows no selection
    Highlights = []  # type: List[Tuple[int, int]]  # place, None shows no selection
    Game_fen = Positions.common_start_fen # type: str  # ep and so on
    Game_role = {"w": Role.human, "b": Role.human}  # false if human can click
    Game_end = False    # true if board lock
    LastMove = None  # type: Tuple[int, int]  # place, None shows no lastmove
    Models = False  # true when promotions and so on, all the main window will block


class ModelLock:
    def __enter__(self):
        Globals.Models = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        Globals.Models = False

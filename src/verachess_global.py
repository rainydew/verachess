# coding: utf-8
# 只有这里的全局变量，被其他模块导入，才能有共同的id，才可以共享通信
from typing import List, Dict, Tuple
from consts import Positions, Stats, Role

if (lambda: None)():
    import verachess


class Globals:
    if (lambda: None)():    # interfaces
        Cell_names = None  # type: List[List[str]]  # r, c -> tk cell name
        Main = None  # type: verachess.MainWindow
        Reverse_cell_names = None  # type: Dict[str, Tuple[int, int]]   # tk cell name -> r, c
        Selection = None  # type: Tuple[int, int]  # place, None shows no selection
        Game_fen = Positions.common_startpos + " " + Stats.common_stats # type: str  # ep and so on
        Game_role = {"w": Role.human, "b": Role.human}  # false if human can click
        Game_end = False    # true if board lock


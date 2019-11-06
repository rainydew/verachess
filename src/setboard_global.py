# coding: utf-8
from typing import List, Dict, Tuple, Optional

if (lambda: None)():
    import setboard


class Globals:
    Cell_names = None  # type: List[List[str]]  # r, c -> tk cell name
    Reverse_cell_names = None  # type: Dict[str, Tuple[int, int]]   # tk cell name -> r, c
    Row_names = []  # type: List[str]  # r -> tk row name
    Column_names = []  # type: List[str]  # c -> tk column name
    Board_array = None  # type: List[List[Optional[str]]]  # r, c -> cell value
    Main = None  # type: setboard.MainWindow

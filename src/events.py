# coding: utf-8
# event handlers
from verachess_global import Globals
from typing import Tuple, Optional
import boards

bd = boards.Fens


def cell_click_handler(selection: Optional[Tuple[int, int]], place: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    fen = Globals.Game_fen
    if Globals.Game_role[bd.get_mover(fen)]:   # not occupied by human
        return None
    if selection is None:
        # show moves
        movelist = bd.get_piece_move(fen, place)
        # 要修改高亮格子的集合，然后写渲染局面的函数
    else:
        # make real moves
        pass

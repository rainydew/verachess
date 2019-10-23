# coding: utf-8
# event handlers
from verachess_global import Globals
from typing import Tuple, Optional, List
import boards
import verachess_support

bd = boards.Fens


def refresh_highlights(new_cells: Optional[List[Tuple[int, int]]] = None) -> None:
    verachess_support.set_cell_back_colors(new_cells, Globals.Highlights)
    Globals.Highlights = new_cells or []


def cell_click_handler(selection: Optional[Tuple[int, int]], place: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    fen = Globals.Game_fen
    if Globals.Game_role[bd.get_mover(fen)]:   # not occupied by human
        return None
    if selection is None:
        if bd.can_control(fen, place):
            move_list = bd.get_piece_move(fen, place) + [place]
            refresh_highlights(move_list)
            return place
        else:
            return None
    else:
        # todo: make real moves
        refresh_highlights()
        return None



# coding: utf-8
# event handlers
from verachess_global import Globals, ModelLock
from typing import Tuple, Optional, List
from consts import Color, Promotions
import easygui
import boards
import verachess_support as vs

bd = boards.Fens


def refresh_highlights(new_cells: Optional[List[Tuple[int, int]]] = None) -> None:
    vs.set_cell_back_colors(new_cells, Globals.Highlights)
    Globals.Highlights = new_cells or []


def clear_sel_highs():
    refresh_highlights()
    vs.set_cell_color(Globals.Selection)
    Globals.Selection = None


def refresh_whole_board():  # recommand
    boards.refresh_cells()
    clear_sel_highs()


def click_handler(place: Tuple[int, int]) -> None:
    fen = Globals.Game_fen
    if Globals.Game_role[bd.get_mover(fen)]:   # not occupied by human, need fen calc so it placed here
        return
    if Globals.Selection == place:
        # click twice to unselect
        clear_sel_highs()
        return
    if place not in Globals.Highlights:
        # change other place to click, no return because it may be my another piece
        clear_sel_highs()
    if Globals.Selection is None:
        if bd.can_control(fen, place):
            move_list = bd.get_piece_move(fen, place) + [place]
            refresh_highlights(move_list)
            vs.set_cell_color(place, Color.blue)
            vs.set_cell_color(Globals.Selection)
            Globals.Selection = place
    else:
        # make a move, c960 castle included
        move = bd.place_to_cellname(Globals.Selection) + bd.place_to_cellname(place)
        if bd.is_promotion(fen, Globals.Selection, place):
            plist, pdict = (Promotions.white, Promotions.white_rev) if place[0] == 0 else (Promotions.black,
                                                                                           Promotions.black_rev)
            with ModelLock():
                res = easygui.buttonbox("选择你要升变的棋子(默认皇后)", "兵的升变", plist, fontsize=24) or plist[0]
            move += pdict[res]

        # make a move, will move to another funtion in the future to handle clock and pgn
        vs.set_cell_color(Globals.LastMove)
        Globals.Game_fen = bd.calc_move(Globals.Game_fen, move)
        refresh_whole_board()
        vs.set_cell_color(place, Color.red)
        Globals.LastMove = place

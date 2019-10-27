#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Oct 06, 2019 11:52:10 PM CST  platform: Windows NT

import sys
import easygui
import pyperclip
import c960confirm
from verachess_global import Globals, release_model_lock
from typing import List, Tuple, Dict
from verachess import Color, destroy_MainWindow
from consts import Pieces, Positions, MenuStatNames, EndType, Winner
from tkinter import CallWrapper
from decos import check_model, model_locked
import events


try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True


CellValues = None    # type: List[List[tk.StringVar]]
MenuStats = {}    # type: Dict[str, tk.BooleanVar]
Eco = None      # type: tk.StringVar


def set_Tk_var():
    global CellValues, MenuStats, Eco
    CellValues = [[tk.StringVar(value="") for _ in range(8)] for _ in range(8)]
    MenuStats[MenuStatNames.flip] = tk.BooleanVar(value=False)
    Eco = tk.StringVar()
    Eco.set('ECO - A00\nIrregular Opening')


def set_cell_values(narrow_fen: str):
    rows = narrow_fen.split("/")
    assert len(rows) == 8, "error fen"
    for i, row in enumerate(rows):
        j = 0
        for char in row:
            if char in Pieces:
                CellValues[i][j].set(Pieces[char])
                j += 1
            else:
                [CellValues[i][r].set("") for r in range(j, j + int(char))]
                j += int(char)    # if this errors, char is illegal


def set_cell_color(cell: Tuple[int, int] = None, color=Color.black, flush_all=False):
    main = Globals.Main
    if flush_all:
        [main.Cells[cell_r][cell_c].configure(foreground=Color.black) for cell_r in range(8) for cell_c in range(8)]
    if cell:
        r, c = cell
        main.Cells[r][c].configure(foreground=color)


def set_player_color(white: bool):
    main = Globals.Main
    main.Holder.configure(foreground=Color.white if white else Color.black)


def set_cell_back_colors(active_color_list: List[Tuple[int, int]] = None, inactive_color_list: List[Tuple[int, int]] =
        None, flush_all=False):
    """
    :param active_color_list: 
    :param inactive_color_list: 
    :param flush_all: 
    :return: 
    """
    main = Globals.Main
    if flush_all:
        [main.Cells[r][c].configure(background=Color.yellow_dark if (r + c) % 2 else Color.yellow_light) for r in range(8)
         for c in range(8)]
    if inactive_color_list:     # deselect old first
        for r, c in inactive_color_list:
            main.Cells[r][c].configure(background=Color.yellow_dark if (r + c) % 2 else Color.yellow_light)
    if active_color_list:
        for r, c in active_color_list:
            main.Cells[r][c].configure(background=Color.cell_sel_dark if (r + c) % 2 else Color.cell_sel_light)


def refresh_flip():
    arg = MenuStats[MenuStatNames.flip].get()
    main = Globals.Main
    now_flip = main.Rows[0].winfo_geometry().split("+")[-1] != "0"
    if arg != now_flip:
        if not arg:
            for r in range(8):
                main.Rows[r].place(y=r * 48)
                main.Columns[r].place(x=r * 48)
                for c in range(8):
                    main.Cells[r][c].place(x=c * 48, y=r * 48)
        else:
            for r in range(8):
                main.Rows[7 - r].place(y=r * 48)
                main.Columns[7 - r].place(x=r * 48)
                for c in range(8):
                    main.Cells[7 - r][7 - c].place(x=c * 48, y=r * 48)


def clear_sunken_cell():
    if Globals.SunkenCell:
        r, c = Globals.SunkenCell
        Globals.Main.Cells[r][c].configure(relief="groove")
        Globals.SunkenCell = None


def set_sunken_cell(place: Tuple[int, int]):
    assert Globals.SunkenCell is None
    Globals.SunkenCell = place
    r, c = place
    Globals.Main.Cells[r][c].configure(relief="sunken")


def reformat_fen(fen: str):
    li = fen.split(" ")
    castle = li[2]
    if castle == "-":
        return fen
    if "k" in castle.lower() or "q" in castle.lower():
        li[2] = "".join(sorted(castle))
    else:
        li[2] = "".join(sorted(castle))[::-1].swapcase()
    return " ".join(li)


def set_game_fen(fen: str):
    Globals.Game_fen = fen
    Globals.History = [fen]
    Globals.AlphabetMovelist = []
    Globals.PGNMovelist = []
    Globals.History_hash = [hash(" ".join(fen.split(" ")[:4]))]
    Globals.Game_end = EndType.unterminated
    Globals.Winner = Winner.unknown
    events.clear_check_cell()
    events.refresh_whole_board()
    set_cell_color(flush_all=True)
    clear_sunken_cell()
    if fen != Positions.common_start_fen:
        events.check_wdl()


def redraw_c960_flags():
    columns = Globals.Main.Columns
    lr, k, rr = Globals.Chess_960_Columns
    for column in columns:
        column.configure(foreground=Color.black)
    if lr is not None:  # pasted c960 fen may return None
        columns[lr].configure(foreground=Color.orange)
    if rr is not None:  # too
        columns[rr].configure(foreground=Color.orange)
    if k is not None:   # too
        columns[k].configure(foreground=Color.magenta)


# events
def exit_game():
    if easygui.ynbox("你确定要退出吗？", "verachess 5.0", ["是", "否"]):
        destroy_MainWindow()
        sys.exit()


@model_locked
def new_normal():
    if any(Globals.Game_role.values()):
        easygui.msgbox("黑白双方都需要处于被玩家控制的状态，且不使用FICS联网时，才能重新开局。如需要")
        return
    if easygui.ynbox("这将重置当前棋局信息，确认重新开始棋局吗？", "verachess 5.0", ["是", "否"]):
        Globals.Chess_960_Columns = (None, None, None)
        redraw_c960_flags()
        set_game_fen(Positions.common_start_fen)
        MenuStats[MenuStatNames.flip].set(False)
        refresh_flip()


@model_locked
def new_c960():
    if any(Globals.Game_role.values()):
        easygui.msgbox("黑白双方都需要处于被玩家控制的状态，且不使用FICS联网时，才能重新开局。如需要")
        return
    if easygui.ynbox("这将重置当前棋局信息，确认重新开始棋局吗？", "verachess 5.0", ["是", "否"]):
        main_window = Globals.Main.Top
        sub_window, confirm_widget = c960confirm.create_Toplevel1(root=main_window)
        sub_window.transient(main_window)   # show only one window in taskbar
        sub_window.grab_set()   # set as model window
        Globals.Main.Top.wait_window(sub_window)    # wait for window return, to get return value
        res = confirm_widget.Result

        if res is None:
            return
        rkr, pos = res
        Globals.Chess_960_Columns = rkr     # 新局面不走校验逻辑，必须手动设置chess960的易位列
        redraw_c960_flags()
        set_game_fen(pos)
        MenuStats[MenuStatNames.flip].set(False)
        refresh_flip()


def flip():
    # this is event for flip click
    refresh_flip()


@model_locked
def copy_fen():
    pyperclip.copy(Globals.Game_fen)
    easygui.msgbox("当前局面已经复制到剪贴板")


@model_locked
def paste_fen():
    if any(Globals.Game_role.values()):
        easygui.msgbox("黑白双方都需要处于被玩家控制的状态，且不使用FICS联网时，才能使用摆局功能")
        return
    elif not easygui.ynbox("将会重置当前棋局的信息，你确认要导入局面吗？", "verachess 5.0", ["是", "否"]):
        return
    fen = pyperclip.paste()
    res, msg = events.check_fen_format_valid(fen)   # 校验格式，如果chess960的局面校验通过，会设置chess960的易位列
    if not res:
        easygui.msgbox("FEN错误\n"+msg)
        return
    release_model_lock()    # very important, set fen require model lock
    set_game_fen(reformat_fen(fen))
    redraw_c960_flags()


@check_model
def cell_click(event: CallWrapper) -> None:
    if Globals.Game_end:
        return
    place = Globals.Reverse_cell_names[str(event.widget)]
    events.click_handler(place)


# event end
def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

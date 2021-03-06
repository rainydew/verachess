#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Nov 06, 2019 11:09:03 PM CST  platform: Windows NT

import easygui
import events
from typing import List, Dict
from tkinter import CallWrapper
from setboard_global import Globals
from verachess_global import Globals as VcGlobals
from consts import Pieces
from boards import Fens

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

PName = FlipVar = C960switch = RrCol = LrCol = Mover = Drawmove = Totalmove = EpCol = None  # type: tk.StringVar
Wkcast = Wqcast = Bkcast = Bqcast = None  # type: tk.IntVar
CellValues = None  # type: List[List[tk.StringVar]]
ColDict = {}  # type: Dict[str, tk.StringVar]


def set_Tk_var():
    global PName, FlipVar, CellValues, C960switch, RrCol, LrCol, Wkcast, Wqcast, Bkcast, Bqcast, Mover, Drawmove, \
        Totalmove, EpCol, ColDict
    PName = tk.StringVar(value="K")
    FlipVar = tk.StringVar(value='翻转局面')
    CellValues = [[tk.StringVar(value="") for _ in range(8)] for _ in range(8)]
    C960switch = tk.StringVar(value="normal")
    RrCol = tk.StringVar(value="h")
    RrCol.trace_variable("w", cacol_filter)
    LrCol = tk.StringVar(value="a")
    LrCol.trace_variable("w", cacol_filter)
    ColDict[str(LrCol)] = LrCol
    ColDict[str(RrCol)] = RrCol
    C960switch.trace_variable("w", c960_switch_callback)
    Wkcast = tk.IntVar(value=1)
    Wqcast = tk.IntVar(value=1)
    Bkcast = tk.IntVar(value=1)
    Bqcast = tk.IntVar(value=1)
    Mover = tk.StringVar(value='w')
    Drawmove = tk.StringVar(value='0')
    Drawmove.trace_variable("w", drawmove_filter)
    Totalmove = tk.StringVar(value="1")
    Totalmove.trace_variable("w", totalmove_filter)
    EpCol = tk.StringVar(value="-")
    EpCol.trace_variable("w", epcol_filter)


def c960_switch_callback(*args):
    main = Globals.Main
    if C960switch.get() == "c960":
        main.KingSide.configure(state='normal')
        main.QueenSide.configure(state='normal')
    else:
        main.KingSide.configure(state='disabled')
        main.QueenSide.configure(state='disabled')


def refresh_aval():
    conf = Globals.Main.Confirm
    if Drawmove.get() and Totalmove.get():
        conf.configure(state="normal")
    else:
        conf.configure(state="disabled")


def drawmove_filter(*args):
    try:
        if Drawmove.get() == "":
            return
        w = int(Drawmove.get())
        if w < 0:
            Drawmove.set("0")
        if w > 100:
            Drawmove.set("100")
    except:
        Drawmove.set("0")
    finally:
        refresh_aval()


def totalmove_filter(*args):
    try:
        if Totalmove.get() == "":
            return
        w = int(Totalmove.get())
        if w < 1:
            Totalmove.set("1")
    except:
        Totalmove.set("")
    finally:
        refresh_aval()


def epcol_filter(*args):
    if EpCol.get() and EpCol.get()[-1].lower() not in ("-", "a", "b", "c", "d", "e", "f", "g", "h"):
        EpCol.set("-")
    else:
        try:
            EpCol.set(EpCol.get()[-1].lower())
        except:
            EpCol.set("-")


def cacol_filter(widget_name, *args):
    widget = ColDict[widget_name]
    if widget.get().lower() not in ("a", "b", "c", "d", "e", "f", "g", "h"):
        widget.set("")
    else:
        widget.set(widget.get().lower())


# events
def cancel():
    destroy_window()


def clear():
    for r in range(8):
        for c in range(8):
            Globals.Board_array[r][c] = None
            CellValues[r][c].set("")


def confirm():
    main = Globals.Main
    narrow_fen = Fens.get_narrow_fen_from_board(Globals.Board_array)
    mover = Mover.get()

    if C960switch.get() == "normal":
        CastleDict = {"K": Wkcast, "Q": Wqcast, "k": Bkcast, "q": Bqcast}
    else:
        lr_col, rr_col = LrCol.get(), RrCol.get()
        if lr_col == "" or rr_col == "":
            easygui.msgbox("Chess960下需要填写双车所在的初始列")
            return
        LR_col, RR_col = lr_col.upper(), rr_col.upper()
        CastleDict = {RR_col: Wkcast, LR_col: Wqcast, rr_col: Bkcast, lr_col: Bqcast}
    castle = ""
    for char in CastleDict.keys():
        if CastleDict[char].get():
            castle += char
    castle = castle if castle else "-"

    if EpCol.get() == "-":
        ep = "-"
    else:
        if mover == "w":
            ep = EpCol.get() + "6"
        else:
            ep = EpCol.get() + "3"

    draw = Drawmove.get()
    totalmove = Totalmove.get()

    fen = " ".join((narrow_fen, mover, castle, ep, draw, totalmove))

    res, msg = events.check_fen_format_valid(fen)  # 校验格式，如果chess960的局面校验通过，会设置chess960的易位列
    if not res:
        easygui.msgbox("FEN错误\n" + msg)
        return

    main.Result = fen
    destroy_window()


def copy():
    narrow_fen, mover, castle, ep, draw, move_count = VcGlobals.GameFen.split(" ")
    Globals.Board_array = Fens.get_board_arrays(narrow_fen)

    for r in range(8):
        for c in range(8):
            piece = Pieces.get(Globals.Board_array[r][c])
            CellValues[r][c].set(piece if piece else "")

    Mover.set(mover)

    lr, k, rr = VcGlobals.Chess_960_Columns
    if lr is None:
        C960switch.set("normal")
        CastleDict = {"K": Wkcast, "Q": Wqcast, "k": Bkcast, "q": Bqcast}
    else:
        C960switch.set("c960")
        lr_col, rr_col = chr(lr + 97), chr(rr + 97)
        LR_col, RR_col = chr(lr + 65), chr(rr + 65)
        CastleDict = {RR_col: Wkcast, LR_col: Wqcast, rr_col: Bkcast, lr_col: Bqcast}
    for char in CastleDict.keys():
        if char in castle:
            CastleDict[char].set(1)
        else:
            CastleDict[char].set(0)

    EpCol.set(ep[:1])
    Drawmove.set(draw)
    Totalmove.set(move_count)


def flip():
    main = Globals.Main
    button = main.Flip
    if button.cget("relief") == "raised":
        button.configure(relief="sunken")
        for r in range(8):
            main.Rows[7 - r].place(y=r * 48)
            main.Columns[7 - r].place(x=r * 48)
            for c in range(8):
                main.Cells[7 - r][7 - c].place(x=c * 48, y=r * 48)
    else:
        button.configure(relief="raised")
        for r in range(8):
            main.Rows[r].place(y=r * 48)
            main.Columns[r].place(x=r * 48)
            for c in range(8):
                main.Cells[r][c].place(x=c * 48, y=r * 48)


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


def cell_click(event: CallWrapper) -> None:
    r, c = Globals.Reverse_cell_names[str(event.widget)]
    piece = PName.get()
    if Globals.Board_array[r][c] == piece:
        Globals.Board_array[r][c] = None
        CellValues[r][c].set("")
    else:
        Globals.Board_array[r][c] = piece
        CellValues[r][c].set(Pieces[piece])

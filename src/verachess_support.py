#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Oct 06, 2019 11:52:10 PM CST  platform: Windows NT

import sys
from verachess_global import Globals
from typing import List, Tuple
from verachess import Color
from consts import Pieces
from tkinter import CallWrapper
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


def set_Tk_var():
    global CellValues
    CellValues = [[tk.StringVar(value="") for _ in range(8)] for _ in range(8)]


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


def set_cell_colors(color_list: List[Tuple[List[Tuple[int, int]], str]] = None, flush_all = True):
    """
    :param color_list: [([(x, y) ...], colors) ...]
    :param flush_all: flush other cells with black
    :return:
    """
    main = Globals.Main
    if flush_all:
        [main.Cells[cell_x][cell_y].configure(foreground=Color.black) for cell_x in range(8) for cell_y in range(8)]
    if color_list:
        for cells, color in color_list:
            for cell_x, cell_y in cells:
                main.Cells[cell_x][cell_y].configure(foreground=color)


def exit():
    print('verachess_support.exit')
    sys.stdout.flush()


def cell_click(event: CallWrapper) -> None:
    if Globals.Game_end:
        return
    place = Globals.Reverse_cell_names[str(event.widget)]
    if Globals.Selection == place:
        Globals.Selection = None
        set_cell_colors(flush_all=True)
    else:
        after = events.cell_click_handler(Globals.Selection, place)
        Globals.Selection = after
        if after is not None:
            set_cell_colors([([after], Color.red)], flush_all=True)
        else:
            set_cell_colors(flush_all=True)


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

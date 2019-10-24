#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Oct 06, 2019 11:51:51 PM CST  platform: Windows NT

import sys

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

import verachess_support
from verachess_global import Globals

from typing import List
from consts import Color, Font, gen_empty_board


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    verachess_support.set_Tk_var()
    top = MainWindow(root)

    Globals.Main = top

    verachess_support.init(root, top)
    root.mainloop()


w = None


def create_MainWindow(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel(root)
    verachess_support.set_Tk_var()
    top = MainWindow(w)
    verachess_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_MainWindow():
    Globals.Main.Top.destroy()  # safe import
    sys.exit()


class MainWindow:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("885x700+350+200")
        top.title("Verachess 5.0")
        top.configure(background="#d9d9d9")

        self.Top = top

        self.ChessBoard = tk.Frame(top)
        self.ChessBoard.place(relx=0.0, rely=0.0, height=385
                              , width=385)
        self.ChessBoard.configure(relief='ridge')
        self.ChessBoard.configure(borderwidth="1")
        self.ChessBoard.configure(relief='ridge')
        self.ChessBoard.configure(background="#d9d9d9")
        self.ChessBoard.configure(highlightbackground="#ffffff")
        self.ChessBoard.configure(highlightcolor="#ffffff")
        self.ChessBoard.configure(width=385)

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.sub_menu = tk.Menu(top, tearoff=0)
        self.menubar.add_cascade(menu=self.sub_menu,
                                 activebackground="#ececec",
                                 activeforeground="#000000",
                                 background="#d9d9d9",
                                 compound="left",
                                 font="TkMenuFont",
                                 foreground="#000000",
                                 label="File")
        self.sub_menu.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            command=verachess_support.exit,
            compound="left",
            font="TkMenuFont",
            foreground="#000000",
            label="Exit")

        self.Rows = self.Columns = None  # type: List[tk.Label]
        self.Cells = None  # type: List[List[tk.Label]]

        create_rows(self, top)
        create_columns(self, top)
        create_cells(self, self.ChessBoard)

        from boards import init_cells
        init_cells()


# user code
def create_columns(main: MainWindow, top: tk.Tk):
    main.Columns = []
    for i in range(8):
        column = tk.Label(top)
        column.place(x=i * 48, y=385, height=16, width=48)
        column.configure(background=Color.cyan_light if i % 2 else Color.cyan_dark)
        column.configure(text=chr(65 + i))
        main.Columns.append(column)

        Globals.Column_names.append(str(column))


def create_rows(main: MainWindow, top: tk.Tk):
    main.Rows = []
    for i in range(8):
        row = tk.Label(top)
        row.place(x=385, y=i * 48, height=48, width=16)
        row.configure(background=Color.pink_light if i % 2 else Color.pink_dark)
        row.configure(text=str(8 - i))
        main.Rows.append(row)

        Globals.Row_names.append(str(row))


def create_cells(main: MainWindow, top: tk.Frame):
    main.Cells = gen_empty_board()
    Globals.Cell_names = gen_empty_board()
    Globals.Reverse_cell_names = {}
    for r in range(8):
        for c in range(8):
            box = tk.Label(top)
            box.place(x=c * 48, y=r * 48, height=48, width=48)  # i行j列
            box.configure(background=Color.lemon_dark if (r + c) % 2 else Color.lemon_light)
            box.configure(font=Font.font_24)

            box.configure(textvariable=verachess_support.CellValues[r][c])
            box.bind('<ButtonRelease-1>', lambda e: verachess_support.cell_click(e))

            Globals.Cell_names[r][c] = str(box)
            Globals.Reverse_cell_names[str(box)] = (r, c)
            main.Cells[r][c] = box


if __name__ == '__main__':
    vp_start_gui()

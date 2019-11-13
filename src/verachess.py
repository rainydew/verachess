#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Oct 06, 2019 11:51:51 PM CST  platform: Windows NT
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

from typing import List, Dict, Callable
from consts import Color, Font, gen_empty_board, MenuStatNames, Style, Positions


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    verachess_support.set_Tk_var()
    top = MainWindow(root)

    Globals.Main = top

    verachess_support.init(root, top)

    # init clock here after ui created
    from clock import Tick_Thread
    Tick_Thread.setDaemon(True)
    Tick_Thread.start()

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
        top.resizable(0, 0)

        self.Top = top

        self.style = ttk.Style()
        self.style.configure(Style.move_list_slider, background=Color.move_normal)

        self.Holder = None  # type: tk.Label
        create_colorhodler(self, top)

        self.ChessBoard = tk.Frame(top)
        self.ChessBoard.place(x=0, y=0, height=385, width=385)
        self.ChessBoard.configure(relief='ridge')
        self.ChessBoard.configure(borderwidth="1")

        self.ClockBoard = tk.Frame(top)
        self.ClockBoard.place(x=402, y=0, height=96, width=375)
        self.ClockBoard.configure(borderwidth="1")
        self.ClockBoard.configure(relief='ridge')

        self.EcoBoard = tk.Frame(top)
        self.EcoBoard.place(x=778, y=0, height=96, width=105)
        self.EcoBoard.configure(relief='ridge')
        self.EcoBoard.configure(borderwidth="1")

        self.ECO = tk.Label(self.EcoBoard)
        self.ECO.place(x=-2, y=-2, height=96, width=105)
        self.ECO.configure(anchor='nw')
        self.ECO.configure(background="#ffffab")
        self.ECO.configure(justify='left')
        self.ECO.configure(wraplength=105)
        self.ECO.configure(textvariable=verachess_support.Eco)
        self.ECO.configure(font=Font.font_9)

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.Menus = {}     # type: Dict[str, List[tk.Menu, int]]  # name, instance, sub_menu length
        self.Sub_menus = {}     # type: Dict[str, List[int, str]]   # name, index, parent name

        create_menus(self, top)

        self.Rows = self.Columns = None  # type: List[tk.Label]
        self.Cells = None  # type: List[List[tk.Label]]
        self.WhitePlayer = self.BlackPlayer = self.WhiteTotal = self.BlackTotal = self.WhiteUse = self.BlackUse = \
            self.WhiteFlag = self.BlackFlag = None  # type: tk.Label

        self.MoveFrame = tk.LabelFrame(top)
        self.MoveFrame.place(x=400, y=96, height=192, width=483)
        self.MoveFrame.configure(relief='groove')
        self.MoveFrame.configure(text='''棋谱''')
        self.MoveFrame.configure(background=Color.move_normal)

        self.Moves = None   # type: List[tk.Label]

        self.MoveScale = ttk.Scale(self.MoveFrame, from_=0, to=0.01)     # add 0.01 to reformat the style!!
        self.MoveScale.place(x=461, y=15, width=20, height=172, bordermode='ignore')
        self.MoveScale.configure(command=verachess_support.ListScroll)
        self.MoveScale.configure(variable=verachess_support.MoveScaleVar)
        self.MoveScale.configure(orient="vertical")
        self.MoveScale.configure(length="130")
        self.MoveScale.configure(style=Style.move_list_slider)

        create_rows(self, top)
        create_columns(self, top)
        create_cells(self, self.ChessBoard)
        create_players(self, self.ClockBoard)
        create_movelist(self, self.MoveFrame)

        verachess_support.set_cell_values(Positions.common_startpos)

        top.bind('<Destroy>', lambda e: verachess_support.destruct(e))


# user code
def create_columns(main: MainWindow, top: tk.Tk):
    main.Columns = []
    for i in range(8):
        column = tk.Label(top)
        column.place(x=i * 48, y=385, height=16, width=48)
        column.configure(background=Color.cyan_light if i % 2 else Color.cyan_dark)
        column.configure(text=chr(65 + i))
        column.configure(relief="raised")
        column.configure(font=Font.add_bold)
        main.Columns.append(column)

        Globals.Column_names.append(str(column))


def create_rows(main: MainWindow, top: tk.Tk):
    main.Rows = []
    for i in range(8):
        row = tk.Label(top)
        row.place(x=385, y=i * 48, height=48, width=16)
        row.configure(background=Color.pink_light if i % 2 else Color.pink_dark)
        row.configure(text=str(8 - i))
        row.configure(relief="raised")
        row.configure(font=Font.add_bold)
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
            box.configure(background=Color.yellow_dark if (r + c) % 2 else Color.yellow_light)
            box.configure(relief="groove")
            box.configure(font=Font.font_24)

            box.configure(textvariable=verachess_support.CellValues[r][c])
            box.bind('<ButtonRelease-1>', lambda e: verachess_support.cell_click(e))

            Globals.Cell_names[r][c] = str(box)
            Globals.Reverse_cell_names[str(box)] = (r, c)
            main.Cells[r][c] = box


def create_colorhodler(main: MainWindow, top: tk.Tk):   # 右下角行棋方指示
    holder = tk.Label(top)

    holder.place(x=384, y=384, height=17, width=17)
    holder.configure(background=Color.green_dark)
    holder.configure(font=Font.font_14)
    holder.configure(text="●")
    holder.configure(foreground=Color.white)
    holder.configure(relief="raised")

    main.Holder = holder


def create_players(main: MainWindow, top: tk.Frame):
    wp = tk.Label(top)
    wp.place(x=0, y=68, height=26, width=187)
    wp.configure(background=Color.white)
    wp.configure(foreground=Color.black)
    wp.configure(textvariable=verachess_support.WhitePlayerInfo)
    wp.configure(font=Font.add_blackbold)

    bp = tk.Label(top)
    bp.place(x=187, y=68, height=26, width=187)
    bp.configure(background=Color.black)
    bp.configure(foreground=Color.white)
    bp.configure(textvariable=verachess_support.BlackPlayerInfo)
    bp.configure(font=Font.add_blackbold)

    wt = tk.Label(top)
    wt.place(x=0, y=0, height=34, width=187)
    wt.configure(background=Color.clock_inactive)
    wt.configure(font=Font.font_clock)
    wt.configure(textvariable=verachess_support.WhiteTotalTime)

    bt = tk.Label(top)
    bt.place(x=187, y=0, height=34, width=187)
    bt.configure(background=Color.clock_inactive)
    bt.configure(font=Font.font_clock)
    bt.configure(textvariable=verachess_support.BlackTotalTime)

    flag_width = verachess_support.FlagWidth

    wu = tk.Label(top)
    wu.place(x=flag_width - 4, y=34, height=34, width=187 - flag_width + 4)
    wu.configure(background=Color.clock_disabled)
    wu.configure(font=Font.font_clock)
    wu.configure(textvariable=verachess_support.WhiteUseTime)

    bu = tk.Label(top)
    bu.place(x=187 + flag_width - 4, y=34, height=34, width=187 - flag_width + 4)
    bu.configure(background=Color.clock_disabled)
    bu.configure(font=Font.font_clock)
    bu.configure(textvariable=verachess_support.BlackUseTime)

    wf = tk.Label(top)
    wf.place(x=0, y=34, height=34, width=flag_width)
    wf.configure(image=verachess_support.WhiteFlagImg)

    bf = tk.Label(top)
    bf.place(x=187, y=34, height=34, width=flag_width)
    bf.configure(image=verachess_support.BlackFlagImg)

    main.WhitePlayer = wp
    main.BlackPlayer = bp
    main.WhiteTotal = wt
    main.BlackTotal = bt
    main.WhiteUse = wu
    main.BlackUse = bu
    main.WhiteFlag = wf
    main.BlackFlag = bf


def create_movelist(main: MainWindow, top: tk.LabelFrame):
    main.Moves = []
    Globals.MoveNames = []
    Globals.MoveRows = []
    Globals.ReverseMoveNames = {}

    move = tk.Label(top)
    move.place(x=3, y=0, height=24)     # 不设width，可以让界面灵活根据内容调整宽度
    move.configure(background=Color.move_highlight)
    move.configure(font=Font.font_move)
    move.configure(text=Globals.Start_pos)
    move.bind('<Button-1>', lambda e: verachess_support.move_click(e))

    main.Moves.append(move)
    Globals.MoveNames.append(str(move))
    Globals.ReverseMoveNames[str(move)] = 0
    Globals.MoveRows.append(0)


def create_menus(main: MainWindow, top: tk.Tk):
    m_file = add_menu(main, top, "文件")
    add_command(main, m_file, "重新开始棋局(普通)", verachess_support.new_normal)
    add_command(main, m_file, "重新开始棋局(Chess960)", verachess_support.new_c960)
    add_separator(main, m_file)
    add_command(main, m_file, "棋局信息", verachess_support.edit_game)
    add_command(main, m_file, "保存棋谱", verachess_support.save_game)
    add_command(main, m_file, "读取棋谱", verachess_support.load_game)
    add_separator(main, m_file)
    add_command(main, m_file, "退出", verachess_support.exit_game)
    m_board = add_menu(main, top, "棋盘")
    add_checkbutton(main, m_board, "翻转视角", verachess_support.flip, verachess_support.MenuStats[MenuStatNames.flip])
    add_command(main, m_board, "复制当前局面FEN", verachess_support.copy_fen)
    add_command(main, m_board, "从剪贴板导入FEN", verachess_support.paste_fen)
    add_command(main, m_board, "摆局", verachess_support.set_board)
    m_clock = add_menu(main, top, "棋钟")
    add_checkbutton(main, m_clock, "关闭棋钟", verachess_support.clock_switch,
                    verachess_support.MenuStats[MenuStatNames.clock])
    add_command(main, m_clock, "设置比赛时长", verachess_support.change_clock)


def add_menu(main: MainWindow, top: tk.Tk, name: str) -> str:
    controller = tk.Menu(top, tearoff=0)
    main.Menus[name] = [controller, 0]     # init sub length = 0
    main.menubar.add_cascade(menu=controller, label=name)
    return name


def add_command(main: MainWindow, parent_name: str, name: str, command: Callable[[], None]):
    parent, length = main.Menus[parent_name]    # type: tk.Menu, int
    main.Menus[parent_name][1] += 1     # can't use length because it won't set to the pointer
    parent.add_command(command=command, label=name)
    assert name not in main.Sub_menus, "sub menu names conflict"
    main.Sub_menus[name] = [length, parent_name]


def add_checkbutton(main: MainWindow, parent_name: str, name: str, command: Callable[[], None], variable: tk.BooleanVar):
    parent, length = main.Menus[parent_name]    # type: tk.Menu, int
    main.Menus[parent_name][1] += 1     # can't use length because it won't set to the pointer
    parent.add_checkbutton(command=command, label=name, variable=variable)
    assert name not in main.Sub_menus, "sub menu names conflict"
    main.Sub_menus[name] = [length, parent_name]


def add_separator(main: MainWindow, parent_name: str):
    parent, length = main.Menus[parent_name]    # type: tk.Menu, int
    main.Menus[parent_name][1] += 1     # can't use length because it won't set to the pointer
    parent.add_separator()


if __name__ == '__main__':
    vp_start_gui()

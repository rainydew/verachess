#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Oct 06, 2019 11:52:10 PM CST  platform: Windows NT

import sys
import easygui
import pyperclip
import c960confirm
import clockconfirm
from clock import refresh_clock
from verachess_global import Globals, release_model_lock
from typing import List, Tuple, Dict
from verachess import destroy_MainWindow
from consts import Pieces, Positions, MenuStatNames, EndType, Winner, Color, Paths, CpuMoveConf
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

CellValues = None  # type: List[List[tk.StringVar]]
MenuStats = {}  # type: Dict[str, tk.BooleanVar]
Eco = WhitePlayerInfo = BlackPlayerInfo = WhiteTotalTime = BlackTotalTime = WhiteUseTime = BlackUseTime = \
    None  # type: tk.StringVar
WhiteFlagImg = BlackFlagImg = None  # type: tk.PhotoImage
MoveScaleVar = None  # type: tk.IntVar
FlagWidth = 54  # modify it if you want


def set_Tk_var():
    global CellValues, MenuStats, Eco, WhitePlayerInfo, BlackPlayerInfo, WhiteTotalTime, BlackTotalTime, WhiteUseTime, \
        BlackUseTime, WhiteFlagImg, BlackFlagImg, MoveScaleVar
    CellValues = [[tk.StringVar(value="") for _ in range(8)] for _ in range(8)]
    MenuStats[MenuStatNames.flip] = tk.BooleanVar(value=False)
    MenuStats[MenuStatNames.clock] = tk.BooleanVar(value=True)
    Eco = tk.StringVar()
    Eco.set('ECO - A00\nIrregular Opening')
    WhitePlayerInfo = tk.StringVar()
    WhitePlayerInfo.set('白方：人类')
    BlackPlayerInfo = tk.StringVar()
    BlackPlayerInfo.set('黑方：人类')
    WhiteTotalTime = tk.StringVar()
    WhiteTotalTime.set("00 : 05 : 00")
    BlackTotalTime = tk.StringVar()
    BlackTotalTime.set("00 : 05 : 00")
    WhiteUseTime = tk.StringVar()
    WhiteUseTime.set("00 : 00")
    BlackUseTime = tk.StringVar()
    BlackUseTime.set("00 : 00")
    WhiteFlagImg = tk.PhotoImage()
    WhiteFlagImg.configure(file=Paths.flag + "china.gif")
    BlackFlagImg = tk.PhotoImage()
    BlackFlagImg.configure(file=Paths.flag + "china.gif")
    MoveScaleVar = tk.IntVar()
    MoveScaleVar.set(0)


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
                j += int(char)  # if this errors, char is illegal


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
        [main.Cells[r][c].configure(background=Color.yellow_dark if (r + c) % 2 else Color.yellow_light) for r in
         range(8)
         for c in range(8)]
    if inactive_color_list:  # deselect old first
        for r, c in inactive_color_list:
            main.Cells[r][c].configure(background=Color.yellow_dark if (r + c) % 2 else Color.yellow_light)
    if active_color_list:
        for r, c in active_color_list:
            main.Cells[r][c].configure(background=Color.cell_sel_dark if (r + c) % 2 else Color.cell_sel_light)


def refresh_flip():
    arg = MenuStats[MenuStatNames.flip].get()
    main = Globals.Main
    now_flip = main.Rows[0].winfo_y() != 0
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
    Globals.GameFen = fen
    Globals.White = fen.split(" ")[1] == "w"
    Globals.History = [fen]
    Globals.InfoHistory = []
    Globals.AlphabetMovelist = []
    Globals.PGNMovelist = []
    Globals.History_hash = [hash(" ".join(fen.split(" ")[:4]))]
    Globals.Game_end = EndType.unterminated
    Globals.Winner = Winner.unknown
    if fen == Positions.common_start_fen:
        Globals.Start_pos = Positions.name_normal_startpos
    else:
        Globals.Start_pos = fen
    Globals.MoveSlider = -1
    events.remove_pgn_from()
    events.refresh_start_pos_in_movelist()
    events.clear_check_cell()
    events.refresh_whole_board()
    set_cell_color(flush_all=True)
    clear_sunken_cell()
    redraw_c960_flags()
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
    if k is not None:  # too
        columns[k].configure(foreground=Color.magenta)


def reset_clock():
    clock_switch(reset=True)
    Globals.Wremain = Globals.Wtime
    Globals.Bremain = Globals.Btime
    Globals.Wuse = 0
    Globals.Buse = 0
    refresh_clock()


def refresh_clock_conf():
    conf = Globals.ClockConf
    Globals.Wtime = (conf.get('WhiteMinEntry') * 60 + conf.get('WhiteSecEntry')) * 1000
    Globals.Winc = conf.get('WhiteIncEntry') * 1000
    if conf.get('Sync'):
        Globals.Btime = Globals.Wtime
        Globals.Binc = Globals.Winc
    else:
        Globals.Btime = (conf.get('BlackMinEntry') * 60 + conf.get('BlackSecEntry')) * 1000
        Globals.Binc = conf.get('BlackIncEntry') * 1000
    Globals.CpuRebal = conf.get('CpuRebal')
    Globals.Cmv = {"UseDepth": CpuMoveConf.use_depth, "UseTimer": CpuMoveConf.use_timer, "UseNode": CpuMoveConf.use_node
                   }[conf.get("Cmv")]
    cpu_set = conf.get('CpuSet')
    if Globals.Cmv == CpuMoveConf.use_depth:
        Globals.CpuSet = int(cpu_set)
    elif Globals.Cmv == CpuMoveConf.use_timer:
        Globals.CpuSet = int(cpu_set * 1000)
    else:
        Globals.CpuSet = int(cpu_set * 1000000)
    reset_clock()


# events
def exit_game():
    if easygui.ynbox("你确定要退出吗？", "verachess 5.0", ["是", "否"]):
        destroy_MainWindow()
        sys.exit()


@model_locked
def new_normal():
    if any(Globals.Game_role.values()):
        easygui.msgbox("黑白双方都需要处于被玩家控制的状态，且不使用FICS联网时，才能重新开局。请先将黑白双方均设为人类")
        return
    if easygui.ynbox("这将重置当前棋局信息，确认重新开始棋局吗？", "verachess 5.0", ["是", "否"]):
        Globals.Chess_960_Columns = (None, None, None)
        set_game_fen(Positions.common_start_fen)
        reset_clock()
        MenuStats[MenuStatNames.flip].set(False)
        refresh_flip()


@model_locked
def new_c960():
    if any(Globals.Game_role.values()):
        easygui.msgbox("黑白双方都需要处于被玩家控制的状态，且不使用FICS联网时，才能重新开局。请先将黑白双方均设为人类")
        return
    if easygui.ynbox("这将重置当前棋局信息，确认重新开始棋局吗？", "verachess 5.0", ["是", "否"]):
        main_window = Globals.Main.Top
        sub_window, confirm_widget = c960confirm.create_Toplevel1(root=main_window)
        sub_window.transient(main_window)  # show only one window in taskbar
        sub_window.grab_set()  # set as model window
        Globals.Main.Top.wait_window(sub_window)  # wait for window return, to get return value
        res = confirm_widget.Result

        if res is None:
            return
        rkr, pos = res
        Globals.Chess_960_Columns = rkr  # 新局面不走校验逻辑，必须手动设置chess960的易位列
        set_game_fen(pos)
        reset_clock()
        MenuStats[MenuStatNames.flip].set(False)
        refresh_flip()


@model_locked
def change_clock():
    if any(Globals.Game_role.values()):
        easygui.msgbox("黑白双方都需要处于被玩家控制的状态，且不使用FICS联网时，才能设置棋钟。请先将黑白双方均设为人类")
        return
    main_window = Globals.Main.Top
    sub_window, confirm_widget = clockconfirm.create_Toplevel1(root=main_window, **Globals.ClockConf)
    # 考虑子窗体独立测试需要，禁止子窗体直接访问需要初始化的Globals变量
    sub_window.transient(main_window)  # show only one window in taskbar
    sub_window.grab_set()  # set as model window
    Globals.Main.Top.wait_window(sub_window)  # wait for window return, to get return value
    res = confirm_widget.Result

    if res is None:
        return
    Globals.ClockConf = res
    refresh_clock_conf()


def flip():
    # this is event for flip click
    refresh_flip()


def clock_switch(reset: bool = False):
    clock_disabled = MenuStats[MenuStatNames.clock]
    if reset:
        clock_disabled.set(True)
    if clock_disabled.get():
        Globals.Main.WhiteUse.configure(background=Color.clock_disabled)
        Globals.Main.BlackUse.configure(background=Color.clock_disabled)
        Globals.Main.WhiteTotal.configure(background=Color.clock_inactive)
        Globals.Main.BlackTotal.configure(background=Color.clock_inactive)
    else:
        Globals.Main.WhiteUse.configure(background=Color.clock_enabled)
        Globals.Main.BlackUse.configure(background=Color.clock_enabled)
        if Globals.White:
            Globals.Main.WhiteTotal.configure(background=Color.clock_active)
            Globals.Main.BlackTotal.configure(background=Color.clock_inactive)
        else:
            Globals.Main.WhiteTotal.configure(background=Color.clock_inactive)
            Globals.Main.BlackTotal.configure(background=Color.clock_active)


@model_locked
def copy_fen():
    pyperclip.copy(Globals.GameFen)
    easygui.msgbox("当前局面已经复制到剪贴板")


@model_locked
def paste_fen():
    if any(Globals.Game_role.values()):
        easygui.msgbox("黑白双方都需要处于被玩家控制的状态，且不使用FICS联网时，才能使用摆局功能")
        return
    elif not easygui.ynbox("将会重置当前棋局的信息，你确认要导入局面吗？", "verachess 5.0", ["是", "否"]):
        return
    fen = pyperclip.paste()
    res, msg = events.check_fen_format_valid(fen)  # 校验格式，如果chess960的局面校验通过，会设置chess960的易位列
    if not res:
        easygui.msgbox("FEN错误\n" + msg)
        return
    release_model_lock()  # very important, set fen require model lock
    set_game_fen(reformat_fen(fen))


@check_model
def cell_click(event: CallWrapper) -> None:
    if Globals.Game_end:
        return
    place = Globals.Reverse_cell_names[str(event.widget)]
    events.click_handler(place)


@check_model
def move_click(event: CallWrapper) -> None:
    place = Globals.ReverseMoveNames[str(event.widget)]
    events.move_change_handler(place)


def ListScroll(value):
    value = int(float(value))

    MoveScaleVar.set(value)
    all_moves = Globals.Main.Moves

    for i, move in enumerate(all_moves):
        row = Globals.MoveRows[i]
        move.place(y=24 * (row - value))


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

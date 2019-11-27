#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Nov 25, 2019 11:32:04 PM CST  platform: Windows NT

import sys

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import CallWrapper

WhiteEngineChoosen = BlackEngineChoosen = ListSelect = EngCountryVar = EngNameVar = EngCommandVar = EngEndingVar = \
    EngPriorityVar = CHashVar = CCpuVar = CpuTempVar = MemLimitVar = None  # type: tk.StringVar
FlagImg = None  # type: tk.PhotoImage
WatchMemLeak = UseWb2Uci = UseHash = UseCpu = WatchTemp = WatchMem = None     # type: tk.BooleanVar


def set_Tk_var():
    global WhiteEngineChoosen, BlackEngineChoosen, ListSelect, EngCountryVar, EngNameVar, EngCommandVar, EngEndingVar, \
        EngPriorityVar, UseHash, CHashVar, UseCpu, CCpuVar, WatchTemp, CpuTempVar, WatchMem, MemLimitVar, \
        WatchMemLeak, UseWb2Uci, FlagImg
    WhiteEngineChoosen = tk.StringVar(value='')
    BlackEngineChoosen = tk.StringVar(value='')
    ListSelect = tk.StringVar(value='')  # use {a b} to support tcl space
    EngCountryVar = tk.StringVar(value='')
    EngNameVar = tk.StringVar(value='')
    EngCommandVar = tk.StringVar(value='')
    EngEndingVar = tk.StringVar(value=r'\r\n')
    EngPriorityVar = tk.StringVar(value='中')
    UseHash = tk.BooleanVar(value=True)
    CHashVar = tk.StringVar(value='')
    UseCpu = tk.BooleanVar(value=True)
    CCpuVar = tk.StringVar(value='')
    WatchTemp = tk.BooleanVar(value=True)
    CpuTempVar = tk.StringVar(value='')
    WatchMem = tk.BooleanVar(value=True)
    MemLimitVar = tk.StringVar(value='')
    WatchMemLeak = tk.BooleanVar(value=True)
    UseWb2Uci = tk.BooleanVar(value=False)
    FlagImg = tk.PhotoImage()


def view():
    print('EngineView_support.view')
    sys.stdout.flush()


def c_close():
    print('EngineView_support.c_close')
    sys.stdout.flush()


def c_copy():
    print('EngineView_support.c_copy')
    sys.stdout.flush()


def configure():
    print('EngineView_support.configure')
    sys.stdout.flush()


def delete():
    print('EngineView_support.delete')
    sys.stdout.flush()


def new():
    print('EngineView_support.new')
    sys.stdout.flush()


def stash():
    print('EngineView_support.stash')
    sys.stdout.flush()


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


def destruct(event: CallWrapper) -> None:
    global FlagImg
    try:
        del FlagImg
    except NameError:
        pass


if __name__ == '__main__':
    import EngineView

    EngineView.vp_start_gui()

#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#    Nov 13, 2019 05:32:12 PM CST  platform: Windows NT
from typing import Dict, Union, List
from notify import alert
from consts import Color
import tkinter as tk
import easygui


if (lambda: None)():
    import uci_chart


w = ...  # type: uci_chart.Toplevel1
tempvar = ...   # type: tk.StringVar


def set_Tk_var():
    global tempvar
    tempvar = tk.StringVar(value="")


def cancel():
    destroy_window()


def confirm():

    destroy_window()


def default():
    print("default")


def choose(event: tk.Event):
    tree = w.Scrolledtreeview1
    if not tree.selection():
        return
    x, y = event.x, event.y
    item = tree.selection()
    v = tree.item(item[0])['values']    # type: List[str]
    v_type = v[1]
    v_default = v[2]
    v_require = v[3]
    v_cur_val = v[4]
    if v_type == "spin":
        m_spin(x, y, item, v_default, v_cur_val, v_require)
    elif v_type == "check" and not w.Editing:
        if v_cur_val == "false":
            tree.set(item, column="Value", value="true")
        else:
            tree.set(item, column="Value", value="false")
    elif v_type == "string":
        m_string(x, y, item, v_default, v_cur_val)
    elif v_type == "button" and not w.Editing:
        if v_cur_val == "":
            tree.set(item, column="Value", value="will push")
        else:
            tree.set(item, column="Value", value="")
    elif v_type == "combo" and not w.Editing:
        w.Editing = True
        vars = v_require.split("|")
        try:
            pre_var = vars.index(v_default)
        except:
            pre_var = 0
        res = easygui.choicebox("选择一个值", "单选类型", vars, pre_var)
        if res:
            tree.set(item, column="Value", value=res)
        w.Editing = False
    else:
        alert("类型{}不被支持".format(v_type))


def m_string(x, y, item, default, current_val):
    if w.Editing:
        return

    def string_conf():
        tree = w.Scrolledtreeview1
        tree.set(item, column="Value", value=tempvar.get())
        w.Temp.destroy()
        w.TempEntry = w.TempDefault = w.TempConfirm = w.TempUseDir = w.TempUseFile = None
        w.Editing = False

    def string_default():
        tempvar.set(default)

    def dir_open():
        tempvar.set(easygui.diropenbox("选择一个文件夹", "路径选择") or "")

    def file_open():
        tempvar.set(easygui.fileopenbox("选择一个文件", "文件选择") or "")

    w.Editing = True
    tempvar.set(current_val)
    w.Temp = tk.Frame(w.Top)
    w.Temp.place(x=x - 55, y=y - 24, height=48, width=140)

    w.TempEntry = tk.Entry(w.Temp)
    w.TempEntry.place(x=0, y=0, height=24, width=80)
    w.TempEntry.configure(background=Color.yellow_eco)
    w.TempEntry.configure(font="TkFixedFont")
    w.TempEntry.configure(textvariable=tempvar)

    w.TempConfirm = tk.Button(w.Temp)
    w.TempConfirm.place(x=80, y=0, height=24, width=30)
    w.TempConfirm.configure(background="#d9d9d9")
    w.TempConfirm.configure(text="确定")
    w.TempConfirm.configure(command=string_conf)

    w.TempDefault = tk.Button(w.Temp)
    w.TempDefault.place(x=110, y=0, height=24, width=30)
    w.TempDefault.configure(background="#d9d9d9")
    w.TempDefault.configure(text="默认")
    w.TempDefault.configure(command=string_default)

    w.TempUseDir = tk.Button(w.Temp)
    w.TempUseDir.place(x=0, y=24, height=24, width=70)
    w.TempUseDir.configure(background="#d9d9d9")
    w.TempUseDir.configure(text="选文件夹")
    w.TempUseDir.configure(command=dir_open)

    w.TempUseFile = tk.Button(w.Temp)
    w.TempUseFile.place(x=70, y=24, height=24, width=70)
    w.TempUseFile.configure(background="#d9d9d9")
    w.TempUseFile.configure(text="选择文件")
    w.TempUseFile.configure(command=file_open)


def m_spin(x, y, item, default, current_val, require):
    if w.Editing:
        return

    def spin_conf():
        val = tempvar.get()
        try:
            assert float(val) == int(val)
            assert int(min) <= int(val) <= int(max)
        except:
            alert("数值或格式不正确")
            return
        tree = w.Scrolledtreeview1
        tree.set(item, column="Value", value=int(val))
        w.Temp.destroy()
        w.TempEntry = w.TempDefault = w.TempConfirm = None
        w.Editing = False

    def spin_default():
        tempvar.set(default)

    w.Editing = True
    min, max = require.split("-")
    tempvar.set(current_val)
    w.Temp = tk.Frame(w.Top)
    w.Temp.place(x=x - 55, y=y, height=24, width=110)

    w.TempEntry = tk.Entry(w.Temp)
    w.TempEntry.place(x=0, y=0, height=24, width=50)
    w.TempEntry.configure(background=Color.yellow_eco)
    w.TempEntry.configure(font="TkFixedFont")
    w.TempEntry.configure(textvariable=tempvar)

    w.TempConfirm = tk.Button(w.Temp)
    w.TempConfirm.place(x=50, y=0, height=24, width=30)
    w.TempConfirm.configure(background="#d9d9d9")
    w.TempConfirm.configure(text="确定")
    w.TempConfirm.configure(command=spin_conf)

    w.TempDefault = tk.Button(w.Temp)
    w.TempDefault.place(x=80, y=0, height=24, width=30)
    w.TempDefault.configure(background="#d9d9d9")
    w.TempDefault.configure(text="默认")
    w.TempDefault.configure(command=spin_default)


def init(top, gui, pgns: List[Dict[str, Union[Dict, str]]]):
    global w, top_level, root
    w = gui  # type: uci_chart.Toplevel1
    top_level = top
    root = top
    columns = w.Columns
    for i, pgn in enumerate(pgns):
        pgn_small = {k.lower(): v for k, v in pgn.get("header").items()}
        if pgn_small.get("variant") and pgn_small.get("variant").lower() in ("chess960", "fischerandom"):
            pgn_small["eco"] = "Chess960"
        w.Scrolledtreeview1.insert("", "end", text=str(i), values=[pgn_small.get(k) or "" for k in columns])


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

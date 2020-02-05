#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Nov 25, 2019 11:32:04 PM CST  platform: Windows NT

import sys
import tkinter as tk
import easygui
import os
import json
import uci_chart
from typing import List, Dict, Union, Optional
from verachess_global import Globals
from consts import Paths, UciAbout, EngineConfigs
from tkinter import CallWrapper
from tooltip import alert
from engineview_global import Globals as engGlobals

if (lambda: None)():
    import engineview

WhiteEngineChoosen = BlackEngineChoosen = ListSelect = EngCountryVar = EngNameVar = EngCommandVar = EngEndingVar = \
    EngPriorityVar = CHashVar = CCpuVar = CpuTempVar = MemLimitVar = None  # type: tk.StringVar
FlagImg = None  # type: tk.PhotoImage
WatchMemLeak = UseWb2Uci = UseHash = UseCpu = WatchTemp = WatchMem = None     # type: tk.BooleanVar
w = None  # type: engineview.Toplevel1
EngineLists = [""]


def set_Tk_var():
    global WhiteEngineChoosen, BlackEngineChoosen, ListSelect, EngCountryVar, EngNameVar, EngCommandVar, EngEndingVar, \
        EngPriorityVar, UseHash, CHashVar, UseCpu, CCpuVar, WatchTemp, CpuTempVar, WatchMem, MemLimitVar, \
        WatchMemLeak, UseWb2Uci, FlagImg
    WhiteEngineChoosen = tk.StringVar(value='')
    BlackEngineChoosen = tk.StringVar(value='')
    ListSelect = tk.StringVar(value='')  # use {a b} to support tcl space
    EngCountryVar = tk.StringVar(value='Unknown')
    EngCountryVar.trace_variable(mode="w", callback=flush_flag)
    EngNameVar = tk.StringVar(value='')
    EngCommandVar = tk.StringVar(value='')
    EngEndingVar = tk.StringVar(value=r'\r\n')
    EngEndingVar.trace_variable(mode="w", callback=validate_ending)
    EngPriorityVar = tk.StringVar(value='中')
    UseHash = tk.BooleanVar(value=True)
    CHashVar = tk.StringVar(value='512')
    UseCpu = tk.BooleanVar(value=True)
    CCpuVar = tk.StringVar(value='4')
    WatchTemp = tk.BooleanVar(value=True)
    CpuTempVar = tk.StringVar(value='80')
    WatchMem = tk.BooleanVar(value=True)
    MemLimitVar = tk.StringVar(value='512')
    WatchMemLeak = tk.BooleanVar(value=True)
    UseWb2Uci = tk.BooleanVar(value=False)
    FlagImg = tk.PhotoImage()
    init_engines_list()


def flush_flag(*args):
    country = EngCountryVar.get()
    if country == "Unknown":
        FlagImg.blank()
    else:
        FlagImg.configure(file=Paths.flag + country.lower() + ".gif")


def validate_ending(*args):
    ending = EngEndingVar.get()
    if ending in [r"\r\n", r"\n"]:
        return
    elif ending in ["\r\n", "\n"]:
        EngEndingVar.set(ending.encode('unicode-escape').decode())
    else:
        alert("引擎的ending类型解析错误，采用默认值代替", "提示")
        EngEndingVar.set(r"\r\n")


def get_selection() -> Optional[int]:
    selection = w.EngineSpinBox.curselection()
    if not selection:
        return None
    else:
        return selection[0]


def info_get(d: dict, k: str, default_type: Optional[type] = None, default_value=None):
    return d.get(k) or default_type() or default_value


def stash_cell():
    EngCountryVar.set('Unknown')
    EngNameVar.set('')
    EngCommandVar.set('')
    EngEndingVar.set(r'\r\n')
    EngPriorityVar.set('中')
    UseHash.set(True)
    CHashVar.set('512')
    UseCpu.set(True)
    CCpuVar.set('4')
    WatchTemp.set(True)
    CpuTempVar.set('80')
    WatchMem.set(True)
    MemLimitVar.set('512')
    WatchMemLeak.set(True)
    UseWb2Uci.set(False)
    w.InfoVar.set(UciAbout.no_info)


def init_engines_list():
    global EngineLists
    file = Paths.binpath + "/../engines/engines.json"
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("[]")
    with open(file, "r", encoding="utf-8", errors="replace") as f:
        try:
            Globals.Engines = json.loads(f.read())  \
                # type: List[Dict[str, Union[str, List[Dict[str, Union[str, int, bool, List[str]]]]]]]
            assert type(Globals.Engines) == list
        except:
            alert("储存引擎信息的文件engines.json格式被损坏，无法识别", "警告")
            Globals.Engines = []
    errored_list = []
    for i, engine in enumerate(Globals.Engines):
        try:
            name = engine.get("name")
            assert type(name) == str
            EngineLists.append(name)
        except:
            errored_list.append(i)
            continue
    if errored_list:
        alert("部分引擎信息解析错误，这些引擎将被忽略。引擎信息文件会自动修复，并剔除这些不可解析的引擎", "警告")
        Globals.Engines = [x for i, x in enumerate(Globals.Engines) if i not in errored_list]
    ListSelect.set(" ".join(EngineLists))


def engine_path_changed(newpath: str, argdict: Dict[str, str]) -> None:
    main_window = engGlobals.Main.Top
    sub_window, setboard_widget = uci_chart.create_Toplevel1(root=main_window, detect_command=newpath)
    sub_window.transient(main_window)  # show only one window in taskbar
    sub_window.grab_set()  # set as model window
    main_window.wait_window(sub_window)  # wait for window return, to get return value
    info = setboard_widget.Result
    # todo argdict combine with info
    print(info)


# events here
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


def new(filepath: Optional[str] = None):
    if filepath is None:
        filepath = easygui.fileopenbox("选择引擎文件", "添加引擎", Paths.engines + "*.exe")
    sub_name = filepath.replace("\\", "/").split("/")[-1].replace(".exe", "").split("_")[0].split("-")[0].split()[0]
    if filepath:
        name = easygui.enterbox("给你的引擎取一个名称(必填)，这个名称要和已有的名称不同", "引擎命名", sub_name)
    else:
        name = sub_name
    if not name:
        name = sub_name

    argdict = {
        "name": name,
        "command": filepath,
        "country": "Unknown",
        "protocol": "uci"
    }

    engine_path_changed(name, argdict)


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


def choose(event: Optional[CallWrapper] = None) -> None:
    selection = get_selection()
    if selection is None:
        stash_cell()
        engGlobals.current_selection = None
    else:
        info_dict = Globals.Engines[selection]
        engGlobals.current_selection = info_dict.get("name")
        w.InfoVar.set(json.dumps({x.get("name"): x.get("value") for x in info_dict.get("options")}, indent=2))
        EngNameVar.set(info_get(info_dict, EngineConfigs.name))
        EngCountryVar.set(info_get(info_dict, EngineConfigs.country))
        EngCommandVar.set(info_get(info_dict, EngineConfigs.command))
        EngEndingVar.set(info_get(info_dict, EngineConfigs.ending))


def destruct(event: CallWrapper) -> None:
    global FlagImg
    try:
        del FlagImg
    except NameError:
        pass

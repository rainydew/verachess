# coding: utf-8
import time
import threading
import tkinter as tk
import verachess_support
from verachess_global import Globals
from consts import MenuStatNames, Color


def to_ms(ms: int):
    return time.strftime("%M : %S", time.gmtime((ms - 1 )// 1000 + 1))


def to_hms(ms: int):
    return time.strftime("%H : %M : %S", time.gmtime(ms // 1000))


def update_string_var(var: tk.StringVar, to_val: str):
    if var.get() != to_val:
        var.set(to_val)     # set is slower


def refresh_clock():
    update_string_var(verachess_support.WhiteTotalTime, to_hms(Globals.Wremain))
    update_string_var(verachess_support.BlackTotalTime, to_hms(Globals.Bremain))
    update_string_var(verachess_support.WhiteUseTime, to_ms(Globals.Wuse))
    update_string_var(verachess_support.BlackUseTime, to_ms(Globals.Buse))


def before_change_mover():
    # use it before mover changed!!!!!!
    if not verachess_support.MenuStats[MenuStatNames.clock].get():
        if Globals.White:
            Globals.Wremain += Globals.Winc
            Globals.Buse = 0
            Globals.Main.WhiteTotal.configure(background=Color.clock_inactive)
            Globals.Main.BlackTotal.configure(background=Color.clock_active)
        else:
            Globals.Bremain += Globals.Binc
            Globals.Wuse = 0
            Globals.Main.WhiteTotal.configure(background=Color.clock_active)
            Globals.Main.BlackTotal.configure(background=Color.clock_inactive)
        refresh_clock()


def tick():
    s = int(time.time() * 1000)
    irange = range(5)
    while True:
        for i in irange:
            time.sleep(0.2)
            now = int(time.time() * 1000)
            margin = now - s
            if not verachess_support.MenuStats[MenuStatNames.clock].get():
                if Globals.White:
                    Globals.Wuse += margin
                    Globals.Wremain -= margin
                else:
                    Globals.Buse += margin
                    Globals.Bremain -= margin
                if not i:
                    refresh_clock()
            s = now


Tick_Thread = threading.Thread(target=tick)

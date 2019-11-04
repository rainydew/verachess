# coding: utf-8
import time
import threading
import tkinter as tk
import verachess_support
import easygui
from verachess_global import Globals, ModelLock
from consts import MenuStatNames, Color, EndType, Winner


def to_ms(ms: int) -> str:
    return time.strftime("%M : %S", time.gmtime((ms - 1 )// 1000 + 1))


def to_hms(ms: int) -> str:
    return time.strftime("%H : %M : %S", time.gmtime(ms // 1000)) if ms >= 0 else time.strftime(
        "-0 : %M : %S", time.gmtime(-(ms // 1000)))


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


def timeout(white: bool, silent: bool = False):
    if Globals.Game_end:
        return
    refresh_clock()
    narrow_fen = Globals.GameFen.split(" ")[0]
    wp, bp = len([x for x in narrow_fen if x.isupper()]), len([x for x in narrow_fen if x.islower()])
    if white:
        if bp != 1:
            Globals.Game_end = EndType.time_forfeit
            message = "白方超时，黑方胜利"
            Globals.Winner = Winner.black
        else:
            Globals.GameFen = EndType.single_king_with_opp_violate
            message = "白方超时，因黑方只有单王，和棋"
            Globals.Winner = Winner.draw
    else:
        if wp != 1:
            Globals.Game_end = EndType.time_forfeit
            message = "黑方超时，白方胜利"
            Globals.Winner = Winner.white
        else:
            Globals.GameFen = EndType.single_king_with_opp_violate
            message = "黑方超时，因白方只有单王，和棋"
            Globals.Winner = Winner.draw
    if not silent:
        with ModelLock():
            easygui.msgbox(message, "棋局结束", "确认")


def tick():
    s = int(time.time() * 1000)
    irange = range(5)
    while True:
        for i in irange:
            time.sleep(0.2)
            now = int(time.time() * 1000)
            margin = now - s
            if not verachess_support.MenuStats[MenuStatNames.clock].get() and not Globals.Game_end:
                if Globals.White:
                    Globals.Wuse += margin
                    Globals.Wremain -= margin
                    if Globals.Wremain < 0:
                        timeout(True)
                else:
                    Globals.Buse += margin
                    Globals.Bremain -= margin
                    if Globals.Bremain < 0:
                        timeout(False)
                if not i:
                    refresh_clock()
            s = now


Tick_Thread = threading.Thread(target=tick)

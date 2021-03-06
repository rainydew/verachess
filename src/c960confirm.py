#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Oct 27, 2019 12:17:52 AM CST  platform: Windows NT

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

import c960confirm_support


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    c960confirm_support.set_Tk_var()
    top = ConfirmWindow(root)
    c960confirm_support.init(root, top)
    root.mainloop()
    print(top.Result)


w = None


def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel(root)
    c960confirm_support.set_Tk_var()
    top = ConfirmWindow(w)
    c960confirm_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class ConfirmWindow:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("288x230+546+174")
        top.title("Chess960局面选择")
        top.configure(background="#d9d9d9")

        self.Label1 = tk.Label(top)
        self.Label1.place(x=40, y=10, height=26, width=156)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(text='''选一个局面编号:1~960''')

        self.Label2 = tk.Label(top)
        self.Label2.place(x=40, y=90, height=26, width=156)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(text='''或者直接输入起始阵型''')

        self.Spinbox1 = tk.Spinbox(top, from_=1.0, to=960.0)
        self.Spinbox1.place(x=40, y=50, height=30, width=155)
        self.Spinbox1.configure(buttonbackground="#d9d9d9")
        self.Spinbox1.configure(command=c960confirm_support.scroll)
        self.Spinbox1.configure(textvariable=c960confirm_support.c960value)
        self.Spinbox1.bind('<KeyRelease>', lambda e: c960confirm_support.spin(e))

        self.Entry1 = tk.Entry(top)
        self.Entry1.place(x=40, y=120, height=21, width=155)
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(textvariable=c960confirm_support.c960pos)
        self.Entry1.bind('<KeyRelease>', lambda e: c960confirm_support.text(e))

        self.Button1 = tk.Button(top)
        self.Button1.place(x=25, y=170, height=33, width=72)
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=c960confirm_support.Confirm)
        self.Button1.configure(text='''确定''')

        self.Button2 = tk.Button(top)
        self.Button2.place(x=110, y=170, height=33, width=72)
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(command=c960confirm_support.Random)
        self.Button2.configure(text='''随机''')

        self.Button3 = tk.Button(top)
        self.Button3.place(x=195, y=170, height=33, width=72)
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(command=c960confirm_support.Cancel)
        self.Button3.configure(text='''取消''')

        self.Result = None      # to return a result


if __name__ == '__main__':
    print("test mode")
    vp_start_gui()

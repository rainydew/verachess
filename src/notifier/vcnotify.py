# coding: utf-8
import sys
import os
import struct
import time
import win32con

from win32api import *

# Try and use XP features, so we get alpha-blending etc.
try:
    from win32gui import *
except ImportError:
    from winxpgui import *


class PyNOTIFYICONDATA:
    _struct_format = (
        "I"  # DWORD cbSize; 结构大小(字节)
        "I"  # HWND hWnd; 处理消息的窗口的句柄
        "I"  # UINT uID; 唯一的标识符
        "I"  # UINT uFlags;
        "I"  # UINT uCallbackMessage; 处理消息的窗口接收的消息
        "I"  # HICON hIcon; 托盘图标句柄
        "128s"  # TCHAR szTip[128]; 提示文本
        "I"  # DWORD dwState; 托盘图标状态
        "I"  # DWORD dwStateMask; 状态掩码
        "256s"  # TCHAR szInfo[256]; 气泡提示文本
        "I"  # union {
        #   UINT  uTimeout; 气球提示消失时间(毫秒)
        #   UINT  uVersion; 版本(0 for V4, 3 for V5)
        # } DUMMYUNIONNAME;
        "64s"  # TCHAR szInfoTitle[64]; 气球提示标题
        "I"  # DWORD dwInfoFlags; 气球提示图标
    )
    _struct = struct.Struct(_struct_format)

    hWnd = 0
    uID = 0
    uFlags = 0
    uCallbackMessage = 0
    hIcon = 0
    szTip = ''.encode()
    dwState = 0
    dwStateMask = 0
    szInfo = ''.encode()
    uTimeoutOrVersion = 0
    szInfoTitle = ''.encode()
    dwInfoFlags = 0

    def pack(self):
        return self._struct.pack(
            self._struct.size,
            self.hWnd,
            self.uID,
            self.uFlags,
            self.uCallbackMessage,
            self.hIcon,
            self.szTip,
            self.dwState,
            self.dwStateMask,
            self.szInfo,
            self.uTimeoutOrVersion,
            self.szInfoTitle,
            self.dwInfoFlags
        )

    def __setattr__(self, name, value):
        # avoid wrong field names
        if not hasattr(self, name):
            raise NameError(name)
        self.__dict__[name] = value


class MainWindow:
    def __init__(self, title, msg, duration=3):
        # Register the Window class.
        title = title.encode("gbk")
        msg = msg.encode("gbk")

        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbarDemo"  # 字符串只要有值即可，下面3处也一样
        wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy}  # could also specify a wndproc.
        classAtom = RegisterClass(wc)

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(classAtom, "Taskbar Demo", style,
                                 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                 0, 0, hinst, None
                                 )
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join(sys.prefix, "pyc.ico"))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "Balloon  tooltip demo")
        Shell_NotifyIcon(NIM_ADD, nid)
        self.show_balloon(title, msg)
        time.sleep(duration)
        DestroyWindow(self.hwnd)

    def show_balloon(self, title, msg):
        # For this message I can't use the win32gui structure because
        # it doesn't declare the new, required fields
        nid = PyNOTIFYICONDATA()
        nid.hWnd = self.hwnd
        nid.uFlags = NIF_INFO

        # type of balloon and text are random
        nid.dwInfoFlags = NIIF_INFO
        nid.szInfo = msg[:64]
        nid.szInfoTitle = title[:256]

        # Call the Windows function, not the wrapped one
        from ctypes import windll
        Shell_NotifyIcon = windll.shell32.Shell_NotifyIconA
        Shell_NotifyIcon(NIM_MODIFY, nid.pack())

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)  # Terminate the app.


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: alert.exe <title> <message>")
        sys.exit()
    MainWindow(sys.argv[1], sys.argv[2])

#!/usr/bin/env python
# coding: utf-8
import os, struct, time, re, sys


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


sys_bit = struct.calcsize("P") * 8
if sys_bit == 64:
    bin = resource_path(os.path.join("cpuz_x64.exe -txt=res"))
elif sys_bit == 32:
    bin = resource_path(os.path.join("cpuz_x32.exe -txt=res"))
else:
    input("你的系统位数{}不受支持，回车退出".format(sys_bit))
    os._exit(0)


record_path = resource_path(os.path.join("res.txt"))
while True:
    try:
        os.remove(record_path)
    except FileNotFoundError:
        pass
    os.system(bin)

    try:
        with open(record_path) as f:
            lines = f.readlines()
            try:
                temp = [re.findall("\t(\d+) degC", x) for x in lines if "(Package)\n" in x][0][0]
                sys.stdout.write(time.strftime("%Y%m%d-%H%M%S") + " " + temp + "\n")
                sys.stdout.flush()
            except:
                input("文件解析错误，可能是不支持cpu温度传感器")
                os._exit(0)
    except:
        input("文件找不到或不能打开")
        os._exit(0)

    time.sleep(25)

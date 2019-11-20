#!/usr/bin/env python
# coding: utf-8
import os, struct, time, re


def _get_bin_path():
    filepath = os.path.abspath(".").replace("\\", "/")  # type: str
    if filepath.split("/")[-2] == "src":
        binpath = filepath + "/../../bin"
    else:
        binpath = filepath
    return binpath


binpath = _get_bin_path()
sys_bit = struct.calcsize("P") * 8
if sys_bit == 64:
    bin = binpath + "/cpu-z/cpuz_x64.exe -txt=res"
elif sys_bit == 32:
    bin = binpath + "/cpu-z/cpuz_x32.exe -txt=res"
else:
    input("你的系统位数{}不受支持，回车退出".format(sys_bit))
    os._exit(0)


while True:
    try:
        os.remove(binpath + "/cpu-z/res.txt")
    except FileNotFoundError:
        pass
    os.system(bin)


    try:
        with open(binpath + "/cpu-z/res.txt") as f:
            lines = f.readlines()
            try:
                temp = [re.findall("\t(\d+) degC", x) for x in lines if "(Package)\n" in x][0][0]
                print(time.strftime("%Y%m%d-%H%M%S") + " " + temp)
            except:
                input("文件解析错误，可能是不支持cpu温度传感器")
                os._exit(0)
    except:
        input("文件找不到或不能打开")
        os._exit(0)

    time.sleep(25)

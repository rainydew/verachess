#!/usr/bin/env python
# coding: utf-8
import subprocess
from psutil import virtual_memory
from threading import Thread
from time import sleep
from consts import Paths
from verachess_global import Tracers

_started = False


def cpu_monitor():
    binary = Paths.binpath + "/monitor.exe"

    while True:
        p = subprocess.Popen(binary, stdout=subprocess.PIPE)
        while p.poll() is None:
            line = p.stdout.readline().strip()
            if line:
                try:
                    _, cpu_temp = line.decode("utf-8").split()
                except:
                    cpu_temp = "N/A"
            Tracers.cpu_temp = cpu_temp

        del p

        sleep(20)


def mem_monitor():
    vm = virtual_memory()
    total = vm.total // 1048576
    while True:
        free = vm.free // 1048576
        Tracers.mem_avail = "%d/%dM" %(free, total)
        sleep(15)
        vm = virtual_memory()


def start_watch():
    global _started
    if not _started:
        _t = Thread(target=cpu_monitor)
        _u = Thread(target=mem_monitor)
        _t.setDaemon(True)
        _u.setDaemon(True)
        _t.start()
        _u.start()
        _started = True

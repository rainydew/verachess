#!/usr/bin/env python
# coding: utf-8
import os
from consts import Paths


def alert(msg: str, title: str = "verachess5.0") -> None:
    os.system(Paths.binpath + "/vcnotify.exe {} {}".format(msg.replace(" ", "_"), title.replace(" ", "_")))

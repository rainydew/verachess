# coding: utf-8
import time
import threading
import verachess_support
from typing import Optional
from verachess_global import Globals
from consts import MenuStatNames


def tick():
    s = int(time.time() * 1000)
    buffer = 0
    last_mover = None   # type: Optional[bool]
    while True:
        time.sleep(0.2)
        now = int(time.time() * 1000)
        if not verachess_support.MenuStats[MenuStatNames.clock]:
            if Globals.White:
                if not last_mover:
                    buffer = 0
                    last_mover = True
                buffer += now - s
            else:
                if last_mover is not False:
                    buffer = 0
                    last_mover = False

        else:
            last_mover = None
        s = now

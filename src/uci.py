# coding: utf-8
from typing import Optional, Union, List
from singleton.singleton import Singleton
from tooltip import alert
import gc
import json
import time
import threading
import subprocess

if (lambda: None)():
    from io import TextIO


def tby(s: str):
    return s.encode("utf-8", errors='replace')


def tst(b: bytes):
    return b.decode("utf-8", errors="replace")


def _get_between(args: List[str], c_name: str, next_name: str = None) -> str:
    if next_name in args:
        return " ".join(args[args.index(c_name) + 1: args.index(next_name)])
    else:
        return " ".join(args[args.index(c_name) + 1:])


def _get_choices(args: List[str]) -> List[str]:
    return " ".join(args[args.index("var") + 1:]).split(" var ")


def time_stamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")


class UciEngine:
    def __init__(self, cmd: str, name: str = "unknown", log_path: Optional[str] = None, buffer: int = 50,
                 ending: Optional[str] = None, setting=None):  # todo: pass a dictionary for configures and auto set uci
        self.cmd = cmd
        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.stdin = self.proc.stdin
        self.stdout = self.proc.stdout
        self.poll = self.proc.poll
        self.kill = self.proc.kill
        self.buffer = buffer
        self.data = []
        self.wait = None
        if log_path:
            self.log_file = open(log_path, "a", buffering=1)  # type: Optional[TextIO]
            self.log_file.write(time_stamp() + "\n")
        else:
            self.log_file = None
        if not ending:
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            time.sleep(0.5)
            p.stdin.write(b"uci\r\n")
            p.stdin.flush()
            p.stdin.write(b'quit\r\n')
            p.stdin.flush()
            p.kill()
            if any([b'uciok' in x for x in p.stdout.readlines()]):
                self.ending = b'\r\n'
            else:
                self.ending = b'\n'
        else:
            time.sleep(0.5)
            self.ending = tby(ending)
        t = threading.Thread(target=self.block_data)
        t.setDaemon(True)
        t.start()
        try:
            res = self.send_wait('uci', 'uciok')
        except TimeoutError:
            alert("命令行{}不是一个有效的uci引擎".format(cmd))
            raise
        opt = {"name": name, "ending": tst(self.ending), "command": cmd, "options": []}
        for line in res:
            if "option" in line:
                args = line.split()
                info_type = args[args.index("type") + 1]
                info = {'name': _get_between(args, 'name', 'type'), 'type': info_type}
                if info_type == "spin":
                    info['default'] = int(args[args.index("default") + 1])
                    info['min'] = int(args[args.index("min") + 1])
                    info['max'] = int(args[args.index("max") + 1])
                    info['value'] = info['default']    # todo: if the values passed is not default...
                elif info_type == "check":
                    info['default'] = json.loads(args[args.index("default") + 1])
                    info['value'] = info['default']
                elif info_type == "string":      # if we wan't to compact cutechess, we may find that he uses "text" instead
                    info['default'] = _get_between(args, 'default')
                    info['value'] = info['default']
                elif info_type == "combo":
                    info['default'] = _get_between(args, 'default', 'var')
                    info['value'] = info['default']
                    info['choices'] = _get_choices(args)
                elif info_type != "button":
                    alert("类型{}不是标准的uci变量类型，不能被识别".format(type))
                    continue
                opt["options"].append(info)
        self.options = opt

    def send(self, cmd: str):
        if self.log_file:
            self.log_file.write(">{}\t{}\n".format(cmd, time_stamp()))
        cmd = tby(cmd)
        if self.ending not in cmd:
            cmd += self.ending
        self.stdin.write(cmd)
        self.stdin.flush()

    def block_data(self):
        # todo: write to console (Scrolled Listbox)
        while self.proc.poll() is None:
            line = tst(self.stdout.readline()).replace("\r", "").replace("\n", "")
            if line:
                self.data.append(line)
                if self.wait and self.wait in line:
                    self.wait = None
                if self.log_file:
                    self.log_file.write(line + "\n")
                if len(self.data) == self.buffer + 10:
                    del self.data[:10]

    def clear_buff(self):
        self.data = []

    def send_wait(self, cmd: str, waitfor: str, timeout: Optional[int] = 3) -> List[str]:
        self.wait = waitfor
        self.clear_buff()
        self.send(cmd)
        s = time.time()
        while time is None or time.time() - s <= timeout:
            if self.wait is None:
                return self.data
            time.sleep(0.05)
        raise TimeoutError("waiting time out")

    def quit(self):
        try:
            # write quit
            self.send('quit')
            self.proc.kill()
            if self.log_file:
                self.log_file.close()
        except:
            pass


@Singleton
class _Engines:
    def __init__(self):
        self._white_engine = None  # type: UciEngine
        self._black_engine = None  # type: UciEngine
        self._anly_engine = None   # type: UciEngine

    @property
    def anly_engine(self):
        if self._anly_engine and self._anly_engine.poll() is not None:
            self._anly_engine = None
        return self._anly_engine

    @anly_engine.setter
    def anly_engine(self, value):
        if self._anly_engine:
            self._anly_engine.quit()
            del self._anly_engine
            gc.collect()
        self._anly_engine = value

    @property
    def white_engine(self) -> Optional[UciEngine]:
        if self._white_engine and self._white_engine.poll() is not None:
            self._white_engine = None
        return self._white_engine

    @white_engine.setter
    def white_engine(self, value: UciEngine):
        if self._white_engine:
            self._white_engine.quit()
            del self._white_engine
            gc.collect()
        self._white_engine = value

    @property
    def black_engine(self) -> Optional[UciEngine]:
        if self._black_engine and self._black_engine.poll() is not None:
            self._black_engine = None
        return self._black_engine

    @black_engine.setter
    def black_engine(self, value: UciEngine):
        if self.black_engine:
            self._black_engine.quit()
            del self._black_engine
            gc.collect()
        self._black_engine = value


Engines = _Engines.instance()   # type: _Engines


if __name__ == '__main__':
    Engines.white_engine = UciEngine('../engines/stockfish/stockfish191114_x64.exe', 'stockfish',
                                     '../engines/stockfish/debug.log')
    print(json.dumps(Engines.white_engine.options, indent=4))
    Engines.white_engine.quit()

# coding: utf-8
import sys
sys.path.append('../')

from boards import Pgns
from consts import Positions
import time

st = time.time()

try:
    with open("verachess.eco", "r", encoding="utf-8") as g:
        res = len(g.readlines())
except:
    res = 0

with open("ecocodes9.txt", encoding="iso8859-1") as f:
    with open("verachess.eco", "a", encoding="utf-8") as g:
        for i, line in enumerate(f):
            if i < res:
                continue
            if "{" not in line:
                continue
            eco, moves = line.strip().split("}")
            eco = eco[1:].replace("   ", " ")
            movelist = moves.strip().replace(". ", ".").split()
            fen = Pgns.pgn_to_fen(Positions.common_start_fen, movelist)
            movestr = " ".join(movelist)
            print(eco, fen, movestr, sep="\t")
            g.write("{}\t{}\t{}\n".format(eco, fen, movestr))
            g.flush()

print("time used:", time.time() - st)
print("then copy verachess.eco to parent dir to make effects")

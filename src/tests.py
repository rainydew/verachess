# coding: utf-8
import prettytable as pt
from typing import List, Tuple
from consts import gen_empty_board


def print_board(movelist: List[Tuple[int, int]], r: int, c:int):
    tb = pt.PrettyTable()
    board = gen_empty_board(" ")
    board[r][c] = "+"
    for r, c in movelist:
        board[r][c] = "*"
    for row in board:
        tb.add_row(row)
    print(tb)


if __name__ == '__main__':
    print_board([(6, 5), (5, 6)], 7, 7)

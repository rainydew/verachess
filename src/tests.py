# coding: utf-8
import prettytable as pt
from typing import List, Tuple, Union
from consts import gen_empty_board


def print_movelist(movelist: List[Tuple[int, int]], r: int, c:int):
    tb = pt.PrettyTable()
    board = gen_empty_board(" ")
    board[r][c] = "+"
    for r, c in movelist:
        board[r][c] = "*"
    for row in board:
        tb.add_row(row)
    print(tb)


def print_board(board: List[List[Union[str, None]]]):
    tb = pt.PrettyTable()
    board = [[cell or " " for cell in r] for r in board]
    for row in board:
        tb.add_row(row)
    print(tb)


if __name__ == '__main__':
    print_movelist([(6, 5), (5, 6)], 7, 7)

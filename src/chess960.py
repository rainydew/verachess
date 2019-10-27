# coding: utf-8
from typing import List, Tuple
from itertools import combinations

knight_place = tuple(combinations(range(5), 2))


def num_to_pos(num: int) -> str:
    assert num in range(1, 961), "局面数需要在1-960之间"
    num = num % 960
    place = [None] * 8  # type: List[str]
    even_bishop = num % 4
    place[even_bishop * 2 + 1] = "b"
    num = num // 4
    odd_bishop = num % 4
    place[odd_bishop * 2] = "b"
    num = num // 4
    queen = num % 6
    avail_place = [i for i, v in enumerate(place) if not v]
    place[avail_place[queen]] = "q"
    num = num // 6
    knight_a, kngiht_b = knight_place[num]
    avail_place = [i for i, v in enumerate(place) if not v]
    place[avail_place[knight_a]] = place[avail_place[kngiht_b]] = "n"
    avail_place = [i for i, v in enumerate(place) if not v]
    place[avail_place[0]] = place[avail_place[2]] = "r"
    place[avail_place[1]] = "k"
    return "".join(place)


def pos_to_num(pos: str) -> int:
    pos = pos.lower()
    place = list([x for x in pos if x not in "bq"])
    knight = tuple([i for i, v in enumerate(place) if v == "n"])
    place = list([x for x in pos if x != "b"])
    queen = place.index("q")
    pos_odd = pos[0::2]
    pos_even = pos[1::2]
    odd_bishop = pos_odd.index("b")
    even_bishop = pos_even.index("b")
    num = knight_place.index(knight) * 96 + queen * 16 + odd_bishop * 4 + even_bishop
    return num if num else 960


def get_c960_cols(fen: str) -> Tuple[Tuple[int, ...], str]:
    fen = fen.split("/")[0]
    lr = fen.index("r")
    rr = fen.rindex("r")
    castle = chr(65 + rr) + chr(65 + lr) + chr(97 + rr) + chr(97 + lr)
    return tuple([lr, fen.index("k"), rr]), "{}/pppppppp/8/8/8/8/PPPPPPPP/{} w {} - 0 1".format(
        fen, fen.upper(), castle)


if __name__ == '__main__':
    print(get_c960_cols("rnbqkbnr"))

# coding: utf-8
from verachess_global import Globals
from consts import Pieces, gen_empty_board, CastleCells, EndType, Winner
from typing import Tuple, List, Union, Dict, Callable, Optional
from copy import deepcopy
from collections import Counter


class Fens:
    def __init__(self):
        raise RuntimeError("this class only provides static methods")

    @staticmethod
    def cellname_to_place(name: str) -> Tuple[int, int]:
        return 8 - int(name[1]), ord(name[0]) - 97

    @staticmethod
    def place_to_cellname(place: Tuple[int, int]) -> str:
        return chr(place[1] + 97) + str(8 - place[0])

    @staticmethod
    def col_to_num(col: str):
        return ord(col) - 65 if col.isupper() else ord(col) - 97

    @staticmethod
    def get_narrow_fen(fen: str):
        return fen.split(" ")[0]

    @staticmethod
    def check_fen_legal(fen: str) -> Tuple[bool, str]:
        # will set Globals.Chess_960_Columns if passed
        narrow_fen, mover, castle, ep, _, _ = fen.split(" ")  # type: str
        board = Fens.get_board_arrays(narrow_fen)
        col_buffer = [None, None, None]

        if ep != "-":
            r, c = Fens.cellname_to_place(ep)
            if board[r][c] != None:
                return False, "过路兵通过格被占用"
            if r == 5:
                if board[6][c] != None:
                    return False, "过路兵始发格被占用"
                if board[4][c] != "P":
                    return False, "过路兵到达格不正确"
            else:
                if board[1][c] != None:
                    return False, "过路兵始发格被占用"
                if board[3][c] != "p":
                    return False, "过路兵到达格不正确"
        if castle != "-":
            if not Fens.is_chess960(fen):
                if "K" in castle:
                    if board[7][4] != "K" or board[7][7] != "R":
                        return False, "白方王翼易位条件不满足"
                if "Q" in castle:
                    if board[7][4] != "K" or board[7][0] != "R":
                        return False, "白方后翼易位条件不满足"
                if "k" in castle:
                    if board[0][4] != "k" or board[0][7] != "r":
                        return False, "黑方王翼易位条件不满足"
                if "q" in castle:
                    if board[0][4] != "k" or board[0][0] != "r":
                        return False, "黑方后翼易位条件不满足"
            else:  # chess960
                castle = "".join(sorted(castle)[::-1]).swapcase()
                if castle[0].isupper() != castle[-1].isupper():  # both side can castle, need same king place
                    try:
                        assert board[0].index("k") == board[7].index("K")
                    except:
                        return False, "chess960下双方都有易位权，但王不在同一直线"
                    king_col = board[0].index("k")
                elif castle[0].isupper():  # only white can castle
                    try:
                        king_col = board[7].index("K")
                    except:
                        return False, "chess960下，白王有易位权，但不在合理的位置"
                else:  # black can castle
                    try:
                        king_col = board[0].index("k")
                    except:
                        return False, "chess960下，黑王有易位权，但不在合理的位置"
                col_buffer[1] = king_col
                rooks = sorted(set(castle.lower()))
                if len(rooks) == 2:
                    # two rooks need to be different side of king
                    lr, rr = rooks
                    lr, rr = ord(lr) - 97, ord(rr) - 97
                    if not lr < king_col < rr:
                        return False, "chess960下，易位的车需要在王两边"
                    col_buffer[0], col_buffer[2] = lr, rr
                else:
                    rook_col = ord(rooks[0]) - 97
                    if rook_col < king_col:
                        col_buffer[0] = rook_col
                    else:
                        col_buffer[2] = rook_col
                for rook_col in castle:
                    col = Fens.col_to_num(rook_col)
                    if rook_col.isupper():
                        if board[7][col] != "R":
                            return False, "chess960下，白方可易位的{}列底线处不是车".format(rook_col)
                    else:
                        if board[0][col] != "r":
                            return False, "chess960下，黑方可易位的{}列底线处不是车".format(rook_col)
        if narrow_fen.count("K") != 1:
            return False, "白王数量不对"
        if narrow_fen.count("k") != 1:
            return False, "黑王数量不对"
        if len(tuple(filter(str.isupper, narrow_fen))) > 16:
            return False, "白棋数量过多"
        if len(tuple(filter(str.islower, narrow_fen))) > 16:
            return False, "黑棋数量过多"
        if "P" in board[0] + board[7] or "p" in board[0] + board[7]:
            return False, "兵不能在底线"
        if Fens.can_capture_opp_king_or_cell(board, mover == "w"):
            return False, "不允许非行棋方的王送吃"

        Globals.Chess_960_Columns = tuple(col_buffer)
        return True, ""

    @staticmethod
    def is_chess960(fen: str) -> bool:
        castle_str = fen.split(" ")[2]
        if castle_str == "-" or "k" in castle_str.lower() or "q" in castle_str.lower():
            return False
        return True

    @staticmethod
    def _check_influence(fen: str, castle: List[bool], influence: List[Tuple[int, int]], is_960: bool) -> None:
        # side effect will modify castle
        if not is_960:
            w_right = (7, 7)
            w_left = (7, 0)
            b_right = (0, 7)
            b_left = (0, 0)
        else:
            w_right = w_left = b_right = b_left = None
            castle_str = fen.split(" ")[2]
            if castle[0]:
                w_right = (7, Fens.col_to_num(castle_str[0]))
            if castle[1]:
                w_left = (7, Fens.col_to_num(castle_str[1 if castle[0] else 0]))
            if castle[2]:
                b_right = (0, Fens.col_to_num(castle_str[-2] if castle[3] else castle_str[-1]))
            if castle[3]:
                b_left = (0, Fens.col_to_num(castle_str[-1]))

        if w_right in influence:
            castle[0] = False  # K
        if w_left in influence:
            castle[1] = False  # Q
        if b_right in influence:
            castle[2] = False  # k
        if b_left in influence:
            castle[3] = False  # q

    @staticmethod
    def calc_move(fen: str, move: str) -> Tuple[str, Optional[Tuple[int, int]]]:
        # no verify
        # print("debug", move, fen)
        # returns (after_fen, None or 960 castle king and rook place)
        is_960 = Fens.is_chess960(fen)

        board = Fens.get_board_arrays(fen)
        start = Fens.cellname_to_place(move[:2])
        sr, sc = start
        end = Fens.cellname_to_place(move[2:4])
        er, ec = end
        piece = board[sr][sc]
        castle = Fens.get_castle(fen)
        count = Fens.get_draw_count(fen)
        total_move = Fens.get_full_move(fen)
        mover = Fens.get_mover(fen)
        special = None

        if piece.lower() in "qrnb":
            if not board[er][ec]:
                count += 1
            else:
                count = 0

            board[er][ec] = piece
            board[sr][sc] = None
            ep = "-"
        elif piece.lower() == "k":
            ep = "-"
            if mover == "w":
                castle[0] = castle[1] = False
            else:
                castle[2] = castle[3] = False
            c960_castle = board[er][ec] and board[er][ec].isupper() == piece.isupper()
            if abs(ec - sc) > 1 or c960_castle:
                # c960 supported here, but castle function need adaption
                board[sr][sc] = None
                if ec > sc:  # short
                    if board[er][ec]:
                        board[er][ec] = None
                    else:
                        board[er][7] = None
                    board[er][6] = "K" if sr != 0 else "k"
                    board[er][5] = "R" if sr != 0 else "r"
                    if c960_castle:
                        special = er, 6
                else:
                    if board[er][ec]:
                        board[er][ec] = None
                    else:
                        board[er][0] = None
                    board[er][2] = "K" if sr != 0 else "k"
                    board[er][3] = "R" if sr != 0 else "r"
                    if c960_castle:
                        special = er, 2
                count += 1  # castling
            else:
                if not board[er][ec]:  # normal move
                    count += 1
                else:
                    count = 0
                board[er][ec] = piece
                board[sr][sc] = None
        else:  # pawn
            count = 0
            if abs(er - sr) == 2:
                ep = Fens.place_to_cellname(((er + sr) // 2, sc))  # make sure it's int, not float.0
            else:
                ep = "-"
            if len(move) == 5:
                to_piece = move[-1].upper() if mover == "w" else move[-1]
                board[er][ec] = to_piece
            else:
                if abs(ec - sc) == 1 and board[er][ec] is None:  # en passent
                    board[sr][ec] = None
                board[er][ec] = piece
            board[sr][sc] = None

        influence = [start, end]  # king or pawn may capture opponent castling rook
        Fens._check_influence(fen, castle, influence, is_960)

        if mover == "w":
            mover = "b"
        else:
            mover = "w"
            total_move += 1

        if not is_960:
            new_fen_list = [Fens.get_narrow_fen_from_board(board), mover, Fens.transfer_castle(castle), ep, str(count),
                            str(total_move)]
        else:
            new_fen_list = [Fens.get_narrow_fen_from_board(board), mover, Fens.transfer_castle(castle, True, fen), ep,
                            str(count), str(total_move)]
        return " ".join(new_fen_list), special

    @staticmethod
    def get_narrow_fen_from_board(board: List[List[Union[str, None]]]) -> str:
        fen_rows = []
        for row in board:
            fen_row = []
            number_now = False
            for col in row:
                if col:
                    fen_row.append(col)
                    number_now = False
                else:
                    if number_now:
                        fen_row[-1] += 1
                    else:
                        fen_row.append(1)
                    number_now = True
            fen_rows.append("".join([str(x) for x in fen_row]))
        return "/".join(fen_rows)

    @staticmethod
    def get_board_arrays(opt_narrow_fen: str) -> List[List[Union[str, None]]]:  # better perfomance
        rows = Fens.get_narrow_fen(opt_narrow_fen).split("/")
        board = gen_empty_board()
        for i, row in enumerate(rows):
            j = 0
            for char in row:
                if char in Pieces:
                    board[i][j] = char
                    j += 1
                else:
                    j += int(char)  # if this errors, char is illegal
        return board

    @staticmethod
    def get_mover(fen: str) -> str:
        return fen.split(" ")[1]

    @staticmethod
    def get_ep(fen: str) -> str:
        return fen.split(" ")[3].replace("-", "")[:1]  # False or column char only

    @staticmethod
    def get_castle(fen: str) -> List[bool]:
        castle = fen.split(" ")[2]
        if not Fens.is_chess960(fen):
            return [x in castle for x in "KQkq"]
        else:
            buffer = [False, False, False, False]
            board = Fens.get_board_arrays(Fens.get_narrow_fen(fen))
            for char in castle:
                col = Fens.col_to_num(char)
                if char.isupper():
                    white_king = board[7].index("K")  # only if char is upper white king will be found at line 7
                    if col < white_king:
                        buffer[1] = True  # queenside after kingside
                    else:
                        buffer[0] = True
                else:
                    black_king = board[0].index("k")  # only if char is upper black king will be found at line 0
                    if col < black_king:
                        buffer[3] = True  # queenside after kingside
                    else:
                        buffer[2] = True
            return buffer

    @staticmethod
    def transfer_castle(castle_list: List[bool], c960: bool = False, fen: str = "") -> str:
        if not c960:
            return "".join(["KQkq"[i] for i, v in enumerate(castle_list) if v]) or "-"
        else:  # must be origin fen, otherwise cannot recognize
            origin_castle_list = Fens.get_castle(fen)
            origin_castle_str = fen.split(" ")[2]
            res = ""
            if castle_list[0] and castle_list[1]:
                res += origin_castle_str[:2]  # HA -> HA
            elif castle_list[0]:
                res += origin_castle_str[0]  # H* -> H
            elif castle_list[1]:
                if origin_castle_list[0]:
                    res += origin_castle_str[1]  # HA -> A
                else:
                    res += origin_castle_str[0]  # A -> A

            if castle_list[2] and castle_list[3]:
                res += origin_castle_str[-2:]  # ha -> ha
            elif castle_list[2]:
                if origin_castle_list[3]:
                    res += origin_castle_str[-2]  # ha -> h
                else:
                    res += origin_castle_str[-1]  # h -> h
            elif castle_list[3]:
                res += origin_castle_str[-1]  # *a -> a

            return res if res else "-"

    @staticmethod
    def get_draw_count(fen: str) -> int:
        return int(fen.split(" ")[4])

    @staticmethod
    def get_full_move(fen: str) -> int:
        return int(fen.split(" ")[5])

    @staticmethod
    def can_control(fen: str, place: Tuple[int, int]) -> bool:
        r, c = place
        piece = Fens.get_board_arrays(fen)[r][c]
        if piece:
            return piece.isupper() if Fens.get_mover(fen) == "w" else piece.islower()
        return False

    @staticmethod
    def is_promotion(fen: str, selection: Tuple[int, int], place: Tuple[int, int]) -> bool:
        sr, sc = selection
        er, ec = place
        piece = Fens.get_board_arrays(fen)[sr][sc]
        return piece and piece in "Pp" and er in [0, 7]

    @staticmethod
    def get_piece_move(fen: str, place: Tuple[int, int]) -> List[Tuple[int, int]]:  # main method
        board = Fens.get_board_arrays(fen)
        r, c = place
        piece = board[r][c]
        assert piece, "no piece in this place to move"
        first_moves = Move_Func_Dict[piece.lower()](board, r, c)  # type: List[Tuple[int, int]]
        secure_moves = Fens._remove_pinned_move(first_moves, board, r, c)
        if piece in "Kk":
            secure_moves += Fens._castle_move(Fens.get_castle(fen), board, piece == "K", Fens.is_chess960(fen), fen)
            # secure check in method
        if piece in "Pp":
            secure_moves += Fens._ep_move(Fens.get_ep(fen), board, r, c)  # secure check in method too
        return secure_moves

    @staticmethod
    def _move_in_board_get_piece_move(board: List[List[Optional[str]]], r: int, c: int, fen: str, end: Tuple[int, int]
                                      ) -> bool:
        # better performace to verify
        piece = board[r][c]
        first_moves = Move_Func_Dict[piece.lower()](board, r, c)  # type: List[Tuple[int, int]]
        secure_moves = Fens._remove_pinned_move(first_moves, board, r, c)
        if piece in "Kk":
            secure_moves += Fens._castle_move(Fens.get_castle(fen), board, piece == "K", Fens.is_chess960(fen), fen)
            # secure check in method
        if piece in "Pp":
            secure_moves += Fens._ep_move(Fens.get_ep(fen), board, r, c)  # secure check in method too
        return end in secure_moves

    @staticmethod
    def verify_uci_move(fen: str, move: str) -> bool:
        narrow_fen, mover, _, _, _, _ = fen.split(" ")
        white_now = mover == "w"
        if len(move) == 5:
            if move[-1] not in "qrnb":
                return False
        elif len(move) != 4:
            return False
        if move[0] not in "abcdefgh" or move[2] not in "abcdefgh" or move[1] not in "12345678" or move[3] not in \
            "12345678":
            return False
        board = Fens.get_board_arrays(narrow_fen)
        start_r, start_c = Fens.cellname_to_place(move[:2])
        piece = board[start_r][start_c]
        end = Fens.cellname_to_place(move[2:4])
        if not piece or piece.isupper() != white_now:
            return False
        return Fens._move_in_board_get_piece_move(board, start_r, start_c, fen, end)

    @staticmethod
    def get_all_moves(fen: str) -> List[str]:
        white = Fens.get_mover(fen) == "w"
        board = Fens.get_board_arrays(fen)
        moves = []
        for sr in range(8):
            for sc in range(8):
                if board[sr][sc] and board[sr][sc].isupper() == white:
                    piece_move = Fens.get_piece_move(fen, (sr, sc))
                    for er, ec in piece_move:
                        algebra_move = chr(sc + 97) + str(8 - sr) + chr(ec + 97) + str(8 - er)
                        if board[sr][sc].lower() == "p" and er in (0, 7):   # promotion
                            for promote_to in "qrnb":
                                moves.append(algebra_move + promote_to)
                        else:
                            moves.append(algebra_move)
        return moves

    @staticmethod
    def _remove_pinned_move(moves: List[Tuple[int, int]], board: List[List[Union[str, None]]], r: int, c: int
                            ) -> List[Tuple[int, int]]:
        after_movelist = []
        white = board[r][c].isupper()
        for move in moves:
            to_r, to_c = move
            after_board = deepcopy(board)
            after_board[to_r][to_c] = after_board[r][c]
            after_board[r][c] = None
            if not Fens.can_capture_opp_king_or_cell(after_board, not white):
                after_movelist.append(move)
        return after_movelist

    @staticmethod
    def _ep_move(ep: str, board: List[List[Union[str, None]]], r: int, c: int) -> List[Tuple[int, int]]:
        if not ep:
            return []
        else:
            ep_col = ord(ep) - 97  # opp column
            white = board[r][c].isupper()
            if abs(c - ep_col) != 1 or (r != 3 if white else r != 4):
                return []
            else:
                after_board = deepcopy(board)
                if white:
                    after_board[2][ep_col] = "P"
                    after_board[3][c] = None  # clear before space
                    after_board[3][ep_col] = None  # remove opponent pawn
                    return [] if Fens.can_capture_opp_king_or_cell(after_board, False) else [(2, ep_col)]
                else:
                    after_board[5][ep_col] = "p"
                    after_board[4][c] = None  # clear before space
                    after_board[4][ep_col] = None  # remove opponent pawn
                    return [] if Fens.can_capture_opp_king_or_cell(after_board, True) else [(5, ep_col)]

    @staticmethod
    def _castle_move(castle_list: List[bool], board: List[List[Union[str, None]]], white: bool, c960: bool = False,
                     fen: str = "") -> List[Tuple[int, int]]:
        pos = []
        if not c960:
            if white:
                if castle_list[0]:  # K
                    # not been blocked or checked and threatend in passway and arrival way
                    if Fens._cells_are_empty(board, CastleCells.white_s_p) and not any((Fens.can_capture_opp_king_or_cell(
                            board, not white, check_place) for check_place in CastleCells.white_short)):
                        pos.append(CastleCells.white_s_arrive)
                if castle_list[1]:  # Q
                    # not been blocked or checked and threaten in pass way and arrival way
                    if Fens._cells_are_empty(board, CastleCells.white_l_p) and not any((Fens.can_capture_opp_king_or_cell(
                            board, not white, check_place) for check_place in CastleCells.white_long)):
                        pos.append(CastleCells.white_l_arrive)
            else:
                if castle_list[2]:  # k
                    # not been blocked or checked and threatend in passway and arrival way
                    if Fens._cells_are_empty(board, CastleCells.black_s_p) and not any((Fens.can_capture_opp_king_or_cell(
                            board, not white, check_place) for check_place in CastleCells.black_short)):
                        pos.append(CastleCells.black_s_arrive)
                if castle_list[3]:  # q
                    # not been blocked or checked and threaten in pass way and arrival way
                    if Fens._cells_are_empty(board, CastleCells.black_l_p) and not any((Fens.can_capture_opp_king_or_cell(
                            board, not white, check_place) for check_place in CastleCells.black_long)):
                        pos.append(CastleCells.black_l_arrive)
        else:
            castle_str = fen.split(" ")[2]
            if white:
                if castle_list[0]:  # -H
                    king_col = board[7].index("K")      # here to prevent king out of this line and error
                    symbol = Fens.col_to_num(castle_str[0])
                    king_finish = 6
                    buffer_board = deepcopy(board)
                    # Throw away self king and castle rook, all [start, end] should
                    # be empty and not checked. This also prevent rRK5 for white to
                    # make an O-O-O castle or 5KRr to make O-O
                    buffer_board[7][king_col] = None
                    buffer_board[7][symbol] = None
                    passway = tuple([(7, c) for c in (range(king_col, king_finish + 1) if king_col < king_finish else
                                                range(king_finish, king_col + 1))])
                    if Fens._cells_are_empty(buffer_board, passway) and not any((Fens.can_capture_opp_king_or_cell(
                            board, not white, check_place) for check_place in passway)):
                        pos.append((7, symbol))     # add the place of rook
                if castle_list[1]:
                    king_col = board[7].index("K")
                    symbol = Fens.col_to_num(castle_str[1] if castle_list[0] else castle_str[1])
                    king_finish = 2
                    buffer_board = deepcopy(board)
                    buffer_board[7][king_col] = None
                    buffer_board[7][symbol] = None
                    passway = tuple([(7, c) for c in (range(king_col, king_finish + 1) if king_col < king_finish else
                                                range(king_finish, king_col + 1))])
                    if Fens._cells_are_empty(buffer_board, passway) and not any((Fens.can_capture_opp_king_or_cell(
                            board, not white, check_place) for check_place in passway)):
                        pos.append((7, symbol))     # add the place of rook
            else:
                if castle_list[2]:
                    king_col = board[0].index("k")
                    symbol = Fens.col_to_num(castle_str[-2] if castle_list[3] else castle_str[-1])
                    king_finish = 6
                    buffer_board = deepcopy(board)
                    buffer_board[0][king_col] = None
                    buffer_board[0][symbol] = None
                    passway = tuple([(0, c) for c in (range(king_col, king_finish + 1) if king_col < king_finish else
                                                range(king_finish, king_col + 1))])
                    if Fens._cells_are_empty(buffer_board, passway) and not any((Fens.can_capture_opp_king_or_cell(
                            board, not white, check_place) for check_place in passway)):
                        pos.append((0, symbol))     # add the place of rook
                if castle_list[3]:
                    king_col = board[0].index("k")
                    symbol = Fens.col_to_num(castle_str[-1])
                    king_finish = 2
                    buffer_board = deepcopy(board)
                    buffer_board[0][king_col] = None
                    buffer_board[0][symbol] = None
                    passway = tuple([(0, c) for c in (range(king_col, king_finish + 1) if king_col < king_finish else
                                                range(king_finish, king_col + 1))])
                    if Fens._cells_are_empty(buffer_board, passway) and not any((Fens.can_capture_opp_king_or_cell(
                            board, not white, check_place) for check_place in passway)):
                        pos.append((0, symbol))     # add the place of rook
        return pos

    @staticmethod
    def _cells_are_empty(board: List[List[Union[str, None]]], places: Tuple[Tuple[int, int]]) -> bool:
        for r, c in places:
            if board[r][c] is not None:
                return False
        return True

    @staticmethod
    def _r_move(board: List[List[Union[str, None]]], r: int, c: int) -> List[Tuple[int, int]]:
        up = [(x, c) for x in range(r - 1, -1, -1)]
        down = [(x, c) for x in range(r + 1, 8, 1)]
        left = [(r, x) for x in range(c - 1, -1, -1)]
        right = [(r, x) for x in range(c + 1, 8, 1)]
        iam_upper = board[r][c].isupper()
        up = Fens._ok_move(board, up, iam_upper)
        down = Fens._ok_move(board, down, iam_upper)
        left = Fens._ok_move(board, left, iam_upper)
        right = Fens._ok_move(board, right, iam_upper)
        return up + down + left + right

    @staticmethod
    def _b_move(board: List[List[Union[str, None]]], r: int, c: int) -> List[Tuple[int, int]]:
        nw = [(r - x, c - x) for x in range(1, min(r, c) + 1)]
        ne = [(r - x, c + x) for x in range(1, min(r, 7 - c) + 1)]
        sw = [(r + x, c - x) for x in range(1, min(7 - r, c) + 1)]
        se = [(r + x, c + x) for x in range(1, min(7 - r, 7 - c) + 1)]
        iam_upper = board[r][c].isupper()
        nw = Fens._ok_move(board, nw, iam_upper)
        ne = Fens._ok_move(board, ne, iam_upper)
        sw = Fens._ok_move(board, sw, iam_upper)
        se = Fens._ok_move(board, se, iam_upper)
        return nw + ne + sw + se

    @staticmethod
    def _q_move(board: List[List[Union[str, None]]], r: int, c: int) -> List[Tuple[int, int]]:
        return Fens._r_move(board, r, c) + Fens._b_move(board, r, c)

    @staticmethod
    def _k_move(board: List[List[Union[str, None]]], r: int, c: int) -> List[Tuple[int, int]]:
        moves = [(r + xr, c + xc) for xr in [-1, 0, 1] for xc in [-1, 0, 1]]
        iam_upper = board[r][c].isupper()
        return Fens._ok_filt(board, list(filter(Fens._in_board_filt, moves)), iam_upper)

    @staticmethod
    def _n_move(board: List[List[Union[str, None]]], r: int, c: int) -> List[Tuple[int, int]]:
        moves = [(r + xr, c + xc) for xr, xc in
                 [(1, 2), (2, 1), (1, -2), (-2, 1), (-1, 2), (2, -1), (-1, -2), (-2, -1)]]
        iam_upper = board[r][c].isupper()
        return Fens._ok_filt(board, list(filter(Fens._in_board_filt, moves)), iam_upper)

    @staticmethod
    def _p_move(board: List[List[Union[str, None]]], r: int, c: int) -> List[Tuple[int, int]]:
        assert r != 0 and r != 7, "pawn at top"
        iam_upper = board[r][c].isupper()
        movelist = []
        if iam_upper:  # white
            if board[r - 1][c] is None:  # forward one step
                movelist.append((r - 1, c))
            if r == 6 and movelist:  # start line for white, ensure one step is okay
                if board[4][c] is None:  # forward one step
                    movelist.append((4, c))
            if c != 0:
                attack = board[r - 1][c - 1]
                if attack and attack.isupper() != iam_upper:
                    movelist.append((r - 1, c - 1))
            if c != 7:
                attack = board[r - 1][c + 1]
                if attack and attack.isupper() != iam_upper:
                    movelist.append((r - 1, c + 1))
        else:  # black
            if board[r + 1][c] is None:  # forward one step
                movelist.append((r + 1, c))
            if r == 1 and movelist:  # start line for white, ensure one step is okay
                if board[3][c] is None:  # forward one step
                    movelist.append((3, c))
            if c != 0:
                attack = board[r + 1][c - 1]
                if attack and attack.isupper() != iam_upper:
                    movelist.append((r + 1, c - 1))
            if c != 7:
                attack = board[r + 1][c + 1]
                if attack and attack.isupper() != iam_upper:
                    movelist.append((r + 1, c + 1))
        return movelist

    @staticmethod
    def _in_board_filt(place: Tuple[int, int]) -> bool:
        r, c = place
        return 0 <= r <= 7 and 0 <= c <= 7

    @staticmethod
    def _ok_filt(board: List[List[Union[str, None]]], movelist: List[Tuple[int, int]], iam_upper: bool) -> List[
        Tuple[int, int]]:
        """
        :param iam_upper: True if white
        """
        return [(r, c) for r, c in movelist if board[r][c] is None or board[r][c].isupper() != iam_upper]

    @staticmethod
    def _ok_move(board: List[List[Union[str, None]]], movelist: List[Tuple[int, int]], iam_upper: bool) -> List[
        Tuple[int, int]]:
        """
        :param iam_upper: True if white
        """
        for i, (r, c) in enumerate(movelist):
            cell = board[r][c]
            if cell:  # has a piece here
                return movelist[:i] if cell.isupper() == iam_upper else movelist[:i + 1]
        return movelist

    @staticmethod
    def get_king_place(board: List[List[Union[str, None]]], white: bool) -> Tuple[int, int]:
        k = "K" if white else "k"
        for r in range(8):
            for c in range(8):
                if board[r][c] == k:
                    return r, c
        raise IndexError("king not found")

    @staticmethod
    def checked_place(fen: str) -> Optional[Tuple[int, int]]:
        board = Fens.get_board_arrays(Fens.get_narrow_fen(fen))
        white = Fens.get_mover(fen) != "w"
        if Fens.can_capture_opp_king_or_cell(board, white):
            return Fens.get_king_place(board, not white)
        return None

    @staticmethod
    def check_wdl(fen: str, history_hash: List[int]) -> int:
        Globals.Winner = Winner.draw
        if not Fens.has_legal_move(fen):
            if Fens.checked_place(fen):
                if Fens.get_mover(fen) == "w":
                    Globals.Winner = Winner.black
                else:
                    Globals.Winner = Winner.white
                return EndType.checkmate
            else:
                return EndType.stalemate
        if Fens.get_draw_count(fen) >= 100:
            return EndType.fifty_rule
        if Fens.has_not_enough_material(fen):
            return EndType.insufficient_material
        if Counter(history_hash).most_common(1)[0][1] > 2:
            return EndType.three_fold
        Globals.Winner = Winner.unknown
        return EndType.unterminated

    @staticmethod
    def has_legal_move(fen: str) -> bool:   # seperate with get_piece_move to make it faster during games
        board = Fens.get_board_arrays(Fens.get_narrow_fen(fen))
        white = Fens.get_mover(fen) == "w"
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece.isupper() == white:
                    first_moves = Move_Func_Dict[piece.lower()](board, r, c)  # type: List[Tuple[int, int]]
                    secure_moves = Fens._remove_pinned_move(first_moves, board, r, c)
                    if piece in "Kk":
                        secure_moves += Fens._castle_move(Fens.get_castle(fen), board,
                                                          piece == "K", Fens.is_chess960(fen), fen)  # secure check in method
                    if piece in "Pp":
                        secure_moves += Fens._ep_move(Fens.get_ep(fen), board, r, c)  # secure check in method too
                    if secure_moves:
                        return True
        return False

    @staticmethod
    def has_not_enough_material(fen: str) -> bool:  # BKNbkn
        narrow_fen = Fens.get_narrow_fen(fen)
        material = narrow_fen.replace("/", "")
        for i in range(1, 9):
            material = material.replace(str(i), "")
        material = "".join(sorted(material))
        if material in ["Kk", "BKk", "Kbk", "KNk", "Kkn"]:
            return True
        if material == ["BKbk"]:
            board = Fens.get_board_arrays(narrow_fen)
            for r in range(8):
                for c in range(8):
                    piece = board[r][c]
                    if not piece or piece not in ["B", "b"]:
                        continue
                    if piece == "B":
                        wb = (r + c) % 2  # odd: dark, even: light
                    else:
                        bb = (r + c) % 2
            return wb == bb  # same odd/even means same color => draw
        return False

    @staticmethod
    def can_capture_opp_king_or_cell(board: List[List[Union[str, None]]], white_now: bool, spec_cell: Tuple[int, int] =
    None) -> bool:  # white_now means this player may kill opp's king at the next move
        opp_king = Fens.get_king_place(board, not white_now) if spec_cell is None else spec_cell  # check castle cells
        for r in range(8):
            for c in range(8):
                cell = board[r][c]
                if cell and cell.isupper() == white_now:
                    movelist = Move_Func_Dict[cell.lower()](board, r, c)  # type: List[Tuple[int, int]]
                    if opp_king in movelist:
                        return True
        return False


Move_Func_Dict = {piece: getattr(Fens, "_{}_move".format(piece)) for piece in "pbnrqk"} \
    # type: Dict[str, Callable[[List[List[str]], int, int], List[Tuple[int, int]]]]


class Pgns:
    @staticmethod
    def single_uci_to_pgn(fen: str, move: str, final_fen: str = None) -> Tuple[str, str, str]:
        # call it before check_wdl. final_fen for performance enhance
        pgn = symbol = ""

        narrow_fen, mover, castle, ep, draw, turn = fen.split(" ")
        prefix = "{}.".format(turn) if mover == "w" else ""

        board = Fens.get_board_arrays(narrow_fen)
        start = move[:2]
        end = move[2:4]
        promote = move[4:]
        sr, sc = Fens.cellname_to_place(start)
        er, ec = Fens.cellname_to_place(end)

        piece = board[sr][sc]

        if piece in "Kk":   # castle
            if abs(sc - ec) > 1 or (board[er][ec] and board[er][ec].isupper() == piece.isupper()):
                pgn = "O-O" if ec > sc else "O-O-O"

        if not pgn:     # normal move
            extra = ["", ""]    # col name, row name
            for r in range(8):
                for c in range(8):
                    if board[r][c] == piece and (c != sc or r != sr):
                        if (er, ec) in Fens.get_piece_move(fen, (r, c)):
                            if c != sc:
                                extra[0] = chr(sc + 97)
                            else:
                                extra[1] = str(8 - sr)

            piece = piece.upper().replace("P", "")
            if not piece:   # is pawn
                if sc != ec:    # pawn takes, must add start column, ep included here
                    extra[0] = chr(sc + 97)

            pgn = piece + "".join(extra) + (
                "x" if board[er][ec] or (board[sr][sc] and board[sr][sc].lower() == "p" and sc != ec) else ""
            ) + end + ("={}".format(promote.upper()) if promote else "")

        if not final_fen:
            final_fen = Fens.calc_move(fen, move)[0]

        if Fens.checked_place(final_fen):
            if Fens.has_legal_move(final_fen):
                symbol = "+"
            else:
                symbol = "#"

        return prefix, pgn, symbol

    @staticmethod
    def single_pgn_to_uci(fen:str, pgn:str) -> str:
        pgn = pgn.split(".")[-1].strip().replace("+", "").replace("=", "").replace("#", "")
        moves = Fens.get_all_moves(fen)
        pgn_moves = {Pgns.single_uci_to_pgn(fen, move)[1]: move for move in moves}  # type: Dict[str, str]
        res = pgn_moves.get(pgn)
        assert res is not None, "move not found"
        return res

    @staticmethod
    def fast_single_pgn_to_uci(fen:str, pgn:str) -> str:
        # todo: doing
        narrow_fen, mover, castle, ep, _, _ = fen.split(" ")


    @staticmethod
    def uci_to_pgn(fen: str, moves: List[str]) -> List[str]:
        reslist = []
        for move in moves:
            next_fen = Fens.calc_move(fen, move)[0]
            reslist.append("".join(Pgns.single_uci_to_pgn(fen, move, next_fen)))
            fen = next_fen
        return reslist

    @staticmethod
    def pgn_to_uci(fen: str, pgn_moves: List[str]) -> List[str]:
        reslist = []
        for pgn_move in pgn_moves:
            move = Pgns.single_pgn_to_uci(fen, pgn_move)
            reslist.append(move)
            fen = Fens.calc_move(fen, move)[0]
        return reslist

    @staticmethod
    def pgn_to_fen(fen: str, pgn_moves: List[str]) -> str:
        for pgn_move in pgn_moves:
            move = Pgns.single_pgn_to_uci(fen, pgn_move)
            fen = Fens.calc_move(fen, move)[0]
        return fen


if __name__ == '__main__':
    from consts import Positions
    res = Pgns.uci_to_pgn(Positions.common_start_fen, ["f2f3", "e7e5", "g2g4", "d8h4"])
    print(res)
    res = Pgns.pgn_to_uci(Positions.common_start_fen, res)
    print(res)

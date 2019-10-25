# coding: utf-8
import verachess_support
from verachess_global import Globals
from consts import Positions, Pieces, gen_empty_board, CastleCells
from typing import Tuple, List, Union, Dict, Callable
from copy import deepcopy


def init_cells(c960: int = None):
    # init pieces
    if c960 is None:
        verachess_support.set_cell_values(Positions.common_startpos)
    else:
        raise NotImplementedError("ToDo")


def refresh_cells():
    fen = Globals.Game_fen
    verachess_support.set_cell_values(Fens.get_narrow_fen(fen))
    verachess_support.set_player_color(Fens.get_mover(fen) == "w")


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
    def get_narrow_fen(fen: str):
        return fen.split(" ")[0]

    @staticmethod
    def calc_move(fen: str, move: str):
        # no verify
        # print("debug", move, fen)
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

        if piece.lower() in "qrnb":
            if not board[er][ec]:
                count += 1
            else:
                count = 0

            board[er][ec] = piece
            board[sr][sc] = None
            ep = "-"
            influence = [start, end]
            if (7, 7) in influence:
                castle[0] = False   # K
            if (7, 0) in influence:
                castle[1] = False   # Q
            if (0, 7) in influence:
                castle[2] = False   # k
            if (0, 0) in influence:
                castle[3] = False   # q
        elif piece.lower() == "k":
            ep = "-"
            if mover == "w":
                castle[0] = castle[1] = False
            else:
                castle[2] = castle[3] = False
            if abs(ec - sc) > 1 or (board[er][ec] and board[er][ec].isupper() == piece.isupper()):
                # c960 supported here, but castle function need adaption
                board[sr][sc] = None
                if ec > sc:  # short
                    if board[er][ec]:
                        board[er][ec] = None
                    else:
                        board[er][7] = None
                    board[er][6] = "K" if sr != 0 else "k"
                    board[er][5] = "R" if sr != 0 else "r"
                else:
                    if board[er][ec]:
                        board[er][ec] = None
                    else:
                        board[er][0] = None
                    board[er][2] = "K" if sr != 0 else "k"
                    board[er][3] = "R" if sr != 0 else "r"
                count += 1  # castling
            else:
                if not board[er][ec]:   # normal move
                    count += 1
                else:
                    count = 0
                board[er][ec] = piece
                board[sr][sc] = None
        else:   # pawn
            count = 0
            if abs(er - sr) == 2:
                ep = Fens.place_to_cellname(((er + sr) // 2, sc))   # make sure it's int, not float.0
            else:
                ep = "-"
            if len(move) == 5:
                to_piece = move[-1].upper() if mover == "w" else move[-1]
                board[er][ec] = to_piece
            else:
                if abs(ec - sc) == 1 and board[er][ec] is None:     # en passent
                    board[sr][ec] = None
                board[er][ec] = piece
            board[sr][sc] = None

        if mover == "w":
            mover = "b"
        else:
            mover = "w"
            total_move += 1

        new_fen_list = [Fens.get_narrow_fen_from_board(board), mover, Fens.transfer_castle(castle), ep, str(count),
                        str(total_move)]
        return " ".join(new_fen_list)

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
    def get_board_arrays(fen: str) -> List[List[Union[str, None]]]:     # better perfomance
        rows = Fens.get_narrow_fen(fen).split("/")
        board = gen_empty_board()
        for i, row in enumerate(rows):
            j = 0
            for char in row:
                if char in Pieces:
                    board[i][j] = char
                    j += 1
                else:
                    j += int(char)    # if this errors, char is illegal
        return board

    @staticmethod
    def get_mover(fen: str) -> str:
        return fen.split(" ")[1]

    @staticmethod
    def get_ep(fen: str) -> str:
        return fen.split(" ")[3].replace("-", "")[:1]   # False or column char only

    @staticmethod
    def get_castle(fen: str) -> List[bool]:
        # todo: c960 support
        return [x in fen.split(" ")[2] for x in "KQkq"]

    @staticmethod
    def transfer_castle(castle_list: List[bool]):
        # todo: c960 support
        return "".join(["KQkq"[i] for i, v in enumerate(castle_list) if v]) or "-"

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
        first_moves = Move_Func_Dict[piece.lower()](board, r, c)    # type: List[Tuple[int, int]]
        secure_moves = Fens._remove_pinned_move(first_moves, board, r, c)
        if piece in "Kk":
            secure_moves += Fens._castle_move(Fens.get_castle(fen), board, piece == "K")     # secure check in method
        if piece in "Pp":
            secure_moves += Fens._ep_move(Fens.get_ep(fen), board, r, c)     # secure check in method too
        return secure_moves

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
    def _ep_move(ep: str, board: List[List[Union[str, None]]], r:int, c:int) -> List[Tuple[int, int]]:
        if not ep:
            return []
        else:
            ep_col = ord(ep) - 97   # opp column
            white = board[r][c].isupper()
            if abs(c - ep_col) != 1 or (r != 3 if white else r != 4):
                return []
            else:
                after_board = deepcopy(board)
                if white:
                    after_board[2][ep_col] = "P"
                    after_board[3][c] = None    # clear before space
                    after_board[3][ep_col] = None   # remove opponent pawn
                    return [] if Fens.can_capture_opp_king_or_cell(after_board, False) else [(2, ep_col)]
                else:
                    after_board[5][ep_col] = "p"
                    after_board[4][c] = None    # clear before space
                    after_board[4][ep_col] = None   # remove opponent pawn
                    return [] if Fens.can_capture_opp_king_or_cell(after_board, True) else [(5, ep_col)]

    @staticmethod
    def _castle_move(castle_list: List[bool], board: List[List[Union[str, None]]], white: bool, c960: bool=False
                     ) -> List[Tuple[int, int]]:
        # only for normal castle
        pos = []
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
            if castle_list[0]:  # k
                # not been blocked or checked and threatend in passway and arrival way
                if Fens._cells_are_empty(board, CastleCells.black_s_p) and not any((Fens.can_capture_opp_king_or_cell(
                        board, not white, check_place) for check_place in CastleCells.black_short)):
                    pos.append(CastleCells.black_s_arrive)
            if castle_list[1]:  # q
                # not been blocked or checked and threaten in pass way and arrival way
                if Fens._cells_are_empty(board, CastleCells.black_l_p) and not any((Fens.can_capture_opp_king_or_cell(
                        board, not white, check_place) for check_place in CastleCells.black_long)):
                    pos.append(CastleCells.black_l_arrive)
        return pos

    @staticmethod
    def _cells_are_empty(board: List[List[Union[str, None]]], places: Tuple[Tuple[int, int]]) -> bool:
        for r, c in places:
            if board[r][c] is not None:
                return False
        return True

    @staticmethod
    def _r_move(board: List[List[Union[str, None]]], r:int, c:int) -> List[Tuple[int, int]]:
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
    def _b_move(board: List[List[Union[str, None]]], r:int, c:int) -> List[Tuple[int, int]]:
        nw = [(r - x, c - x) for x in range(1, min(r, c)+1)]
        ne = [(r - x, c + x) for x in range(1, min(r, 7 - c)+1)]
        sw = [(r + x, c - x) for x in range(1, min(7 - r, c)+1)]
        se = [(r + x, c + x) for x in range(1, min(7 - r, 7 - c)+1)]
        iam_upper = board[r][c].isupper()
        nw = Fens._ok_move(board, nw, iam_upper)
        ne = Fens._ok_move(board, ne, iam_upper)
        sw = Fens._ok_move(board, sw, iam_upper)
        se = Fens._ok_move(board, se, iam_upper)
        return nw + ne + sw + se

    @staticmethod
    def _q_move(board: List[List[Union[str, None]]], r:int, c:int) -> List[Tuple[int, int]]:
        return Fens._r_move(board, r, c) + Fens._b_move(board, r, c)

    @staticmethod
    def _k_move(board: List[List[Union[str, None]]], r:int, c:int) -> List[Tuple[int, int]]:
        moves = [(r + xr, c + xc) for xr in [-1, 0, 1] for xc in [-1, 0, 1]]
        iam_upper = board[r][c].isupper()
        return Fens._ok_filt(board, list(filter(Fens._in_board_filt, moves)), iam_upper)

    @staticmethod
    def _n_move(board: List[List[Union[str, None]]], r:int, c:int) -> List[Tuple[int, int]]:
        moves = [(r + xr, c + xc) for xr, xc in [(1, 2), (2, 1), (1, -2), (-2, 1), (-1, 2), (2, -1), (-1, -2), (-2, -1)]]
        iam_upper = board[r][c].isupper()
        return Fens._ok_filt(board, list(filter(Fens._in_board_filt, moves)), iam_upper)

    @staticmethod
    def _p_move(board: List[List[Union[str, None]]], r:int, c:int) -> List[Tuple[int, int]]:
        assert r != 0 and r != 7, "pawn at top"
        iam_upper = board[r][c].isupper()
        movelist = []
        if iam_upper:   # white
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
        else:   # black
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
            if cell:    # has a piece here
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
    def can_capture_opp_king_or_cell(board: List[List[Union[str, None]]], white_now: bool, spec_cell: Tuple[int, int] =
    None) -> bool:
        opp_king = Fens.get_king_place(board, not white_now) if spec_cell is None else spec_cell   # check castle cells
        # print(" opp_king", opp_king)
        for r in range(8):
            for c in range(8):
                cell = board[r][c]
                if cell and cell.isupper() == white_now:
                    movelist = Move_Func_Dict[cell.lower()](board, r, c)    # type: List[Tuple[int, int]]

                    # print(" movelist", r, c, movelist)
                    if opp_king in movelist:
                        # print(" hit")
                        return True
        return False


Move_Func_Dict = {piece: getattr(Fens, "_{}_move".format(piece)) for piece in "pbnrqk"}   \
    # type: Dict[str, Callable[[List[List[str]], int, int], List[Tuple[int, int]]]]


if __name__ == '__main__':
    pass

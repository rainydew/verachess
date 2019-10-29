# coding: utf-8
# event handlers
from verachess_global import Globals, ModelLock, calc_fen_hash
from typing import Tuple, Optional, List
from consts import Color, Promotions, EndType, Winner
import easygui
import boards
import verachess_support as vs

bd = boards.Fens


def refresh_highlights(new_cells: Optional[List[Tuple[int, int]]] = None) -> None:
    vs.set_cell_back_colors(new_cells, Globals.Highlights)
    Globals.Highlights = new_cells or []


def clear_sel_highs():
    refresh_highlights()
    vs.set_cell_color(Globals.Selection)
    Globals.Selection = None


def set_check_cell(place: Tuple[int, int]):
    vs.set_cell_color(place, Color.magenta)
    Globals.Check = place


def clear_check_cell():
    vs.set_cell_color(Globals.Check)
    Globals.Check = None


def refresh_opp_check():
    fen = Globals.Game_fen
    cell = bd.checked_place(fen)
    if cell:
        set_check_cell(cell)


def refresh_whole_board():  # recommand
    boards.refresh_cells()
    clear_sel_highs()
    refresh_opp_check()


def check_wdl(silent: bool = False):
    res = bd.check_wdl(Globals.Game_fen, Globals.History_hash)
    if res and not Globals.Game_end:    # prevent overwrite
        Globals.Game_end = res
        if res == EndType.checkmate:
            message = "{}方将死了对手，获得胜利".format("白" if Globals.Winner == Winner.white else "黑")
        elif res == EndType.three_fold:
            message = "三次重复局面，和棋"
        elif res == EndType.fifty_rule:
            message = "五十回合内没有吃子和动兵，和棋"
        elif res == EndType.stalemate:
            message = "行棋方无子可动且未被将军，逼和"
        elif res == EndType.insufficient_material:
            message = "双方剩余子力均不能将死对方，和棋"
        if not silent:
            with ModelLock():
                easygui.msgbox(message, "棋局结束", "确认")


def check_fen_format_valid(fen: str) -> Tuple[bool, str]:
    # 只检查格式，调用后面的函数来检查局面合理性
    try:
        f_list = fen.strip().split(" ")
        msg = "FEN格式不正确。FEN应包含六段信息：局面 行棋方 易位权 过路兵格 和棋计数 当前回合数\n" \
              "每一步棋如是动兵或吃子，则和棋计数重置为0，反之计数加1。如这个数达到100(即50回合)时仍不能将死，会判和棋"
        assert len(f_list) == 6
        narrow_fen, mover, castle, ep, drawcount, movecount = f_list    # type: str
        msg = "和棋计数或当前回合数不正确"
        assert int(drawcount) >= 0 and int(movecount) >= 1
        msg = "易位信息不正确。易位权由这些字符组成：K=白方王翼易位，Q=白方后翼易位，k=黑方王翼易位，q=黑方后翼易位\n" \
              "如果双方均无易位权，填-\n" \
              "如果是chess960，填王翼车和后翼车的列号，大写白棋，小写黑棋。例如HAha"
        if not bd.is_chess960(fen):
            # normal
            assert castle in ["".join([s if i & p else "" for p, s in {8: "K", 4:"Q", 2:"k", 1:"q"}.items()]) if i != 0 else
                              "-" for i in range(16)]
        else:
            # c960
            assert len(set(castle.lower())) in (1, 2) and len(set(castle)) == len(castle) and all(
                [x.lower() in "abcdefgh" for x in castle])
        msg = "过路兵格的值不正确。过路兵格是兵直进两格时，通过中间格的坐标。如果上一步没有兵直进两格，则填-"
        assert ep == "-" or (len(ep) == 2 and ep[1] in "36" and ord(ep[0]) in range(97, 105))
        msg = "行棋方不正确。必须为w (白放) 或 b (黑方)"
        assert mover in list("wb")  # other wise wb and '' returns True
        msg = "局面内有非法字符。斜杠/用来隔开局面的每一行，记录顺序是从黑方的第8行到白方的第1行\n" \
              "每一行中要么为数字1-8，代表连续的空位个数；要么为棋子字母 k=王 q=后 r=车 b=象 n=马 p=兵\n" \
              "大写字母表示白棋，小写字母表示黑棋"
        assert all([char in "12345678KkQqBbNnRrPp/" for char in narrow_fen])
        rows = narrow_fen.split("/")
        msg = "局面的行数不是8行"
        assert len(rows) == 8
        for row in rows:
            msg = "行{}的格子数不是8个".format(row)
            assert sum([int(char) if char in "12345678" else 1 for char in row]) == 8
    except:
        return False, msg
    else:
        return bd.check_fen_legal(fen)


def click_handler(place: Tuple[int, int]) -> None:
    fen = Globals.Game_fen
    if Globals.Game_role[bd.get_mover(fen)]:   # not occupied by human, need fen calc so it placed here
        return
    if Globals.Selection == place:
        # click twice to unselect
        clear_sel_highs()
        return
    vs.clear_sunken_cell()
    if place not in Globals.Highlights:
        # change other place to click, no return because it may be my another piece
        clear_sel_highs()
    if Globals.Selection is None:
        if bd.can_control(fen, place):
            clear_check_cell()      # unlink check magenta
            move_list = bd.get_piece_move(fen, place) + [place]
            refresh_highlights(move_list)
            vs.set_cell_color(place, Color.blue)
            vs.set_cell_color(Globals.Selection)
            Globals.Selection = place
    else:
        # make a move, c960 castle included
        move = bd.place_to_cellname(Globals.Selection) + bd.place_to_cellname(place)
        if bd.is_promotion(fen, Globals.Selection, place):
            plist, pdict = (Promotions.white, Promotions.white_rev) if place[0] == 0 else (Promotions.black,
                                                                                           Promotions.black_rev)
            with ModelLock():
                res = easygui.buttonbox("选择你要升变的棋子(默认皇后)", "兵的升变", plist, fontsize=24) or plist[0]
            move += pdict[res]
        # make a move, will move to another funtion in the future to handle clock and pgn
        vs.set_cell_color(Globals.LastMove)
        new_fen, special = bd.calc_move(Globals.Game_fen, move)
        Globals.Game_fen = new_fen
        Globals.White = not Globals.White
        Globals.History.append(new_fen)
        Globals.History_hash.append(calc_fen_hash(new_fen))
        Globals.AlphabetMovelist.append(move)  # todo: pgn movelist
        vs.set_sunken_cell(Globals.Selection)
        clear_sel_highs()
        refresh_whole_board()
        if special:
            place = special
        vs.set_cell_color(place, Color.red)
        Globals.LastMove = place
        check_wdl()

# coding: utf-8
# event handlers
from verachess_global import Globals, ModelLock, calc_fen_hash
from typing import Tuple, Optional, List
from consts import Color, Promotions, EndType, Winner, Font, InfoTypes, Positions, EcoBook, EndTypeToInfo, Winner_Dict
from notify import alert
import tkinter as tk
import easygui
import boards
import verachess_support as vs

bd = boards.Fens
pg = boards.Pgns


def refresh_cells():
    fen = Globals.GameFen
    vs.set_cell_values_and_diff(bd.get_narrow_fen(fen))
    vs.set_player_color(bd.get_mover(fen) == "w")


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
    fen = Globals.GameFen
    cell = bd.checked_place(fen)
    if cell:
        set_check_cell(cell)


def refresh_eco():
    if Globals.Chess_960_Columns[0] is not None:
        eco = "Chess960"
    else:
        eco = EcoBook.get(" ".join(Globals.GameFen.split()[:4]))
    label = Globals.Main.ECO
    if eco:
        vs.Eco.set(eco)
        label.configure(foreground=Color.black)
    else:
        label.configure(foreground=Color.red)


def refresh_scroll_state():
    rows = Globals.MoveRows[-1]

    if rows > 6:
        Globals.Main.MoveScale.configure(to=0.01 + rows - 6)
        vs.ListScroll(rows - 6)
    else:
        Globals.Main.MoveScale.configure(to=0.01)
        vs.ListScroll(0)


def refresh_end_type():
    vs.TerminateInfo.set("棋局状态：{}\n{}".format(Winner_Dict.get(Globals.Winner), EndTypeToInfo.get(Globals.Game_end)))


def add_last_pgn():
    main = Globals.Main

    lastmove = main.Moves[-1]
    lastmove.configure(background=Color.move_normal)

    # print("debug", lastmove.winfo_geometry(), lastmove.winfo_x(), lastmove.winfo_y(), lastmove.winfo_width())

    x, y = lastmove.winfo_x() + lastmove.winfo_width(), lastmove.winfo_y() - 22   # frame label height
    max_width = main.MoveFrame.winfo_x() + 12
    last_pgn = Globals.PGNMovelist[-1]
    move = tk.Label(main.MoveFrame)

    move.configure(background=Color.move_highlight)
    move.configure(font=Font.font_move)
    move.configure(text=last_pgn)
    move.bind('<Button-1>', lambda e: vs.move_click(e))

    if move.winfo_width() + x > max_width:  # wrap the line after text set      if True or xxx to make a stub
        move.place(x=3, y=y + 24, height=24)
        add_new_row = True
    else:
        move.place(x=x, y=y, height=24)
        add_new_row = False

    move.update()   # otherwise we cannot get correct geometry, x or y during pgn loading!!!

    main.Moves.append(move)
    Globals.MoveNames.append(str(move))
    Globals.MoveRows.append(Globals.MoveRows[-1] if not add_new_row else Globals.MoveRows[-1] + 1)
    Globals.ReverseMoveNames[str(move)] = len(Globals.MoveNames) - 1

    refresh_scroll_state()


def remove_pgn_from(pos: int = 1):
    assert pos > 0, "cannot remove base PGN info"
    main = Globals.Main

    del Globals.MoveNames[pos:]      # garbage collection
    del Globals.MoveRows[pos:]
    while len(main.Moves) > pos:
        del Globals.ReverseMoveNames[str(main.Moves[-1])]
        main.Moves[-1].destroy()
        del main.Moves[-1]

    main.Moves[-1].configure(background=Color.move_highlight)
    Globals.MoveSlider = -1
    refresh_scroll_state()


def set_board_to_old(pos: int):
    assert pos > 0, "cannot remove base PGN info"
    move_pos = pos - 1   # no startpos in movelist

    del Globals.AlphabetMovelist[move_pos:]
    del Globals.PGNMovelist[move_pos:]
    del Globals.InfoHistory[move_pos:]
    del Globals.History[pos:]
    del Globals.History_hash[pos:]
    remove_pgn_from(pos)


def refresh_start_pos_in_movelist():
    main = Globals.Main
    main.Moves[0].configure(text=Globals.Start_pos)


def refresh_whole_board():  # recommand
    refresh_cells()
    clear_sel_highs()
    refresh_opp_check()
    refresh_eco()


def check_wdl(silent: bool = False):
    res = bd.check_wdl(Globals.GameFen, Globals.History_hash)
    if res and not Globals.Game_end:  # prevent overwrite
        Globals.Game_end = res
        if res == EndType.checkmate:
            if Globals.Winner == Winner.white:
                Globals.TerminationInfo = "white mates"
                message = "白方将死了对手，获得胜利"
            else:
                Globals.TerminationInfo = "black mates"
                message = "黑方将死了对手，获得胜利"
        elif res == EndType.three_fold:
            Globals.TerminationInfo = "three fold repeatation"
            message = "三次重复局面，和棋"
        elif res == EndType.fifty_rule:
            Globals.TerminationInfo = "fifty moves rule"
            message = "五十回合内没有吃子和动兵，和棋"
        elif res == EndType.stalemate:
            Globals.TerminationInfo = "stalemate"
            message = "行棋方无子可动且未被将军，逼和"
        elif res == EndType.insufficient_material:
            Globals.TerminationInfo = "insufficient material"
            message = "双方剩余子力均不能将死对方，和棋"
        if not silent:
            with ModelLock():
                easygui.msgbox(message, "棋局结束", "确认")
    refresh_end_type()


def check_fen_format_valid(fen: str) -> Tuple[bool, str]:
    # 只检查格式，调用后面的函数来检查局面合理性
    try:
        f_list = fen.strip().split(" ")
        msg = "FEN格式不正确。FEN应包含六段信息：局面 行棋方 易位权 过路兵格 和棋计数 当前回合数\n" \
              "每一步棋如是动兵或吃子，则和棋计数重置为0，反之计数加1。如这个数达到100(即50回合)时仍不能将死，会判和棋"
        assert len(f_list) == 6
        narrow_fen, mover, castle, ep, drawcount, movecount = f_list  # type: str
        msg = "和棋计数或当前回合数不正确"
        assert int(drawcount) >= 0 and int(movecount) >= 1
        msg = "易位信息不正确。易位权由这些字符组成：K=白方王翼易位，Q=白方后翼易位，k=黑方王翼易位，q=黑方后翼易位\n" \
              "如果双方均无易位权，填-\n" \
              "如果是chess960，填王翼车和后翼车的列号，大写白棋，小写黑棋。例如HAha"
        if not bd.is_chess960(fen):
            # normal
            assert castle in [
                "".join([s if i & p else "" for p, s in {8: "K", 4: "Q", 2: "k", 1: "q"}.items()]) if i != 0 else
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
    fen = Globals.GameFen
    if Globals.Game_role[bd.get_mover(fen)]:  # not occupied by human, need fen calc so it placed here
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
            clear_check_cell()  # unlink check magenta
            move_list = bd.get_piece_move(fen, place) + [place]
            refresh_highlights(move_list)
            vs.set_cell_color(place, Color.blue)
            vs.set_cell_color(Globals.Selection)
            Globals.Selection = place
    else:
        # make a move, c960 castle included
        if Globals.MoveSlider != -1:
            if not easygui.ynbox("这将覆盖原先的棋谱，确定继续吗？", "当前局面不是棋谱记录的最终局面", ["是", "否"]):
                return
            remove_pgn_from(Globals.MoveSlider + 1)
        move = bd.place_to_cellname(Globals.Selection) + bd.place_to_cellname(place)
        if bd.is_promotion(fen, Globals.Selection, place):
            plist, pdict = (Promotions.white, Promotions.white_rev) if place[0] == 0 else (Promotions.black,
                                                                                           Promotions.black_rev)
            with ModelLock():
                res = easygui.buttonbox("选择你要升变的棋子(默认皇后)", "兵的升变", plist, fontsize=24) or plist[0]
            move += pdict[res]
        # make a move, will move to another funtion in the future to handle clock and pgn
        vs.set_cell_color(Globals.LastMove)
        old_fen = Globals.GameFen
        new_fen, special = bd.calc_move(old_fen, move)
        Globals.InfoHistory.append({})      # set it earlier than clock change mover
        from clock import before_change_mover
        before_change_mover()
        Globals.GameFen = new_fen
        Globals.White = not Globals.White
        Globals.History.append(new_fen)
        Globals.History_hash.append(calc_fen_hash(new_fen))
        Globals.AlphabetMovelist.append(move)
        Globals.PGNMovelist.append("".join(pg.single_uci_to_pgn(old_fen, move, new_fen)))
        vs.set_sunken_cell(Globals.Selection)
        refresh_whole_board()
        if special:
            place = special
        vs.set_cell_color(place, Color.red)
        Globals.LastMove = place
        add_last_pgn()
        check_wdl()


def pgn_move(movelist: List[str]) -> Optional[str]:
    # loading pgn
    for pgn in movelist:
        # print(pgn)
        move = pg.verified_fast_single_pgn_to_uci(Globals.GameFen, pgn)
        # print(move)
        if move is None:
            break
        ai_move_handler(move, need_verify=False)
    else:
        return None
    return "error loading at {}".format(pgn)


def ai_move_handler(move: str, need_verify: bool = True) -> Optional[str]:
    vs.clear_sunken_cell()
    if Globals.MoveSlider != -1:
        remove_pgn_from(Globals.MoveSlider + 1)
    vs.set_cell_color(Globals.LastMove)
    old_fen = Globals.GameFen
    # check move
    if need_verify and not bd.verify_uci_move(old_fen, move):
        return "illegal move {}".format(move)
    new_fen, special = bd.calc_move(old_fen, move)
    Globals.InfoHistory.append({})  # set it earlier than clock change mover
    from clock import before_change_mover
    before_change_mover()
    Globals.GameFen = new_fen
    Globals.White = not Globals.White
    Globals.History.append(new_fen)
    Globals.History_hash.append(calc_fen_hash(new_fen))
    Globals.AlphabetMovelist.append(move)
    Globals.PGNMovelist.append("".join(pg.single_uci_to_pgn(old_fen, move, new_fen)))
    refresh_whole_board()
    if special:
        place = special
    else:
        place = bd.cellname_to_place(move[2:4])
    vs.set_sunken_cell(place)
    vs.set_cell_color(place, Color.red)
    Globals.LastMove = place
    add_last_pgn()
    check_wdl()
    return None     # without errorinfo


def change_position(place: int):
    main = Globals.Main
    main.Moves[Globals.MoveSlider].configure(background=Color.move_normal)

    vs.clear_sunken_cell()
    vs.set_cell_color(flush_all=True)
    vs.set_cell_back_colors(flush_all=True)

    time_place = place - 1
    Globals.GameFen = Globals.History[place] if place else \
                      Globals.Start_pos if Globals.Start_pos != Positions.name_normal_startpos else \
                      Positions.common_start_fen
    Globals.White = bd.get_mover(Globals.GameFen)
    if place:
        res = Globals.InfoHistory[time_place].get(InfoTypes.time_remain)
        res_use = Globals.InfoHistory[time_place].get(InfoTypes.time_use)
        assert res is not None, "no time data"
        assert res_use is not None, "no time use data"
        if Globals.White == "w":
            Globals.Bremain = res
            Globals.Buse = res_use
            Globals.Wuse = 0
            if time_place:
                res = Globals.InfoHistory[time_place - 1].get(InfoTypes.time_remain)
                assert res, "no prev time data"
                Globals.Wremain = res
            else:
                Globals.Wremain = Globals.Wtime
        else:
            Globals.Wremain = res
            Globals.Wuse = res_use
            Globals.Buse = 0
            if time_place:
                res = Globals.InfoHistory[time_place - 1].get(InfoTypes.time_remain)
                assert res, "no prev time data"
                Globals.Bremain = res
            else:
                Globals.Bremain = Globals.Btime
    else:
        Globals.Wremain = Globals.Wtime
        Globals.Bremain = Globals.Btime
        Globals.Wuse = Globals.Buse = 0
    Globals.MoveSlider = -1 if place == len(Globals.History) - 1 else place
    main.Moves[Globals.MoveSlider].configure(background=Color.move_highlight)
    refresh_whole_board()
    from clock import refresh_clock
    refresh_clock()


def move_change_handler(place: int) -> None:
    if not vs.MenuStats[vs.MenuStatNames.clock].get() or any(Globals.Game_role.values()):  # clock enabled, cannot click
        alert("在时钟开启、有引擎参与、或有联网棋手的情况下，不能切换棋谱局面")
        return
    change_position(place)

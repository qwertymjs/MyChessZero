# -*- coding: utf-8 -*-
import tkinter
import time

h_level_index = {'south' : (u"九",u"八",u"七",u"六",u"五",u"四",u"三",u"二",u"一"), 'north' : (u"１",u"２",u"３",u"４",u"５",u"６",u"７",u"８",u"９")}
v_change_index = {'south' : (u'', u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"), 'north' : (u'', u"１",u"２",u"３",u"４",u"５",u"６",u"７",u"８",u"９")}

def board_coord(x):
    return 30 + 40*x

class ChessView:
    root = tkinter.Tk()
    root.title("Chinese Chess")
    root.resizable(0, 0)
    can = tkinter.Canvas(root, width=600, height=420)
    can.pack(expand=tkinter.YES, fill=tkinter.BOTH)
    img = tkinter.PhotoImage(file="images/WHITE.gif")
    can.create_image(0, 0, image=img, anchor=tkinter.NW)
    piece_images = dict()
    move_images = []

    def __init__(self, board):
        self.board = board
        self.delay_sec = 1

    def draw_board(self, board):
        self.piece_images.clear()
        self.move_images = []
        pieces = board.pieces
        self.can.delete("label1", 'label2')
        self.can.create_text(420, 30, text="走子记录", tags = "label1")
        self.can.create_line(380, 200, 600, 200)
        self.can.create_text(440, 230, text="AlphaZero信息", tags = "label2")
        for (x, y) in pieces.keys():
            self.piece_images[x, y] = tkinter.PhotoImage(file=pieces[x, y].get_image_file_name())
            self.can.create_image(board_coord(x), board_coord(y), image=self.piece_images[x, y])
 

    def update(self, move=None, disp_data=None, is_show_gui=1, title="Chinese Chess"):
        self.root.title(title)
        x_trans = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8}
        if move != None:
            src = move[0:2]
            dst = move[2:4]

            src_x = int(x_trans[src[0]])
            src_y = int(src[1])

            dst_x = int(x_trans[dst[0]])
            dst_y = int(dst[1])
            piece_zh_name = self.board.pieces[src_x, src_y].zh_name
            board_side = self.board.pieces[src_x, src_y].direction
            board_side_name = u'黑'
            diff = dst_y - src_y
            if board_side == 'south':
                diff = -1 * diff
                board_side_name = u'红'
            if diff == 0:
                diff_str = u'平'
            elif diff > 0:
                diff_str = u'进'
            elif diff < 0:
                diff_str = u'退'

            if piece_zh_name in [u"士", u"仕", u"馬", u"马", u"象", u"相"]:
                dest_str = h_level_index[board_side][dst_x]
            else:
                if diff == 0:
                    dest_str = h_level_index[board_side][dst_x]
                elif diff > 0:
                    dest_str = v_change_index[board_side][diff]
                else:
                    dest_str = v_change_index[board_side][-diff]

            move_txt = '{} : {}{}{}{}'.format(board_side_name, piece_zh_name, h_level_index[board_side][src_x], diff_str, dest_str)
            self.board.move(src_x, src_y, dst_x - src_x, dst_y - src_y)
        self.draw_board(self.board)
        self.can.delete("move", 'm_number', "mcts_time", 'win_rate')
        print('{}'.format(move_txt))
        self.can.create_text(430, 80, text = move_txt, tags = "move")
        m_number_text = '走子总步数 {}'.format(disp_data['move_number'] + 1)
        self.can.create_text(430, 60, text = m_number_text, tags = "m_number")
        self.can.create_text(450, 260, text="MCTS搜索时间 : {}".format('%.1f' % disp_data['mcts_time']), tags = "mcts_time")
        self.can.create_text(445, 280, text="局势预估胜率 : {}".format('%.3f' % disp_data['win_rate'][0][0]), tags = "win_rate")
        # self.can.create_text(440, 300, text="MCTS搜索结果 : ")
        if is_show_gui:
            self.root.update()
            time.sleep(self.delay_sec)
# -*- coding: utf-8 -*-
import tkinter
import time

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
        self.delay_sec = 3

    def draw_board(self, board):
        self.piece_images.clear()
        self.move_images = []
        pieces = board.pieces
        self.can.create_text(420, 30, text="走子记录")
        self.can.create_line(380, 200, 600, 200)
        self.can.create_text(440, 230, text="AlphaZero信息")
        for (x, y) in pieces.keys():
            self.piece_images[x, y] = tkinter.PhotoImage(file=pieces[x, y].get_image_file_name())
            self.can.create_image(board_coord(x), board_coord(y), image=self.piece_images[x, y])
 

    def update(self, move=None, title="Chinese Chess", is_show_gui=1):
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
            diff = dst_y - src_y
            if diff == 0:
                diff_str = u'平'
            elif diff > 0:
                diff_str = u'进'
            elif diff < 0:
                diff_str = u'退'
            move_txt = '{} ({} {}) {} ({} {})'.format(piece_zh_name, src_x, src_y, diff_str ,dst_x, dst_y) 
            self.board.move(src_x, src_y, dst_x - src_x, dst_y - src_y)
        self.draw_board(self.board)
        self.can.delete("move")
        print('{}'.format(move_txt))
        self.can.create_text(430, 60, text = move_txt, tags = "move")
        if is_show_gui:
            self.root.update()
            time.sleep(self.delay_sec)
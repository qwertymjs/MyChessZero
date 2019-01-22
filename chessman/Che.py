# -*- coding: utf-8 -*-
from ChessPiece import ChessPiece

class Che(ChessPiece):

    def __init__(self, x, y, is_red, direction):
        ChessPiece.__init__(self, x, y, is_red, direction)
        self.zh_name = self.name()

    def name(self):
        if self.direction == 'north':
            return u"車"
        else:
            return u'车'

    def can_move(self, board, dx, dy):
        if dx != 0 and dy != 0: # 车不能斜着走
            return False
        nx, ny = self.x + dx, self.y + dy
        if nx < 0 or nx > 8 or ny < 0 or ny > 9: # 超出棋盘
            return False
        if (nx, ny) in board.pieces:
            if board.pieces[nx, ny].is_red == self.is_red: # 位置有己方棋子
                return False
        cnt = self.count_pieces(board, self.x, self.y, dx, dy)
        if (nx, ny) not in board.pieces: # 目标位置没有子
            if cnt != 0: # 车走的线路上有子，不能走
                return False
        else:
            if cnt != 0: # 车走的线路上有子，不能走
                return False
            else:
                return True # 走到该位置或者吃子
        return True

    def get_image_file_name(self):
        if self.selected:
            if self.is_red:
                return "images/RRS.gif"
            else:
                return "images/BRS.gif"
        else:
            if self.is_red:
                return "images/RR.gif"
            else:
                return "images/BR.gif"

    def get_selected_image(self):
        if self.is_red:
            return "images/RRS.gif"
        else:
            return "images/BRS.gif"
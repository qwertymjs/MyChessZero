# -*- coding: utf-8 -*-
from ChessPiece import ChessPiece

class Bing(ChessPiece):

    def __init__(self, x, y, is_red, direction):
        ChessPiece.__init__(self, x, y, is_red, direction)
        self.zh_name = self.name()

    def name(self):
        if self.direction == 'north':
            return u"卒"
        else:
            return u'兵'
    def can_move(self, board, dx, dy):
        if abs(dx) + abs(dy) != 1: # 走一格判断
            return False
        if (self.is_north() and dy == -1) or (self.is_south() and dy==1): # 回头判断
            return False
        if dy == 0:
            if (self.is_north() and self.y <5) or (self.is_south() and self.y >=5): # 兵过河才能横走
                return False
        nx, ny = self.x + dx, self.y + dy
        if nx < 0 or nx > 8 or ny < 0 or ny > 9: # 超出棋盘
            return False
        if (nx, ny) in board.pieces:
            if board.pieces[nx, ny].is_red == self.is_red: # 当前有己方的子
                return False
            else:
                pass # 走到该位置或者吃子
        return True

    def get_image_file_name(self):
        if self.selected:
            if self.is_red:
                return "images/RPS.gif"
            else:
                return "images/BPS.gif"
        else:
            if self.is_red:
                return "images/RP.gif"
            else:
                return "images/BP.gif"

    def get_selected_image(self):
        if self.is_red:
            return "images/RPS.gif"
        else:
            return "images/BPS.gif"
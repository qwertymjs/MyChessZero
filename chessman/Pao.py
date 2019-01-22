# -*- coding: utf-8 -*-
from ChessPiece import ChessPiece

class Pao(ChessPiece):

    def __init__(self, x, y, is_red, direction):
        ChessPiece.__init__(self, x, y, is_red, direction)
        self.zh_name = self.name()

    def name(self):
        if self.direction == 'north':
            return u"砲"
        else:
            return u"炮"

    def can_move(self, board, dx, dy):
        if dx != 0 and dy != 0: # 炮不能斜着走
            return False
        nx, ny = self.x + dx, self.y + dy
        if nx < 0 or nx > 8 or ny < 0 or ny > 9: # 超出棋盘
            return False
        if (nx, ny) in board.pieces:
            if board.pieces[nx, ny].is_red == self.is_red: # 位置有己方棋子
                return False
        cnt = self.count_pieces(board, self.x, self.y, dx, dy)
        if (nx, ny) not in board.pieces:
            if cnt!= 0:
                return False # 目标位置没有子，路线有子，不能走
        else:
            if cnt != 1: # 目标位置有子， 但路线上没子，不能走
                return False
        return True

    def get_image_file_name(self):
        if self.selected:
            if self.is_red:
                return "images/RCS.gif"
            else:
                return "images/BCS.gif"
        else:
            if self.is_red:
                return "images/RC.gif"
            else:
                return "images/BC.gif"

    def get_selected_image(self):
        if self.is_red:
            return "images/RCS.gif"
        else:
            return "images/BCS.gif"

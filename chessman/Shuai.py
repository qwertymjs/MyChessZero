# -*- coding: utf-8 -*-
from ChessPiece import ChessPiece

class Shuai(ChessPiece):

    is_king = True
    def __init__(self, x, y, is_red, direction):
        ChessPiece.__init__(self, x, y, is_red, direction)
        self.zh_name = self.name()

    def name(self):
        if self.direction == 'north':
            return u"帅"
        else:
            return u"将"

    def can_move(self, board, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if nx < 0 or nx > 8 or ny < 0 or ny > 9: # 超出棋盘
            return False
        if (nx, ny) in board.pieces:
            if board.pieces[nx, ny].is_red == self.is_red: # 位置有己方棋子
                return False
        if dx == 0 and self.count_pieces(board, self.x, self.y, dx, dy) == 0 and ((nx, ny) in board.pieces) and board.pieces[nx, ny].is_king:
            return True # 将帅不能相对
        if not (self.is_north() and 3 <= nx <=5 and 0<= ny <=2) and not (self.is_south() and 3 <= nx <= 5 and 7 <= ny <= 9):
            return False # 走出九宫格
        if abs(dx) + abs(dy) != 1: # 单格或者斜走
            return False
        return True

    def get_image_file_name(self):
        if self.selected:
            if self.is_red:
                return "images/RKS.gif"
            else:
                return "images/BKS.gif"
        else:
            if self.is_red:
                return "images/RK.gif"
            else:
                return "images/BK.gif"

    def get_selected_image(self):
        if self.is_red:
            return "images/RKS.gif"
        else:
            return "images/BKS.gif"


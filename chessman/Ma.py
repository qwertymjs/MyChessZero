# -*- coding: utf-8 -*-
from ChessPiece import ChessPiece

class Ma(ChessPiece):

    def __init__(self, x, y, is_red, direction):
        ChessPiece.__init__(self, x, y, is_red, direction)
        self.zh_name = self.name()

    def name(self):
        if self.direction == 'north':
            return u"馬"
        else:
            return u"马"

    def can_move(self, board, dx, dy):
        x, y = self.x, self.y
        nx, ny = x+dx, y+dy
        if nx < 0 or nx > 8 or ny < 0 or ny > 9: # 超出棋盘
            return False
        if dx == 0 or dy == 0: # 斜着走
            return False
        if abs(dx) + abs(dy) !=3: # 马走日
            return False
        if (nx, ny) in board.pieces: # 位置有己方棋子
            if board.pieces[nx, ny].is_red == self.is_red:
                return False
        if (x if abs(dx) ==1 else x+dx/2, y if abs(dy) ==1 else y+ (dy/2)) in board.pieces: # 绊马脚
            return False
        return True

    def get_image_file_name(self):
        if self.selected:
            if self.is_red:
                return "images/RNS.gif"
            else:
                return "images/BNS.gif"
        else:
            if self.is_red:
                return "images/RN.gif"
            else:
                return "images/BN.gif"

    def get_selected_image(self):
        if self.is_red:
            return "images/RNS.gif"
        else:
            return "images/BNS.gif"

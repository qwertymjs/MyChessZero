# -*- coding: utf-8 -*-
from ChessBoard import *
from ChessView import ChessView
import time

class ChessGame:

    def __init__(self, human_color = "b"):
        self.human_color = human_color
        self.current_player = "w"
        self.players = {}
        self.players[self.human_color] = "human"
        ai_color = "w" if self.human_color == "b" else "b"
        self.players[ai_color] = "AI"

        self.board = ChessBoard(self.human_color == 'b')
        self.view = ChessView(board=self.board)

    def start_self_play(self, is_show_gui=1, temp=1e-3):
 
        self.view.update()
        time.sleep(4)
        self.board.move(7,7, -1, 0)
        self.view.update(is_show_gui=0)

game = ChessGame()
game.start_self_play()
time.sleep(3)
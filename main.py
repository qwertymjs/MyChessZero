# -*- coding: utf-8 -*-
import numpy as np
from GameBoard import GameState, start_game_play
from collections import defaultdict, deque
from policy_value_network import *
from mcts_alphaZero import MCTSPlayer
import time


class alphaZero(object):
    def __init__(self, search_threads = 16, res_block_nums = 7, init_modle = None):
        self.temperature = 1
        self.buffer_size = 10000
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.search_threads = search_threads
        self.temp = 1.0
        self.n_playout = 500
        self.c_puct = 5

        # 是否加载原先已经存在的训练数据
        if init_modle:
            self.policy_value_net = PolicyValueNet()
        else:
            self.policy_value_net = PolicyValueNet()

        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn, c_puct=self.c_puct,
                                      n_playout=self.n_playout, is_selfplay=1)
    
    # 收集自对弈数据
    def collect_selfplay_data(self, n_games=1):
        for i in range(n_games):
            winner, play_data = start_game_play(self.mcts_player, temp=self.temp)
            print("winner {}".format(winner))
            print("play_data {}".format(play_data))        
            
            


if __name__ == '__main__':
    obj = alphaZero()
    obj.collect_selfplay_data()

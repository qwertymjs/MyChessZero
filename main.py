# -*- coding: utf-8 -*-
import numpy as np
import random
from GameBoard import GameState, start_game_play
from collections import defaultdict, deque
from policy_value_network import *
from mcts_alphaZero import MCTSPlayer
import time
import datetime
import pickle
import os
import sys
import logging
import argparse

class alphaZero(object):
    def __init__(self, search_threads = 16, res_block_nums = 7, init_modle = None):
        self.temperature = 1
        self.batch_size = 1024
        self.buffer_size = 10000
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.search_threads = search_threads
        self.temp = 1.0
        self.n_playout = 400
        self.c_puct = 5
        self.epochs = 5
        self.learn_rate = 0.001
        self.lr_multiplier = 1.0
        self.kl_targ = 0.02
        self.board_width = 9
        self.board_height = 10
        self.model_file = train_file = os.getcwd() + '/model/tf_policy_model'
        # 是否加载原先已经存在的训练数据
        if init_modle:
            self.policy_value_net = PolicyValueNet(self.model_file)
        else:
            self.policy_value_net = PolicyValueNet()

        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn, c_puct=self.c_puct,
                                      n_playout=self.n_playout, is_selfplay=1)
    
    # 收集自对弈数据
    def start_selfplay_data(self, n_games=1):
        for i in range(n_games):
            winner, play_data = start_game_play(self.mcts_player, temp=self.temp)
            now = datetime.datetime.now()
            train_data_file = now.strftime("%Y%m%d%H%M%S")
            train_data = {}
            train_data['winner'] = winner
            train_data['play_data'] = play_data
            f = open(os.getcwd() + '/train_data/' +str(train_data_file), 'wb')
            pickle.dump(train_data, f)

    # 读取selfplay数据训练
    def start_model_train(self, n_train=10000, buffer_size=10000, train_batch_size=2400, model_file=None):
        try:
            gs = GameState()
            if model_file:
                self.policy_value_net = PolicyValueNet(model_file)
            else:
                self.policy_value_net = PolicyValueNet()
            # 加载对弈数据
            data_buffer = deque(maxlen=buffer_size)
            train_file = os.getcwd() + '/train_data/'
            parents = os.listdir(train_file)
            extend_data = []
            for parent in parents:
                f = open(train_file + str(parent), 'rb')
                train_data = pickle.load(f)
                winner = train_data['winner']
                play_data = train_data['play_data']    
                for state, mcts_prob, winner in play_data:
                    states_data = gs.state_to_positions(state)
                    extend_data.append((states_data, mcts_prob, winner))
                self.data_buffer.extend(extend_data)
            print('data_buffer {}'.format(len(self.data_buffer)))
            if len(self.data_buffer) > self.batch_size:
                self.policy_update(self.policy_value_net)
                self.policy_value_net.saver.save(self.policy_value_net.session, self.policy_value_net.model_file)
            print(winner)
        except KeyboardInterrupt:
             logging.info('\n\rquit') 

    def policy_update(self, policy_value_net, verbose=True):
        """update the policy-value net"""
        mini_batch = random.sample(self.data_buffer, self.batch_size)
        state_batch = [data[0].reshape(14, self.board_width, self.board_height) for data in mini_batch]
        mcts_probs_batch = [data[1] for data in mini_batch]
        winner_batch = [data[2] for data in mini_batch]
        old_probs, old_v = policy_value_net.policy_value(state_batch)
        # print('old_probs {} old_v {}'.format(old_probs, old_v))
        loss_list = []
        entropy_list = []
        for i in range(self.epochs): 
            loss, entropy = policy_value_net.train_step(state_batch, 
                                             mcts_probs_batch, 
                                             winner_batch,
                                             self.learn_rate*self.lr_multiplier)
            
            loss_list.append(loss)
            entropy_list.append(entropy)
            
            new_probs, new_v = policy_value_net.policy_value(state_batch)
            kl = np.mean(np.sum(old_probs * (
                    np.log(old_probs + 1e-10) - np.log(new_probs + 1e-10)),
                    axis=1)
            )
            if kl > self.kl_targ * 4:  # early stopping if D_KL diverges badly
                break
        
        if kl > self.kl_targ * 2 and self.lr_multiplier > 0.1:
            self.lr_multiplier /= 1.5
        elif kl < self.kl_targ / 2 and self.lr_multiplier < 10:
            self.lr_multiplier *= 1.5
            
        if verbose:
            explained_var_old = (1 -
                                 np.var(np.array(winner_batch) - old_v.flatten()) /
                                 np.var(np.array(winner_batch)))
            explained_var_new = (1 -
                                 np.var(np.array(winner_batch) - new_v.flatten()) /
                                 np.var(np.array(winner_batch)))
            
            print(("kl: {:.3f}, "
                   "lr_multiplier: {:.3f}\n"
                   "loss: {:.3f}, "
                   "entropy: {:.3f}\n"
                   "explained old: {:.3f}, "
                   "explained new: {:.3f}\n"
                   ).format(kl,
                            self.lr_multiplier,
                            np.mean(loss_list),
                            np.mean(entropy_list),
                            explained_var_old,
                            explained_var_new))        


    # 与纯mcts对弈n_games盘
    def start_model_evaluate(self, n_games=10):
        pass         

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='train', choices=['train', 'selfplay', 'evaluate'], type=str, help='train or selfplay or evaluate')
    args = parser.parse_args()
    obj = alphaZero(init_modle=True)
    if args.type == 'train':
        obj.start_model_train()
    elif args.type == 'selfplay':
        obj.start_selfplay_data()
    elif args.type == 'evaluate':
        obj.start_model_evaluate()

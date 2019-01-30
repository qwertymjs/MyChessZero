# -*- coding: utf-8 -*-
import os
import numpy as np
import time

def sim_do_action(in_action, in_state):
    x_trans = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8}
    src = in_action[0:2]
    dst = in_action[2:4]
    src_x = int(x_trans[src[0]])
    src_y = int(src[1])
    dst_x = int(x_trans[dst[0]])
    dst_y = int(dst[1])
    board_positions = board_to_pos_name(in_state)
    line_lst = []
    for line in board_positions:
        line_lst.append(list(line))
    lines = np.array(line_lst)
    lines[dst_y][dst_x] = lines[src_y][src_x]
    lines[src_y][src_x] = '1'
    board_positions[dst_y] = ''.join(lines[dst_y])
    board_positions[src_y] = ''.join(lines[src_y])
    board = "/".join(board_positions)
    board = board.replace("111111111", "9")
    board = board.replace("11111111", "8")
    board = board.replace("1111111", "7")
    board = board.replace("111111", "6")
    board = board.replace("11111", "5")
    board = board.replace("1111", "4")
    board = board.replace("111", "3")
    board = board.replace("11", "2")
    return board

def board_to_pos_name(board):
    board = board.replace("2", "11")
    board = board.replace("3", "111")
    board = board.replace("4", "1111")
    board = board.replace("5", "11111")
    board = board.replace("6", "111111")
    board = board.replace("7", "1111111")
    board = board.replace("8", "11111111")
    board = board.replace("9", "111111111")
    return board.split("/")

def print_board(board, action = None):
    def string_reverse(string):
        return ''.join(string[i] for i in range(len(string) - 1, -1, -1))

    x_trans = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}

    if(action != None):
        src = action[0:2]

        src_x = int(x_trans[src[0]])
        src_y = int(src[1])

    board = board.replace("1", " ")
    board = board.replace("2", "  ")
    board = board.replace("3", "   ")
    board = board.replace("4", "    ")
    board = board.replace("5", "     ")
    board = board.replace("6", "      ")
    board = board.replace("7", "       ")
    board = board.replace("8", "        ")
    board = board.replace("9", "         ")
    board = board.split('/')
    print("     abcdefghi")
    for i,line in enumerate(board):
        if (action != None):
            if(i == src_y):
                s = list(line)
                s[src_x] = 'x'
                line = ''.join(s)
        print(i,line)

def read_png(filename):
    result = {}
    chess = []
    with open(filename) as rd:
        data = rd.readlines()
        for line in data:
            line = line.strip()
            if len(line) == 0:
                continue
            line = line.decode('gbk')
            if '.' in line and '[' not in line:
                chess.append(line)
            if 'Result' in line:
                result['result'] = line
    result['data'] = chess
    return result

def get_chess_pos(state, move, side):
    h_level_index = {'south' : (u"九",u"八",u"七",u"六",u"五",u"四",u"三",u"二",u"一"), 'north' : (u"１",u"２",u"３",u"４",u"５",u"６",u"７",u"８",u"９")}
    v_change_index = {'south' : (u'', u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"), 'north' : (u'', u"１",u"２",u"３",u"４",u"５",u"６",u"７",u"８",u"９")}
    chess_name_dict = {
        u"帅" : 'K',
        u"帥" : 'K',
        u"将" : 'k',
        u"仕" : 'A',
        u"士" : 'a',
        u"相" : 'B', 
        u"象" : 'b',
        u"马" : 'N',
        u"馬" : 'N',
        u"车" : 'R',
        u"車" : 'R',
        u"炮" : 'C',
        u'砲' : 'C',
        u"兵" : 'P', 
        u"卒" : 'p'    
    }
    chess_line = {u"一":9, u"二":8, u"三":7, u"四":6, u"五":5, u"六":4, u"七":3, u"八":2, u"九":1}
    dis_line = {u"一":1, u"二":2, u"三":3, u"四":4, u"五":5, u"六":6, u"七":7, u"八":8, u"九":9}
    if move[0] in chess_name_dict:
        if side == 'w':
            chess = chess_name_dict[move[0]].lower()
            src = int(chess_line[move[1]])
            action = move[2]
            if action == u'平' or chess in ['n', 'N', 'A', 'a', 'B', 'b']:
                dis = int(chess_line[move[3]])
            else:
                dis = int(dis_line[move[3]])
        else:
            chess = chess_name_dict[move[0]].upper()
            src = int(move[1])
            action = move[2]
            dis = int(move[3])
    else:
        if side == 'w':
            chess = chess_name_dict[move[1]].lower()
            src = move[0]
            action = move[2]
            if action == u'平' or chess in ['n', 'N', 'A', 'a', 'B', 'b']:
                dis = int(chess_line[move[3]])
            else:
                dis = int(dis_line[move[3]])
        else:
            chess = chess_name_dict[move[1]].upper()
            src = move[0]
            if src == u'前':
                src = u'后'
            else:
                src = u'前'
            action = move[2]
            dis = int(move[3])

    ys = '9876543210'[::-1]
    xs = 'abcdefghi'
    board = state.replace("1", " ")
    board = board.replace("2", "  ")
    board = board.replace("3", "   ")
    board = board.replace("4", "    ")
    board = board.replace("5", "     ")
    board = board.replace("6", "      ")
    board = board.replace("7", "       ")
    board = board.replace("8", "        ")
    board = board.replace("9", "         ")
    board = board.split('/')
    # print(board)
    # print chess, src, action, dis
    if chess in ['r', 'R', 'P', 'p', 'k', 'K', 'c', 'C']:
        if action != u'平' and side == 'w':
            dis = - dis
        if src in range(10):
            for i in range(10):
                if board[i][src - 1] == chess:
                    x = "{}{}".format(xs[src - 1], ys[i])
        elif src == u'前':
            if chess in ['p', 'P']:
                x_list = []
                for i in range(10):
                    for j in range(9):
                        if board[9 - i][j] == chess:
                            x1 = "{}{}".format(xs[j], ys[9 - i])
                            x_list.append(x1)
                x_list = sorted(x_list, reverse = True)
                cur_pos = x_list[0][0]
                for each in x_list[1:]:
                    if each[0] != cur_pos:
                        cur_pos = each[0]
                    else:
                        x = each
            else:
                flag = 0
                for i in range(10):
                    for j in range(9):
                        if board[i][j] == chess:
                            flag = 1
                            x = "{}{}".format(xs[j], ys[i])
                            break
                    if flag == 1:
                        break
        elif src == u'后':
            if chess in ['p', 'P']:
                x_list = []
                for i in range(10):
                    for j in range(9):
                        if board[9 - i][j] == chess:
                            x1 = "{}{}".format(xs[j], ys[9 - i])
                            x_list.append(x1)
                x_list = sorted(x_list)
                cur_pos = x_list[0][0]
                for each in x_list[1:]:
                    if each[0] != cur_pos:
                        cur_pos = each[0]
                    else:
                        x = each
                # print x
            else:
                flag = 0
                for i in range(10):
                    for j in range(9):
                        if board[9 - i][j] == chess:
                            flag = 1
                            x = "{}{}".format(xs[j], ys[9 - i])
                            break
                    if flag == 1:
                        break
        if action == u'平':
            y = "{}{}".format(xs[dis - 1], x[1])
        elif action == u'进':
            y = "{}{}".format(x[0], int(x[1]) + dis)
        elif action == u'退':
            y = "{}{}".format(x[0], int(x[1]) - dis)
    else:
        if src in range(10):
            x_list = []
            for i in range(10):
                if board[i][src - 1] == chess:
                    x = "{}{}".format(xs[src - 1], ys[i])
                    x_list.append(x)
            if len(x_list) > 1:
                for each in x_list:
                    if chess == 'a' and action == u'进' and int(each[1]) in [8, 9]:
                        x = each
                        break
                    if chess == 'a' and action == u'退' and int(each[1]) in [7, 8]:
                        x = each
                        break                        
                    if chess == 'A' and action == u'进' and int(each[1]) in [0, 1]:
                        x = each
                        break
                    if chess == 'A' and action == u'退' and int(each[1]) in [1, 2]:
                        x = each
                        break
                    if chess == 'b' and action == u'进' and int(each[1]) in [7, 9]:
                        x = each
                        break
                    if chess == 'b' and action == u'退' and int(each[1]) in [5, 7]:
                        x = each
                        break                        
                    if chess == 'B' and action == u'进' and int(each[1]) in [0, 2]:
                        x = each
                        break
                    if chess == 'B' and action == u'退' and int(each[1]) in [2, 4]:
                        x = each
                        break                      
        elif src == u'前':
            if chess in ['p', 'P']:
                x_list = []
                for i in range(10):
                    for j in range(9):
                        if board[9 - i][j] == chess:
                            x = "{}{}".format(xs[j], ys[9 - i])
                            x_list.append(x)
                # print(x_list)
            else:
                flag = 0
                for i in range(10):
                    for j in range(9):
                        if board[i][j] == chess:
                            flag = 1
                            x = "{}{}".format(xs[j], ys[i])
                            break
                    if flag == 1:
                        break
        elif src == u'后':
            if chess in ['p', 'P']:
                x_list = []
                for i in range(10):
                    for j in range(9):
                        if board[9 - i][j] == chess:
                            x = "{}{}".format(xs[j], ys[9 - i])
                            x_list.append(x)
                # print(x_list)
            else:
                flag = 0
                for i in range(10):
                    for j in range(9):
                        if board[9 - i][j] == chess:
                            flag = 1
                            x = "{}{}".format(xs[j], ys[9 - i])
                            break
                    if flag == 1:
                        break
        # print x
        if action == u'进':
            x_map = {'a':1, 'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9}
            if src == u"前" or src == u'后':
                # print src
                src = x_map[x[0]]
                # print src
            abs_ = abs(src - dis)
            if chess in ['n','N']:
                if abs_ == 1:
                    abs_ = 2
                else:
                    abs_ = 1
            if side == 'w':
                abs_ = - abs_
            y = "{}{}".format(xs[dis - 1], int(x[1]) + abs_)
        elif action == u'退':
            x_map = {'a':1, 'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9}
            if src == u"前" or src == u'后':
                # print src
                src = x_map[x[0]]
                # print src
            abs_ = abs(src - dis)
            if chess in ['n','N']:
                if abs_ == 1:
                    abs_ = 2
                else:
                    abs_ = 1
            if side == 'w':
                abs_ = - abs_
            y = "{}{}".format(xs[dis - 1], int(x[1]) - abs_)
    # print x + y, src, dis
    return x + y
if __name__ == '__main__':
    import pickle
    import os
    from GameBoard import *
    # train_file = os.getcwd() + '/train_data/20190130145012'
    # f = open(train_file, 'rb')
    # train_data = pickle.load(f, encoding='bytes')
    # gs = GameState()
    # cur_player = 'w'
    # for state, mcts_prob, winner in train_data[b'play_data']:
    #     state = str(state, 'utf-8')
    #     print((state))
    #     legal_moves = (GameBoard.get_legal_moves(state, cur_player))
    #     legal_moves_id = []
    #     for each in legal_moves:
    #         legal_moves_id.append(label2id[each])
    #     print(legal_moves_id)
    #     print(winner)
    #     if cur_player == 'w':
    #         cur_player = 'b'
    #     else:
    #         cur_player = 'w'
    # exit()
    train_dir = os.getcwd() + '/data/imsa_play/'
    err_file = 'err_file.log'
    f = open(err_file, 'wb')
    num = 0
    for file_name in os.listdir(train_dir):
        if num % 100 == 0:
            print(num)
        num += 1
        state = 'RNBAKABNR/9/1C5C1/P1P1P1P1P/9/9/p1p1p1p1p/1c5c1/9/rnbakabnr'
        train_file = train_dir + file_name
        train_data = read_png(train_file)
        result = (train_data['result'])
        if '1-0' in result or u'红胜' in result or u'黑负' in result:
            winner = 'w'
        elif '0-1' in result or u'黑胜' in result or u'红负' in result:
            winner = 'b'
        else:
            winner = 'tie'
        steps = (train_data['data'])
        try:
            states, mcts_probs, winner_z = [], [], []
            for step in steps:
                step = step.split('.')[1].split(' ')
                if len(step) == 1:
                    input_state = state
                    w_step = step[0]
                    side = 'w'
                    # print("%s %s" % (w_step, side))
                    if side == 'w':
                        cur_player = 'b'
                    else:
                        cur_player = 'w'
                    legal_moves = (GameBoard.get_legal_moves(state, cur_player))
                    legal_moves_id = []
                    for each in legal_moves:
                        legal_moves_id.append(label2id[each])
                    # print(legal_moves_id)
                    pos = get_chess_pos(state, w_step, side)
                    pos_id = label2id[pos]
                    # print(label2id[pos])
                    state = sim_do_action(pos, state)
                    move_probs = np.zeros(2086)
                    move_probs[pos_id] = 0.5
                    other_prob = 0.5 / len(legal_moves_id)
                    for each in legal_moves_id:
                        move_probs[each] = other_prob
                    if winner == 'w':
                        leaf_value = 1.0
                    elif winner == 'b':
                        leaf_value = -1.0
                    else:
                        leaf_value = 0
                    states.append(input_state)
                    mcts_probs.append(move_probs)
                    winner_z.append(leaf_value)
                  
                elif len(step) == 2:
                    input_state = state
                    # print(state)
                    # print_board(state)
                    w_step = step[0]
                    side = 'w'
                    if side == 'w':
                        cur_player = 'b'
                    else:
                        cur_player = 'w'
                    # print("%s %s" % (w_step, side))
                    legal_moves = (GameBoard.get_legal_moves(state, cur_player))
                    legal_moves_id = []
                    for each in legal_moves:
                        legal_moves_id.append(label2id[each])
                    # print(legal_moves_id)
                    pos = get_chess_pos(state, w_step, side)
                    pos_id = label2id[pos]
                    # print(label2id[pos])
                    state = sim_do_action(pos, state)
                    move_probs = np.zeros(2086)
                    move_probs[pos_id] = 0.5
                    other_prob = 0.5 / len(legal_moves_id)
                    for each in legal_moves_id:
                        move_probs[each] = other_prob
                    if winner == 'w':
                        leaf_value = 1.0
                    elif winner == 'b':
                        leaf_value = -1.0
                    else:
                        leaf_value = 0
                    states.append(input_state)
                    mcts_probs.append(move_probs)
                    winner_z.append(leaf_value)

                    input_state = state
                    # print_board(state)
                    b_step = step[1]
                    side = 'b'
                    if side == 'w':
                        cur_player = 'b'
                    else:
                        cur_player = 'w'
                    # print("%s %s" % (b_step, side))
                    legal_moves = (GameBoard.get_legal_moves(state, cur_player))
                    legal_moves_id = []
                    for each in legal_moves:
                        legal_moves_id.append(label2id[each])
                    # print(legal_moves_id)
                    pos = get_chess_pos(state, b_step, side)
                    pos_id = label2id[pos]
                    # print(label2id[pos])
                    state = sim_do_action(pos, state)
                    move_probs = np.zeros(2086)
                    move_probs[pos_id] = 0.5
                    other_prob = 0.5 / len(legal_moves_id)
                    for each in legal_moves_id:
                        move_probs[each] = other_prob
                    if winner == 'w':
                        leaf_value = -1.0
                    elif winner == 'b':
                        leaf_value = 1.0
                    else:
                        leaf_value = 0
                    states.append(input_state)
                    mcts_probs.append(move_probs)
                    winner_z.append(leaf_value)
            play_data = zip(states, mcts_probs, winner_z)
            out_put = {}
            out_put['play_data'] = play_data
            out_put['winner'] = winner
            import datetime
            now = datetime.datetime.now()
            train_data_file = now.strftime("%Y%m%d%H%M%S")
            f = open(os.getcwd() + '/train_data/' +str(train_data_file), 'w')
            pickle.dump(out_put, f)
        except Exception as E:
            f.write(file_name + '\n')
            # raise E
    f.close()

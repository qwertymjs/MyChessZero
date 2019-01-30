# -*- coding: utf-8 -*-
import numpy as np
from ChessBoard import *
from ChessView import ChessView
import time

pieces_order = 'KARBNPCkarbnpc' # 9 x 10 x 14
ind = {pieces_order[i]: i for i in range(14)}

# 翻转UCI
def flipped_uci_labels(param):
    def repl(x):
        return "".join([(str(9 - int(a)) if a.isdigit() else a) for a in x])
    return [repl(x) for x in param]

# 创建所有合法走子UCI，size 2086
def create_uci_labels():
    labels_array = []
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    Advisor_labels = ['d7e8', 'e8d7', 'e8f9', 'f9e8', 'd0e1', 'e1d0', 'e1f2', 'f2e1',
                      'd2e1', 'e1d2', 'e1f0', 'f0e1', 'd9e8', 'e8d9', 'e8f7', 'f7e8']
    Bishop_labels = ['a2c4', 'c4a2', 'c0e2', 'e2c0', 'e2g4', 'g4e2', 'g0i2', 'i2g0',
                     'a7c9', 'c9a7', 'c5e7', 'e7c5', 'e7g9', 'g9e7', 'g5i7', 'i7g5',
                     'a2c0', 'c0a2', 'c4e2', 'e2c4', 'e2g0', 'g0e2', 'g4i2', 'i2g4',
                     'a7c5', 'c5a7', 'c9e7', 'e7c9', 'e7g5', 'g5e7', 'g9i7', 'i7g9']

    for l1 in range(9):
        for n1 in range(10):
            destinations = [(t, n1) for t in range(9)] + \
                           [(l1, t) for t in range(10)] + \
                           [(l1 + a, n1 + b) for (a, b) in
                            [(-2, -1), (-1, -2), (-2, 1), (1, -2), (2, -1), (-1, 2), (2, 1), (1, 2)]]  # 马走日
            for (l2, n2) in destinations:
                if (l1, n1) != (l2, n2) and l2 in range(9) and n2 in range(10):
                    move = letters[l1] + numbers[n1] + letters[l2] + numbers[n2]
                    labels_array.append(move)

    for p in Advisor_labels:
        labels_array.append(p)

    for p in Bishop_labels:
        labels_array.append(p)

    return labels_array

labels_array = create_uci_labels()
labels_len = len(labels_array)
flipped_labels = flipped_uci_labels(labels_array)
unflipped_index = [labels_array.index(x) for x in flipped_labels]

id2label = {i: val for i, val in enumerate(labels_array)}
label2id = {val: i for i, val in enumerate(labels_array)}


def get_pieces_count(state):
    count = 0
    for s in state:
        if s.isalpha():
            count += 1
    return count

def is_kill_move(state_prev, state_next):
    return get_pieces_count(state_prev) - get_pieces_count(state_next)

def create_position_labels():
    labels_array = []
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    letters.reverse()
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for l1 in range(9):
        for n1 in range(10):
            move = letters[8 - l1] + numbers[n1]
            labels_array.append(move)
    return labels_array

def create_position_labels_reverse():
    labels_array = []
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    letters.reverse()
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for l1 in range(9):
        for n1 in range(10):
            move = letters[l1] + numbers[n1]
            labels_array.append(move)
    labels_array.reverse()
    return labels_array

class GameBoard(object):
    board_pos_name = np.array(create_position_labels()).reshape(9,10).transpose()
    Ny = 10
    Nx = 9

    def __init__(self):
        self.state = "RNBAKABNR/9/1C5C1/P1P1P1P1P/9/9/p1p1p1p1p/1c5c1/9/rnbakabnr"#"rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR"    #
        self.round = 1
        self.current_player = "w"
        self.restrict_round = 0      

    def reload(self):
        self.state = "RNBAKABNR/9/1C5C1/P1P1P1P1P/9/9/p1p1p1p1p/1c5c1/9/rnbakabnr"#"rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR"    #
        self.round = 1
        self.current_player = "w"
        self.restrict_round = 0

    @staticmethod
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
        print("  abcdefghi")
        for i,line in enumerate(board):
            if (action != None):
                if(i == src_y):
                    s = list(line)
                    s[src_x] = 'x'
                    line = ''.join(s)
            print(i,line)

    @staticmethod
    def sim_do_action(in_action, in_state):
        x_trans = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8}

        src = in_action[0:2]
        dst = in_action[2:4]

        src_x = int(x_trans[src[0]])
        src_y = int(src[1])

        dst_x = int(x_trans[dst[0]])
        dst_y = int(dst[1])

        board_positions = GameBoard.board_to_pos_name(in_state)
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

    @staticmethod
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

    @staticmethod
    def check_bounds(toY, toX):
        if toY < 0 or toX < 0:
            return False

        if toY >= GameBoard.Ny or toX >= GameBoard.Nx:
            return False

        return True

    @staticmethod
    def validate_move(c, upper=True):
        if (c.isalpha()):
            if (upper == True):
                if (c.islower()):
                    return True
                else:
                    return False
            else:
                if (c.isupper()):
                    return True
                else:
                    return False
        else:
            return True

    @staticmethod
    def get_legal_moves(state, current_player):
        moves = []
        k_x = None
        k_y = None

        K_x = None
        K_y = None

        face_to_face = False

        board_positions = np.array(GameBoard.board_to_pos_name(state))
        for y in range(board_positions.shape[0]):
            for x in range(len(board_positions[y])):
                if(board_positions[y][x].isalpha()):
                    if(board_positions[y][x] == 'r' and current_player == 'b'):
                        toY = y
                        for toX in range(x - 1, -1, -1):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (board_positions[toY][toX].isalpha()):
                                if (board_positions[toY][toX].isupper()):
                                    moves.append(m)
                                break

                            moves.append(m)

                        for toX in range(x + 1, GameBoard.Nx):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (board_positions[toY][toX].isalpha()):
                                if (board_positions[toY][toX].isupper()):
                                    moves.append(m)
                                break

                            moves.append(m)

                        toX = x
                        for toY in range(y - 1, -1, -1):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (board_positions[toY][toX].isalpha()):
                                if (board_positions[toY][toX].isupper()):
                                    moves.append(m)
                                break

                            moves.append(m)

                        for toY in range(y + 1, GameBoard.Ny):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (board_positions[toY][toX].isalpha()):
                                if (board_positions[toY][toX].isupper()):
                                    moves.append(m)
                                break

                            moves.append(m)

                    elif(board_positions[y][x] == 'R' and current_player == 'w'):
                        toY = y
                        for toX in range(x - 1, -1, -1):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (board_positions[toY][toX].isalpha()):
                                if (board_positions[toY][toX].islower()):
                                    moves.append(m)
                                break

                            moves.append(m)

                        for toX in range(x + 1, GameBoard.Nx):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (board_positions[toY][toX].isalpha()):
                                if (board_positions[toY][toX].islower()):
                                    moves.append(m)
                                break

                            moves.append(m)

                        toX = x
                        for toY in range(y - 1, -1, -1):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (board_positions[toY][toX].isalpha()):
                                if (board_positions[toY][toX].islower()):
                                    moves.append(m)
                                break

                            moves.append(m)

                        for toY in range(y + 1, GameBoard.Ny):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (board_positions[toY][toX].isalpha()):
                                if (board_positions[toY][toX].islower()):
                                    moves.append(m)
                                break

                            moves.append(m)

                    elif ((board_positions[y][x] == 'n' or board_positions[y][x] == 'h') and current_player == 'b'):
                        for i in range(-1, 3, 2):
                            for j in range(-1, 3, 2):
                                toY = y + 2 * i
                                toX = x + 1 * j
                                if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX], upper=False) and board_positions[toY - i][x].isalpha() == False:
                                    moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                                toY = y + 1 * i
                                toX = x + 2 * j
                                if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX], upper=False) and board_positions[y][toX - j].isalpha() == False:
                                    moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                    elif ((board_positions[y][x] == 'N' or board_positions[y][x] == 'H') and current_player == 'w'):
                        for i in range(-1, 3, 2):
                            for j in range(-1, 3, 2):
                                toY = y + 2 * i
                                toX = x + 1 * j
                                if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX], upper=True) and board_positions[toY - i][x].isalpha() == False:
                                    moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                                toY = y + 1 * i
                                toX = x + 2 * j
                                if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX], upper=True) and board_positions[y][toX - j].isalpha() == False:
                                    moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                    elif ((board_positions[y][x] == 'b' or board_positions[y][x] == 'e') and current_player == 'b'):
                        for i in range(-2, 3, 4):
                            toY = y + i
                            toX = x + i

                            if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX],
                                                                        upper=False) and toY >= 5 and \
                                            board_positions[y + i // 2][x + i // 2].isalpha() == False:
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                            toY = y + i
                            toX = x - i

                            if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX],
                                                                        upper=False) and toY >= 5 and \
                                            board_positions[y + i // 2][x - i // 2].isalpha() == False:
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                    elif ((board_positions[y][x] == 'B' or board_positions[y][x] == 'E') and current_player == 'w'):
                        for i in range(-2, 3, 4):
                            toY = y + i
                            toX = x + i

                            if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX],
                                                                        upper=True) and toY <= 4 and \
                                            board_positions[y + i // 2][x + i // 2].isalpha() == False:
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                            toY = y + i
                            toX = x - i

                            if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX],
                                                                        upper=True) and toY <= 4 and \
                                            board_positions[y + i // 2][x - i // 2].isalpha() == False:
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                    elif (board_positions[y][x] == 'a' and current_player == 'b'):
                        for i in range(-1, 3, 2):
                            toY = y + i
                            toX = x + i

                            if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX],
                                                                        upper=False) and toY >= 7 and toX >= 3 and toX <= 5:
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])

                            toY = y + i
                            toX = x - i

                            if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX],
                                                                        upper=False) and toY >= 7 and toX >= 3 and toX <= 5:
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                    elif (board_positions[y][x] == 'A' and current_player == 'w'):
                        for i in range(-1, 3, 2):
                            toY = y + i
                            toX = x + i

                            if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX],
                                                                        upper=True) and toY <= 2 and toX >= 3 and toX <= 5:
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])

                            toY = y + i
                            toX = x - i

                            if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX],
                                                                        upper=True) and toY <= 2 and toX >= 3 and toX <= 5:
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                    elif (board_positions[y][x] == 'k'):
                        k_x = x
                        k_y = y

                        if(current_player == 'b'):
                            for i in range(2):
                                for sign in range(-1, 2, 2):
                                    j = 1 - i
                                    toY = y + i * sign
                                    toX = x + j * sign

                                    if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX],
                                                                                upper=False) and toY >= 7 and toX >= 3 and toX <= 5:
                                        moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                    elif (board_positions[y][x] == 'K'):
                        K_x = x
                        K_y = y

                        if(current_player == 'w'):
                            for i in range(2):
                                for sign in range(-1, 2, 2):
                                    j = 1 - i
                                    toY = y + i * sign
                                    toX = x + j * sign

                                    if GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX],
                                                                                upper=True) and toY <= 2 and toX >= 3 and toX <= 5:
                                        moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])
                    elif (board_positions[y][x] == 'c' and current_player == 'b'):
                        toY = y
                        hits = False
                        for toX in range(x - 1, -1, -1):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (hits == False):
                                if (board_positions[toY][toX].isalpha()):
                                    hits = True
                                else:
                                    moves.append(m)
                            else:
                                if (board_positions[toY][toX].isalpha()):
                                    if (board_positions[toY][toX].isupper()):
                                        moves.append(m)
                                    break

                        hits = False
                        for toX in range(x + 1, GameBoard.Nx):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (hits == False):
                                if (board_positions[toY][toX].isalpha()):
                                    hits = True
                                else:
                                    moves.append(m)
                            else:
                                if (board_positions[toY][toX].isalpha()):
                                    if (board_positions[toY][toX].isupper()):
                                        moves.append(m)
                                    break

                        toX = x
                        hits = False
                        for toY in range(y - 1, -1, -1):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (hits == False):
                                if (board_positions[toY][toX].isalpha()):
                                    hits = True
                                else:
                                    moves.append(m)
                            else:
                                if (board_positions[toY][toX].isalpha()):
                                    if (board_positions[toY][toX].isupper()):
                                        moves.append(m)
                                    break

                        hits = False
                        for toY in range(y + 1, GameBoard.Ny):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (hits == False):
                                if (board_positions[toY][toX].isalpha()):
                                    hits = True
                                else:
                                    moves.append(m)
                            else:
                                if (board_positions[toY][toX].isalpha()):
                                    if (board_positions[toY][toX].isupper()):
                                        moves.append(m)
                                    break
                    elif (board_positions[y][x] == 'C' and current_player == 'w'):
                        toY = y
                        hits = False
                        for toX in range(x - 1, -1, -1):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (hits == False):
                                if (board_positions[toY][toX].isalpha()):
                                    hits = True
                                else:
                                    moves.append(m)
                            else:
                                if (board_positions[toY][toX].isalpha()):
                                    if (board_positions[toY][toX].islower()):
                                        moves.append(m)
                                    break

                        hits = False
                        for toX in range(x + 1, GameBoard.Nx):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (hits == False):
                                if (board_positions[toY][toX].isalpha()):
                                    hits = True
                                else:
                                    moves.append(m)
                            else:
                                if (board_positions[toY][toX].isalpha()):
                                    if (board_positions[toY][toX].islower()):
                                        moves.append(m)
                                    break

                        toX = x
                        hits = False
                        for toY in range(y - 1, -1, -1):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (hits == False):
                                if (board_positions[toY][toX].isalpha()):
                                    hits = True
                                else:
                                    moves.append(m)
                            else:
                                if (board_positions[toY][toX].isalpha()):
                                    if (board_positions[toY][toX].islower()):
                                        moves.append(m)
                                    break

                        hits = False
                        for toY in range(y + 1, GameBoard.Ny):
                            m = GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX]
                            if (hits == False):
                                if (board_positions[toY][toX].isalpha()):
                                    hits = True
                                else:
                                    moves.append(m)
                            else:
                                if (board_positions[toY][toX].isalpha()):
                                    if (board_positions[toY][toX].islower()):
                                        moves.append(m)
                                    break
                    elif (board_positions[y][x] == 'p' and current_player == 'b'):
                        toY = y - 1
                        toX = x

                        if (GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX], upper=False)):
                            moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])

                        if y < 5:
                            toY = y
                            toX = x + 1
                            if (GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX], upper=False)):
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])

                            toX = x - 1
                            if (GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX], upper=False)):
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])

                    elif (board_positions[y][x] == 'P' and current_player == 'w'):
                        toY = y + 1
                        toX = x

                        if (GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX], upper=True)):
                            moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])

                        if y > 4:
                            toY = y
                            toX = x + 1
                            if (GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX], upper=True)):
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])

                            toX = x - 1
                            if (GameBoard.check_bounds(toY, toX) and GameBoard.validate_move(board_positions[toY][toX], upper=True)):
                                moves.append(GameBoard.board_pos_name[y][x] + GameBoard.board_pos_name[toY][toX])

        if(K_x != None and k_x != None and K_x == k_x):
            face_to_face = True
            for i in range(K_y + 1, k_y, 1):
                if(board_positions[i][K_x].isalpha()):
                    face_to_face = False

        if(face_to_face == True):
            if(current_player == 'b'):
                moves.append(GameBoard.board_pos_name[k_y][k_x] + GameBoard.board_pos_name[K_y][K_x])
            else:
                moves.append(GameBoard.board_pos_name[K_y][K_x] + GameBoard.board_pos_name[k_y][k_x])
        return moves

class GameState(object):
    def __init__(self, enable_record_im=False):
        self.statestr = 'RNBAKABNR/9/1C5C1/P1P1P1P1P/9/9/p1p1p1p1p/1c5c1/9/rnbakabnr'
        self.currentplayer = 'w'
        self.ys = '9876543210'[::-1]
        self.xs = 'abcdefghi'
        self.pastdic = {}
        self.maxrepeat = 0
        self.lastmove = ""
        self.move_number = 0
        self.enable_record_im = enable_record_im
        self.board = ChessBoard()
        self.view = ChessView(board=self.board)
        self.restrict_round = 0
        self.tie_num = 75
        
    def is_check_catch(self):
        moveset = GameBoard.get_legal_moves(self.statestr,self.get_next_player())
        targetset = set([i[-2:] for i in moveset])
        
        wk,bk = self.get_king_pos()
        targetkingdic = {'b':wk,'w':bk}
        targ_king = targetkingdic[self.get_next_player()]
        # TODO add long catch logic
        if targ_king in targetset:
            return True
        else:
            return False
        
    def get_king_pos(self):
        board = self.statestr.replace("1", " ")
        board = board.replace("2", "  ")
        board = board.replace("3", "   ")
        board = board.replace("4", "    ")
        board = board.replace("5", "     ")
        board = board.replace("6", "      ")
        board = board.replace("7", "       ")
        board = board.replace("8", "        ")
        board = board.replace("9", "         ")
        board = board.split('/')
        for i in range(3):
            pos = board[i].find('K')
            if pos != -1:
                K = "{}{}".format(self.xs[pos],self.ys[i])
        for i in range(-1,-4,-1):
            pos = board[i].find('k')
            if pos != -1:
                k = "{}{}".format(self.xs[pos],self.ys[i])
        return K,k
            
    def game_end(self):
        if self.restrict_round > self.tie_num:
            return True, -1 # tie
        if self.statestr.find('k') == -1:
            return True,'w'
        elif self.statestr.find('K') == -1:
            return True,'b'
        wk, bk = self.get_king_pos()
        targetkingdic = {'b':wk,'w':bk}
        moveset = GameBoard.get_legal_moves(self.statestr,self.get_current_player())
        targetset = set([i[-2:] for i in moveset])
        targ_king = targetkingdic[self.currentplayer]
        if targ_king in targetset:
            return True,self.currentplayer
        return False,None
    
    def get_current_player(self):
        return self.currentplayer
    
    def get_next_player(self):
        if self.currentplayer == 'w':
            return 'b'
        elif self.currentplayer == 'b':
            return 'w'
    
    def do_move(self, move, is_show_gui=0, disp_data=None):
        self.lastmove = move
        state_pre = self.statestr
        self.statestr = GameBoard.sim_do_action(move, self.statestr)
        if self.currentplayer == 'w':
            self.currentplayer = 'b'
        elif self.currentplayer == 'b':
            self.currentplayer = 'w'
        self.pastdic.setdefault(self.statestr,[0,False,self.get_next_player()]) # times, longcatch/check
        self.pastdic[self.statestr][0] += 1
        self.maxrepeat = self.pastdic[self.statestr][0]
        if self.enable_record_im:
            self.pastdic[self.statestr][1] = self.is_check_catch()
        self.move_number += 1
        if self.is_kill_move(state_pre, self.statestr) == 0:
            self.restrict_round += 1
        else:
            self.restrict_round = 0
        if is_show_gui == 1:
            # GameBoard.print_board(self.statestr)
            self.view.update(move, disp_data)

    def get_pieces_count(self, state):
        count = 0
        for s in state:
            if s.isalpha():
                count += 1
        return count

    def is_kill_move(self, state_prev, state_next):
        return self.get_pieces_count(state_prev) - self.get_pieces_count(state_next)

    def should_cutoff(self):
        # the pastdic is empty when first move was made
        if self.move_number < 2:
            return False
        state_appear_num = self.pastdic[self.statestr][0]
        if state_appear_num > 1 and self.is_check_catch():
            if conf.verbose:
                print("find something to cut off")
            return True
        else:
            return False

    def get_legal_move_label(self):
        legal_moves = GameBoard.get_legal_moves(self.statestr, self.get_next_player())
        return legal_moves
    
    def get_legal_move_id(self):
        id_set = []
        legal_moves = GameBoard.get_legal_moves(self.statestr, self.get_next_player())
        for each in legal_moves:
            id_set.append(label2id[each])
        return id_set

    def get_move_label_id(self, move_id):
        return id2label[move_id]

    def current_state(self):
        state, palyer = self.try_flip(self.statestr, self.get_next_player(), self.is_black_turn(self.get_next_player()))
        return self.state_to_positions(state)

    def flip_policy(self, prob):
        prob = prob.flatten()
        return np.asarray([prob[ind] for ind in unflipped_index])

    def replace_board_tags(self, board):
        board = board.replace("2", "11")
        board = board.replace("3", "111")
        board = board.replace("4", "1111")
        board = board.replace("5", "11111")
        board = board.replace("6", "111111")
        board = board.replace("7", "1111111")
        board = board.replace("8", "11111111")
        board = board.replace("9", "111111111")
        return board.replace("/", "")

    # 感觉位置有点反了，当前角色的棋子在右侧，plane的后面
    def state_to_positions(self, state):
        # TODO C plain x 2
        board_state = self.replace_board_tags(state)
        pieces_plane = np.zeros(shape=(9, 10, 14))
        for rank in range(9):    #横线
            for file in range(10):    #直线
                v = board_state[rank * 9 + file]
                if v.isalpha():
                    pieces_plane[rank][file][ind[v]] = 1
        assert pieces_plane.shape == (9, 10, 14)
        return pieces_plane

    def try_flip(self, state, current_player, flip=False):
        if not flip:
            return state, current_player

        rows = state.split('/')

        def swapcase(a):
            if a.isalpha():
                return a.lower() if a.isupper() else a.upper()
            return a

        def swapall(aa):
            return "".join([swapcase(a) for a in aa])

        return "/".join([swapall(row) for row in reversed(rows)]),  ('w' if current_player == 'b' else 'b')

    def is_black_turn(self, current_player):
        return current_player == 'b'

def start_game_play(player, temp=1e-3, is_shown=1):
        game_state = GameState()
        states, mcts_probs, current_players = [], [], []
        while True:
            start = time.time()
            move, move_probs, win_rate = player.get_action(game_state, temp=temp, return_prob=1)
            mcts_time = time.time() - start
            print('mcts time {}'.format(mcts_time))
            print('restrict_round {}'.format(game_state.restrict_round))
            print('move_number {}'.format(game_state.move_number))
            # store the data
            states.append(game_state.statestr)
            GameBoard.print_board(game_state.statestr)
            mcts_probs.append(move_probs)
            current_players.append(game_state.get_current_player())
            # perform a move
            disp_data = {}
            disp_data['mcts_time'] = mcts_time
            disp_data['move_number'] = game_state.move_number
            disp_data['win_rate'] = win_rate
            game_state.do_move(move, 1, disp_data)
            end, winner = game_state.game_end()
            if end:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                    # 当局胜利为1，失败为-1，平局为0
                    # 这个分数代表的reward
                # reset MCTS root node
                player.reset_player()
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player:", winner)
                    else:
                        print("Game end. Tie")
                return winner, zip(states, mcts_probs, winners_z)  # 返回当前的状态空间S，转移概率矩阵d，奖励R
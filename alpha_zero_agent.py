import Arena
from MCTS import MCTS
from othello.OthelloGame import OthelloGame
from othello.OthelloPlayers import *
from othello.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from utils import *





class AlphaZeroAgent:
    def __init__(self, side):
        """
        --------------------------------------------------------
        #### 物件 : 電腦
        --------------------------------------------------------
        #### 函式
        - isOnCorner() : 根據輸入的位置判斷是否在棋盤的角落
        - isOnBorder() : 根據輸入的位置判斷是否在棋盤的邊緣
        - choose() : 選擇下一步的位置
        --------------------------------------------------------
        #### 傳入的參數
        - side : 此電腦拿的棋子顏色 (以字串型態表示 : "black"或"white")
        --------------------------------------------------------
        #### 物件中的屬性
        - side : 此電腦拿的棋子顏色
        - name : 此物件的名稱，因為是電腦所以命名成"agent"
        - opponentSide : 對手的棋子顏色
        --------------------------------------------------------
        """
        self.side = side
        self.name = "agent"
        self.opponentSide = "black" if self.side == "white" else "white"
        self.g = OthelloGame(8)
        n1 = NNet(self.g)
        n1.load_checkpoint('./pretrained_models/othello/pytorch/','8x8_100checkpoints_best.pth.tar')
        args1 = dotdict({'numMCTSSims': 250, 'cpuct':1.0})
        self.mcts1 = MCTS(self.g, n1, args1)

    def convert_board(self, board):
        res = np.zeros((8, 8))
        for i in range(8):
            for j in range(8):
                if board[i][j] == "black":
                    res[i][j] = 1
                elif board[i][j] == "white":
                    res[i][j] = -1
        
        res = self.g.getCanonicalForm(res, (1 if self.side == "black" else -1))
        return res
    
    def choose(self, board, valid_moves):
        """
        --------------------------------------------------------
        #### 功能 : 選擇下一步的位置 (最白癡的greedy演算法)
        --------------------------------------------------------
        #### 參數
        - board : 棋盤
        - valid_moves : 目前可以下的位置 (資料型態 : 陣列)
        --------------------------------------------------------
        #### 回傳值
        - 含有兩個元素的陣列，表示最後選擇的位置 ; 若沒有選擇, 回傳None
        --------------------------------------------------------
        """
        action = np.argmax(self.mcts1.getActionProb(self.convert_board(board), temp=0))
        return [action // 8, action % 8] if action != 64 else None

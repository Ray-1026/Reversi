from agent import Agent
import pygame


class PlayerAgent(Agent):
    def __init__(self, side):
        """
        物件 : 玩家

        函式 :
        - isOnCorner() :
        - isOnBorder() :
        - choose() :
        --------------------------------------------------------
        #### Input
        - side : 玩家拿的棋子顏色 (以字串型態表示 : "black"或"white")
        --------------------------------------------------------
        #### Init
        - side : 玩家拿的棋子顏色
        - name : 玩家名稱, 在此處皆命名成"human"
        - opponentSide : 對手的棋子顏色
        --------------------------------------------------------
        """
        super().__init__(side)
        self.name = "human"

    def choose(self, board, valid_moves):
        ########################################################
        # - board: the status of the tiles in the current board
        # ------------------------------------------------------
        # - return false if no possible move left, otherwise
        # - return the best move with greedy algorithm
        #######################################################
        x, y = pygame.mouse.get_pos()
        col, row = int((x - 20) / 50), int((y - 20) / 50)
        if [col, row] in valid_moves:
            return [col, row]

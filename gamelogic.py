import pygame
import utils
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from board import Board


class GameLogic:
    def __init__(self, agent1, agent2, screen):
        """
        --------------------------------------------------------
        #### 物件 : 遊戲邏輯
        --------------------------------------------------------
        #### 函式
        - run() : 雙方開始對戰直到分出勝負
        --------------------------------------------------------
        #### Input
        - agent1 : 玩家1號
        - agent2 : 玩家2號
        - screen : 遊戲視窗
        --------------------------------------------------------
        #### Init
        - agent1 : 玩家1號
        - agent2 : 玩家2號
        - board : 遊戲畫面
        - screen : 遊戲視窗
        - last_move : 上一次下的位置
        - direct : 八個方位 (上、下、左、右、左上、左下、右上、右下)
        --------------------------------------------------------
        """

        self.agent1 = agent1
        self.agent2 = agent2
        self.board = Board()
        self.screen = screen
        self.last_move = None
        self.direct = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    def run(self, screen, main_clock):
        """
        --------------------------------------------------------
        #### 功能 : 雙方開始對戰直到分出勝負
        --------------------------------------------------------
        #### 參數
        - screen : 遊戲視窗
        - main_clock : 控制遊戲幀數
        --------------------------------------------------------
        #### 回傳值
        - 無
        --------------------------------------------------------
        """
        self.cur_agent = self.agent1 if self.agent1.side == "black" else self.agent2
        while not utils.noMoreMove(self.board.board):
            pos = []
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif self.cur_agent.name == "human" and event.type == MOUSEBUTTONDOWN:
                    pos = self.cur_agent.choose(self.board.board, utils.getValidMoves(self.board.board, self.cur_agent.side))

            if self.cur_agent.name == "agent":
                pos = self.cur_agent.choose(self.board.board, utils.getValidMoves(self.board.board, self.cur_agent.side))

            if pos or self.cur_agent.name == "agent":
                if utils.isValidMove(self.board.board, self.cur_agent.side, pos[0], pos[1]):
                    utils.flip(self.board.board, self.cur_agent.side, pos[0], pos[1])
                    self.last_move = [pos[0], pos[1]]

                if utils.getValidMoves(self.board.board, self.cur_agent.opponentSide):
                    self.cur_agent = self.agent2 if self.cur_agent == self.agent1 else self.agent1

            self.board.draw(screen, "run", self)

            pygame.display.update()
            main_clock.tick(60)

        pygame.time.delay(1000)  # 停留在結果畫面1秒

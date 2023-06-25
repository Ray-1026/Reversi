import pygame
import utils
import sys
import pickle
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from board import Board

from client import send_move

class GameLogic:
    def __init__(self, agent1, agent2, screen, sock=None, username=None):
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
        #### 物件中的屬性
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
        self.sock = sock
        self.username = username
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
        self.cur_agent = self.agent1 if self.agent1.side == "black" else self.agent2  # 紀錄目前輪到哪個玩家
        while not utils.noMoreMove(self.board.board): # 當還有位置下
            pos = None  # 下棋的位置
            # print(self.cur_agent.side, self.cur_agent.name)
            # 事件監聽
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif self.cur_agent.name == "human" and event.type == MOUSEBUTTONDOWN:  # 如果目前輪到玩家且按下滑鼠左鍵
                    pos = self.cur_agent.choose(self.board.board, utils.getValidMoves(self.board.board, self.cur_agent.side))

            # 如果目前輪到電腦，直接呼叫choose()函式決定下的位置
            if self.cur_agent.name == "agent":
                pos = self.cur_agent.choose(self.board.board, utils.getValidMoves(self.board.board, self.cur_agent.side))
            elif self.cur_agent.name == "remote":
                pos = self.cur_agent.choose(self.sock)
        
            if pos:
                if utils.isValidMove(self.board.board, self.cur_agent.side, pos[0], pos[1]):  # 如果pos的位置可以下
                    utils.flip(self.board.board, self.cur_agent.side, pos[0], pos[1])  # 翻轉棋子
                    self.last_move = [pos[0], pos[1]]  # 更新last_move
                    if self.sock is not None and self.cur_agent.name != "remote":
                        send_move(self.sock, pos, self.username)

                # 判斷下回合是否要交換玩家
                if utils.getValidMoves(self.board.board, self.cur_agent.opponentSide):
                    self.cur_agent = self.agent2 if self.cur_agent == self.agent1 else self.agent1

            self.board.draw(screen, "run", self)

            pygame.display.update()
            main_clock.tick(60)

        pygame.time.delay(1000)  # 停留在結果畫面1秒

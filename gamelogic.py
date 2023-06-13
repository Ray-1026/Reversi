import pygame
import utils
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from board import Board

class GameLogic:
    #宣告
    def __init__(self, agent1, agent2, screen):
        ########################################################
        # - player_first: whether player move first
        # - pvc: whether the game is player against computer
        #------------------------------------------------------
        # - opponent: who you are against
        # - mySide: the side of the player1's disk
        # - opponentSide:  the side of the player2's disk
        # - turn: who's turn to play
        # - last_move: the last move of the computer
        # - status: the status of the game
        # - direct: the 8 directions
        ########################################################
        self.agent1 = agent1
        self.agent2 = agent2
        self.board = Board()
        self.screen = screen
        self.last_move = None
        self.direct = [
            [0, 1],
            [1, 1],
            [1, 0],
            [1, -1],
            [0, -1],
            [-1, -1],
            [-1, 0],
            [-1, 1]
        ]

    def run(self, screen, main_clock):
        self.cur_agent = self.agent1
        while not utils.noMoreMove(self.board.board):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            # pygame.time.delay(500)
            pos = self.cur_agent.choose(self.board.board, utils.getValidMoves(self.board.board, self.cur_agent.side))
            if utils.isValidMove(self.board.board, self.cur_agent.side, pos[0], pos[1]):
                utils.flip(self.board.board, self.cur_agent.side, pos[0], pos[1])
                self.last_move = [pos[0], pos[1]]
            
            if utils.getValidMoves(self.board.board, self.cur_agent.opponentSide):
                self.cur_agent = self.agent2 if self.cur_agent == self.agent1 else self.agent1
            
            self.board.drawBoard(screen, 1, self)
            pygame.display.update()
            main_clock.tick(40)
           
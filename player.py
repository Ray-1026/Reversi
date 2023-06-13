from agent import Agent
import pygame

class PlayerAgent(Agent):
    def __init__(self, side):
        super().__init__(side)
        self.name = "human"
    
    def choose(self, board, valid_moves):
        ########################################################
        # - board: the status of the tiles in the current board
        #------------------------------------------------------
        # - return false if no possible move left, otherwise
        # - return the best move with greedy algorithm
        #######################################################
        # possible = self.game.getValidMoves(board, self.game.opponentSide)
        x, y = pygame.mouse.get_pos()
        col, row = int((x - 20) / 50), int((y - 20) / 50)
        if (col, row) in valid_moves:
            return (col, row)
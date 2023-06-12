import random
from gamelogic import GameLogic


class Agent:
    def __init__(self, player_first):
        ########################################################
        # - player_first: whether player move first
        ########################################################
        self.game = GameLogic(player_first)

    def getBoardCopy(self, board):
        ########################################################
        # - board: the status of the tiles in the current board
        ########################################################
        copied = []
        for i in range(8):
            copied.append(["none"] * 8)
        for x in range(8):
            for y in range(8):
                copied[x][y] = board[x][y]
        return copied

    def isOnCorner(self, x, y):
        ########################################################
        # - x: x location of the tile
        # - y: y location of the tile
        #------------------------------------------------------
        # - return whether the tile is on corner
        #######################################################
        return (
            (x == 0 and y == 0) or (x == 0 and y == 7) 
            or (x == 7 and y == 0) or (x == 7 and y == 7)
        )

    def isOnBorder(self, x, y):
        ########################################################
        # - x: x location of the tile
        # - y: y location of the tile
        #------------------------------------------------------
        # - return whether the tile is on border
        #######################################################
        return ( (x >= 0 and x <= 7 and y >= 0 and y <= 7) and
            ((x == 0 ) or (y == 7) or (x == 7) or (y == 0))
        )
    
    def choose(self, board):
        ########################################################
        # - board: the status of the tiles in the current board
        #------------------------------------------------------
        # - return false if no possible move left, otherwise
        # - return the best move with greedy algorithm
        #######################################################
        possible = self.game.getValidMoves(board, self.game.computerSide)
        random.shuffle(possible)

        bestScore = -1
        bestMove = False
        for x, y in possible:
            if self.isOnCorner(x, y):
                return [x, y]
            copyBoard = self.getBoardCopy(board)
            self.game.flip(copyBoard, self.game.computerSide, x, y)
            score = self.game.getScore(copyBoard)[self.game.computerSide]
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score
        return bestMove
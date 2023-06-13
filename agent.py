import random
import utils


class Agent:
    def __init__(self, side):
        """
        物件 : 電腦

        函式 :
        - isOnCorner() :
        - isOnBorder() :
        - choose() :
        --------------------------------------------------------
        #### Input
        - side : 此電腦拿的棋子顏色 (以字串型態表示 : "black"或"white")
        --------------------------------------------------------
        #### Init
        - side : 此電腦拿的棋子顏色
        - name : 此電腦的名稱, 在此處皆命名成"agent"
        - opponentSide : 對手的棋子顏色
        --------------------------------------------------------
        """
        self.side = side
        self.name = "agent"
        self.opponentSide = "black" if self.side == "white" else "white"

    def isOnCorner(self, x, y):
        ########################################################
        # - x: x location of the tile
        # - y: y location of the tile
        # ------------------------------------------------------
        # - return whether the tile is on corner
        #######################################################
        return (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7)

    def isOnBorder(self, x, y):
        ########################################################
        # - x: x location of the tile
        # - y: y location of the tile
        # ------------------------------------------------------
        # - return whether the tile is on border
        #######################################################
        return (x >= 0 and x <= 7 and y >= 0 and y <= 7) and ((x == 0) or (y == 7) or (x == 7) or (y == 0))

    def choose(self, board, valid_moves):
        ########################################################
        # - board: the status of the tiles in the current board
        # ------------------------------------------------------
        # - return false if no possible move left, otherwise
        # - return the best move with greedy algorithm
        #######################################################
        # possible = self.game.getValidMoves(board, self.game.opponentSide)
        random.shuffle(valid_moves)

        bestScore = -1
        bestMove = False
        for x, y in valid_moves:
            if self.isOnCorner(x, y):
                return [x, y]
            copyBoard = utils.getBoardCopy(board)
            utils.flip(copyBoard, self.opponentSide, x, y)
            score = utils.getScore(copyBoard)[self.opponentSide]
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score

        return bestMove

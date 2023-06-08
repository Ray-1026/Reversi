import random
from gamelogic import GameLogic


class Agent:
    def __init__(self, player_first):
        self.game = GameLogic(player_first)

    def getBoardCopy(self, board):
        """
        複製棋盤
        """
        copied = []
        for i in range(8):
            copied.append(["none"] * 8)
        for x in range(8):
            for y in range(8):
                copied[x][y] = board[x][y]
        return copied

    def isOnCorner(self, x, y):
        """
        判斷x, y是否在角落
        """
        return (
            (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7)
        )

    def choose(self, board):
        """
        用最白癡的greedy選擇最佳的走法
        """
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

import random
from gamelogic import GameLogic


class Agent:
    def __init__(self, first):
        self.game = GameLogic(first)

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
    def evaluate(self, board):
        """
        評估函數
        """
        score = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == self.game.computerTile:
                    score += 1
                elif board[x][y] == self.game.playerTile:
                    score -= 1
        return score
    
    def minimax(self, board, depth, maximized, alpha, beta):
        if depth == 0 or self.game.getValidMoves(board, self.game.computerTile) == 0:
            return self.evaluate(board), None
        if maximized:
            val = -100000
            move = None
            for x, y in self.game.getValidMoves(board, self.game.computerTile):
                copyBoard = self.getBoardCopy(board)
                self.game.makeMove(copyBoard, self.game.computerTile, x, y)
                child_score, m = self.minimax(copyBoard, depth-1, False, alpha, beta)
                
                # START YOUR CODE #
                if child_score>val :
                    val=child_score
                    move=m 
                # END YOUR CODE #
                if val>=beta :
                    break
                alpha=max(alpha, val)
            return val, move
        else:
            val = 100000
            move = None
            for x, y in self.game.getValidMoves(board, self.game.playerTile):
                copyBoard = self.getBoardCopy(board)
                self.game.makeMove(copyBoard, self.game.playerTile, x, y)
                child_score, m = self.minimax(copyBoard, depth-1, False, alpha, beta)           
                # START YOUR CODE #s
                if child_score<val :
                    val=child_score
                    move=m
                # END YOUR CODE #
                if val<=alpha :
                    break
                beta=min(beta, val)
            return val, move

    def choose(self, board):
        """
        用最白癡的greedy選擇最佳的走法
        """
        _, bestMove = self.minimax(board, 3, True)
        return bestMove

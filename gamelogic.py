import pygame


class GameLogic:
    def __init__(self, first):
        if first == "player":
            self.playerTile = "black"
            self.computerTile = "white"
            self.turn = "player"
        else:
            self.playerTile = "white"
            self.computerTile = "black"
            self.turn = "computer"

        self.last_move = []
        self.status = 0
        self.direct = [
            [0, 1],
            [1, 1],
            [1, 0],
            [1, -1],
            [0, -1],
            [-1, -1],
            [-1, 0],
            [-1, 1],
        ]

    def isValidMove(self, board, tile, xstart, ystart):
        """
        判斷這一步是否合法，並回傳要被翻轉的棋子
        """
        if not self.isOnBoard(xstart, ystart) or board[xstart][ystart] != "none":
            return False
        board[xstart][ystart] = tile
        otherTile = "white"
        if tile == "white":
            otherTile = "black"
        flip = []
        for xdirect, ydirect in self.direct:
            x, y = xstart + xdirect, ystart + ydirect
            if self.isOnBoard(x, y) and board[x][y] == otherTile:
                x += xdirect
                y += ydirect
                if not self.isOnBoard(x, y):
                    continue
                while board[x][y] == otherTile:
                    x += xdirect
                    y += ydirect
                    if not self.isOnBoard(x, y):
                        break
                if not self.isOnBoard(x, y):
                    continue
                if board[x][y] == tile:
                    while True:
                        x -= xdirect
                        y -= ydirect
                        if x == xstart and y == ystart:
                            break
                        flip.append([x, y])
        board[xstart][ystart] = "none"
        if len(flip) == 0:
            return False
        return flip

    def isOnBoard(self, x, y):
        """
        是否在棋盤的範圍內
        """
        return 7 >= x and x >= 0 and 7 >= y and y >= 0

    def getValidMoves(self, board, tile):
        """
        取得可以下的位置
        """
        valid = []
        for x in range(8):
            for y in range(8):
                if self.isValidMove(board, tile, x, y) != False:
                    valid.append([x, y])
        return valid

    def getScore(self, board):
        """
        計算目前黑白各子的數量
        """
        bscore = 0
        wscore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == "black":
                    bscore += 1
                elif board[x][y] == "white":
                    wscore += 1
        return {"black": bscore, "white": wscore}

    def makeMove(self, board, tile, xstart, ystart):
        """
        下棋
        """
        flip = self.isValidMove(board, tile, xstart, ystart)
        if flip == False:
            return False
        board[xstart][ystart] = tile
        for x, y in flip:
            board[x][y] = tile
        return True

    def PlayerTurn(self, board):
        """
        玩家回合
        """
        if self.status == 1 and self.turn == "player":
            x, y = pygame.mouse.get_pos()
            col, row = int((x - 20) / 50), int((y - 20) / 50)
            if self.makeMove(board, self.playerTile, col, row) == True:
                if self.getValidMoves(board, self.computerTile) != []:
                    self.turn = "computer"
                else:
                    if self.getValidMoves(board, self.playerTile) == []:
                        self.status = 2

    def ComputerTurn(self, board, agent):
        """
        電腦回合
        """
        if self.status == 1 and self.turn == "computer":
            pos = agent.choose(board)
            if pos:
                self.makeMove(board, self.computerTile, pos[0], pos[1])
                self.last_move = [pos[0], pos[1]]
                if self.getValidMoves(board, self.playerTile) != []:
                    self.turn = "player"
            else:
                if self.getValidMoves(board, self.playerTile) != []:
                    self.turn = "player"
                else:
                    self.status = 2

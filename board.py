from gamelogic import pygame


class Board:
    def __init__(self, game):
        self.BACKGROUNDCOLOR = (0, 0, 0)

        self.startImage = pygame.image.load("img/start.jpg")
        self.boardImage = pygame.image.load("img/board.jpg")
        self.boardRect = self.boardImage.get_rect()
        self.blackImage = pygame.image.load("img/black.jpg")
        self.blackRect = self.blackImage.get_rect()
        self.whiteImage = pygame.image.load("img/white.jpg")
        self.whiteRect = self.whiteImage.get_rect()
        self.hintImage = pygame.image.load("img/hint.jpg")
        self.hintRect = self.hintImage.get_rect()

        self.LastMoveImage = pygame.image.load("img/" + game.computerTile + "1.jpg")
        self.LastMoveRect = self.LastMoveImage.get_rect()

        self.board = self.getNewBoard()
        self.resetBoard()

    def resetBoard(self):
        """
        重製棋盤
        """
        for x in range(8):
            for y in range(8):
                self.board[x][y] = "none"
        self.board[3][3] = "black"
        self.board[3][4] = "white"
        self.board[4][3] = "white"
        self.board[4][4] = "black"

    def getNewBoard(self):
        """
        建立新棋盤
        """
        board = []
        for _ in range(8):
            board.append(["none"] * 8)
        return board

    def drawBoard(self, screen, game):
        """
        繪製棋盤
        """
        screen.fill(self.BACKGROUNDCOLOR)
        if game.status == 0:
            screen.blit(self.startImage, self.boardRect, self.boardRect)

        elif game.status == 1:
            screen.blit(self.boardImage, self.boardRect, self.boardRect)
            for x in range(8):
                for y in range(8):
                    rectDst = pygame.Rect(x * 50 + 20, y * 50 + 20, 50, 50)
                    if self.board[x][y] == "black":
                        screen.blit(self.blackImage, rectDst, self.blackRect)
                    elif self.board[x][y] == "white":
                        screen.blit(self.whiteImage, rectDst, self.whiteRect)

            if (
                game.last_move
                and self.board[game.last_move[0]][game.last_move[1]] == game.computerTile
            ):
                x, y = game.last_move[0], game.last_move[1]
                rectDst = pygame.Rect(x * 50 + 20, y * 50 + 20, 50, 50)
                screen.blit(self.LastMoveImage, rectDst, self.LastMoveRect)

            if game.turn == "player":
                hint = game.getValidMoves(self.board, game.playerTile)
                for x, y in hint:
                    rectDst = pygame.Rect(x * 50 + 20, y * 50 + 20, 50, 50)
                    screen.blit(self.hintImage, rectDst, self.hintRect)

        else:
            score = game.getScore(self.board)
            result = "Black  " + str(score["black"]) + "   :   " + str(score["white"]) + "  White"
            if score["black"] > score["white"]:
                winner = "black"
            elif score["black"] < score["white"]:
                winner = "white"
            else:
                winner = "tie"

            if winner == game.playerTile:
                message = "Player Win"
            elif winner == game.computerTile:
                message = "Computer Win"
            else:
                message = "Tie"

            font = pygame.font.SysFont("Arial", 35)
            text1 = font.render(result, True, (255, 255, 255))
            text2 = font.render(message, True, (255, 255, 255))
            screen.blit(text1, text1.get_rect(center=(220, 120)))
            screen.blit(text2, text2.get_rect(center=(220, 200)))

from gamelogic import pygame


class Board:
    def __init__(self, game):
        """
        物件: 棋盤

        功能: \\
        getNewBoard() -> 建立全新的空白棋盤 \\
        resetBoard() -> 重製棋盤，使棋盤上只有黑白各兩子 \\
        drawBoard() -> 繪製遊戲畫面，包括開始、棋盤、結束畫面 
        """

        # 設定背景畫面顏色 (0, 0, 0) = 黑色
        self.BACKGROUNDCOLOR = (0, 0, 0)

        # 讀取和載入圖片
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

        # 初始化棋盤
        self.board = self.getNewBoard()
        self.resetBoard()

    def getNewBoard(self):
        """
        建立全新的空白棋盤
        """
        # 空白的8*8棋盤，"none"表示該位置沒有棋子
        board = []
        for _ in range(8):
            board.append(["none"] * 8)
        return board

    def resetBoard(self):
        """
        重製棋盤，使棋盤上只有黑白各兩子
        """
        # 重製8*8的所有位置
        for x in range(8):
            for y in range(8):
                self.board[x][y] = "none"

        # 在棋盤中間放上黑白各兩子
        self.board[3][3] = "black"
        self.board[3][4] = "white"
        self.board[4][3] = "white"
        self.board[4][4] = "black"

    def drawBoard(self, screen, game):
        """
        繪製遊戲畫面，包括開始、棋盤、結束畫面
        """
        screen.fill(self.BACKGROUNDCOLOR)
        if game.status == 0:
            screen.blit(self.startImage, self.boardRect, self.boardRect)

        elif game.status == 1:
            screen.blit(self.boardImage, self.boardRect, self.boardRect)

            # 根據board判斷8*8的位置是要放白棋、黑棋的圖片，或什麼都不放
            for x in range(8):
                for y in range(8):
                    # 計算圖片該放的位置
                    rectDst = pygame.Rect(x * 50 + 20, y * 50 + 20, 50, 50)
                    # "black"放黑棋的圖片；"white"放白棋的圖片
                    if self.board[x][y] == "black":
                        screen.blit(self.blackImage, rectDst, self.blackRect)
                    elif self.board[x][y] == "white":
                        screen.blit(self.whiteImage, rectDst, self.whiteRect)

            # 判斷電腦的最後一步在哪裡，並標記
            if (
                game.last_move
                and self.board[game.last_move[0]][game.last_move[1]] == game.computerTile
            ):
                x, y = game.last_move[0], game.last_move[1]
                rectDst = pygame.Rect(x * 50 + 20, y * 50 + 20, 50, 50)
                screen.blit(self.LastMoveImage, rectDst, self.LastMoveRect)

            # 如果現在是玩家的回合，給出哪裡可以下的提示
            if game.turn == "player":
                hint = game.getValidMoves(self.board, game.playerTile)
                for x, y in hint:
                    rectDst = pygame.Rect(x * 50 + 20, y * 50 + 20, 50, 50)
                    screen.blit(self.hintImage, rectDst, self.hintRect)

        else:
            # 計算結果
            score = game.getScore(self.board)
            result = "Black  " + str(score["black"]) + "   :   " + str(score["white"]) + "  White"

            # 判斷黑白的輸贏
            if score["black"] > score["white"]:
                winner = "black"
            elif score["black"] < score["white"]:
                winner = "white"
            else:
                winner = "tie"

            # 根據黑白的勝負判斷玩家或電腦誰贏
            if winner == game.playerTile:
                message = "Player Win"
            elif winner == game.computerTile:
                message = "Computer Win"
            else:
                message = "Tie"

            # 印出結果的文字在遊戲畫面上
            font = pygame.font.SysFont("Arial", 35)
            text1 = font.render(result, True, (255, 255, 255))
            text2 = font.render(message, True, (255, 255, 255))
            screen.blit(text1, text1.get_rect(center=(220, 120)))
            screen.blit(text2, text2.get_rect(center=(220, 200)))

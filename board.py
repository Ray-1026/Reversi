from gamelogic import pygame
import utils


class Board:
    def __init__(self):
        """
        --------------------------------------------------------
        #### 物件 : 棋盤
        --------------------------------------------------------
        #### 功能
        - getNewBoard() : 建立全新的空白棋盤
        - resetBoard() : 重製棋盤，使棋盤上只有黑白各兩子
        - drawBoard() : 繪製遊戲畫面，包括開始、棋盤、結束畫面
        --------------------------------------------------------
        #### 傳入的參數
        - 無
        --------------------------------------------------------
        #### 物件中的屬性
        - BACKGROUNDCOLOR : 背景顏色 (黑色)
        - white : 白色
        - startImage : 遊戲起始畫面圖片
        - boardImage : 棋盤圖片
        - blackImage : 黑棋圖片
        - whiteImage : 白棋圖片
        - hintImage : 提示圖片
        - BlackLastMoveImage : 黑棋上一步的提示圖片
        - WhiteLastMoveImage : 白棋上一步的提示圖片
        - boardRect : 棋盤圖片大小
        - cellRect : 棋盤方格大小
        - board : 棋盤
        --------------------------------------------------------
        """

        # 設定顏色
        self.BACKGROUNDCOLOR = (0, 0, 0)  # (0, 0, 0) = 黑色
        self.white = (255, 255, 255)

        # 讀取和載入圖片
        self.startImage = pygame.image.load("img/start.jpg")
        self.boardImage = pygame.image.load("img/board.jpg")
        self.blackImage = pygame.image.load("img/black.jpg")
        self.whiteImage = pygame.image.load("img/white.jpg")
        self.hintImage = pygame.image.load("img/hint.jpg")
        self.BlackLastMoveImage = pygame.image.load("img/black1.jpg")
        self.WhiteLastMoveImage = pygame.image.load("img/white1.jpg")

        # 讀取圖片大小
        self.boardRect = self.boardImage.get_rect()
        self.cellRect = self.whiteImage.get_rect()

        # 初始化棋盤
        self.board = self.getNewBoard()
        self.resetBoard()

    def getNewBoard(self):
        """
        --------------------------------------------------------
        #### 功能 : 建立全新的空白棋盤
        --------------------------------------------------------
        #### 參數
        - 無
        --------------------------------------------------------
        #### 回傳值
        - 8*8的二維陣列, 每一個元素皆為"none"
        --------------------------------------------------------
        """
        # 空白的8*8棋盤，"none"表示該位置沒有棋子
        board = []
        for _ in range(8):
            board.append(["none"] * 8)
        return board

    def resetBoard(self):
        """
        --------------------------------------------------------
        #### 功能 : 重製棋盤，使棋盤上只有黑白各兩子
        --------------------------------------------------------
        #### 參數
        - 無
        --------------------------------------------------------
        #### 回傳值
        - 無
        --------------------------------------------------------
        """
        # 重製8*8的所有位置
        """
        Q4. 巢狀迴圈
        Todo : 為了重製8*8棋盤的所有位置，所以使用巢狀迴圈將self.board中的所有值等於"none"
        Hint : 
        1. 3行程式碼
        2. self.board是一個8*8的二維串列
        """
        # Q4 begin your code here

        # Q4 end your code

        # 在棋盤中間放上黑白各兩子
        self.board[3][3] = "black"
        self.board[3][4] = "white"
        self.board[4][3] = "white"
        self.board[4][4] = "black"

    def draw(self, screen, status, game=None):
        """
        --------------------------------------------------------
        #### 功能 : 繪製遊戲畫面，包括開始、棋盤、結束畫面
        --------------------------------------------------------
        #### 參數
        - screen : 遊戲視窗
        - status : 遊戲狀態
        - game : 遊戲邏輯物件
        --------------------------------------------------------
        #### 回傳值
        - 無
        --------------------------------------------------------
        """
        screen.fill(self.BACKGROUNDCOLOR)
        if status == "start":
            screen.blit(self.startImage, self.boardRect, self.boardRect)

        elif status == "run":
            screen.blit(self.boardImage, self.boardRect, self.boardRect)

            # 根據board判斷8*8的位置是要放白棋、黑棋的圖片，或什麼都不放
            for x in range(8):
                for y in range(8):
                    # 計算圖片位置
                    rectDst = pygame.Rect(x * 50 + 20, y * 50 + 20, 50, 50)
                    # "black"放黑棋的圖片；"white"放白棋的圖片
                    if self.board[x][y] == "black":
                        screen.blit(self.blackImage, rectDst, self.cellRect)
                    elif self.board[x][y] == "white":
                        screen.blit(self.whiteImage, rectDst, self.cellRect)

            # 在last_move的位置畫出上一步的提示圖片
            if game and game.last_move:
                x, y = game.last_move[0], game.last_move[1]
                rectDst = pygame.Rect(x * 50 + 20, y * 50 + 20, 50, 50)
                img = self.BlackLastMoveImage if self.board[x][y] == "black" else self.WhiteLastMoveImage
                screen.blit(img, rectDst, self.cellRect)

            # 如果現在是玩家的回合，給出哪裡可以下的提示
            if game and game.cur_agent.name == "human":
                hint = utils.getValidMoves(self.board, game.cur_agent.side)
                for x, y in hint:
                    rectDst = pygame.Rect(x * 50 + 20, y * 50 + 20, 50, 50)
                    screen.blit(self.hintImage, rectDst, self.cellRect)

        elif status == "end":
            # 計算結果
            score = utils.getScore(game.board.board)
            result = "Black  " + str(score["black"]) + "   :   " + str(score["white"]) + "  White"

            # 判斷黑白的輸贏
            if score["black"] > score["white"]:
                winner = "Black"
            elif score["black"] < score["white"]:
                winner = "White"
            else:
                winner = "tie"

            if winner != "tie":
                message = str(winner) + " Win"
            else:
                message = "Tie"

            # 印出結果的文字在遊戲畫面上
            font = pygame.font.SysFont("Arial", 35)
            text1 = font.render(result, True, self.white)
            text2 = font.render(message, True, self.white)
            screen.blit(text1, text1.get_rect(center=(220, 120)))
            screen.blit(text2, text2.get_rect(center=(220, 200)))

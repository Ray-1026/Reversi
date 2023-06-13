import random
import utils


class Agent:
    def __init__(self, side):
        """
        --------------------------------------------------------
        #### 物件 : 電腦
        --------------------------------------------------------
        #### 函式
        - isOnCorner() : 根據輸入的位置判斷是否在棋盤的角落
        - isOnBorder() : 根據輸入的位置判斷是否在棋盤的邊緣
        - choose() : 選擇下一步的位置
        --------------------------------------------------------
        #### 傳入的參數
        - side : 此電腦拿的棋子顏色 (以字串型態表示 : "black"或"white")
        --------------------------------------------------------
        #### Init
        - side : 此電腦拿的棋子顏色
        - name : 此物件的名稱，因為是電腦所以命名成"agent"
        - opponentSide : 對手的棋子顏色
        --------------------------------------------------------
        """
        self.side = side
        self.name = "agent"
        self.opponentSide = "black" if self.side == "white" else "white"

    def isOnCorner(self, x, y):
        """
        --------------------------------------------------------
        #### 功能 : 根據輸入的位置判斷是否在棋盤的角落
        --------------------------------------------------------
        #### 參數
        - x : 棋盤的x軸座標
        - y : 棋盤的y軸座標
        --------------------------------------------------------
        #### 回傳值
        - True or False :
        --------------------------------------------------------
        """
        return (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7)

    def isOnBorder(self, x, y):
        """
        --------------------------------------------------------
        #### 功能 : 根據輸入的位置判斷是否在棋盤的邊緣
        --------------------------------------------------------
        #### 參數
        - x : 棋盤的x軸座標
        - y : 棋盤的y軸座標
        --------------------------------------------------------
        #### 回傳值
        - True or False :
        --------------------------------------------------------
        """
        return (x >= 0 and x <= 7 and y >= 0 and y <= 7) and ((x == 0) or (y == 7) or (x == 7) or (y == 0))

    def choose(self, board, valid_moves):
        """
        --------------------------------------------------------
        #### 功能 : 選擇下一步的位置
        --------------------------------------------------------
        #### 參數
        - board :
        - valid_moves :
        --------------------------------------------------------
        #### 回傳值
        --------------------------------------------------------
        """
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

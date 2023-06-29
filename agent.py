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
        #### 物件中的屬性
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
        - 如果(x, y)在棋盤角落, 回傳True ; 否則回傳False
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
        - 如果(x, y)在棋盤邊緣, 回傳True ; 否則回傳False
        --------------------------------------------------------
        """
        return (x >= 0 and x <= 7 and y >= 0 and y <= 7) and ((x == 0) or (y == 7) or (x == 7) or (y == 0))

    def choose(self, board, valid_moves):
        """
        --------------------------------------------------------
        #### 功能 : 選擇下一步的位置 (最白癡的greedy演算法)
        --------------------------------------------------------
        #### 參數
        - board : 棋盤
        - valid_moves : 目前可以下的位置 (資料型態 : 陣列)
        --------------------------------------------------------
        #### 回傳值
        - 含有兩個元素的陣列，表示最後選擇的位置 ; 若沒有選擇, 回傳None
        --------------------------------------------------------
        """
        random.shuffle(valid_moves)

        bestScore = -1
        bestMove = None
        for x, y in valid_moves:
            # 如果(x, y)在棋盤角落，直接選擇下在那裏
            if self.isOnCorner(x, y):
                return [x, y]

            # 下在(x, y)的位置，並選擇分數最高的
            copyBoard = utils.getBoardCopy(board)
            utils.flip(copyBoard, self.opponentSide, x, y)
            """
            Q5. 完成以下的程式碼
            Todo : 得到目前的score，若score比bestScore大，更新bestMove和bestScore，最終我們可以得到最高的score
            Hint :
            1. "?"替換成utils.py中的某個可以計算黑白棋分數的函式(ABC選項其中一個)
                A. utils.noMoreMove
                B. utils.getBoardCopy
                C. utils.getScore
            2. if條件式判斷score是否比bestScore大
            3. 如果條件成立，bestMove = [x, y]，那麼bestScore應該等於什麼?
            """
            # Q5 begin your code here
            score = "?"(copyBoard)[self.opponentSide]
            ## if條件式(共3行)

            # Q5 end your code

        return bestMove

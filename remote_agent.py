import pickle

class RemoteAgent:
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
        self.name = "remote"
        self.opponentSide = "black" if self.side == "white" else "white"
    def choose(self, s):
        """
        --------------------------------------------------------
        #### 功能 : 選擇下一步的位置 (最白癡的greedy演算法)
        --------------------------------------------------------
        #### 參數
        - board : 棋盤
        - valid_moves : 目前可以下的位置 (資料型態 : 陣列)
        - s: 連線物件
        --------------------------------------------------------
        #### 回傳值
        - 含有兩個元素的陣列，表示最後選擇的位置 ; 若沒有選擇, 回傳None
        --------------------------------------------------------
        """
        data = s.recv(1024).decode()
        data = data.split("#")
        print(data)
        if 'play' in data[0]:
            move = [int(data[1]), int(data[2])]
            return move

        
import utils

class MinimaxAgent:
    def __init__(self, side):
        self.side = side
        self.name = "agent"
        self.opponentSide = "black" if self.side == "white" else "white"

    def evaluate(self, board):
        """
        評估函數
        """
        X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
        Y1 = [0, 1, 1, 1, 0, -1, -1, -1]
        V = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [ 11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [ 11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [ 20, -3, 11, 8, 8, 11, -3, 20],
        ]
        my_tiles = 0
        opp_tiles = 0
        my_front_tiles = 0
        opp_front_tiles = 0
        p = 0
        c = 0
        l = 0
        m = 0
        f = 0
        d = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == self.side:
                    d += V[i][j]
                    my_tiles += 1
                elif board[i][j] == self.opponentSide:
                    d -= V[i][j]
                    opp_tiles += 1
                if board[i][j] != "none":
                    for k in range(8):
                        x = i + X1[k]
                        y = j + Y1[k]
                        if x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] == "none":
                            if board[i][j] == self.side: my_front_tiles += 1
                            else: opp_front_tiles += 1
                            break
        if my_tiles > opp_tiles:
            p = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            p = 0
        
        if my_front_tiles > opp_front_tiles:
            f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
        elif my_front_tiles < opp_front_tiles:
            f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)
        else:
            f = 0

        my_tiles = opp_tiles = 0
        if board[0][0] == self.side: my_tiles += 1
        elif board[0][0] == self.opponentSide: opp_tiles += 1

        if board[0][7] == self.side: my_tiles += 1
        elif board[0][7] == self.opponentSide: opp_tiles += 1

        if board[7][0] == self.side: my_tiles += 1
        elif board[7][0] == self.opponentSide: opp_tiles += 1

        if board[7][7] == self.side: my_tiles += 1
        elif board[7][7] == self.opponentSide: opp_tiles += 1

        c = 25 * (my_tiles - opp_tiles)

        my_tiles = opp_tiles = 0
        if board[0][0] == "none":
            if board[0][1] == self.side: my_tiles += 1
            elif board[0][1] == self.opponentSide: opp_tiles += 1

            if board[1][1] == self.side: my_tiles += 1
            elif board[1][1] == self.opponentSide: opp_tiles += 1

            if board[1][0] == self.side: my_tiles += 1
            elif board[1][0] == self.opponentSide: opp_tiles += 1
        
        if board[0][7] == "none":
            if board[0][6] == self.side: my_tiles += 1
            elif board[0][6] == self.opponentSide: opp_tiles += 1

            if board[1][6] == self.side: my_tiles += 1
            elif board[1][6] == self.opponentSide: opp_tiles += 1

            if board[1][7] == self.side: my_tiles += 1
            elif board[1][7] == self.opponentSide: opp_tiles += 1
        
        if board[7][0] == "none":
            if board[7][1] == self.side: my_tiles += 1
            elif board[7][1] == self.opponentSide: opp_tiles += 1

            if board[6][1] == self.side: my_tiles += 1
            elif board[6][1] == self.opponentSide: opp_tiles += 1

            if board[6][0] == self.side: my_tiles += 1
            elif board[6][0] == self.opponentSide: opp_tiles += 1
        
        if board[7][7] == "none":
            if board[6][7] == self.side: my_tiles += 1
            elif board[6][7] == self.opponentSide: opp_tiles += 1

            if board[6][6] == self.side: my_tiles += 1
            elif board[6][6] == self.opponentSide: opp_tiles += 1

            if board[7][6] == self.side: my_tiles += 1
            elif board[7][6] == self.opponentSide: opp_tiles += 1
        
        l = -12.5 * (my_tiles - opp_tiles)

        my_tiles = len(utils.getValidMoves(board, self.side))
        opp_tiles = len(utils.getValidMoves(board, self.opponentSide))

        if my_tiles > opp_tiles:
            m = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            m = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            m = 0

        score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)

        return score
    
    def minimax(self, board, depth, maximized, alpha, beta):
        if depth == 0 or len(utils.getValidMoves(board, self.side if maximized else self.opponentSide)) == 0:
            return self.evaluate(board), None
       
        if maximized:
            val = float("-inf")
            move = None
            for x, y in utils.getValidMoves(board, self.side):
                copyBoard = utils.getBoardCopy(board)
                utils.flip(copyBoard, self.side, x, y)
                child_score, _ = self.minimax(copyBoard, depth-1, False, alpha, beta)
                if child_score > val:
                    val = child_score
                    move = [x, y]

                if val > beta:
                    break

                alpha = max(alpha, val)
        
            return val, move
        else:
            val = float("inf")
            move = None
            for x, y in utils.getValidMoves(board, self.opponentSide):
                copyBoard = utils.getBoardCopy(board)
                utils.flip(copyBoard, self.opponentSide, x, y)
                child_score, _ = self.minimax(copyBoard, depth-1, True, alpha, beta)           

                if child_score < val:
                    val = child_score
                    move = [x, y]
                
                if val < alpha:
                    break

                beta = min(beta, val)
            return val, move

    def choose(self, board, valid_moves):
        """
        用最白癡的greedy選擇最佳的走法
        """
        _, bestMove = self.minimax(board, 5, True, float("-inf"), float("inf"))

        return bestMove

direct = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]


def isOnBoard(x, y):
    """
    --------------------------------------------------------
    #### 功能 : 判斷輸入的x、y值的位置是否在棋盤上
    --------------------------------------------------------
    #### 參數
    - x :
    - y :
    --------------------------------------------------------
    #### 回傳值
    - True or False
    --------------------------------------------------------
    """
    return 7 >= x and x >= 0 and 7 >= y and y >= 0


def isValidMove(board, side, xstart, ystart):
    """
    --------------------------------------------------------
    #### 功能 :
    --------------------------------------------------------
    #### 參數
    - board :
    - side :
    - xstart :
    - ystart :
    --------------------------------------------------------
    #### 回傳值
    - True or False :
    --------------------------------------------------------
    """
    #######################################################
    # - board: the status of the tiles in the current board
    # - side: the side of the placed disk
    # - xstart: x location of the placed disk
    # - ystart: y location of the placed disk
    # ------------------------------------------------------
    # - return whether the move is valid
    #######################################################
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != "none" or len(getFlipDisks(board, side, xstart, ystart)) == 0:
        return False
    return True


def getValidMoves(board, side):
    """
    --------------------------------------------------------
    #### 功能 :
    --------------------------------------------------------
    #### 參數
    - board :
    - side :
    --------------------------------------------------------
    #### 回傳值
    --------------------------------------------------------
    """
    #######################################################
    # - board: the status of the tiles in the current board
    # - side: the side of the placed disk
    # ------------------------------------------------------
    # - return the list of valid moves
    #######################################################
    valid = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, side, x, y):
                valid.append([x, y])
    return valid


def getScore(board):
    """
    --------------------------------------------------------
    #### 功能 : 計算棋盤上黑棋和白棋的數量
    --------------------------------------------------------
    #### 參數
    - board :
    --------------------------------------------------------
    #### 回傳值
    --------------------------------------------------------
    """
    #######################################################
    # - board: the status of the tiles in the current board
    # ------------------------------------------------------
    # - return the scores of two sides
    #######################################################
    bscore = 0
    wscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == "black":
                bscore += 1
            elif board[x][y] == "white":
                wscore += 1
    return {"black": bscore, "white": wscore}


def getFlipDisks(board, side, xstart, ystart):
    """
    --------------------------------------------------------
    #### 功能 :
    --------------------------------------------------------
    #### 參數
    - board :
    - side :
    - xstart :
    - ystart :
    --------------------------------------------------------
    #### 回傳值
    --------------------------------------------------------
    """
    ########################################################
    # - board: the status of the tiles in the current board
    # - side: the side of the placed disk
    # - xstart: x location of the the placed disk
    # - ystart: y location of the the placed disk
    # ------------------------------------------------------
    # - return the list of disks that should be flipped
    #######################################################
    board[xstart][ystart] = side
    otherside = "white"
    if side == "white":
        otherside = "black"
    flipped_disks = []
    for xdirect, ydirect in direct:
        x, y = xstart + xdirect, ystart + ydirect
        temp = []
        while isOnBoard(x, y) and board[x][y] != "none":
            if board[x][y] == otherside:
                temp.append([x, y])
                x += xdirect
                y += ydirect
            if not isOnBoard(x, y):
                break
            if board[x][y] == side:
                flipped_disks += temp
                break
    board[xstart][ystart] = "none"
    return flipped_disks


def flip(board, side, xstart, ystart):
    """
    --------------------------------------------------------
    #### 功能 :
    --------------------------------------------------------
    #### 參數
    - board :
    - side :
    - xstart :
    - ystart :
    --------------------------------------------------------
    #### 回傳值
    - 無
    --------------------------------------------------------
    """
    #######################################################
    # - board: the status of the tiles in the current board
    # - side: the side of the placed disk
    # - xstart: x location of the the placed disk
    # - ystart: y location of the the placed disk
    # ------------------------------------------------------
    # - return nothing and flip the disks on move
    #######################################################
    disks = getFlipDisks(board, side, xstart, ystart)
    board[xstart][ystart] = side
    for x, y in disks:
        board[x][y] = side


def noMoreMove(board):
    """
    --------------------------------------------------------
    #### 功能 : 判斷棋局是否結束
    --------------------------------------------------------
    #### 參數
    - board :
    --------------------------------------------------------
    #### 回傳值
    --------------------------------------------------------
    """
    #######################################################
    # - board: the status of the tiles in the current board
    # ------------------------------------------------------
    # - return whether there is no more move
    #######################################################
    return not getValidMoves(board, "white") and not getValidMoves(board, "black")


def getBoardCopy(board):
    """
    --------------------------------------------------------
    #### 功能 : 複製一個8*8一模一樣的棋盤
    --------------------------------------------------------
    #### 參數
    - board :
    --------------------------------------------------------
    #### 回傳值
    --------------------------------------------------------
    """
    ########################################################
    # - board: the status of the tiles in the current board
    ########################################################
    copied = []
    for _ in range(8):
        copied.append(["none"] * 8)
    for x in range(8):
        for y in range(8):
            copied[x][y] = board[x][y]
    return copied

# 將盤面加上編號，讓玩家可以選擇消除
def add_labels(board, dic):
    labeled_board = [[' '] + [str(i+1) for i in range(len(board[0]))]]  # 列标号
    for i in range(len(board[0])):
        dic[str(i+1)] = ('Column', i)
    for i, row in enumerate(board):
        labeled_board.append([chr(ord('A') + i)] + [str(cell) for cell in row])  # 行标号
        dic[chr(ord('A') + i)] = ('Row', i)
    return labeled_board

# 印出標號後的盤面
def print_board(board):
    for row in board:
        print(' '.join(row))

# 計算盤面上的棋子數量，使用 for 迴圈將盤面上的數加起來
def count_pieces(board):
    count = 0
    for row in board:
        for val in row:
            count += val
    return count

# 檢查遊戲是否結束，也就是盤面上是否還有棋子，判斷數量是否為 0
def terminal_state(board):
    return count_pieces(board) == 0

# 取得所有合法的移動，分為 Row 及 Column ，先判斷該移動上是否有棋子，若有才會加入
def get_legal_moves(board):
    legal_moves = []
    for i in range(len(board)):
        if sum(board[i]) > 0:
            legal_moves.append(('Row', i))
    for j in range(len(board[0])):
        if sum([board[i][j] for i in range(len(board))]) > 0:
            legal_moves.append(('Column', j))
    return legal_moves

# 將盤面依照傳入的 move 進行移動，將 1 變成 0，同時計算該玩家得到了幾顆棋子
def make_move(board, move):
    point = 0
    new_board = [row[:] for row in board]
    if move[0] == 'Row':
        row_index = move[1]
        for j in range(len(board[0])):
            if new_board[row_index][j] != 0:
                point += 1
            new_board[row_index][j] = 0
    else:
        col_index = move[1]
        for i in range(len(board)):
            if new_board[i][col_index] != 0:
                point += 1
            new_board[i][col_index] = 0
    return new_board, point

def boardGame(board, is_max_player, score, run):
    dic = {}

    labeled_board = add_labels(board, dic)
    print("------------Run ", run, "------------")
    print_board(labeled_board)
    if terminal_state(board):
        return score

    if is_max_player: # 輪到玩家
        while(True):
            print("\033[94m{}\033[00m".format("\nYour turn"))
            print("\033[94m{}\033[00m".format("Which Row / Column you want to remove ? (Row : A, B, C... Column : 1, 2, 3...)"))
            choose = input()
            if choose in dic:
                break
            else:
                print("\033[91m {}\033[00m" .format("This operation is not allow"))
        new_board, point = make_move(board, dic[choose]) # 取得移動後新盤面
        score = boardGame(new_board, False, score + point, run) # 遞迴傳入
        return score
    else: # 輪到 AI
        print("\033[93m{}\033[00m".format("\nAI's turn"))
        best_point = -float("inf")
        best_move = None
        for move in get_legal_moves(board):
            new_board, point = make_move(board, move) # 取得移動後新盤面
            if point > best_point:
                best_point = point
                best_move = move
        
        print("\033[93m{}\033[00m".format("AI choose " + best_move[0] + " " + str(best_move[1] + 1)))
        new_board, point = make_move(board, best_move) # 取得移動後新盤面
        score = boardGame(new_board, True, score - point, run + 1) # 遞迴傳入
        return score

if __name__ == "__main__":    
    with open("input.txt", "r") as f:
        # 讀取第一行，並轉換為數字列表
        n, m = list(map(int, f.readline().split()))

        # 讀取接下來的n行，並將每一行轉換為數字列表，形成一個二維陣列
        board = [list(map(int, f.readline().split())) for i in range(n)]

    score = boardGame(board, True, 0, 1)

    if score > 0:
        print("\nWin, score :", score)
    elif score < 0:
        print("\nLoss, score :", score)
    else:
        print("\nTie, score :", score)


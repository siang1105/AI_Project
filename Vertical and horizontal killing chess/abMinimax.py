import time

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

# 實作 minimax 演算法部分
def minimax(board, is_max_player, alpha, beta, score):
    best_step = []
    if terminal_state(board):
        return score, []

    if is_max_player:
        best_score = -float("inf")
 
        for move in get_legal_moves(board):
            new_board, point = make_move(board, move) # 取得移動後新盤面
            max_score, step = minimax(new_board, False, alpha, beta, point + score) # 遞迴傳入
            
            step = [("max", move[0], move[1]+1)] + step # 紀錄走步路徑
            if max_score > best_score: # 若有較好，更新走步路徑
                best_step = step
            best_score = max(best_score, max_score) # 若有較大，更新分數
            # 實作 alpha - beta pruning 部分
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score, best_step
    else:
        best_score = float("inf")
        step = None
        for move in get_legal_moves(board):
            new_board, point = make_move(board, move) # 取得移動後新盤面
            min_score, step = minimax(new_board, True, alpha, beta, score - point) # 遞迴傳入
            step = [("min", move[0], move[1]+1)] + step # 紀錄走步路徑
            if min_score < best_score: # 若有較好，更新走步路徑
                best_step = step
            best_score = min(best_score, min_score) # 若有較小，更新分數
            # 實作 alpha - beta pruning 部分
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return best_score, best_step


if __name__ == "__main__":    
    with open("input.txt", "r") as f:
        # 讀取第一行，並轉換為數字列表
        n, m = list(map(int, f.readline().split()))

        # 讀取接下來的n行，並將每一行轉換為數字列表，形成一個二維陣列
        board = [list(map(int, f.readline().split())) for i in range(n)]

    start_time = time.time()
    score, best_step = minimax(board, True, -float("inf"), float("inf"), 0) # 呼叫核心函式
    end_time = time.time()

    with open('output.txt', 'w') as f:
        f.write(str(best_step[0][1]) + " # : " + str(best_step[0][2]) + "\n")
        f.write(str(score) + " points\n")
        f.write("Total run time = " + str(end_time - start_time) + " seconds.\n")


import time
import numpy as np

# 控制每個搜尋的深度limit
def iterative_deepening_dfs(input_list, n):
    depth = 0 # 初始值為0
    while True:
        move = []
        dic = {}
        for i in range(500): # 初始字典各深度list，為了紀錄該層相同盤面
            dic[i] = []
        result = depth_limited_dfs(input_list, 0, depth, n, move, dic) #傳入最初盤面，開始做遞迴，回傳值為一tuple(是否找到解, 走步list)
        if result[0]:
            return result[1] # 若有解則回傳移動步驟
        depth += 1 # 若沒找到解則把限制深度加一，再傳入遞迴
        if depth > 500: # 目前設置若到深度300還沒有解，就停止程式
            return False

# 處理衍生細胞盤面
def cell_grow(input_list, index):
    left_shifted = input_list[:]
    right_shifted = input_list[:]
    left_shifted[index] = 0 # 將選擇消滅的細胞設為0
    right_shifted[index] = 0
    right_shifted.pop() # 處理右移
    right_shifted.insert(0, 0)
    left_shifted.pop(0) # 處理左移
    left_shifted.append(0)
    cell = np.bitwise_or(left_shifted, right_shifted).tolist() #使用numpy函式做OR運算
    return cell
    
# 主要遞迴部分
def depth_limited_dfs(input_list, depth, limit, n, move, dic):
    if dic[depth].count(input_list) == 0: # 若此盤面在該層還會走過，將它加入字典
        dic[depth].append(input_list)
    depth += 1
    total = sum(input_list) # 計算盤面癌細胞數量
    if total == 0: # 若為0表示已完全消滅，則回傳True以及移動步驟
        return (True, move)
    elif depth >= limit: # 若深度已經超過，就回傳False
        return (False, None)
    else:
        for i in range(n): # 選取要消滅細胞，有n種可能
            if input_list[i] != 0: # 有癌細胞的地方才可以選
                m = move[:]
                m.append(i+1) # 紀錄走步
                new_cell = cell_grow(input_list, i) # 處理衍生細胞，傳回新的盤面
                if dic[depth].count(new_cell) == 0: # 判斷該盤面在該層是否展開過
                    result = depth_limited_dfs(new_cell, depth, limit, n, m, dic) # 沒有展開過就傳入遞迴
                    if result[0] == True: 
                        return (True, result[1]) # 找到解法就回傳True，以及走步
    return (False, None)

if __name__ == "__main__":
    # 讀取輸入檔
    with open('input.txt', 'r') as f:
        test_cases = f.readlines()

    # 讀取輸入檔的每一行測資，紀錄程式執行時間，並把結果寫入output.txt
    for test_case in test_cases:
        input_list = list(map(int, test_case.split()))
        start_time = time.time()
        result = iterative_deepening_dfs(input_list, len(input_list))
        end_time = time.time()

        if result != False:
            with open('output.txt', 'w') as f:
                f.write("Total run time = " + str(end_time - start_time) + " seconds.\n")
                f.write("An optimal solution has " + str(len(result)) + " moves:\n")
                f.write(" ".join(str(x) for x in result) + "\n")
        else:
            with open('output.txt', 'w') as f:
                f.write("There is no solution.\n")
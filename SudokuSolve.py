from random import choice, randint, sample
import random
import time, copy


def random_board(copied_board):
    for i in range(9):
        default = [1,2,3,4,5,6,7,8,9]
        for j in range(9):
            if copied_board[i][j] != 0:
                default.remove(copied_board[i][j])
        for t in range(9):
            if copied_board[i][t] == 0:
                rand_value = random.choice(default)
                copied_board[i][t] = rand_value
                default.remove(rand_value)    

def N_operator(initial_board,board,N):
    # idx = 0
    # for i in range(9):
    #     for j in range(9):
    #         if initial_board[i][j] == 0:
    #             if (random.random()<=N):
    #                 value = random.randint(0,8)
    #                 board[i][j],board[i][value] = board[i][value],board[i][j]
    #                 #idx = -1 if (random.random()<=N) else 1
    #                 # board[i][j] = board[i][j] + (idx if board[i][j] in range(2,9) else 1 if board[i][j] == 1 else -1)
    # return board
    permuterow(initial_board,board)
    if(random.random()<=N):
        first_X = second_X = row = 0
        while True:
            first_X = random.randint(0, 9 - 1)
            second_X = random.randint(0, 9- 1)
            row = random.randint(0, 9 - 1)
            if first_X == second_X or initial_board[row][first_X]!= 0  or  initial_board[row][second_X]!= 0 :
                continue
            board[row][first_X], board[row][second_X] = board[row][second_X], board[row][first_X]
            break
    return board
def B_operator(initial_board,board,B):
    for i in range(9):
        for j in range(9):
            if initial_board[i][j] == 0:
                if (random.random() <= B):
                        board[i][j] = random.randint(1, 9)
    return board
def heuristic_function(matrix):
    # res = 0
    # for i in board:
    #     value = sum(i)
    #     res += abs(value -45)
    # for i in range(9):
    #     value = 0
    #     for j in range(9):
    #         value += board[j][i]
    #     res+= abs(value -45)

    # for x in range(0,9,3):
    #     for y in range(0,9,3):
    #         value = 0
    #         for z in range(x, x + 3):
    #             for t in range(y, y + 3):
    #                 value += board[z][t]
    #         res += abs(value - 45)
    # return res
    duplicates = 0
    # Check rows
    for row in matrix:
        duplicates += len(row) - len(set(row))

    # Check columns
    for col in range(9):
        column_values = [matrix[row][col] for row in range(9)]
        duplicates += len(column_values) - len(set(column_values))

    # Check 3x3 boxes
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            box_values = [matrix[row][col] for row in range(i, i+3) for col in range(j, j+3)]
            duplicates += len(box_values) - len(set(box_values))
    return duplicates
      
def solve(board, gui=None):
    """Solves the board and displays board to GUI. Returns solved board as nested list """
    solved_board = dfs_solve(board, gui)
    if gui:
        gui.toggle_buttons(True, True)
    return solved_board

def solve_Heuristic(board, gui=None):
    """Solves the board and displays board to GUI/renables buttons if gui is not none.
    Returns solved board as nested list """
    initial = board
    for i in range(15):
        solved_board = heuristic_solve(initial, gui)
        if solved_board == False:
            continue
        else: break
    if gui:
        gui.toggle_buttons(True, True)
    return solved_board
def permuterow(init_board,board):
    lst = []
    row = random.randint(0, 9 - 1)
    for i in range(9):
        if init_board[row][i] != 0:
            lst.append(init_board[row][i])
    for i in range(9):
        if init_board[row][i] != 0: continue
        while True:
            random_num = random.randint(1,9)
            if random_num  not in lst:
                lst.append(random_num)
                board[row][i] = random_num
                break


def heuristic_solve(board, gui=None):
    #TODO: Hiện thực giải thuật leo đồi và một hàm lượng giá kèm theo
    # hiện thực heuristic function với beta-hillclimbing https://www.researchgate.net/publication/319886025_b-Hill_Climbing_Algorithm_for_Sudoku_Game
    in_board = [row[:] for row in board]
    N = 0.5
    B = 0.5
    random_board(in_board)
    z = heuristic_function(in_board)
    itr = 0 
    x1 = in_board
    x2 = in_board
    while itr <= 10000:
        copy_inboard = [row[:] for row in in_board]
        x1 = N_operator(board,copy_inboard,N)
        if (random.random()<= B):
            x2 = B_operator(board,x1,B)
        z2 = heuristic_function(x2)
        z1 = heuristic_function(x1)
        z_best= z2 if z2<z1 else z1
        xbest= x2 if z2<z1 else x1
        if(z_best < z):
            if(z_best == 0 and is_solution(xbest)):
                print(xbest)
                gui.move_array.append(copy.deepcopy(xbest))
                return xbest
            in_board = xbest
            z = z_best
        itr +=1
    return False



    


# Mỗi bước thay đổi đều được cập nhật trên giao diện -> sửa số trong board -> thêm trạng thái mới vào move_array
def dfs_solve(board, gui):
    """Solves the sudoku board represented as a nested list using DFS backtracking.
    If a GUI reference is passed in, the solving process is displayed to the user"""
    if is_solution(board):
        return board
    row, col = get_first_unfilled_square(board)
    possible_solutions = get_valid_numbers(board, row, col)
    if possible_solutions:
        for number in possible_solutions:
            if gui:
                # cập nhật giao diện
                gui.update_single_grid_gui_square(row, col, "Green", number)
            # cập nhật board
            board[row][col] = number
            if gui:
                # thêm lịch sử vào move_array
                gui.move_array.append(copy.deepcopy(board))
            solved = dfs_solve(board, gui)
            if is_solution(solved):
                return solved

    # board[row][col] = 0
    if gui:
        # cập nhật giao diện
        gui.update_single_grid_gui_square(row, col, "Red")
        # cập nhật board
        board[row][col] = 'X'
        # thêm lịch sử vào move_array
        gui.move_array.append(copy.deepcopy(board))
        time.sleep(0.05)

        board[row][col] = 0
        gui.update_single_grid_gui_square(row, col, "Red", 0)
        gui.move_array.append(copy.deepcopy(board))
        # time.sleep(0.05)
    return board


def get_valid_numbers(board, row, col):
    """Returns a set of possible numbers that could be inserted in a grid cell"""
    return get_valid_numbers_in_row(board, row, col) & get_valid_in_column(board, row, col) & get_valid_in_square(board, row, col)


def get_valid_numbers_in_row(board, row, col):
    """Returns a set of numbers valid in box given the sudoku row constraints"""
    valid_numbers = {1,2,3,4,5,6,7,8,9}
    for index, item in enumerate(board[row]):
        if index == col:
            continue
        elif item in valid_numbers:
            valid_numbers.remove(item)
    return valid_numbers


def get_valid_in_column(board, row, col):
    """Returns a set of numbers valid in the column given sudoku constraints"""
    valid_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for row_index in range(9):
        if row_index == row:
            continue
        square = board[row_index][col]
        if square in valid_numbers:
            valid_numbers.remove(square)
    return valid_numbers


def get_valid_in_square(board, row, col):
    """Returns a set of numbers valid in terms of SUB-SQUARE-GROUP constraint"""
    valid_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    start_x = (col // 3) * 3
    start_y = (row // 3) * 3
    for y in range(start_y, start_y + 3):
        for x in range(start_x, start_x + 3):
            square_value = board[y][x]
            if y == row and x == col:
                continue
            elif square_value in valid_numbers:
                valid_numbers.remove(square_value)
    return valid_numbers


def is_solution(board):
    """Checks if the board is completely filled with VALID numbers"""
    for row in range(9):
        for col in range(9):
            if board[row][col] not in get_valid_numbers(board, row, col):
                return False
    return True


def get_first_unfilled_square(board):
    """Gets the first square in the board that has a value of zero"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col


# You can get it from this thread on StackOverFlow:
# https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python
def generate_new_board():
    '''Generator which makes new sudokuboard'''
    base  = 3
    side  = base*base

    # pattern for a baseline valid solution
    def pattern(r,c): return (base*(r%base)+r//base+c)%side

    # randomize rows, columns and numbers (of valid base pattern)
    def shuffle(s): return sample(s,len(s)) 
    rBase = range(base) 
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    new_board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

    # clearing...
    for row in range(9):
        num_squares_to_delete = randint(4,9)
        for _ in range(num_squares_to_delete):
            col = randint(0,8)
            new_board[row][col] = 0

    return new_board





class sudokuSolver:
    def __init__(self,board):
        self.board = board
        self.legal_numbers = {}
        self.initializeLegalNumbers()

    #Create the original dictionary of all possible numbers
    def initializeLegalNumbers(self):
        #Assume the board is completely empty board every cell can be between 1 and 9
        initial_values = set(range(1,10))
        for row in range(9):
            for col in range(9):
                if (self.board[row][col] == 0):
                    self.legal_numbers[(row,col)] = initial_values
        self.updateLegalValues()

    #Find the numbers used in that row and remove them from the legal number dict
    def removeIllegalNumbersRow(self,row,seen):
        for i in range(9):
            key = (row,i)
            if (key in self.legal_numbers):
                self.legal_numbers[key] = self.legal_numbers[key]-seen

    #Find the numbers used in that col and remove them from the legal number dict
    def removeIllegalNumbersCol(self,col,seen):
        for i in range(9):
            key = (i,col)
            if (key in self.legal_numbers):
                self.legal_numbers[key] = self.legal_numbers[key]-seen

    #Find the numbers used in that box and remove them from the legal number dict
    def removeIllegalNumbersBlock(self,row,col,seen):
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        for current_row in range(start_row, start_row + 3):
            for current_col in range(start_col, start_col + 3):
                key = (current_row,current_col)
                if (key in self.legal_numbers):
                    self.legal_numbers[key] = self.legal_numbers[key]-seen

    #Update the legal moves dict to have the new values
    def updateLegalValues(self):
        for i in range(9):
            row_seen = self.checkRow(i)
            col_seen = self.checkCol(i)
            self.removeIllegalNumbersRow(i,row_seen)
            self.removeIllegalNumbersCol(i,col_seen)
        for row in range(0,9,3):
            for col in range(0,9,3):
                block_seen = self.checkBlock(row,col)
                self.removeIllegalNumbersBlock(row,col,block_seen)
                
    #See if the num in a specific row
    def checkRow(self,row,num=-1):
        if num != -1:
            for val in self.board[row]:
                if val == num:
                    return False
            return True
        else:
            seen = set()
            for val in self.board[row]:
                seen.add(val)
            seen.remove(0)
            return seen

    #See if the num in a specific col
    def checkCol(self,col,num=-1):
        if (num != -1):
            for current_row in self.board:
                if current_row[col] == num:
                    return False
            return True
        else:
            seen = set()
            for row in self.board:
                seen.add(row[col])
            seen.remove(0)
            return seen

    #See if the num in a specific box
    def checkBlock(self,row,col,num=-1):
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        if (num != -1):
            for current_row in range(start_row, start_row + 3):
                for current_col in range(start_col, start_col + 3):
                    if self.board[current_row][current_col] == num:
                        return False
            return True
        else:
            seen = set()
            for current_row in range(start_row, start_row + 3):
                for current_col in range(start_col, start_col + 3):
                    seen.add(self.board[current_row][current_row])
            seen.remove(0)
            return seen

    #Check if the number can be placed in the current row and col
    def checkLegalCell(self,row,col,num):
        if not self.checkRow(row,num):
            return False
        if not self.checkCol(col,num):
            return False
        if not self.checkBlock(row,col,num):
            return False
        return True

    #Find the first empty cell
    def findEmptyCell(self):
        #Makes sure that we don't loop over a cell that's already seen
        for current_row in range(9):
            for current_col in range(9):
                if self.board[current_row][current_col] == 0:
                    return current_row,current_col
        return -1,-1
        
    def solveSudoku(self):
        return self.solveSudokuHelper()

    def solveSudokuHelper(self):
        row,col = self.findEmptyCell()
        if row == -1 and col == -1:
            return self.board
        else:
            for i in range(1, 10):
                if self.checkLegalCell(row,col,i):
                    self.board[row][col] = i
                    board_solved = self.solveSudokuHelper()
                    if board_solved is not None:
                        return self.board
                    self.board[row][col] = 0
            return None
        
if __name__ == '__main__':
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    solver = sudokuSolver(board)
    solved_board = solver.solveSudoku()
    '''for key,value in list(solver.legal_numbers.items()):
        print(f"{key} | {value} | {solved_board[key[0]][key[1]]}")'''
    for row in solved_board:
        print(row)
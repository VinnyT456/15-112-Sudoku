class sudokuSolver:
    def __init__(self,board):
        self.board = board
        self.legal_numbers = {}
        self.initializeLegalNumbers()

    def initializeLegalNumbers(self):
        for row in range(9):
            for col in range(9):
                if (self.board[row][col] == 0):
                    self.legal_numbers[(row,col)] = set(i for i in range(1,10))
        self.removeIllegalNumbers()

    #Find the numbers used in that row and remove them from the legal number dict
    def removeIllegalNumbersRow(self,row):
        seen = set()
        for i in range(9):
            seen.add(self.board[row][i])
        seen.remove(0)
        for key in self.legal_numbers:
            if (key[0] > row):
                break
            if (key[0] == row):
                self.legal_numbers[key] = self.legal_numbers[key]-seen

    #Find the numbers used in that col and remove them from the legal number dict
    def removeIllegalNumbersCol(self,col):
        seen = set()
        for i in range(9):
            seen.add(self.board[i][col])
        seen.remove(0)
        for key in self.legal_numbers:
            if (key[1] == col):
                self.legal_numbers[key] = self.legal_numbers[key]-seen

    #Find the numbers used in that box and remove them from the legal number dict
    def removeIllegalNumbersBox(self,row,col):
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        seen = set()
        for current_row in range(start_row, start_row + 3):
            for current_col in range(start_col, start_col + 3):
                seen.add(board[current_row][current_col])
        seen.remove(0)
        for current_row in range(start_row, start_row + 3):
            for current_col in range(start_col, start_col + 3):
                key = (current_row,current_col)
                if (key in self.legal_numbers):
                    self.legal_numbers[key] = self.legal_numbers[key]-seen

    #Update the legal moves dict to have the new values
    def removeIllegalNumbers(self):
        for i in range(9):
            self.removeIllegalNumbersRow(i)
            self.removeIllegalNumbersCol(i)
        for row in range(0,9,3):
            for col in range(0,9,3):
                self.removeIllegalNumbersBox(row,col)
                
    #See if the num in a specific row
    def checkRow(self,row,num):
        for val in self.board[row]:
            if val == num:
                return False
        return True

    #See if the num in a specific col
    def checkCol(self,col,num):
        for current_row in self.board:
            if current_row[col] == num:
                return False
        return True

    #See if the num in a specific box
    def checkBlock(self,row,col,num):
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        for current_row in range(start_row, start_row + 3):
            for current_col in range(start_col, start_col + 3):
                if self.board[current_row][current_col] == num:
                    return False
        return True

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
    for key,value in list(solver.legal_numbers.items()):
        print(key,value)
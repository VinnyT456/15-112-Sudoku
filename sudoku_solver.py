import time
import os

class sudokuBoard:
    def __init__(self,board):
        self.board = board

    def getBoardValue(self,row,col):
        return self.board[row][col]

    def updateBoardValue(self,row,col,val):
        self.board[row][col] = val

    def clearBoardValue(self,row,col):
        self.board[row][col] = 0

    def checkRow(self,row,num):
        for val in self.board[row]:
            if val == num:
                return False
        return True
    
    def checkCol(self,col,num):
        for current_row in self.board:
            if current_row[col] == num:
                return False
        return True
        
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
        return self.checkRow(row,num) and self.checkCol(col,num) and self.checkBlock(row,col,num)
    
class sudokuSolver:
    def __init__(self,board):
        self.puzzle = board
        self.legal_numbers = {}
        self.positions_available = []
        self.initializeLegalNumbers()

    def initializeLegalNumbers(self):
        #Assume the board is completely empty board every cell can be between 1 and 9
        initial_values = set(range(1,10))
        self.legal_numbers = dict()
        for row in range(9):
            for col in range(9):
                if (self.puzzle.getBoardValue(row,col) == 0):
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

    #Fewest Legal Moves and Most Legal Moves
    #Learned (sorted(key)) from https://www.geeksforgeeks.org/python-sorted-function/
    #Learn items (dictionary) from https://www.w3schools.com/python/ref_dictionary_items.asp
    def sortLegalValues(self):
        numbers_available = sorted([self.legal_numbers[position] for position in self.legal_numbers],key=len)
        self.positions_available = []
        for number in numbers_available:
            for position,num in self.legal_numbers.items():
                if (number == num and position not in self.positions_available):
                    self.positions_available.append(position)
                    break
        self.legal_numbers = dict()
        for i in range(len(numbers_available)):
            self.legal_numbers[self.positions_available[i]] = numbers_available[i]

    #Update the legal moves dict to have the new values
    def updateLegalValues(self):
        for i in range(9):
            row = col = i
            block_row,block_col = i // 3 * 3,i % 3 * 3
            row_seen = self.checkRow(row)
            col_seen = self.checkCol(col)
            block_seen = self.checkBlock(block_row,block_col)
            self.removeIllegalNumbersRow(i,row_seen)
            self.removeIllegalNumbersCol(i,col_seen)
            self.removeIllegalNumbersBlock(block_row,block_col,block_seen)
        self.sortLegalValues()
                
    #See if the num in a specific row
    def checkRow(self,row):
        return {val for val in self.puzzle.board[row] if val != 0}

    #See if the num in a specific col
    def checkCol(self,col):
        return {row[col] for row in self.puzzle.board if row[col] != 0}

    #See if the num in a specific box
    def checkBlock(self,row,col):
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        seen = set()
        for current_row in range(start_row, start_row + 3):
            for current_col in range(start_col, start_col + 3):
                seen.add(self.puzzle.board[current_row][current_col])
        if (0 in seen): 
            seen.remove(0)
        return seen

    def solveSudoku(self):
        return self.solveSudokuHelper()

    def solveSudokuHelper(self):
        #Gets the cell to solve
        row,col = self.positions_available.pop(0) if self.positions_available != [] else (-1,-1)
        if row == -1 and col == -1:
            return self.puzzle.board
        else:
            #Gets the possible values
            legal_value = self.legal_numbers[(row,col)]
            for val in legal_value:
                if self.puzzle.checkLegalCell(row,col,val):
                    self.puzzle.updateBoardValue(row,col,val)
                    self.initializeLegalNumbers()
                    board_solved = self.solveSudokuHelper()
                    if board_solved != None:
                        return board_solved
                    self.puzzle.clearBoardValue(row,col)
            #Ensures it doesn't skip a cell after failing
            self.positions_available.insert(0,(row,col))
            return None
        
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
    
#if __name__ == '__main__': copied from https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/
if __name__ == '__main__':
    boards = []
        
    for filename in os.listdir('boards'):
        if filename.endswith('.txt'):
            pathToFile = f'boards/{filename}'
            fileContents = readFile(pathToFile)
            current_board = []
            for row in fileContents.splitlines():
                board = []
                for i in row.split(' '):
                    board.append(int(i))
                current_board.append(board)
            boards.append(current_board)

    for board in boards:
        start = time.time()
        sudoku_board = sudokuBoard(board)
        solver = sudokuSolver(sudoku_board)
        solved_board = solver.solveSudoku()
        end = time.time()
        print(end-start)
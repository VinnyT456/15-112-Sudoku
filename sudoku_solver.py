import time
import os
class sudokuSolver:
    def __init__(self,board):
        self.board = board
        self.legal_numbers = {}
        self.positions_available = []
        self.initializeLegalNumbers()

    #Create the original dictionary of all possible numbers
    def initializeLegalNumbers(self):
        #Assume the board is completely empty board every cell can be between 1 and 9
        initial_values = set(range(1,10))
        self.legal_numbers = dict()
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
            row_seen = self.checkRow(i)
            col_seen = self.checkCol(i)
            self.removeIllegalNumbersRow(i,row_seen)
            self.removeIllegalNumbersCol(i,col_seen)
        for row in range(0,9,3):
            for col in range(0,9,3):
                block_seen = self.checkBlock(row,col)
                self.removeIllegalNumbersBlock(row,col,block_seen)
        self.sortLegalValues()
        
                
    #See if the num in a specific row
    def checkRow(self,row,num=-1):
        if num != -1:
            for val in self.board[row]:
                if val == num:
                    return False
            return True
        else:
            seen = {val for val in self.board[row] if val != 0}
            return seen

    #See if the num in a specific col
    def checkCol(self,col,num=-1):
        if (num != -1):
            for current_row in self.board:
                if current_row[col] == num:
                    return False
            return True
        else:
            seen = {row[col] for row in self.board if row[col] != 0}
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
                    seen.add(self.board[current_row][current_col])
            if (0 in seen):
                seen.remove(0)
            return seen

    #Check if the number can be placed in the current row and col
    def checkLegalCell(self,row,col,num):
        return self.checkRow(row,num) and self.checkCol(col,num) and self.checkBlock(row,col,num)

    #Find the first empty cell
    def findEmptyCell(self):
        if (self.positions_available != []):
            return self.positions_available.pop(0)
        return -1,-1

    def solveSudoku(self):
        return self.solveSudokuHelper()

    def solveSudokuHelper(self):
        row,col = self.findEmptyCell()
        if row == -1 and col == -1:
            return self.board
        else:
            legal_value = self.legal_numbers[(row,col)]
            for val in legal_value:
                if self.checkLegalCell(row,col,val):
                    self.board[row][col] = val
                    self.initializeLegalNumbers()
                    board_solved = self.solveSudokuHelper()
                    if board_solved != None:
                        return self.board
                    self.board[row][col] = 0
            #Ensures it doesn't skip a cell after failing
            self.positions_available.insert(0,(row,col))
            return None
        
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
    
boards = {}
    
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
        boards[filename] = current_board

for name,board in boards.items():
    start = time.time()
    solver = sudokuSolver(board)
    solved_board = solver.solveSudoku()
    end = time.time()
    print(f"Board {name} Time Spent {end-start}")

#for key in solver.legal_numbers:
#    print(f"{key} | {solver.legal_numbers[key]} | {solved_board[key[0]][key[1]]}")
#for row in solved_board:
#    print(row)
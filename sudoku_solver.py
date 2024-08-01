import itertools
import copy

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
        for col in range(len(self.board[row])):
            if self.board[col] == num:
                return False,row,col
        return True,-1,-1
    
    def checkCol(self,col,num):
        for row in range(len(self.board)):
            if self.board[row][col] == num:
                return False,row,col
        return True,-1,-1
        
    def checkBlock(self,row,col,num):
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        for current_row in range(start_row, start_row + 3):
            for current_col in range(start_col, start_col + 3):
                if self.board[current_row][current_col] == num:
                    return False,current_row,current_col
        return True,-1,-1
    
    #Check if the number can be placed in the current row and col
    def checkLegalCell(self,row,col,num):
        return self.checkRow(row,num)[0] and self.checkCol(col,num)[0] and self.checkBlock(row,col,num)[0]
    
class LegalValues:
    def __init__(self,board):
        self.puzzle = board
        self.legal_numbers = {}
        self.positions_available = []
        self.legal_numbers_hint = {}
        self.initializeLegalNumbers()
            
    def initializeLegalNumbers(self):
        #Assume the board is completely empty board every cell can be between 1 and 9
        initial_values = set(range(1,10))
        self.legal_numbers = dict()
        for row in range(9):
            for col in range(9):
                if (self.puzzle.getBoardValue(row,col) == 0):
                    self.legal_numbers[(row,col)] = initial_values
                    self.legal_numbers_hint[(row,col)] = initial_values
        self.updateLegalValues()

    #Find the numbers used in that row and remove them from the legal number dict
    def removeIllegalNumbersRow(self,row,seen):
        for i in range(9):
            key = (row,i)
            if (key in self.legal_numbers and seen != self.legal_numbers[key]):
                self.legal_numbers[key] = self.legal_numbers[key]-seen
                self.legal_numbers_hint[key] = self.legal_numbers_hint[key]-seen

    #Find the numbers used in that col and remove them from the legal number dict
    def removeIllegalNumbersCol(self,col,seen):
        for i in range(9):
            key = (i,col)
            if (key in self.legal_numbers):
                self.legal_numbers[key] = self.legal_numbers[key]-seen
                self.legal_numbers_hint[key] = self.legal_numbers_hint[key]-seen

    #Find the numbers used in that box and remove them from the legal number dict
    def removeIllegalNumbersBlock(self,row,col,seen):
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        for current_row in range(start_row, start_row + 3):
            for current_col in range(start_col, start_col + 3):
                key = (current_row,current_col)
                if (key in self.legal_numbers):
                    self.legal_numbers[key] = self.legal_numbers[key]-seen
                    self.legal_numbers_hint[key] = self.legal_numbers_hint[key]-seen

    #Fewest Legal Moves and Most Legal Moves
    #Learned (sorted(key)) from https://www.geeksforgeeks.org/python-sorted-function/
    #Learned items (dictionary) from https://www.w3schools.com/python/ref_dictionary_items.asp
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
    
class sudokuHints(LegalValues):
    def __init__(self,board):
        super().__init__(board)
        self.puzzle = board

    def checkValidTuple(self,combo):
        cells = len(combo)
        number_of_legal_value = set()
        for i in range(cells): 
            for j in combo[i]:
                number_of_legal_value.add(j)
        return (cells == len(number_of_legal_value))
    
    def combineCombos(self,combos):
        new_combos = []
        for i in range(len(combos)):
            for j in combos[i]:
                new_combos.append(j)
        return new_combos

    def checkDuplicatesRow(self,row):
        legals = []
        most_legal = -1
        for i in range(9):
            if ((row,i) in self.legal_numbers_hint and len(self.legal_numbers_hint[(row,i)]) != 1):
                legals.append(self.legal_numbers_hint[(row,i)])
                most_legal = max(most_legal,len(self.legal_numbers_hint[(row,i)]))
        
        possible_combos = [] 

        #Copied itertools.combinations() from https://www.cs.cmu.edu/~112/notes/tp-sudoku.html
        for i in range(1,most_legal+1):
            found = False
            for current_combo in itertools.combinations(legals, i):
                valid = self.checkValidTuple(current_combo)
                if (valid == True and len(current_combo) != 1):
                    possible_combos.append(current_combo)
                    found = True
                    break
            if (found):
                break

        possible_combos = self.combineCombos(possible_combos)
        print(possible_combos)
        if (possible_combos != []):
            self.updateRow(row,possible_combos)

    def checkDuplicatesCol(self,col):
        legals = []
        most_legal = -1
        for i in range(9):
            if ((i,col) in self.legal_numbers_hint and len(self.legal_numbers_hint[(i,col)]) != 1):
                legals.append(self.legal_numbers_hint[(i,col)])
                most_legal = max(most_legal,len(self.legal_numbers_hint[(i,col)]))
        
        possible_combos = [] 

        #Copied itertools.combinations() from https://www.cs.cmu.edu/~112/notes/tp-sudoku.html
        for i in range(1,most_legal+1):
            found = False
            for current_combo in itertools.combinations(legals, i):
                valid = self.checkValidTuple(current_combo)
                if (valid == True and len(current_combo) != 1):
                    possible_combos.append(current_combo)
                    found = True
                    break
            if (found):
                break

        possible_combos = self.combineCombos(possible_combos)
        print(possible_combos)
        if (possible_combos != []):
            self.updateCol(col,possible_combos)

    def updateRow(self,row,combos):
        for combo in combos:
            for i in range(9):
                key = (row,i)
                if (key in self.legal_numbers and self.legal_numbers[key] not in combos):
                    self.legal_numbers[key]-=combo
                    self.legal_numbers_hint[key]-=combo

    def updateCol(self,col,combos):
        for combo in combos:
            for i in range(9):
                key = (i,col)
                if (key in self.legal_numbers and self.legal_numbers[key] not in combos):
                    self.legal_numbers[key]-=combo
                    self.legal_numbers_hint[key]-=combo

    def obviousTuple(self):
        for i in range(9):
            old_legal = copy.deepcopy(self.legal_numbers_hint)
            self.checkDuplicatesRow(i)
            if (self.legal_numbers_hint != old_legal):
                self.sortLegalValues()
                break 
            
        for i in range(9):
            old_legal = copy.deepcopy(self.legal_numbers_hint)
            self.checkDuplicatesCol(i)
            if (self.legal_numbers_hint != old_legal):
                self.sortLegalValues()
                break 

    def getHint(self,row=-1,col=-1):
        self.initializeLegalNumbers()
        if (self.positions_available != []):
            row,col = self.positions_available.pop(0)
            if len(self.legal_numbers[(row,col)]) == 1:
                return row,col,self.legal_numbers[(row,col)].pop()
            #self.obviousTuple()
            return None,None,set()

    def applyHint(self):
        row,col,val = self.getHint()
        if (row != None and col != None and val != set()):
            self.puzzle.updateBoardValue(row,col,val)
    
class sudokuSolver(LegalValues):
    def __init__(self,board):
        super().__init__(board)
        self.puzzle = board

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
        
#if __name__ == '__main__': copied from https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/
if __name__ == '__main__':
    board = [[6,0,0,1,3,2,4,0,9],
             [7,3,4,0,0,0,0,6,0],
             [2,1,0,0,6,0,0,0,8],
             [9,0,6,8,0,0,0,4,5],
             [8,5,1,3,0,0,7,0,0],
             [0,0,0,2,0,0,0,0,1],
             [0,0,0,4,0,0,0,0,3],
             [3,4,0,9,0,5,0,8,0],
             [1,9,0,6,8,0,0,5,0]]

    sudoku_board = sudokuBoard(board)
    hint = sudokuHints(sudoku_board)
    '''for i in range(9):
        print('-------------')
        print(f'Row {i}')
        for key in hint.legal_numbers_hint:
            if (key[0] == i):
                print(key,hint.legal_numbers_hint[key])
        print('--------------')
        hint.getHint(row=i)
        print('--------------')
        for key in hint.legal_numbers_hint:
            if (key[0] == i):
                print(key,hint.legal_numbers_hint[key])
    print("----------------------")
    for i in range(9):
        print('-------------')
        print(f'Col {i}')
        for key in hint.legal_numbers_hint:
            if (key[1] == i):
                print(key,hint.legal_numbers_hint[key])
        print('--------------')
        hint.getHint(col=i)
        print('--------------')
        for key in hint.legal_numbers_hint:
            if (key[1] == i):
                print(key,hint.legal_numbers_hint[key])
    '''

from cmu_graphics import *
from sudoku_solver import *
from difficulty_screen import app
from PIL import Image
import math
import copy
import random


def readFile(path):
    with open(path, "rt") as f:
        return f.read()
    
#Learned random.choice() from https://www.w3schools.com/python/ref_random_choice.asp
def getBoards(difficulty):
    boards = []
    for filename in os.listdir('boards'):
        if filename.endswith('.txt') and filename.startswith(f'{difficulty.lower()}'):
            pathToFile = f'boards/{filename}'
            fileContents = readFile(pathToFile)
            current_board = []
            for row in fileContents.splitlines():
                board = []
                for i in row.split(' '):
                    board.append(int(i))
                current_board.append(board)
            boards.append(current_board)
    return random.choice(boards)

def initializeBoard(app):
    app.board_color = []
    for row in range(9):
        current_row = [] 
        for col in range(9):
            if (app.user_board.getBoardValue(row,col) != 0):
                current_row.append('skyBlue')
            else:
                current_row.append(None)
        app.board_color.append(current_row)

def initializeUserLegals(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            if (app.board[row][col] == 0):
                app.user_legal_values[(row,col)] = set()

def resetBoardLayout(app):
    for current_row in range(9):
        for current_col in range(9):
            if (app.board_color[current_row][current_col] == 'deepSkyBlue'):
                app.board_color[current_row][current_col] = None

#Copied from TP Resources Image Demos
def gameScreen_onAppStart(app):
    app.current_difficulty = app.difficulty if (app.difficulty != '') else 'evil'
    app.cellSelected = (None,None)
    app.rows = app.cols = 9
    app.hint_row = None
    app.hint_col = None
    app.hint_val = 0
    app.cellBorderWidth = 1
    app.boardWidth = app.boardHeight = 790
    app.boardLeft = app.boardTop = 5
    app.board = getBoards(app.current_difficulty)
    app.solved_board = sudokuSolver(sudokuBoard(copy.deepcopy(app.board))).solveSudoku()
    app.user_board = sudokuBoard(copy.deepcopy(app.board))
    app.legal_values = LegalValues(app.user_board)
    app.user_legal_values = dict()
    app.auto = False
    app.solve = False
    app.manual = False
    app.edit = False
    app.game_over = False
    app.move = 0
    app.hints = sudokuHints(app.user_board)
    initializeUserLegals(app)
    initializeBoard(app)

def gameScreen_onScreenActivate(app):
    if ((app.current_difficulty != app.difficulty and app.difficulty != '') or app.game_over): 
        reset(app)

def cellSelected(app,x,y):
    cellWidth,cellHeight = getCellSize(app)
    dx = x - app.boardLeft
    dy = y - app.boardTop
    row = math.floor(dy/cellHeight)
    col = math.floor(dx/cellWidth)
    if (0 <= row < app.rows and 0 <= col < app.cols):
        if (app.board_color[row][col] != 'skyBlue'):
            resetBoardLayout(app)
            app.board_color[row][col] = 'deepSkyBlue'
            app.cellSelected = (row,col)

def gameScreen_onMousePress(app,mouseX,mouseY):
    cellSelected(app,mouseX,mouseY)

def drawButtons(app):
    for i in range(len(app.game_images)):
        app.game_images[i].drawButton()

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def getCellLeftTop(app,row,col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

#Update the cell colors
def checkCell(app,row,col):
    cell_number = app.user_board.getBoardValue(row,col)
    if (cell_number != app.solved_board[row][col] and cell_number != 0):
        app.board_color[row][col] = 'red'
    elif (app.board[row][col] == cell_number and app.board[row][col] != 0):
        app.board_color[row][col] = 'skyBlue'
    elif (app.hint_row != None and app.hint_col != None and 
        app.board[app.hint_row][app.hint_col] == 0 and
        app.cellSelected != (app.hint_row,app.hint_col)):
        app.board_color[app.hint_row][app.hint_col] = 'yellow'
    else:
        app.board_color[row][col] = None
    
    if (app.edit and app.cellSelected != (None,None)):
        row,col = app.cellSelected
        app.board_color[row][col] = 'deepSkyBlue'

def drawCell(app,row,col):
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    cell_number = app.user_board.getBoardValue(row,col)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
            fill=app.board_color[row][col], border='black',
            borderWidth=app.cellBorderWidth)
    checkCell(app,row,col)
    #If legal mode draw legal values
    if (app.auto or app.manual):
        drawLegal(app,row,col)
    if (cell_number != 0):
        drawLabel(f'{cell_number}',cellLeft+44,cellTop+44,size=50)
    

def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols): 
            drawCell(app,row,col)

#Draws the legal values
def drawLegal(app,row,col):
    legal_values = None
    if (app.auto == True):
        legal_values = app.legal_values.legal_numbers
    if (app.manual == True):
        legal_values = app.user_legal_values
    if ((row,col) not in legal_values):
        return 
    if (app.user_board.getBoardValue(row,col) != 0):
        return 
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    legals = legal_values[(row,col)]
    for i in range(1,10):
        if i in legals: 
            drawLabel(i,cellLeft+13+(30*((i-1)%3)),cellTop+15+(30*((i-1)//3)),size=20)

#Pressable Keys
def gameScreen_onKeyPress(app,key):
    cell_row,cell_col = app.cellSelected
    if (key == 'escape'):
        setActiveScreen('mainScreen')

    if (key == 'backspace' and (cell_row,cell_col) != (None,None)):
        if (app.edit):
            app.user_legal_values[(cell_row,cell_col)] = set()
            return
        app.user_board.clearBoardValue(cell_row,cell_col)
        app.board_color[cell_row][cell_col] = None 
        if (app.hint_row != None and app.hint_col != None):
            app.board_color[app.hint_row][app.hint_col] = 'yellow'
        app.legal_values.initializeLegalNumbers()

    if (key.isdigit() and (cell_row,cell_col) != (None,None)):
        key = int(key)
        if (1 <= key <= 9):
            if (not app.edit):
                app.user_board.updateBoardValue(cell_row,cell_col,key)
                checkCell(app,cell_row,cell_col)
                app.legal_values.initializeLegalNumbers()
                if (app.hint_row == cell_row and app.hint_col == cell_col):
                    app.hint_row = None
                    app.hint_col = None
                app.move+=1
            else:
                if (key in app.user_legal_values[(cell_row,cell_col)]):
                    app.user_legal_values[(cell_row,cell_col)].remove(key) 
                else:
                    app.user_legal_values[(cell_row,cell_col)].add(key)

    if (key == 'l'):
        app.auto = not app.auto
        app.manual = False
        app.edit = False

    if (key == 'm'):
        app.manual = not app.manual
        app.edit = False
        app.auto = False
        
    if (key == 'e' and app.manual and not app.auto):
        app.edit = not app.edit

    if (key == 'n'):
        new_game(app)

    if (key == 'h' and app.hint_row == None and app.hint_col == None):
        app.hint_row,app.hint_col,app.hint_val = app.hints.getHint()
        if (app.hint_row == None and app.hint_col == None and app.hint_val == set()):
            return
        app.board_color[app.hint_row][app.hint_col] = 'yellow'

    if (key == 'a'):
        if (app.hint_row == None and app.hint_col == None):
            app.hints.applyHint()
            app.legal_values.initializeLegalNumbers()
        else:
            app.user_board.updateBoardValue(app.hint_row,app.hint_col,app.hint_val)
            app.legal_values.initializeLegalNumbers()
            app.board_color[app.hint_row][app.hint_col] = None
            app.hint_row,app.hint_col = None,None
        app.move+=1

    if (key == 'space'):
        gameOver(app)

def gameOver(app):
    app.game_over = True
    for row in range(9):
        for col in range(9):
            if (app.user_board.getBoardValue(row,col) != app.solved_board[row][col]):
                setActiveScreen('gameOverScreen')
                return
    setActiveScreen('congratulationScreen')
    

def drawBorder(app):
    drawRect(0,0,app.width,app.height,fill=None,border='black',borderWidth=10)
    cellWidth,cellHeight = getCellSize(app)
    for i in range(9):
        row,col = i // 3 * 3,i % 3 * 3
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        cellLeft,cellTop = getCellLeftTop(app,start_row,start_col)
        drawRect(cellLeft,cellTop,cellWidth*3,cellHeight*3,fill=None,border='black',borderWidth=5)

def new_game(app):
    app.board = getBoards(app.current_difficulty)
    app.solved_board = sudokuSolver(sudokuBoard(copy.deepcopy(app.board))).solveSudoku()
    app.user_board = sudokuBoard(copy.deepcopy(app.board))
    app.legal_values = LegalValues(app.user_board)
    initializeBoard(app)

def reset(app):
    app.current_difficulty = app.difficulty
    app.board = getBoards(app.current_difficulty)
    app.solved_board = sudokuSolver(sudokuBoard(copy.deepcopy(app.board))).solveSudoku()
    app.user_board = sudokuBoard(copy.deepcopy(app.board))
    app.legal_values = LegalValues(app.user_board)
    app.hints = sudokuHints(app.user_board)
    app.hint_row = None
    app.hint_col = None
    app.cellSelected = (None,None)
    app.auto = False
    app.solve = False
    app.manual = False
    app.edit = False
    app.move = 0
    initializeBoard(app)

def gameScreen_redrawAll(app):
    drawGrid(app)
    drawBorder(app)
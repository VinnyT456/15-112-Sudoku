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
                current_row.append(rgb(192,214,232))
            else:
                current_row.append(None)
        app.board_color.append(current_row)

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
    app.cellBorderWidth = 1
    app.boardWidth = app.boardHeight = 790
    app.boardLeft = app.boardTop = 5
    app.board = getBoards(app.current_difficulty)
    app.solved_board = sudokuSolver(sudokuBoard(copy.deepcopy(app.board))).solveSudoku()
    app.user_board = sudokuBoard(copy.deepcopy(app.board))
    app.legal_values = LegalValues(app.user_board)
    initializeBoard(app)

def gameScreen_onScreenActivate(app):
    if (app.current_difficulty != app.difficulty and app.difficulty != ''): 
        app.current_difficulty = app.difficulty
        app.board = getBoards(app.current_difficulty)
        app.solved_board = sudokuSolver(sudokuBoard(copy.deepcopy(app.board))).solveSudoku()
        app.user_board = sudokuBoard(copy.deepcopy(app.board))
        app.legal_values = LegalValues(app.user_board)
        initializeBoard(app)

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

def checkCell(app,row,col):
    cell_number = app.user_board.getBoardValue(row,col)
    if (cell_number != app.solved_board[row][col] and cell_number != 0):
        app.board_color[row][col] = 'red'
    elif (app.board[row][col] == cell_number and app.board[row][col] != 0):
        app.board_color[row][col] = 'skyBlue'
    else:
        app.board_color[row][col] = None

def drawCell(app,row,col):
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    cell_number = app.user_board.getBoardValue(row,col)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
            fill=app.board_color[row][col], border='black',
            borderWidth=app.cellBorderWidth)
    checkCell(app,row,col)
    if (cell_number != 0):
        drawLabel(f'{cell_number}',cellLeft+44,cellTop+44,size=50)
    

def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols): 
            drawCell(app,row,col)

def drawLegal(app,row,col):
    if ((row,col) not in app.legal_values.legal_numbers):
        return 

def gameScreen_onKeyPress(app,key):
    row,col = app.cellSelected
    if (key == 'escape'):
        setActiveScreen('mainScreen')
    if (key == 'backspace' and (row,col) != (None,None)):
        app.user_board.clearBoardValue(row,col)
        app.board_color[row][col] = None
    if (key.isdigit() and (row,col) != (None,None)):
        key = int(key)
        if (1 <= key <= 9):
            app.user_board.updateBoardValue(row,col,key)
            checkCell(app,row,col)
            app.legal_values.initializeLegalNumbers()
    if (key == 'r'):
        reset(app)

def drawBorder(app):
    drawRect(0,0,app.width,app.height,fill=None,border='black',borderWidth=10)
    cellWidth,cellHeight = getCellSize(app)
    for i in range(9):
        row,col = i // 3 * 3,i % 3 * 3
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        cellLeft,cellTop = getCellLeftTop(app,start_row,start_col)
        drawRect(cellLeft,cellTop,cellWidth*3,cellHeight*3,fill=None,border='black',borderWidth=5)

def reset(app):
    app.board = getBoards(app.current_difficulty)
    app.solved_board = sudokuSolver(sudokuBoard(copy.deepcopy(app.board))).solveSudoku()
    app.user_board = sudokuBoard(copy.deepcopy(app.board))
    app.legal_values = LegalValues(app.user_board)
    initializeBoard(app)

def gameScreen_redrawAll(app):
    drawGrid(app)
    drawBorder(app)
    for key,val in app.legal_values.legal_numbers.items():
        print(f"{key} | {val}")
    print("________________________")
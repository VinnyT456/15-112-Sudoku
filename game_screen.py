from cmu_graphics import *
from sudoku_solver import *
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
        if filename.endswith('.txt') and filename.startswith(f'{difficulty}'):
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

def resetBoardLayout(app):
    for current_row in range(9):
        for current_col in range(9):
            if (app.board_color[current_row][current_col] == 'deepSkyBlue'):
                app.board_color[current_row][current_col] = None

#Copied from TP Resources Image Demos
def gameScreen_onAppStart(app):
    app.cellSelected = (None,None)
    app.rows = 9
    app.cols = 9
    app.cellBorderWidth = 1
    app.boardWidth = 790
    app.boardHeight = 790
    app.boardLeft = 5
    app.boardTop = 5
    app.board = getBoards('easy')
    app.solved_board = sudokuSolver(sudokuBoard(copy.deepcopy(app.board))).solveSudoku()
    app.user_board = sudokuBoard(copy.deepcopy(app.board))
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

def drawCell(app,row,col):
    cellWidth,cellHeight = getCellSize(app)
    cellLeft,cellTop = getCellLeftTop(app,row,col)
    cell_number = app.user_board.getBoardValue(row,col)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
            fill=app.board_color[row][col], border='black',
            borderWidth=app.cellBorderWidth)
    if (cell_number != 0):
        drawLabel(f'{cell_number}',cellLeft+44,cellTop+44,size=50)

def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols): 
            drawCell(app,row,col)

def gameScreen_onKeyPress(app,key):
    row,col = app.cellSelected
    if (key == 'escape'):
        setActiveScreen('mainScreen')
    if (key == 'backspace' and (row,col) != (None,None)):
        app.board.clearBoardValue(row,col)
    if (key.isdigit() and (row,col) != (None,None)):
        if (1 <= int(key) <= 9):
            app.user_board.updateBoardValue(row,col,key)
    if (key == 'r'):
        app.board = sudokuBoard(getBoards('easy'))
        initializeBoard(app)
        
def drawBorder(app):
    drawRect(0,0,app.width,app.height,fill=None,border='black',borderWidth=10)
    cellWidth,cellHeight = getCellSize(app)
    for i in range(9):
        row,col = i // 3 * 3,i % 3 * 3
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        cellLeft,cellTop = getCellLeftTop(app,start_row,start_col)
        drawRect(cellLeft,cellTop,cellWidth*3,cellHeight*3,fill=None,border='black',borderWidth=5)

def gameScreen_redrawAll(app):
    drawGrid(app)
    drawBorder(app)
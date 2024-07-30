from cmu_graphics import *
from PIL import Image
import os
import random

class Buttons:
    def __init__(self,name,image,x_coord,y_coord,width,height):
        self.name = name
        self.image = image
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height

    def drawButton(self):
        drawRect(self.x_coord+5,self.y_coord,self.width-10,self.height,fill=None)
        drawImage(self.image,self.x_coord,self.y_coord)

    def checkButtonClick(self,app,x,y):
        left = self.x_coord
        right = self.x_coord+self.width
        top = self.y_coord
        bottom = self.y_coord+self.height
        if (left <= x <= right and top <= y <= bottom):
            self.buttonAction(app)

    def buttonAction(self,app):
        #Copied width and height from image demos
        #Learned random.choice from tp resources
        app.board_image = random.choice(app.difficulty_boards[self.name])
        app.difficulty = self.name.lower()
    
#Learned random.choice() from https://www.w3schools.com/python/ref_random_choice.asp
#Learned Image.resize from https://www.geeksforgeeks.org/python-pil-image-resize-method/
def getBoards(app,difficulty):
    boards = []
    for filename in os.listdir('tp-starter-files/board-images'):
        if filename.endswith('.png') and filename.startswith(f'{difficulty.lower()}'):
            path = f'tp-starter-files/board-images/{filename}'
            image = (Image.open(path))
            image = CMUImage(image)
            boards.append(image)
    app.difficulty_boards[difficulty] = boards

def initializeImageBoard(app):
    positions = {
        'Easy':(5,10,150,90),
        "Medium":(165,10,150,90),
        "Hard":(325,10,150,90),
        "Expert":(485,10,150,90),
        "Evil":(645,10,150,90)
    }
    for name in positions:
        getBoards(app,name)
        image = (Image.open(f"button_image/{name}.png"))
        image = CMUImage(image)
        x_coord,y_coord,width,height = positions[name]
        app.difficulty_images.append(Buttons(name,image,x_coord,y_coord,width,height))

#Copied from TP Resources Image Demos
def difficultyScreen_onAppStart(app):
    app.difficulty_images = []
    app.difficulty_boards = {
        'Easy':[],
        'Medium':[],
        'Hard':[],
        'Expert':[],
        'Evil':[]
    }
    app.difficulty = ''
    app.board_image = None
    initializeImageBoard(app)

def difficultyScreen_onScreenActivate(app):
    app.board_image = None

def difficultyScreen_onMousePress(app,mouseX,mouseY):
    for i in range(len(app.difficulty_images)):
        app.difficulty_images[i].checkButtonClick(app,mouseX,mouseY)
    
def difficultyScreen_onKeyPress(app,key):
    if (key == 'escape'):
        setActiveScreen('mainScreen')

#Copied from TP Resources Image Demo
def difficultyScreen_redrawAll(app):
    for i in range(len(app.difficulty_images)):
        app.difficulty_images[i].drawButton()
    if (app.board_image != None):
        drawImage(app.board_image,75,125,width=650,height=650)
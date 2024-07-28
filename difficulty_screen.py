from cmu_graphics import *
from PIL import Image

class Buttons:
    def __init__(self,name,image,x_coord,y_coord,width,height):
        self.name = name
        self.image = image
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height

    def drawButton(self):
        #drawRect(self.x_coord+5,self.y_coord,self.width-10,self.height,fill=None)
        drawImage(self.image,self.x_coord,self.y_coord)

    def checkButtonClick(self,x,y):
        left = self.x_coord
        right = self.x_coord+self.width
        top = self.y_coord
        bottom = self.y_coord+self.height
        if (left <= x <= right and top <= y <= bottom):
            self.buttonAction()

    def buttonAction(self):
        pass

def initializeImage(app):
    positions = {
        'Easy':(10,10,160,110),
        "Medium":(180,10,160,110),
        "Hard":(350,10,160,110),
        "Expert":(520,10,160,110),
    }
    for name in positions:
        image = (Image.open(f"button_image/{name}.png"))
        image = CMUImage(image)
        x_coord,y_coord,width,height = positions[name]
        app.difficulty_images.append(Buttons(name,image,x_coord,y_coord,width,height))

#Copied from TP Resources Image Demos
def difficultyScreen_onAppStart(app):
    app.difficulty_images = []
    initializeImage(app)

def difficultyScreen_onMousePress(app,mouseX,mouseY):
    for i in range(len(app.difficulty_images)):
        app.difficulty_images[i].checkButtonClick(mouseX,mouseY)
    
def difficultyScreen_onKeyPress(app,key):
    if (key == 'escape'):
        setActiveScreen('mainScreen')

def difficultyScreen_redrawAll(app):
    for i in range(len(app.difficulty_images)):
        app.difficulty_images[i].drawButton()
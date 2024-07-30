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
        drawRect(self.x_coord+5,self.y_coord,self.width-10,self.height,fill=None)
        drawImage(self.image,self.x_coord,self.y_coord)

    def checkButtonClick(self,x,y):
        left = self.x_coord
        right = self.x_coord+self.width
        top = self.y_coord
        bottom = self.y_coord+self.height
        if (left <= x <= right and top <= y <= bottom):
            self.buttonAction()

    def buttonAction(self):
        if (self.name == "Start"):
            setActiveScreen('helpScreen')
        if (self.name == "Difficulty"):
            setActiveScreen('difficultyScreen')
        if (self.name == "Help"):
            setActiveScreen('helpScreen')

def initializeImage(app):
    positions = {
        'Start':(190,560,410,70),
        'Difficulty':(190,640,410,70),
        'Help':(190,720,410,70),
        "Light Blue1":(0,0,100,100),
        "Light Blue2":(560,0,100,100)
    }
    for name in positions:
        image = (Image.open(f"button_image/{name}.png"))
        image = CMUImage(image)
        x_coord,y_coord,width,height = positions[name]
        app.main_images.append(Buttons(name,image,x_coord,y_coord,width,height))

#Copied from TP Resources Image Demos
def mainScreen_onAppStart(app):
    app.main_images = []
    initializeImage(app)

def mainScreen_onMousePress(app,mouseX,mouseY):
    for i in range(len(app.main_images)):
        app.main_images[i].checkButtonClick(mouseX,mouseY)

def mainScreen_redrawAll(app):
    for i in range(len(app.main_images)):
        app.main_images[i].drawButton()
from cmu_graphics import *
from game_over_screen import app

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
        drawRect(self.x_coord+5,self.y_coord,self.width,self.height,fill=None)
        drawImage(self.image,self.x_coord,self.y_coord)

#Copied from TP Resources Image Demos
def initializeImageBoard(app):
    positions = {
        'congratulations':(105,5,0.1,0.1),
        'solved':(105,90,0.1,0.1),
        'moves':(105,175,0.1,0.1),
        'restart':(175,260,0.1,0.1),
    }
    for name in positions:
        image = (Image.open(f"button_image/{name}.png"))
        image = CMUImage(image)
        x_coord,y_coord,width,height = positions[name]
        app.congratulation_images.append(Buttons(name,image,x_coord,y_coord,width,height))

#Copied from TP Resources Image Demos
def congratulationScreen_onAppStart(app):
    app.congratulation_images = []
    initializeImageBoard(app)

#Game over Screen
def congratulationScreen_onKeyPress(app,key):
    if (key.lower() == 'r'):
        setActiveScreen('gameScreen')
    if (key == 'escape'):
        setActiveScreen('mainScreen')

def congratulationScreen_redrawAll(app):
    for i in range(len(app.congratulation_images)):
        app.congratulation_images[i].drawButton()
    drawLabel(app.move,605,210,size=50)
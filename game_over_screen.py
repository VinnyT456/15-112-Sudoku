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
        'game over':(105,5,0.1,0.1),
        'not solved':(105,90,0.1,0.1),
        'moves 1':(105,175,0.1,0.1),
        'restart 1':(175,260,0.1,0.1),
    }
    for name in positions:
        image = (Image.open(f"button_image/{name}.png"))
        image = CMUImage(image)
        x_coord,y_coord,width,height = positions[name]
        app.game_over_images.append(Buttons(name,image,x_coord,y_coord,width,height))

#Copied from TP Resources Image Demos
def gameOverScreen_onAppStart(app):
    app.game_over_images = []
    initializeImageBoard(app)

#Game over Screen
def gameOverScreen_onKeyPress(app,key):
    if (key.lower() == 'r'):
        setActiveScreen('gameScreen')
    if (key == 'escape'):
        setActiveScreen('mainScreen')

def gameOverScreen_redrawAll(app):
    for i in range(len(app.game_over_images)):
        app.game_over_images[i].drawButton()
    drawLabel(app.move,605,210,size=50)
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
        'Instructions':(195,5,0.1,0.1),
        'Enter':(5,100,0.1,0.1),
        'Game':(5,180,0.1,0.1),
        'Back':(5,270,0.1,0.1),
        'Hint':(425,270,0.1,0.1),
        'New':(5,350,0.1,0.1),
        'Apply':(425,350,0.1,0.1),
        'Undo':(5,430,0.1,0.1),
        'Automatic':(425,430,0.1,0.1),
        'Manual':(5,510,0.1,0.1),
        'Edit':(425,510,0.1,0.1),
    }
    for name in positions:
        image = (Image.open(f"button_image/{name}.png"))
        image = CMUImage(image)
        x_coord,y_coord,width,height = positions[name]
        app.help_images.append(Buttons(name,image,x_coord,y_coord,width,height))

#Copied from TP Resources Image Demos
def helpScreen_onAppStart(app):
    app.help_images = []
    initializeImageBoard(app)
    
def helpScreen_onKeyPress(app,key):
    if (key == 'enter'):
        setActiveScreen('gameScreen')
    if (key == 'escape'):
        setActiveScreen('mainScreen')

def helpScreen_redrawAll(app):
    for i in range(len(app.help_images)):
        app.help_images[i].drawButton()
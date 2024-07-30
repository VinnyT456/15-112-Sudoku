from cmu_graphics import *
from PIL import Image

import os

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

    def checkButtonClick(self,app,x,y):
        left = self.x_coord
        right = self.x_coord+self.width
        top = self.y_coord
        bottom = self.y_coord+self.height
        if (left <= x <= right and top <= y <= bottom):
            self.buttonAction(app)

def initializeImageBoard(app):
    positions = {
        'Instructions':(195,5,0.1,0.1),
        'Enter':(5,100,0.1,0.1),
        'Back':(5,195,0.1,0.1),
        'Hint':(425,195,0.1,0.1),
        'New':(5,290,0.1,0.1),
        'Apply':(425,290,0.1,0.1),
        'Undo':(5,385,0.1,0.1),
        'Automatic':(425,385,0.1,0.1),
        'Manual':(5,490,0.1,0.1),
        'Edit':(425,490,0.1,0.1),
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

'''def helpScreen_onMousePress(app,mouseX,mouseY):
    app.main_images[-1].checkButtonClick(mouseX,mouseY)
    app.main_images[-2].checkButtonClick(mouseX,mouseY)'''
    
def helpScreen_onKeyPress(app,key):
    if (key == 'enter'):
        setActiveScreen('gameScreen')
    if (key == 'escape'):
        setActiveScreen('mainScreen')

def helpScreen_redrawAll(app):
    for i in range(len(app.help_images)):
        app.help_images[i].drawButton()
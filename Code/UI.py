from cmu_graphics import *
from PIL import *
import os
import pathlib
import random


class Button:
    def __init__(self, sizeTuple, x, y, image, buttonName):
        # x is top left corner
        # y is general height
        # image is ment to fit within the rectangle of the thing being pressed
        self.sizeTuple = sizeTuple
        self.x = x
        self.y = y
        self.image = image
        self.pressed = False
        self.buttonName = buttonName

    def pressButton(self):
        self.pressed = True

    def __repr__(self):
        return f"The button is located at (X:{self.x}, Y:{self.y}) and is called {self.buttonName}"

    def isButtonClicked(self, app, mouseX, mouseY):
        # only run this onMousePressed
        # check if the  mouse is within the rectangle of the button and is being pressed
        if self.x <= mouseX <= self.sizeTuple[0]+self.x and self.y <= mouseY <= self.sizeTuple[1]+self.y:
            return True
        return False

    def buttonAction(self, action):
        return action

    def drawButton(self, app):
        drawRect(self.x, self.y,
                 self.sizeTuple[0], self.sizeTuple[1], fill="Red")
        temp = Image.open(self.image)
        drawImage(self.image, self.x, self.y,
                  width=self.sizeTuple[0], height=self.sizeTuple[1])


class Banner:
    def __init__(self, alignmnet, app, List):
        self.alignmnet = alignmnet
        # group is the cmu_graphics group which allows us to create groups of
        # polygons
        # self.group = group
        self.isActive = True
        self.x = 0
        self.y = 0
        self.width = app.width
        self.height = 30
        color = "blue"
        self.List = []

    def drawBanner(self, app):
        drawRect(0, 0, self.width, self.height, fill="blue")
        for i in self.List:
            # print(i)
            for elem in i:
                # print(elem)
                # print(elem[0])
                if isinstance(elem[0], str):
                    drawLabel(elem[0], elem[1], elem[2], size=20)
                elif isinstance(elem[0], int):
                    drawRect(elem[0], elem[1], 20, 20,)
                    # Create banner and in the group align each element specifically to a space in the screen


class Panel:
    def __init__(self, buttonList, app, x, y, enabled, sizeTuple, image):
        self.buttonList = buttonList
        self.app = app
        self.x = x
        self.y = y
        self.enabled = enabled
        self.sizeTuple = sizeTuple
        self.image = image

    def __repr__(self):
        return f"Panel X:{self.x},Y:{self.y} with buttons{self.buttonList}"

    def drawPanel(self, app):
        # This will assume that the banner will usually be bigger for the buttons
        drawRect(self.x, self.y, self.sizeTuple[0], self.sizeTuple[1])
        temp = Image.open(self.image)
        drawImage(self.image, self.x, self.y,
                  width=self.sizeTuple[0], height=self.sizeTuple[1])
        for button in self.buttonList:
            button.drawButton(app)


class IntentionIcon:
    def __init__(self, app, sizeTuple, image, name):
        self.app = app
        self.enabled = True
        self.sizeTuple = sizeTuple
        self.image = image
        self.name = name

    @staticmethod
    def drawIcon(enemy):
        # This will assume that the banner will usually be bigger for the buttons
        drawRect(enemy.x, enemy.y + 20, 40, 40, fill=None)

        temp = Image.open(f"{enemy.intention}Intent.png")
        image = f"{enemy.intention}Intent.png"
        drawImage(image, enemy.x, enemy.y + 20,
                  width=40, height=40)

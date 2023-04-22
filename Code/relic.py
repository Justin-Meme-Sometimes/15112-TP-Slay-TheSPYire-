from cmu_graphics import *
from PIL import *
import os
import pathlib
import random


class relic:
    def __init__(self, name, type, rectCoords):
        self.name = name
        self.type = type
        self.rectCoords = rectCoords

    def drawRelic(self, x, y):
        drawRect(x, y,
                 self.rectCoords[0]+1, self.rectCoords[1]+1, fill="Red")
        temp = Image.open(self.image)
        drawImage(self.image, x, y,
                  width=self.rectCoords[0], height=self.rectCoords[1])

    def isMouseTouching(self, app, mouseX, mouseY):
        # TODO check if the card is being touched by the mouse
        if self.x <= mouseX <= self.rectCoords[0]+self.x and self.y <= mouseY <= self.rectCoords[1]+self.y:
            return True
        return False

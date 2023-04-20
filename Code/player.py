from cmu_graphics import *
from PIL import *
import os
import pathlib
import random


class Player:
    def __init__(self, health, energy, cardPlayedPerTurn, rectSize, image, x, y):
        self.health = health
        self.energy = energy
        self.cardPlayedPerTurn = cardPlayedPerTurn
        self.rectSize = rectSize
        self.image = image
        self.x = x
        self.y = y
        self.effects = {"poision": 0, "strength": 0, "dexterity": 0, }

    def drawPlayer(self):
        drawRect(self.x, self.y,
                 self.rectSize[0]+1, self.rectSize[1]+1, fill="White")
        temp = Image.open(self.image)
        drawImage(self.image, self.x, self.y,
                  width=self.rectSize[0], height=self.rectSize[1])
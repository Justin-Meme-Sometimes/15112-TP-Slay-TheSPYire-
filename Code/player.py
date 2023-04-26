from cmu_graphics import *
from PIL import *
import os
import pathlib
import random


class Player:
    def __init__(self, health, energy, cardPlayedPerTurn, rectSize, image, x, y, relicList):
        self.health = health
        self.maxHealth = health
        self.energy = energy
        self.cardPlayedPerTurn = cardPlayedPerTurn
        self.rectSize = rectSize
        self.maxEnergy = 3
        self.image = image
        self.x = x
        self.y = y
        self.strength = 0
        self.dex = 0
        self.currentDefense = 0
        self.effects = {"poision": 0, "strength": 0, "dexterity": 0, }
        self.relicList = relicList
        self.attacksDone = 0
        self.cardPlayed = None
        self.gold = 0

    def drawPlayer(self):
        drawRect(self.x, self.y,
                 self.rectSize[0]+1, self.rectSize[1]+1, fill=None)
        temp = Image.open(self.image)
        drawImage(self.image, self.x, self.y,
                  width=self.rectSize[0], height=self.rectSize[1])

    def isPlayerAlive(self):
        return self.health >= 0

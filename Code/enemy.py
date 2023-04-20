from cmu_graphics import *
from PIL import *
import os
import pathlib
import random


class Enemy:
    def __init__(self, name, health, image, animationList, type, x, y, rectCoords):
        self.name = name
        self.health = health
        self.image = image
        self.animationList = animationList
        self.type = type
        self.x = x
        self.y = y
        self.currentDefense = 0
        self.rectCoords = rectCoords
        self.effects = {"poision": 0, "strength": 0, "dexterity": 0, }

    def __repr__(self):
        return f"This enemy has is {self.name} that has {self.health} with {self.type}"

    def doSkill(self, action, parameter):
        return action(parameter)

    def isDead(self):
        return self.health <= 0

    def drawEnemy(self):
        drawRect(self.x, self.y,
                 self.rectCoords[0]+1, self.rectCoords[1]+1, fill="White", borderWidth=10)
        temp = Image.open(self.image)
        drawImage(self.image, self.x, self.y,
                  width=self.rectCoords[0], height=self.rectCoords[1])

    def isMouseTouching(self, app, mouseX, mouseY, isPlayerTurn, isLineOnEnemy):
        # TODO check if the card is being touched by the mouse
        if self.x <= mouseX <= self.rectCoords[0]+self.x and self.y <= mouseY <= self.rectCoords[1]+self.y:
            if isPlayerTurn == "Player Turn" and isLineOnEnemy == True:
                print("Enemy has been targeted and casted on")
                return True
        return False

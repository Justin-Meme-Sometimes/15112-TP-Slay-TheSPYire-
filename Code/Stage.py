from cmu_graphics import *
from PIL import *


class Stage:
    def __init__(self, type, stageNumber, enemyList, background, player, deck, gold):
        self.type = type
        self.stageNumber = stageNumber
        self.enemies = enemyList
        self.backgroundImage = background
        self.player = player
        self.deck = deck
        self.gold = gold

    def __repr__(self):
        return f"The node is {self.type} type and is {self.row}"

    def nextStage(self):
        self.stageNumber += 1

    def drawBackground(self, app):
        temp = Image.open(self.backgroundImage)
        drawImage(self.backgroundImage, 0, 0,
                  width=400, height=400)

    def stageHandler(self):
        if self.type == "Combat":
            print("CombatStage")
        elif self.type == "Shop":
            print("ShopStage")
        elif self.type == "Boss":
            print("Boss Stage")

    def showShop(self):
        pass


class Map:
    def __init__(self, NodeList, floor):
        self.NodeList = NodeList
        self.floor = floor

    def __repr__(self):
        return f"This Floor is the {self.floor}th floor"

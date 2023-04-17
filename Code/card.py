from cmu_graphics import *
from PIL import *
import os
import pathlib
import random


class Card:
    def __init__(self, image, energyCost, skill, name, rectCoords, app):
        self.image = image
        self.energyCost = energyCost
        self.skill = skill
        self.name = name
        self.cardType = None
        self.rectCoords = rectCoords
        self.x = None
        self.y = None

    def __repr__(self):
        return f"The card has {self.energyCost} and {self.name}"

    def __hash__(self):
        return hash(str(self))

    def isMouseTouching(self, app, mouseX, mouseY):
        # TODO check if the card is being touched by the mouse
        print(self.x, self.rectCoords[0]+self.x, mouseX)
        print(self.y, self.y+self.rectCoords[1], mouseY)
        if self.x <= mouseX <= self.rectCoords[0]+self.x and self.y <= mouseY <= self.rectCoords[1]+self.y:
            print(f"{self} is being touched currently")
            return True
        # if self.Rect.contains(mouseX, mouseY):
            # return True
        return False

    def drawCard(self, app, x, y):
        drawRect(x, y,
                 self.rectCoords[0]+1, self.rectCoords[1]+1, fill="Red")
        temp = Image.open(self.image)
        drawImage(self.image, x, y,
                  width=self.rectCoords[0], height=self.rectCoords[1])

    def setCoords(self, x, y):
        self.x = x
        self.y = y


class SkillCard(Card):
    def __init__(self, image, energyCost, skill, name):
        super.__init__(image, energyCost, skill, name)
        super.cardType = "skill"


class AttackCard(Card):
    def __init__(self, image, energyCost, skill, name):
        super.__init__(image, energyCost, skill, name)
        super.cardType = "attack"

    def attackEnemy():
        return "Attack Enemy"


class ColorlessCard(Card):
    def __init__(self, image, energyCost, skill, name):
        super.__init__(image, energyCost, skill, name)
        super.cardType = "colorless"


class Deck:
    def __init__(self, cardList):
        self.cards = cardList

    def shuffle(self):
        random.shuffle(self.cards)

    def discard(self, card):
        if (isinstance(card, Card) or isinstance(card, SkillCard) or isinstance(card, AttackCard) or
                isinstance(card, ColorlessCard)):
            self.cards.remove(card)
        return None

    def isTouchingCard(self, app, mouseX, mouseY):
        for card in self.cards:
            if card.isMouseTouching(app, mouseX, mouseY):
                return card
        return None

    def drawDeck(self, app):
        offsetX = 0
        for c in self.cards:
            offsetX += 30
            c.drawCard(app, offsetX+40, 330)
            c.setCoords(offsetX+40, 330)

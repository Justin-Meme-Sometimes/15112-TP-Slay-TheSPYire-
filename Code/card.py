from cmu_graphics import *
from PIL import *
import os
import pathlib
import random
from player import Player
from enemy import Enemy


class Card:
    initial = 40

    def __init__(self, image, energyCost, skill, name, rectCoords, app):
        self.image = image
        self.energyCost = energyCost
        self.skill = skill
        self.name = name
        self.cardType = None
        self.armor = 0
        self.rectCoords = rectCoords
        if self != None:
            self.x = Card.initial + 70
            Card.initial += 40
        self.y = 330
        self.clicked = False
        self.damageDone = 0

    def __repr__(self):
        return f"card: {self.energyCost} and {self.name}"

    def __hash__(self):
        return hash(str(self))

    def isMouseTouching(self, app, mouseX, mouseY):
        # TODO check if the card is being touched by the mouse
        # print(self.x, self.rectCoords[0]+self.x, mouseX)
        # print(self.y, self.y+self.rectCoords[1], mouseY)
        if self.x <= mouseX <= self.rectCoords[0]+self.x and self.y <= mouseY <= self.rectCoords[1]+self.y:
            # print(f"{self}touched")
            return True
        # if self.Rect.contains(mouseX, mouseY):
            # return True
        return False

    def drawCard(self, app, x, y):
        drawRect(x, y,
                 self.rectCoords[0]+1, self.rectCoords[1]+1, fill=None)
        temp = Image.open(self.image)
        drawImage(self.image, x, y,
                  width=self.rectCoords[0], height=self.rectCoords[1])

    def setCoords(self, x, y):
        self.x = x
        self.y = y

    def attackEnemy(self, damageAmount, type, target, player):
        damageAmount += player.strength
        if type == "Physical":
            if target.currentDefense > damageAmount:
                currentDamage = target.currentDefense - damageAmount
            else:
                currentDamage = damageAmount - target.currentDefense
            print(target.currentDefense)
            target.currentDefense -= damageAmount
            if target.currentDefense < 0:
                target.currentDefense = 0
            target.health = (
                target.health) - currentDamage
            if target.health > target.maxHealth:
                target.health = target.maxHealth
            # damageDone = (target.health + target.currentDefense) - damageAmount
            return f"Damage Done was {currentDamage}"
        if type == "Poison":
            target.effects["poision"] += 1
            return f"Applied Poison to {target.name}"


class SkillCard(Card):
    def __init__(self, image, energyCost, skill, name):
        super.__init__(image, energyCost, skill, name)
        super.cardType = "skill"


class AttackCard(Card):
    def __init__(self, image, energyCost, skill, name):
        super.__init__(image, energyCost, skill, name)
        super.cardType = "attack"

    def attacksEnemy(self, damageAmount, type, target):
        if type == "Physical":
            target.health = (target.health + target.armor) - (damageAmount)
            damageDone = (target.health + target.armor) - damageAmount
            return f"Damage Done was {damageDone}"
        if type == "Poison":
            target.effects["poision"] += 1
            return f"Applied Poison to {target.name}"


class ColorlessCard(Card):
    def __init__(self, image, energyCost, skill, name):
        super.__init__(image, energyCost, skill, name)
        super.cardType = "colorless"


class Deck:
    def __init__(self, cardList):
        self.cards = cardList

    def shuffle(self):
        random.shuffle(self.cards)

    def add(self, card):
        if len(self.cards) >= 1:
            card.x = self.cards[-1].x + 40
            card.y = 330
        else:
            card.x = 40+70
            card.y = 330
        self.cards.append(card)

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

    def drawDeck(self, app, x):
        offsetX = 0
        for c in self.cards:
            offsetX += 40
            c.drawCard(app, c.x, c.y)
            c.setCoords(c.x, c.y)

    def positionToNextCard(self, card, deck):
        # Measure the position of this card to the next card in the hand of cards
        pass

    def initialPosition(self, app):
        L = []
        offsetX = 0
        for c in self.cards:
            offsetX += 40
            # print(c, c.x, c.y)
            L.append((0 + offsetX+70, 330))

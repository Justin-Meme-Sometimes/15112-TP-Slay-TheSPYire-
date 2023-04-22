from cmu_graphics import *
from PIL import *
import os
import pathlib
import random
from player import Player


class Enemy:
    def __init__(self, name, health, image, hitSpriteSheet, type, x, y, rectCoords, defenseRange, attackRange, empowerRange, empowerType, debuffRange):
        self.name = name
        self.maxHealth = health
        self.health = health
        self.image = image
        self.hitSpriteSheet = hitSpriteSheet
        self.type = type
        self.x = x
        self.y = y
        self.currentDefense = 0
        self.armor = 0
        self.rectCoords = rectCoords
        self.strength = 0
        self.dex = 0
        self.effects = {"poision": 0, "strength": 0, "dexterity": 0, }
        self.hitAnimationList = []
        self.spriteCounter = 0
        self.defenseRange = defenseRange
        self.attackRange = attackRange
        self.empowerRange = empowerRange
        self.debuffRange = debuffRange
        self.intention = "Attack"
        self.hasAttackedRecently = False

    def __repr__(self):
        return f"This enemy has is {self.name} that has {self.health} with {self.type}"

    def doSkill(self, action, parameter):
        return action(parameter)

    def instaniateSpritesHitSheet(self):
        spritestrip = openImage(self.hitSpriteSheet)
        for i in range(3):
            sprite = CMUImage(spritestrip.crop(
                (64+64*i, 0, 128+64*i, )))
            self.hitAnimationList.append(sprite)

    def isDead(self):
        return self.health <= 0

    def attack(self, player, damage):
        player.health = (player.currentDefense + player.health) - \
            (damage + self.strength)
        if player.health > player.maxHealth:
            player.health = player.maxHealth

    def debuff(self, player, debuffAmount):
        player.strength -= debuffAmount

    def defend(self, shieldAmount):
        self.currentDefense += shieldAmount

    def empower(self, empowerAmount):
        self.strength += empowerAmount

    def metallicize(self, amount):
        self.dexterity += amount

    def drawEnemy(self):
        drawRect(self.x, self.y,
                 self.rectCoords[0]+1, self.rectCoords[1]+1, fill="White", borderWidth=10)
        temp = Image.open(self.image)
        drawImage(self.image, self.x, self.y,
                  width=self.rectCoords[0], height=self.rectCoords[1])

    def drawEnemyAttack(self, enemyAnimationList):
        pass

    def drawEnemyEffects(self, enemyEffectsList):
        pass

    def drawEnemyHitList(self, enemyHitList, spriteCounter):
        sprite = enemyHitList[spriteCounter]
        drawImage(sprite, 200, 200)

    def isMouseTouching(self, app, mouseX, mouseY, isPlayerTurn, isLineOnEnemy):
        # TODO check if the card is being touched by the mouse
        if self.x <= mouseX <= self.rectCoords[0]+self.x and self.y <= mouseY <= self.rectCoords[1]+self.y:
            if isPlayerTurn == "Player Turn" and isLineOnEnemy == True:
                print("Enemy has been targeted and casted on")
                return True
        return False


def openImage(fileName):
    return Image.open(os.path.join(pathlib.Path(__file__).parent, fileName))

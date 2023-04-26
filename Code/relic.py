from cmu_graphics import *
from PIL import *
from UI import Banner
from card import Card
from card import Deck
from UI import Button
from UI import Panel
from battleTurn import StateMachine
from player import Player
from enemy import Enemy
import os
import pathlib
import random
from Stage import Stage
from Stage import Map


class relic:
    relicSet = {"Red Skull", "Kunai", "Anchor",
                "Nunchaku", "The Boot", "Bloodied Cross", "Chains"}

    def __init__(self, name, type, rectCoords, image, cost):
        self.name = name
        self.type = type
        self.rectCoords = rectCoords
        self.image = image
        self.x = 0
        self.y = 0
        self.cost = cost
        self.applied = False

    def drawRelic(self, x, y):
        drawRect(x, y,
                 self.rectCoords[0]+1, self.rectCoords[1]+1, fill=None)
        temp = Image.open(self.image)
        drawImage(self.image, x, y,
                  width=self.rectCoords[0], height=self.rectCoords[1])
        self.x = x
        self.y = y

    def isMouseTouching(self, app, mouseX, mouseY):
        # TODO check if the card is being touched by the mouse
        if self.x <= mouseX <= self.rectCoords[0]+self.x and self.y <= mouseY <= self.rectCoords[1]+self.y:
            return True
        return False

    @staticmethod
    def relicHandler(player, turn):
        for relic in player.relicList:
            if relic.name in relic.relicSet:
                if relic.name == "RedSkull":
                    if player.health <= (player.maxHealth / 2) and relic.applied == False:
                        relic.applied = True
                        player.strength += 5
                    if player.health >= (player.maxHealth / 2):
                        relic.applied = False
                elif relic.name == "Kunai":
                    if turn == "Player Turn":
                        player.dex += 1
                elif relic.name == "Anchor":
                    if turn == "Player Turn" and relic.applied == False:
                        player.currentDefense += 10
                        relic.applied = True
                elif relic.name == "Nunchaku":
                    if player.attacksDone % 10 == 0 and player.attacksDone >= 10:
                        if turn == "Player Turn":
                            player.energy += 1
                elif relic.name == "Bloodided Cross":
                    player.canCrit == True
                elif relic.name == "Chains":
                    player.strength = player.strength + 3
                    player.health = player.health - 5
                elif relic.name == "The Boot":
                    player.health += 10
                    if player.health > player.maxHealth:
                        player.health = player.maxHealth
        # player.cardPlayed = None
        # player.cardPlayed.damageDone = 0

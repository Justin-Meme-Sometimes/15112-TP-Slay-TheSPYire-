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


def onAppStart(app):
    app.image = 10
    # can pass app into the in the constuctor in objects
    # app.image  = Image.open("images/dog.jpg")
    # app.imageFlipped = CMUImage(app.imageFlipped)
    # buttons(app)
    app.player = Player(100, 4, 0, (120, 120),
                        "images/PlayerSprite.png", 90, 200)
    app.e1 = Enemy("Python", 100, "images/PythonEnemySprite.png",
                   [], "Easy Mob", 300, 200, (100, 100))
    app.enemies = [app.e1]
    app.stateMachine = StateMachine(app.player, app.enemies, "PlayerTurn")
    app.et = Button((60, 20), 300, 350, "images/endTurnButton.png", "End Turn")
    app.opD = Button((60, 20), 300, 320,
                     "images/openDeckButton.png", "Open Deck")
    cardList = initialCardList(app)
    app.d = Deck(cardList)
    app.cardLine = False
    app.currCardCoords = (None, None)
    app.globalMouseX = 0
    app.globalMouseY = 0
    app.currentCard = None
    app.clickedCard = None
    app.deckCoords = [(c.x, c.y) for c in app.d.cards]
    app.previousCard = None
    app.turn = "Player Turn"


def initialCardList(app):
    app.c = Card("images/testCard.png", 4, 4, "Test Card", (40, 40), app)
    app.r = Card("images/RedCard.png", 1, 3, "Red Card", (40, 40), app)
    app.b = Card("images/BrownCard.png", 3, 2, "Brown Card", (40, 40), app)
    app.bl = Card("images/blackCard.png", 1, 2, "Black Card", (40, 40), app)
    return [app.c, app.r, app.b, app.bl]


def buttons(app):
    # app.et = Button((20, 60), 200, 300, "images/endTurnButton.png", "End Turn")
    pass


def turnHandler(app):
    if app.turn == "Player Effects Turn":
        for enemy in app.enemies:
            for key in enemy.effects:
                if key == "poision":
                    enemy.health -= enemy.effects["poision"]
                    enemy.effects["poision"] -= 1
                elif key == "strength":
                    enemy.Strength += enemy.effects["strength"]
                elif key == "dexertity":
                    enemy.dexertity += enemy.effects["dexertity"]
    elif app.turn == "Enemy Effects Turn":
        for key in app.player.effects:
            if key == "poision":
                app.player.health -= app.player.effects["poision"]
                app.player.effects["poision"] -= 1
            elif key == "strength":
                app.player.Strength += app.player.effects["strength"]
            elif key == "dexertity":
                app.player.dexertity += app.player.effects["dexertity"]
    elif app.turn == "Enemy Turn":
        for enemy in app.enemies:
            # Create Algothorithim for AI here
            enemy.attack()


def redrawAll(app):
    banner1 = Banner(20, app, [])
    # drawImage(app.image, 100, 100, align = "center")
    potionButtonList = [(100, 5), (150, 5), (200, 5)]
    LabelGroupList = [("Name:", 40, 20)]
    banner1.List.append(potionButtonList)
    banner1.List.append(LabelGroupList)
    banner1.drawBanner(app)
    app.et.drawButton(app)
    app.d.drawDeck(app, 0)
    app.opD.drawButton(app)
    app.player.drawPlayer()
    for enemy in app.enemies:
        enemy.drawEnemy()
    # app.c.drawCard(app, 30, 30)
    if app.cardLine == True:
        if app.clickedCard != None:
            drawLine(
                app.globalMouseX, app.globalMouseY, app.clickedCard.x, app.clickedCard.y, fill="black")


def onKeyPress(app, key):
    pass


def onStep(app):
    if app.clickedCard != None:
        if app.clickedCard.clicked == True:
            app.cardLine = True
    else:
        app.cardLine = False


def endTurn(app):
    # print("Turn Ended")
    # print(app.turn)
    app.turn = app.stateMachine.nextTurn(app.turn)
    print(app.turn)


def doDamage(defaultParameter):
    print("Do damage!")


def onMousePress(app, mouseX, mouseY):
    app.previousClicked = app.clickedCard
    app.clickedCard = app.d.isTouchingCard(app, mouseX, mouseY)
    # app.currentCard = currentCard

    if app.e1.isMouseTouching(
            app, mouseX, mouseY, app.turn, app.cardLine):
        print(app.previousClicked)
        if app.previousClicked in app.d.cards:
            app.deckCoords.pop(app.d.cards.index(app.previousClicked))
            app.d.discard(app.previousClicked)
    if (app.et.isButtonClicked(app, mouseX, mouseY)):
        app.et.buttonAction(endTurn(app))
    if app.clickedCard != None:
        app.clickedCard.clicked = not app.clickedCard.clicked


def onMouseMove(app, mouseX, mouseY):
    app.currentCard = app.d.isTouchingCard(app, mouseX, mouseY)
    app.globalMouseX, app.globalMouseY = mouseX, mouseY
    # if app.currentCard != None:
    # print(app.currentCard.clicked)
    if app.currentCard != None and app.currentCard.isMouseTouching(app, mouseX, mouseY):
        if app.currentCard != app.previousCard:
            if app.previousCard != None:
                correctCoords(app.d.cards, app.d.initialPosition(app))
            # print(app.previousCard, app.currentCard)
            moveDeck(app.d.cards, app.currentCard, app)
        app.currentCard.rectCoords = (60, 60)
        for card in app.d.cards:
            if card != app.currentCard:
                card.rectCoords = (40, 40)
        app.previousCard = app.currentCard

    elif app.currentCard == None:
        correctCoords(app.d.cards, app.deckCoords)
        for card in app.d.cards:
            card.rectCoords = (40, 40)
            app.previousCard = None


def correctCoords(M, L):
    if L != None:
        for i in range(len(L)):
            M[i].x, M[i].y = L[i][0], L[i][1]


def moveDeck(L, card, app):
    if card not in L or len(L) == 1 or L == None or card == None:
        return None
    length = len(L)
    position = None
    for i in range(length):
        if L[i] == card:
            position = i
    for cardPos in range(length):
        if L[cardPos] != None:
            if cardPos < position:
                # print(L[cardPos].x)
                # print(L[cardPos], L[cardPos].x)
                # correctCoords(app.d.cards, app.d.initialPosition(app))
                L[cardPos].x -= 50
                # print(L[cardPos].x)
            elif cardPos > position:
                # correctCoords(app.d.cards, app.d.initialPosition(app))
                L[cardPos].x += 50


def onMouseDrag(app, mouseX, mouseY):
    pass


def Main():
    runApp()


Main()

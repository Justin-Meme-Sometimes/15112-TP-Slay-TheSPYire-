from cmu_graphics import *
from PIL import *
from UI import Banner
from card import Card
from card import Deck
from UI import Button
from UI import Panel
import os
import pathlib


def onAppStart(app):
    app.image = 10
    # can pass app into the in the constuctor in objects
    # app.image  = Image.open("images/dog.jpg")
    # app.imageFlipped = CMUImage(app.imageFlipped)
    # buttons(app)
    app.et = Button((60, 20), 300, 350, "images/endTurnButton.png", "End Turn")
    app.opD = Button((60, 20), 300, 320,
                     "images/openDeckButton.png", "Open Deck")
    cardList = initialCardList(app)
    app.d = Deck(cardList)


def initialCardList(app):
    app.c = Card("images/testCard.png", 4, 4, "Test Card", (40, 40), app)
    app.r = Card("images/RedCard.png", 1, 3, "Red Card", (40, 40), app)
    app.b = Card("images/BrownCard.png", 3, 2, "Brown Card", (40, 40), app)
    app.bl = Card("images/blackCard.png", 1, 2, "Black Card", (40, 40), app)
    return [app.c, app.r, app.b, app.bl]


def buttons(app):
    # app.et = Button((20, 60), 200, 300, "images/endTurnButton.png", "End Turn")
    pass


def redrawAll(app):
    banner1 = Banner(20, app, [])
    # drawImage(app.image, 100, 100, align = "center")
    potionButtonList = [(100, 5), (150, 5), (200, 5)]
    LabelGroupList = [("Name:", 40, 20)]
    banner1.List.append(potionButtonList)
    banner1.List.append(LabelGroupList)
    banner1.drawBanner(app)
    app.et.drawButton(app)
    app.d.drawDeck(app)
    app.opD.drawButton(app)
    # app.c.drawCard(app, 30, 30)


def onKeyPress(app, key):
    pass


def onStep(app):
    pass


def endTurn():
    print("Turn Ended")


def doDamage(defaulParameter):
    print("Do damage!")


def onMousePress(app, mouseX, mouseY):
    currentCard = app.d.isTouchingCard(app, mouseX, mouseY)
    if currentCard != None:
        currentCard.castSkill(doDamage(), None)

    if (app.et.isButtonClicked(app, mouseX, mouseY)):
        app.et.buttonAction(endTurn())


def Main():
    runApp()


Main()

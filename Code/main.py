from cmu_graphics import *
from PIL import *
from UI import Banner
from card import Card
from card import Deck
import os
import pathlib


def onAppStart(app):
    app.image = 10
    # can pass app into the in the constuctor in objects
    # app.image  = Image.open("images/dog.jpg")
    # app.imageFlipped = CMUImage(app.imageFlipped)
    app.c = Card("testCard.png", 4, 4, "Test Card", (40, 40), app)
    app.r = Card("RedCard.png", 1, 3, "Red Card", (40, 40), app)
    app.b = Card("BrownCard.png", 3, 2, "Brown Card", (40, 40), app)
    app.bl = Card("blackCard.png", 1, 2, "Black Card", (40, 40), app)
    cardList = [app.c, app.r, app.b, app.bl]
    app.d = Deck(cardList)


def redrawAll(app):
    banner1 = Banner(20, app, [])
    # drawImage(app.image, 100, 100, align = "center")
    potionButtonList = [(100, 5), (150, 5), (200, 5)]

    LabelGroupList = [("Name:", 40, 20)]
    banner1.List.append(potionButtonList)
    banner1.List.append(LabelGroupList)
    banner1.drawBanner(app)
    app.d.drawDeck(app)
    # app.c.drawCard(app, 30, 30)


def onKeyPress(app, key):
    pass


def onStep(app):
    pass


def onMouseDown(app, mouseX, mouseY):
    pass


def Main():
    runApp()


Main()

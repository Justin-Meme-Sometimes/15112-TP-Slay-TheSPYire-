from cmu_graphics import *
from PIL import Image
from UI import Banner
from card import Card


def onAppStart(app):
    app.image = 10
    # can pass app into the in the constuctor in objects
    # app.image  = Image.open("images/dog.jpg")
    # app.imageFlipped = CMUImage(app.imageFlipped)


def redrawAll(app):
    banner1 = Banner(20, app, [])
    # drawImage(app.image, 100, 100, align = "center")
    potionButtonList = [(100, 5), (150, 5), (200, 5)]

    LabelGroupList = [("Name:", 40, 20)]
    banner1.List.append(potionButtonList)
    banner1.List.append(LabelGroupList)
    banner1.drawBanner(app)


def onKeyPress(app, key):
    pass


def onStep(app):
    pass


def onMouseDown(app, mouseX, mouseY):
    pass


def Main():
    runApp()


Main()

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


def onAppStart(app):
    app.image = 10
    # can pass app into the in the constuctor in objects
    # app.image  = Image.open("images/dog.jpg")
    # app.imageFlipped = CMUImage(app.imageFlipped)
    # buttons(app)
    app.enemyIntentions = ["Attack", "Empower",
                           "Defend", "Metallicize", "Debuff"]
    app.player = Player(100, 4, 0, (90, 120),
                        "images/PlayerSprite.png", 90, 200)
    app.e1 = Enemy("Python", 100, "images/PythonEnemySprite.png",
                   "images/PythonEnemySpriteSheetHit.png", "Easy Mob", 240, 200, (60, 80), [3, 7], [3, 5], [2, 3], [4, 5], [3, 5])
    # app.e1.instaniateSpritesHitSheet()
    app.enemyWasRecentlyHit = False
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
    app.normalTimer = 5
    app.playerAnimationCurrently = True
    app.animationTimer = 20
    app.stepsPerSecond = 25
    app.displayLowEnergy = False
    app.lowEnergyCounter = 0
    app.turnTimer = 0
    app.turnHandlerBegin = False


def initialCardList(app):
    app.c = Card("images/testCard.png", 4, 4, "Test Card", (40, 40), app)
    app.r = Card("images/RedCard.png", 1, 3, "Red Card", (40, 40), app)
    app.b = Card("images/BrownCard.png", 3, 2, "Brown Card", (40, 40), app)
    app.bl = Card("images/blackCard.png", 1, 2, "Black Card", (40, 40), app)
    return [app.c, app.r, app.b, app.bl]


def buttons(app):
    # app.et = Button((20, 60), 200, 300, "images/endTurnButton.png", "End Turn")
    pass


def loadSpriteStrips(app):
    app.enemySpriteSheet = "images/PythonEnemySpriteSheetHit.png"


def turnHandler(app):
    if app.turn == "Player Effects":
        for enemy in app.enemies:
            for key in enemy.effects:
                if key == "poision":
                    enemy.health -= enemy.effects["poision"]
                    enemy.effects["poision"] -= 1
                elif key == "strength":
                    enemy.strength += enemy.effects["strength"]
                elif key == "dexerity":
                    enemy.dexertity += enemy.effects["dexertity"]
        app.turn = app.stateMachine.nextTurn(app.turn)
        print(app.turn, " Ended")
        # playPEffectsAnimation(app, app.player, app.enemies)
        # endTurn(app)
    if app.turn == "Enemy Turn":
        for enemy in app.enemies:
            # Create Algothorithim for AI here
            enemy.attack(app.player, 10)
            print(app.player.health)
        app.turn = app.stateMachine.nextTurn(app.turn)
        # playEnemyAttackAnim(app, app.player, app.enemies)
        # print(app.turn, " Ended")
    if app.turn == "Enemy Effects":
        for key in app.player.effects:
            if key == "poision":
                app.player.health -= app.player.effects["poision"]
                app.player.effects["poision"] -= 1
            elif key == "strength":
                app.player.strength += app.player.effects["strength"]
            elif key == "dexerity":
                app.player.dexertity += app.player.effects["dexertity"]
        app.turn = app.stateMachine.nextTurn(app.turn)
       # print(app.turn, " Ended")
        # playEEffectsAnimation(app, app.player, app.enemies)
        # preparePlayerTurn(app)
        # endTurn(app)
        # endTurn(app)


def prepareForNextPlayerTurn(app):
    app.player.energy = app.player.maxEnergy
    start = random.randrange(1, 2)
    finish = random.randrange(2, 4)+1
    print(start, finish)
    cardList = initialCardList(app)[start:finish]
    print(cardList)

    for card in cardList:
        if len(cardList) > 0:
            app.d.add(card)
    for card in cardList:
        print(card.x)
    for card in app.d.cards:
        if len(cardList) > 0:
            card.x -= 70
    app.deckCoords = [(c.x, c.y) for c in app.d.cards]
    for enemy in app.enemies:
        enemy.intention = app.enemyIntentions[random.randrange(
            0, len(app.enemyIntentions))]
        print(enemy.intention)


def intentionHandler(app):
    for enemy in app.enemies:
        if enemy.intention != None:
            if enemy.intention == "Attack":
                # Draw Intention
                enemy.attack(app.player, random.randrange(
                    enemy.attackRange[0], enemy.attackRange[1]))
                print("Enemy Attacked")
            elif enemy.intention == "Empower":
                enemy.empower(random.randrange(
                    enemy.empowerRange[0], enemy.empowerRange[1]))
                print("Enemy Empowered Themselves")
            elif enemy.intention == "Defend":
                enemy.defend(random.randrange(
                    enemy.defenseRange[0], enemy.defenseRange[1]))
                print("The Enemy Defendeed Themselves")
            elif enemy.intention == "Metallicize":
                enemy.metallicize(3)
                print("The Enemy is Preparing the Defend")
            elif enemy.intention == "Debuff":
                enemy.debuff(app.player, random.randrange(
                    enemy.debuffRange[0], enemy.debuffRange[1]))
                print("The Enemy is Debuffing")


def playerEffectsTurn(app):
    # app.playerAnimationCurrently = True
    for enemy in app.enemies:
        for key in enemy.effects:
            if key == "poision":
                enemy.health -= enemy.effects["poision"]
                enemy.effects["poision"] -= 1
            elif key == "strength":
                if enemy.strength - 1 >= 0:
                    enemy.strength -= 1
            elif key == "dexerity":
                if enemy.dexertity - 1 >= 0:
                    enemy.dexertity -= 1
    print(app.turn, "Ended")
    app.turn = app.stateMachine.nextTurn(app.turn)


def enemyTurn(app):
    for enemy in app.enemies:
        # Create Algothorithim for AI here
        intentionHandler(app)
        # print(app.player.health)
        # app.turnTimer += 1
    print(app.turn, "Ended")
    # Make sure to play an animation here
    app.turn = app.stateMachine.nextTurn(app.turn)


def enemyEffectsTurn(app):
    for key in app.player.effects:
        if key == "poision":
            app.player.health -= app.player.effects["poision"]
            app.player.effects["poision"] -= 1
        elif key == "strength":
            if app.player.strength - 1 >= 0:
                app.player.strength -= 1
        elif key == "dexerity":
            if app.player.dexerity - 1 >= 0:
                app.player.dexertity -= 1
    print(app.turn, "Ended")
    app.turn = app.stateMachine.nextTurn(app.turn)
    prepareForNextPlayerTurn(app)
    app.turnHandlerBegin = False


def playEnemyAttackAnim(app, player, enemies):
    pass


def playPEffectsAnimation(app, player, enemies):
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
    energyString = f"{app.player.energy}/{app.player.maxEnergy}"
    drawLabel("Energy", 20, 270, size=13)
    drawLabel(energyString, 20, 300, size=20)
    drawCircle(20, 300, 20, fill=None, border="black")
    if app.enemyWasRecentlyHit:
        # app.e1.drawEnemyHitList(app.e1.hitAnimationList, app.e1.spriteCounter)
        print("LOL")
    if app.displayLowEnergy:
        drawLabel("You do not have enough room to do this", 120, 150)


def onKeyPress(app, key):
    pass


def onStep(app):
    if app.playerAnimationCurrently:
        app.stepsPerSecond = 20
    if app.clickedCard != None:
        if app.clickedCard.clicked == True:
            app.cardLine = True
    else:
        app.cardLine = False
    for enemy in app.enemies:
        app.stateMachine.removeEnemy(enemy)
    if app.enemyWasRecentlyHit:
        app.e1.spriteCounter = (
            1 + app.e1.spriteCounter) % len(app.e1.hitAnimationList)
    if app.displayLowEnergy == True:
        app.lowEnergyCounter += 1
        if app.lowEnergyCounter == 75:
            app.displayLowEnergy = False
            app.lowEnergyCounter = 0
    if app.turnHandlerBegin == True:
        # print(app.turnTimer)
        app.turnTimer += 1
        if app.turnTimer == 75 and app.turn == "Player Effects":
            playerEffectsTurn(app)
            app.turnTimer = 0
        if app.turnTimer == 75 and app.turn == "Enemy Turn":
            enemyTurn(app)
            app.turnTimer = 0
        if app.turnTimer == 75 and app.turn == "Enemy Effects":
            enemyEffectsTurn(app)
            app.turnTimer = 0


def endTurn(app):
    # print("Turn Ended")
    # print(app.turn)
    app.turn = app.stateMachine.nextTurn(app.turn)
    print(app.turn)
    app.turnHandlerBegin = True
    # turnHandler(app)


def doDamage(defaultParameter):
    print("Do damage!")


def currentHandDiscard(app):
    app.deckCoords.pop(app.d.cards.index(app.previousClicked))
    app.d.discard(app.previousClicked)


def onMousePress(app, mouseX, mouseY):
    app.previousClicked = app.clickedCard
    app.clickedCard = app.d.isTouchingCard(app, mouseX, mouseY)
    # app.currentCard = currentCard
    # Do the math on shit

    if app.e1.isMouseTouching(
            app, mouseX, mouseY, app.turn, app.cardLine):
        print(app.previousClicked.energyCost)
        if app.previousClicked in app.d.cards and (app.player.energy - app.previousClicked.energyCost) > 0:
            app.player.energy -= app.previousClicked.energyCost
            app.previousClicked.attackEnemy(20, "Physical", app.e1)
            currentHandDiscard(app)
        else:
            app.displayLowEnergy = True
    if (app.et.isButtonClicked(app, mouseX, mouseY)):
        app.et.buttonAction(endTurn(app))
    if app.clickedCard != None:
        app.clickedCard.clicked = not app.clickedCard.clicked


def onMouseMove(app, mouseX, mouseY):
    app.currentCard = app.d.isTouchingCard(app, mouseX, mouseY)
    app.globalMouseX, app.globalMouseY = mouseX, mouseY
    if app.currentCard != None and app.currentCard.isMouseTouching(app, mouseX, mouseY):
        if app.currentCard != app.previousCard:
            if app.previousCard != None:
                correctCoords(app.d.cards, app.d.initialPosition(app))
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

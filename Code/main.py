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
from relic import relic


def onAppStart(app):

    app.relics = totalRelicList(app)
    app.gold = 0
    app.player = Player(100, 4, 0, (64, 96),
                        "images/PlayerSprite.png", 90, 240, [])
    app.ogPlayerPos = (90, 240)
    app.stageNumber = 1
    index = random.randrange(0, len(totalEnemyList(app)))
    app.enemies = [totalEnemyList(app)[index]]
    app.player.relicList = []
    app.backgroundImage = "/images/Backgroundimage1.png"
    app.d = Deck([])
    for card in initialCardList(app):
        app.d.add(card)
    app.stage = Stage("Combat", app.stageNumber, app.enemies,
                      app.backgroundImage, app.player, app.d, app.gold)
    app.deckCoords = [(c.x, c.y) for c in app.stage.deck.cards]
    app.ogEnemyPositions = [(enemy.x, enemy.y) for enemy in app.stage.enemies]
    initializeStage(app)


def initializeStage(app):
    app.et = Button((60, 20), 320, 130, "images/endTurnButton.png", "End Turn")
    app.opD = Button((60, 20), 320, 110,
                     "images/openDeckButton.png", "Open Deck")
    app.enemyAttackTimer = 0
    app.enemyIntentions = ["Attack", "Empower", "Defend", "Debuff"]
    app.cardLine = False
    app.deckCoords = [(c.x, c.y) for c in app.stage.deck.cards]
    app.currCardCoords = (None, None)
    app.globalMouseX = 0
    app.globalMouseY = 0
    app.currentCard = None
    app.clickedCard = None
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
    app.playerAttackAnim = False
    app.playerAttackTimer = 0
    app.stateMachine = StateMachine(app.stage.player, app.stage.enemies)
    app.stageWon = False
    app.ogEnemyPositions = [(enemy.x, enemy.y) for enemy in app.stage.enemies]
    app.stage.player.x, app.stage.player.y = app.ogPlayerPos[
        0], app.ogPlayerPos[1]
    app.showEndBanner = False


def startStage(app):
    app.stageNumber += 1
    # app.enemies.pop()
    if app.stage.type == "Combat" or app.stage.type == "Boss":
        app.stage = Stage("Shop", app.stageNumber, totalEnemyList(app)[1:],
                          app.backgroundImage, app.player, app.d, app.gold)

        app.endshop = Button((60, 20), 320, 130,
                             "images/endTurnButton.png", "End Shopping ")
        initializeStage(app)
    elif app.stage.type == "Shop":
        app.d = Deck([])
        for card in initialCardList(app):
            app.d.add(card)

        # prepareForNextPlayerTurn(app)
        app.stage = Stage("Combat", app.stageNumber, totalEnemyList(app),
                          app.backgroundImage, app.player, app.d, app.gold)
        initializeStage(app)
    # TODO load next stage


def drawBackground(app):
    currentFloor = 1
    backgroundImage = f"images/background{currentFloor}.png"
    temp = Image.open(backgroundImage)
    drawImage(backgroundImage, 0, 0,
              width=400, height=400)


def totalRelicList(app):
    app.r1 = relic("Red Skull", "Normal", (40, 40), "images/RedSkull.png", 50)
    app.r2 = relic("Kunai", "Normal", (40, 40), "images/Kunai.png", 50)
    app.r3 = relic("Anchor", "Normal", (40, 40), "images/Anchor.png", 50)
    app.r4 = relic("Nunchaku", "Normal", (40, 40),  "images/Nunchaku.png", 50)
    app.r5 = relic("The Boot", "Normal", (40, 40), "images/The Boot.png", 50)
    return [app.r1, app.r2, app.r3, app.r4, app.r5]


def totalEnemyList(app):

    # All assets were made by me and all code was written by me
    app.e1 = Enemy("Python", 100, "images/PythonEnemySprite.png",
                   "Easy Mob", 240, 250, (60, 80), [3, 7], [3, 15], [2, 3], [4, 5], [3, 5])
    app.e2 = Enemy("Lemon Slime", 50, "images/Lemon Slime.png",
                   "Easy Mob", 240, 260, (60, 80), [3, 7], [3, 15], [2, 3], [4, 5], [3, 5])
    app.e3 = Enemy("Turtle", 150, "images/Turtle Enemy.png", "Easy Mob",
                   240, 240, (100, 100), [5, 10], [2, 5], [0, 1], [5, 10], [2, 5])
    app.e4 = Enemy("Mimic", 50,  "images/MimicEnemy.png", "Easy Mob",
                   240, 200, (120, 120), [1, 2], [10, 20], [0, 5], [3, 10], [4, 5])
    app.e5 = Enemy("Merman", 200, "images/MermanSprite.png", "Easy Mob",
                   240, 200, (120, 120), [5, 5], [10, 12], [0, 5], [5, 5], [3, 5])
    app.e6 = Enemy("HauntedHelmet", 75, "images/HelmetEnemy.png", "Easy Mob",
                   240, 220, (100, 100), [20, 21], [0, 5], [3, 2], [3, 3], [1, 2])
    # app.e7 = Enemy("")
    img = Image.open(app.e6.image)
    pixels = img.load()  # create the pixel map

    img.putpixel((x, y), (255, 0, 0))
    return [app.e1, app.e2, app.e3, app.e4, app.e5, app.e6]


def initialCardList(app):
    app.ATK = Card("images/AttackCard.png", 0, 4, "Attack Card", (40, 40), app)
    app.ATK2 = Card("images/AttackCard.png", 0, 4,
                    "Attack Card", (40, 40), app)
    app.DEX = Card("images/DexCard.png", 1, 3, "Dex Card", (40, 40), app)
    app.DEF = Card("images/DefenseCard.png", 0, 2,
                   "Defense Card", (40, 40), app)
    app.STR = Card("images/StrengthCard.png", 1, 2,
                   "Strength Card", (40, 40), app)
    return [app.ATK, app.ATK2, app.DEF, app.STR]


def buttons(app):
    # app.et = Button((20, 60), 200, 300, "images/endTurnButton.png", "End Turn")
    pass


def prepareForNextPlayerTurn(app):
    app.player.currentDefense = 0
    app.player.energy = app.player.maxEnergy
    start = random.randrange(0, len(initialCardList(app)))
    card = initialCardList(app)[start]

    if len(app.d.cards) < 7:
        app.d.add(card)
        for card in app.d.cards:
            card.x -= 30
    app.deckCoords = [(c.x, c.y) for c in app.d.cards]
    for enemy in app.stage.enemies:
        enemy.intention = app.enemyIntentions[random.randrange(
            0, len(app.enemyIntentions))]
        print(enemy.intention)
    relic.relicHandler(app.stage.player, app.turn)


def intentionHandler(app):
    for enemy in app.stage.enemies:
        if enemy.intention != None:
            if enemy.intention == "Attack":
                # Draw Intention
                print(enemy.attack(app.player, random.randrange(
                    enemy.attackRange[0], enemy.attackRange[1])))
                enemy.hasAttackedRecently = True
                playEnemyAttackAnimation(app, enemy)
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
    app.stage.player.currentDefense += app.stage.player.dex
    for enemy in app.stage.enemies:
        enemy.currentDefense = 0
        for key in enemy.effects:
            if key == "poision":
                # enemy.health -= enemy.effects["poision"]
                enemy.effects["poision"] -= 1
            elif key == "strength":
                if enemy.strength - 1 >= 0:
                    enemy.strength -= 1
            elif key == "dexerity":
                if enemy.dex - 1 >= 0:
                    enemy.dex -= 1

    print(app.turn, "Ended")
    app.turn = app.stateMachine.nextTurn(app.turn)


def drawMap(app):
    app.map = Map()


def enemyTurn(app):
    # for enemy in app.stage.enemies:
    # Create Algothorithim for AI here
    intentionHandler(app)
    # print(app.player.health)
    # app.turnTimer += 1
    print(app.turn, "Ended")
    # Make sure to play an animation here
    app.turn = app.stateMachine.nextTurn(app.turn)


def enemyEffectsTurn(app):
    for enemy in app.stage.enemies:
        enemy.currentDefense += enemy.dex
    for key in app.stage.player.effects:
        if key == "poision":
            # app.player.health -= app.player.effects["poision"]
            app.stage.player.effects["poision"] -= 1
        elif key == "strength":
            if app.stage.player.strength - 1 >= 0:
                app.stage.player.strength -= 1
            if app.stage.player.strength < 0:
                app.stage.player.strength += 1
        elif key == "dexerity":
            if app.stage.player.dex - 1 >= 0:
                app.stage.player.dex -= 1
            if app.stage.player.dex < 0:
                app.stage.player.dex += 1
    print(app.turn, "Ended")
    app.turn = app.stateMachine.nextTurn(app.turn)
    prepareForNextPlayerTurn(app)
    app.turnHandlerBegin = False


def playPlayerAttackAnimation(app):
    for i in range(5):
        app.stage.player.x += (i*10)
    # app.player.x = app.ogPlayerPos[0]


def playEnemyAttackAnimation(app, enemy):
    if enemy.hasAttackedRecently:
        for i in range(5):
            enemy.x -= (i*10)


def playPEffectsAnimation(app, player, enemies):
    pass


def redrawAll(app):
    drawBackground(app)
    if app.stage.type == "Combat":
        if app.stage.player.isPlayerAlive():
            app.et.drawButton(app)
            if app.turn == "Player Turn":
                app.stage.deck.drawDeck(app, 0)
                # app.stage.Deck.resetDeck(app.stage.deck)
            app.opD.drawButton(app)
            app.stage.player.drawPlayer()
            for enemy in app.stage.enemies:
                enemy.drawEnemy()
            # app.c.drawCard(app, 30, 30)
            if app.cardLine == True:
                if app.clickedCard != None:
                    drawLine(
                        app.globalMouseX, app.globalMouseY, app.clickedCard.x, app.clickedCard.y, fill="black")
            energyString = f"{app.stage.player.energy}/{app.stage.player.maxEnergy}"
            drawLabel("Energy", 20, 270, size=13)
            drawLabel(energyString, 20, 300, size=20)
            drawCircle(20, 300, 20, fill=None, border="black")

            if app.displayLowEnergy:
                drawLabel("You do not have enough room to do this", 120, 150)
            pHealth = f"Health: {app.stage.player.health}"
            pSheild = f"Shield: {app.stage.player.currentDefense}"
            drawLabel(pHealth, app.stage.player.x+20, app.stage.player.y-30)
            drawLabel(pSheild, app.stage.player.x+20, app.stage.player.y-15)
            drawLabel(f"Eff: STR: {app.stage.player.strength} DEX: {app.stage.player.dex}",
                      app.stage.player.x+20, app.stage.player.y-45)
            drawLabel(f"Gold: {app.stage.player.gold}",
                      app.stage.player.x+20, app.stage.player.y-55)
            for enemy in app.stage.enemies:
                drawLabel(f"Health: {enemy.health}", enemy.x, enemy.y - 40)
                drawLabel(f"Shield: {enemy.currentDefense}",
                          enemy.x, enemy.y - 20)
                drawLabel(
                    f"Eff: STR: {enemy.strength} DEX: {enemy.dex}", enemy.x, enemy.y - 5)
        else:
            drawLabel("You Lost", 200, 200)
        if app.showEndBanner == True:
            drawEndBanner(app)
        offset = 0
        drawLabel("Relics", 33, 10, size=25)
        for relic in app.stage.player.relicList:
            relic.drawRelic(offset, 25)
            offset += 50
    elif app.stage.type == "Shop":
        app.endshop.drawButton(app)
        drawShop(app)


def drawEndBanner(app):
    # app.cardList(app)
    drawRect(150, 50, 150, 300, fill="lightSeaGreen")
    drawLabel("Pick A Card", 200, 75)


def drawShop(app):
    drawLabel("Buy Items", 200, 150, size=40)

    offset = 0

    for relic in app.relics:
        offset += 50
        relic.drawRelic(50 + offset, 200)
        # relic.x, relic.y = 50 + offset, 150
        drawLabel("50 C", relic.x, relic.y - 20)


def onKeyPress(app, key):
    pass


def onStep(app):
    if app.stateMachine.isCombatOver(app.stage) == "Stage Over":
        startStage(app)
    if app.stage.type == "Combat":
        if app.playerAnimationCurrently:
            app.stepsPerSecond = 20
        if app.clickedCard != None:
            if app.clickedCard.clicked == True:
                app.cardLine = True
        else:
            app.cardLine = False
        for enemy in app.stage.enemies:
            removedEnemy = app.stateMachine.removeEnemy(enemy)
            if removedEnemy != None:
                if removedEnemy.name == "Mimic":
                    app.stage.player.gold += 50
                else:
                    app.stageplayer.gold += 20
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
        if app.playerAttackAnim == True:
            app.playerAttackTimer += 1
            if app.playerAttackTimer == 5:
                app.stage.player.x = app.ogPlayerPos[0]
                app.playerAttackTimer = 0
                app.playerAttackAnim = False
        for enemy in app.stage.enemies:
            if enemy.hasAttackedRecently:
                app.enemyAttackTimer += 1
                if app.enemyAttackTimer == 15:
                    enemy.x = app.ogEnemyPositions[app.stage.enemies.index(
                        enemy)][0]
                    app.enemyAttackTimer = 0
                    enemy.hasAttackedRecently = False


def endTurn(app):
    # print(app.turn)
    app.turn = app.stateMachine.nextTurn(app.turn)
    print(app.turn)
    app.turnHandlerBegin = True


def currentHandDiscard(app):
    app.deckCoords.pop(app.d.cards.index(app.previousClicked))
    offset = 0
    for coord in range(len(app.deckCoords)):
        offset += 40
        app.deckCoords[coord] = (offset + 70, 330)
    app.d.discard(app.previousClicked)


def cardSkillHandler(app, card, enemy, player):
    if card.name == "Strength Card":
        player.strength += 1
    elif card.name == "Attack Card":
        card.attackEnemy(
            500, "Physical", enemy, app.stage.player)
        player.attacksDone += 1
    elif card.name == "Defense Card":
        player.currentDefense += 5
    elif card.name == "Dex Card":
        player.dex += 3


def onMousePress(app, mouseX, mouseY):
    if app.stage.type == "Combat":
        app.previousClicked = app.clickedCard
        app.clickedCard = app.d.isTouchingCard(app, mouseX, mouseY)

        for enemy in app.stage.enemies:
            if enemy.isMouseTouching(
                    app, mouseX, mouseY, app.turn, app.cardLine):
                if app.previousClicked in app.d.cards and (app.stage.player.energy - app.previousClicked.energyCost) > 0 and app.previousClicked != None:
                    app.stage.player.energy -= app.previousClicked.energyCost
                    cardSkillHandler(app, app.previousClicked,
                                     enemy, app.stage.player)
                    if app.playerAttackAnim == False:
                        playPlayerAttackAnimation(app)
                        app.playerAttackAnim = True
                    currentHandDiscard(app)
                else:
                    app.displayLowEnergy = True
        if (app.et.isButtonClicked(app, mouseX, mouseY)):
            app.et.buttonAction(endTurn(app))
        if app.clickedCard != None:
            app.clickedCard.clicked = not app.clickedCard.clicked
    if app.stage.type == "Shop":
        for relic in app.relics:
            if relic.isMouseTouching(app, mouseX, mouseY):
                if app.stage.player.gold >= relic.cost:
                    app.stage.player.relicList.append(relic)
                    app.relics.remove(relic)
        if app.endshop.isButtonClicked(app, mouseX, mouseY):
            startStage(app)


def onMouseMove(app, mouseX, mouseY):
    if app.stage.type == "Combat":
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

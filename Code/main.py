from cmu_graphics import *
from PIL import *
from UI import Banner
from card import Card
from card import Deck
from UI import Button
from UI import Panel
from UI import IntentionIcon
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
    app.stage = Stage("StartScreen", None, None, None, None, None, None)
    app.startGame = False
    app.startButton = Button((100, 50), 160, 220,
                             "images/StartButton.png", "startButton")
    app.floor = 1

    app.relics = totalRelicList(app)
    app.gold = 0
    app.player = Player(100, 4, 0, (64, 96),
                        "images/BetterPlayer.png", "images/BetterPlayerHit.png", 90, 240, [])
    app.ogPlayerPos = (90, 240)
    app.stageNumber = 1
    index = random.randrange(0, len(totalEnemyList(app)))
    app.enemies = [totalEnemyList(app)[index]]
    app.player.relicList = []
    app.backgroundImage = "/images/Backgroundimage1.png"
    app.d = Deck([])
    for card in initialCardList(app):
        app.d.add(card)
    app.deckCoords = [(c.x, c.y) for c in app.d.cards]
    app.stage = Stage("Combat", app.stageNumber, app.enemies,
                      app.backgroundImage, app.player, app.d, app.gold)
    app.deckCoords = [(c.x, c.y) for c in app.stage.deck.cards]
    app.ogEnemyPositions = [(enemy.x, enemy.y)
                            for enemy in app.stage.enemies]
    app.skillPoints = 0
    app.gameOver = False
    app.previousStage = app.stage.type
    intentIconList(app)
    initializeStage(app)


def initializeStage(app):
    app.et = Button((60, 20), 320, 130, "images/endTurnButton.png", "End Turn")
    app.opD = Button((60, 20), 320, 110,
                     "images/openDeckButton.png", "Open Deck")
    app.enemyAttackTimer = 0
    app.enemyIntentions = ["Attack", "Empower", "Defend", "Debuff"]
    app.cardLine = False
    if app.stage.deck != None:
        app.deckCoords = [(c.x, c.y) for c in app.stage.deck.cards]
    app.currCardCoords = (None, None)
    app.globalMouseX = 0
    app.globalMouseY = 0
    app.currentCard = None
    app.clickedCard = None
    app.previousCard = None
    app.turn = "Player Turn"
    app.turnCount = 0
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
    if app.stage.enemies != None:
        app.ogEnemyPositions = [(enemy.x, enemy.y)
                                for enemy in app.stage.enemies]
    if app.stage.player != None:
        app.stage.player.x, app.stage.player.y = app.ogPlayerPos[
            0], app.ogPlayerPos[1]
    app.showEndBanner = False
    app.enemyHitTimer = 0
    app.playerHitTimer = 0
    if app.stage.enemies != None:
        app.enemyImage = app.stage.enemies[0].image

    app.bombEffect = False
    app.bombCounter = 0


def intentIconList(app):
    app.attackItentIcon = IntentionIcon(
        app, (40, 40), "images/AttackEnemyIntent.png", "Attack")
    app.defendIntentIcon = IntentionIcon(
        app, (40, 40), "images/DefenseEnemyIntent.png", "Defense")
    app.empowerIntentIcon = IntentionIcon(
        app, (40, 40), "images/EmpowerIntent.png",  "Empower")
    app.debuffIntentIcon = IntentionIcon(
        app, (40, 40), "images/Debuff Intent.png", "Debuff")


def startStage(app):

    app.previousStage = app.stage.type
    if app.gameOver == True:
        app.stage = Stage("Game Over", app.floor, app.enemies,
                          app.backgroundImage, app.player, app.d, app.gold)
    app.floor += 1
    # app.enemies.pop()
    stageList = ["Combat", "Combat", "Combat", "Level Up", "Shop", "Shop",]
    if app.gameOver == False:
        currentStage = random.randrange(0, len(stageList))
        pickedStage = stageList[currentStage]
        if app.floor % 5 == 0 and app.floor != 0:
            pickedStage = "Boss"
        if pickedStage == "Combat":
            index = random.randrange(0, len(totalEnemyList(app)))
            app.enemies = [totalEnemyList(app)[index]]
            app.d = Deck([])
            for card in initialCardList(app)[:3]:
                app.d.add(card)
            app.enemies[0].health += app.floor * 5
            app.enemies[0].attackRange[1] += app.floor * 3
            app.stage = Stage(stageList[currentStage], app.floor, app.enemies,
                              app.backgroundImage, app.player, app.d, app.gold)
            initializeStage(app)
        elif pickedStage == "Shop":
            app.endshop = Button((60, 20), 320, 130,
                                 "images/endTurnButton.png", "End Shopping ")
            app.stage = Stage("Shop", app.stageNumber, totalEnemyList(app)[1:],
                              app.backgroundImage, app.player, app.d, app.gold)

            initializeStage(app)
        elif pickedStage == "Level Up":
            app.levelUpButtons = makeLevelUpButtons(app)
            app.endshop = Button((60, 20), 320, 130,
                                 "images/endTurnButton.png", "End Shopping ")
            app.stage = Stage("Level Up", app.stageNumber, totalEnemyList(app)[1:],
                              app.backgroundImage, app.player, app.d, app.gold)

        if pickedStage == "Boss":
            index = random.randrange(0, len(totalBossList(app)))
            app.enemies = [totalBossList(app)[index]]
            app.enemies[0].health += app.floor * 5
            app.enemies[0].attackRange[1] += app.floor * 3
            app.d = Deck([])
            for card in initialCardList(app)[:4]:
                app.d.add(card)
            app.stage = Stage("Boss", app.floor, app.enemies,
                              app.backgroundImage, app.player, app.d, app.gold)
            initializeStage(app)
    # if app.stage.type == "Combat" or app.stage.type == "Boss":
      # print("hello")

    # elif app.stage.type == "Shop":
       # app.d = Deck([])
        # for card in initialCardList(app):
        #   app.d.add(card)

        # prepareForNextPlayerTurn(app)
      #  app.stage = Stage("Combat", app.stageNumber, totalEnemyList(app),
        # app.backgroundImage, app.player, app.d, app.gold)
     #   initializeStage(app)


def makeLevelUpButtons(app):
    app.lvlUp1 = Button((20, 20), 260, 220,
                        "images/PlusButton.png", "HealButton")
    app.lvlUp2 = Button((20, 20), 260, 245,
                        "images/PlusButton.png", "StrengthButton")
    app.lvlUp3 = Button((20, 20), 260, 270,
                        "images/PlusButton.png", "HealthButton")
    app.lvlUp4 = Button((20, 20), 260, 295,
                        "images/PlusButton.png", "DexButton")
    return [app.lvlUp1, app.lvlUp2, app.lvlUp3, app.lvlUp4]
    # TODO load next stage


def levelUpButtonHandler(app, mouseX, mouseY):
    for button in app.levelUpButtons:
        if button.isButtonClicked(app, mouseX, mouseY):
            if (app.skillPoints >= 1):
                app.skillPoints -= 1
                player = app.stage.player
                if button.buttonName == "HealButton":
                    player.health += 10
                    if player.health > player.maxHealth:
                        player.health = player.maxHealth
                elif button.buttonName == "StrengthButton":
                    player.strength += 3
                elif button.buttonName == "HealthButton":
                    player.maxHealth += 20
                elif button.buttonName == "DexButton":
                    player.dex += 2


def drawBackground(app):
    currentFloor = 1
    backgroundImage = f"images/background{currentFloor}.png"
    temp = Image.open(backgroundImage)
    drawImage(backgroundImage, 0, 0,
              width=400, height=400)


def totalRelicList(app):
    app.r1 = relic("Red Skull", "Normal", (40, 40), "images/RedSkull.png", 100)
    app.r2 = relic("Kunai", "Normal", (40, 40), "images/Kunai.png", 50)
    app.r3 = relic("Anchor", "Normal", (40, 40), "images/Anchor.png", 20)
    app.r4 = relic("Nunchaku", "Normal", (40, 40),  "images/Nunchaku.png", 30)
    app.r5 = relic("The Boot", "Normal", (40, 40), "images/The Boot.png", 60)
    app.r6 = relic("Bloodied Cross", "Normal", (40, 40),
                   "images/BloodiedCross.png", 200)
    app.r7 = relic("Chains", "Normal", (40, 40),
                   "images/Chains.png", 50)
    return [app.r1, app.r2, app.r3, app.r4, app.r5, app.r6, app.r7]


def totalBossList(app):
    app.b1 = Enemy("Flamingo", 300,  "images/FlamingoBoss.png", "images/FlamingoBossHit.png", "Boss Mob",
                   240, 200, (120, 120), [15, 25], [10, 20], [0, 5], [3, 10], [4, 5], ["Defend", "Attack", "Attack", "Attack"])
    app.b2 = Enemy("Money", 275, "images/coinSprite.png", "images/coinSpriteHit.png", "Boss Mob",
                   240, 200, (120, 120), [15, 50], [10, 20], [0, 5], [5, 5], [3, 5], ["Attack", "Defend", "Defend", "Defend"])
    app.b3 = Enemy("Neptunes Trident", 200, "images/NeptunesTridentBoss.png", "images/NeptunesTridentBossHit.png", "Boss Mob",
                   240, 220, (100, 100), [10, 15], [20, 40], [3, 2], [3, 3], [1, 2], ["Empower", "Attack", "Attack", "Attack"])
    return [app.b1, app.b2, app.b3]


def totalEnemyList(app):

    # All assets were made by me and all code was written by me
    app.e1 = Enemy("Python", 100, "images/PythonEnemySprite.png", "images/PythonEnemySpriteHit.png",
                   "Easy Mob", 240, 250, (60, 80), [3, 9], [3, 15], [2, 3], [4, 5], [3, 5], ["Attack", "Attack", "Attack", "Debuff"])
    app.e2 = Enemy("Lemon Slime", 50, "images/Lemon Slime.png", "images/Lemon SlimeHit.png",
                   "Easy Mob", 240, 260, (60, 80), [5, 10], [3, 15], [2, 3], [4, 5], [3, 5], ["Attack", "Attack", "Debuff", "Debuff"])
    app.e3 = Enemy("Turtle", 150, "images/Turtle Enemy.png", "images/Turtle EnemyHit.png", "Easy Mob",
                   240, 240, (100, 100), [5, 10], [5, 10], [0, 1], [5, 10], [2, 5], ["Attack", "Defend", "Defend", "Debuff"])
    app.e4 = Enemy("Mimic", 50,  "images/MimicEnemy.png", "images/MimicEnemyHit.png", "Easy Mob",
                   240, 200, (120, 120), [1, 2], [10, 20], [0, 5], [3, 10], [4, 5], ["Attack", "Debuff", "Debuff", "Debuff"])
    app.e5 = Enemy("Merman", 200, "images/MermanSprite.png", "images/MermanSpriteHit.png", "Easy Mob",
                   240, 200, (120, 120), [5, 5], [10, 12], [0, 5], [5, 5], [3, 5], ["Attack", "Empower", "Attack", "Empower"])
    app.e6 = Enemy("HauntedHelmet", 75, "images/HelmetEnemy.png", "images/HelmetEnemyHit.png", "Easy Mob",
                   240, 220, (100, 100), [20, 21], [1, 5], [3, 2], [3, 3], [1, 2], ["Attack", "Defend", "Debuff", "Debuff"])

    return [app.e1, app.e2, app.e3, app.e4, app.e5, app.e6]


def forbiddenCards(app):
    app.BOMB = Card("images/BombCard.png", 3, 4, "Bomb Card", (40, 40), app)
    app.RUN = Card("images/RunCard.png", 0, 4, "Run Card," (40, 40), app)
    return [app.BOMB, app.RUN]


def initialCardList(app):
    app.ATK = Card("images/AttackCard.png", 1, 4, "Attack Card", (40, 40), app)
    app.ATK2 = Card("images/AttackCard.png", 1, 4,
                    "Attack Card", (40, 40), app)
    app.DEX = Card("images/DexCard.png", 1, 3, "Dex Card", (40, 40), app)
    app.DEF = Card("images/DefenseCard.png", 2, 2,
                   "Defense Card", (40, 40), app)
    app.STR = Card("images/StrengthCard.png", 1, 2,
                   "Strength Card", (40, 40), app)
    return [app.ATK, app.ATK2, app.DEF, app.STR, app.DEX]


def buttons(app):
    # app.et = Button((20, 60), 200, 300, "images/endTurnButton.png", "End Turn")
    pass


def prepareForNextPlayerTurn(app):
    app.player.currentDefense = 0
    app.player.energy = app.player.maxEnergy
    start = random.randrange(0, 19)
    # card = initialCardList(app)[start]
    card = initialCardList(app)[0]
    if 0 <= start <= 9:
        card = initialCardList(app)[0]
    elif 9 < start <= 13:
        card = initialCardList(app)[1]
    elif 13 < start <= 17:
        card = initialCardList(app)[2]
    elif 17 < start <= 18:
        card = initialCardList(app)[3]
    elif 18 < start < 19:
        card = initialCardList(app)[4]

    if len(app.d.cards) < 7:
        app.d.add(card)
        for card in app.d.cards:
            card.x -= 30
    app.deckCoords = [(c.x, c.y) for c in app.d.cards]
    for enemy in app.stage.enemies:
        chance = random.randrange(0, 20)
        if 0 <= chance <= 10:
            enemy.intention = enemy.enemyIntentions[0]
        elif 10 <= chance <= 15:
            enemy.intention = enemy.enemyIntentions[1]
        elif 15 <= chance <= 17:
            enemy.intetion = enemy.enemyIntentions[2]
        elif 17 <= chance <= 19:
            enemy.intetion = enemy.enemyIntentions[3]
        # enemy.intention = app.enemyIntentions[random.randrange(
            # 0, len(app.enemyIntentions))]
        print(enemy.intention)
    app.turnCount += 1
    if app.bombEffect == True:
        if app.bombCounter < 3:
            app.bombCounter += 1
        elif app.bombCounter <= 3:
            app.stage.enemies[0].health -= 50
            app.bombEffet = False

    relic.relicHandler(app.stage.player, app.turn)


def intentionHandler(app):
    for enemy in app.stage.enemies:
        if enemy.intention != None:
            if enemy.intention == "Attack":
                # Draw Intention
                print(enemy.attack(app.player, random.randrange(
                    enemy.attackRange[0], enemy.attackRange[1])))
                enemy.hasAttackedRecently = True
                app.stage.player.wasHitRecently = True
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
    drawLabel(f"current Floor: {app.floor}", 250, 50)
    if app.stage.type == "Combat" or app.stage.type == "Boss":
        if app.stage.player.isPlayerAlive():
            app.et.drawButton(app)
            if app.turn == "Player Turn":
                app.stage.deck.drawDeck(app, 0)
                # app.stage.Deck.resetDeck(app.stage.deck)
            app.opD.drawButton(app)
            if app.stage.player.wasHitRecently:
                app.stage.player.drawPlayer(app.stage.player.imageHit, -10, 10)
            else:
                app.stage.player.drawPlayer(app.stage.player.image, 0, 0)
            for enemy in app.stage.enemies:
                if enemy.wasHitRecently == False:
                    enemy.drawEnemy(enemy.image, 0, 0)
                    IntentionIcon.drawIcon(enemy)
                else:
                    enemy.drawEnemy(enemy.hitImage, +10, 10)
                    IntentionIcon.drawIcon(enemy)
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
            drawLabel(f"Turn count: {app.turnCount}", 350, 50)

            pHealth = f"Health: {app.stage.player.health}"
            pSheild = f"Shield: {app.stage.player.currentDefense}"
            drawLabel(pHealth, app.stage.player.x+20, app.stage.player.y-30)
            drawLabel(pSheild, app.stage.player.x+20, app.stage.player.y-15)
            drawLabel(f"Eff: STR: {app.stage.player.strength} DEX: {app.stage.player.dex}",
                      app.stage.player.x+20, app.stage.player.y-45)
            drawLabel(f"Gold: {app.stage.player.gold}",
                      app.stage.player.x+20, app.stage.player.y-55)
            for enemy in app.stage.enemies:
                drawLabel(f"Health: {enemy.health}", enemy.x, enemy.y - 70)
                drawLabel(f"Shield: {enemy.currentDefense}",
                          enemy.x, enemy.y - 50)
                drawLabel(
                    f"Eff: STR: {enemy.strength} DEX: {enemy.dex}", enemy.x, enemy.y - 30)
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
    elif app.stage.type == "Level Up":
        app.endshop.drawButton(app)
        drawLevelUpScreen(app)
    if app.stage.type == "Game Over":
        drawGameOverScreen(app)
    if app.stage.type == "StartScreen":
        drawStartScreen(app)
        app.startButton.drawButton(app)


def drawGameOverScreen(app):
    drawLabel("You Lost", 150, 200, size=40)
    drawLabel(f"You lasted {app.floor} floors", 150, 250)


def drawStartScreen(app):
    backgroundImage = f"images/background2.png"
    temp = Image.open(backgroundImage)
    drawImage(backgroundImage, 0, 0,
              width=400, height=400)
    drawLabel("Slay the Spyre", 200, 200, size=50)


def drawLevelUpScreen(app):
    drawLabel("Level Up", 200, 180, size=30)
    drawLabel("Heal", 200, 220, size=15)
    drawLabel("Level Strength", 200, 250, size=15)
    drawLabel("Level Health", 200, 280, size=15)
    drawLabel("Level Dex", 200, 300, size=15)
    drawLabel(f"Current skill points {app.skillPoints}", 80, 100)

    for button in app.levelUpButtons:
        button.drawButton(app)


def drawEndBanner(app):
    # app.cardList(app)
    drawRect(150, 50, 150, 300, fill="lightSeaGreen")
    drawLabel("Pick A Card", 200, 75)


def drawShop(app):
    drawLabel("Buy Items", 200, 150, size=40)

    offset = 0

    for relic in app.relics:
        offset += 50
        relic.drawRelic(offset, 200)
        # relic.x, relic.y = 50 + offset, 150
        drawLabel(f"{relic.cost}C", relic.x, relic.y - 20)
    drawLabel(f"current Gold {app.stage.player.gold}", 200, 250, size=20)


def onKeyPress(app, key):
    pass


def onStep(app):
    if app.gameOver == False:
        if app.stateMachine.isCombatOver(app.stage) == "Stage Over":
            startStage(app)
        if app.stateMachine.isCombatOver(app.stage) == "Game Over":
            app.gameOver = True
            startStage(app)
    if app.stage.type == "Combat" or app.stage.type == "Boss":
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
                app.skillPoints += 1
                if removedEnemy.name == "Mimic":
                    app.stage.player.gold += 90
                elif removedEnemy.type == "Boss":
                    if app.removed.Enemy.name == "Money":
                        app.stage.player.gold += 200
                    if app.removed.Enemy.name == "Flamingo":
                        app.stage.player.strength += 20
                    app.stage.player.health = app.stage.player.maxHealth
                    app.stage.player.gold += 150
                    app.skillPoints += 4
                    # app.stage.player.forbiddenCards.append(
                    # forbiddenCards(app)[random.randrange(0, 1)])
                    # app.stage.player.forbiddenCards = list(
                    # set(app.stage.player.forbiddenCards))
                else:
                    app.stage.player.gold += 50
        if app.displayLowEnergy == True:
            app.lowEnergyCounter += 1
            if app.lowEnergyCounter == 75:
                app.displayLowEnergy = False
                app.lowEnergyCounter = 0
        if app.turnHandlerBegin == True:
            # print(app.turnTimer)
            app.turnTimer += 1
            if app.turnTimer == 25 and app.turn == "Player Effects":
                playerEffectsTurn(app)
                app.turnTimer = 0
            if app.turnTimer == 25 and app.turn == "Enemy Turn":
                enemyTurn(app)
                app.turnTimer = 0
            if app.turnTimer == 25 and app.turn == "Enemy Effects":
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
            if enemy.wasHitRecently:
                app.enemyHitTimer += 1
                if app.enemyHitTimer == 5:
                    app.enemyHitTimer = 0
                    enemy.wasHitRecently = False
        if app.stage.player.wasHitRecently:
            app.playerHitTimer += 1
            if app.playerHitTimer == 10:
                app.playerHitTimer = 0
                app.stage.player.wasHitRecently = False


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
        player.strength += 2
    elif card.name == "Attack Card":
        card.attackEnemy(
            45, "Physical", enemy, app.stage.player)
        if app.stage.player.canCrit == True:
            card.attackEnemy(
                75, "Physical", enemy, app.stage.player)
        player.attacksDone += 1
    elif card.name == "Defense Card":
        player.currentDefense += 10
    elif card.name == "Dex Card":
        player.dex += 3
    elif card.name == "The Bomb":
        app.bombEffect = True
        app.bombCounter = 0
    elif card.name == "Run":
        startStage(app)


def onMousePress(app, mouseX, mouseY):
    if app.stage.type == "Combat" or app.stage.type == "Boss":
        app.previousClicked = app.clickedCard
        app.clickedCard = app.d.isTouchingCard(app, mouseX, mouseY)

        for enemy in app.stage.enemies:
            if enemy.isMouseTouching(
                    app, mouseX, mouseY, app.turn, app.cardLine):
                if app.previousClicked in app.d.cards and (app.stage.player.energy - app.previousClicked.energyCost) > 0 and app.previousClicked != None:
                    app.stage.player.energy -= app.previousClicked.energyCost
                    cardSkillHandler(app, app.previousClicked,
                                     enemy, app.stage.player)
                    enemy.wasHitRecently = True
                    if app.playerAttackAnim == False:
                        playPlayerAttackAnimation(app)
                        app.playerAttackAnim = True
                    currentHandDiscard(app)
                else:
                    app.displayLowEnergy = True
        if app.turn == "Player Turn":
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
    if app.stage.type == "Level Up":
        levelUpButtonHandler(app, mouseX, mouseY)
        if app.endshop.isButtonClicked(app, mouseX, mouseY):
            startStage(app)
    if app.stage.type == "StartScreen":
        if app.startButton.isButtonClicked(app, mouseX, mouseY):
            app.startGame = True


def onMouseMove(app, mouseX, mouseY):
    if app.stage.type == "Combat" or app.stage.type == "Boss":
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

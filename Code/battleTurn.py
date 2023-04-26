from Stage import Stage


class StateMachine:
    def __init__(self, player, enemyList):
        self.Turns = ["Player Turn", "Player Effects",
                      "Enemy Turn", "Enemy Effects"]
        self.player = player
        self.enemyList = enemyList
        self.turnCount = 1
        self.currentTurn = "Player Turn"
        self.turnIterator = 1

    def nextTurn(self, currentTurn):
        if self.turnCount % 4 == 0 and (self.turnIterator != 0 or self.turnIterator != 2):
            self.turnIterator = 0
        self.turnCount += 1

        currentTurn = self.Turns[self.turnIterator]
        self.turnIterator += 1
        return currentTurn

    def playerTurn(self, player):
        player.showhand()
        if player.isTurnOver == True:
            self.nextTurn(self.currentTurn)
            return "Player Turn is Done!"

    def enemyTurn(self, enemy):
        if self.currentTurn == "Enemy Turn":
            for enemy in self.enemyList:
                enemy.doSkill(player)
            self.nextTurn(self.currentTurn)
            return "Enemy Turn is Done!"
        return "Not EnemyTurn"

    def removeEnemy(self, enemy):
        if enemy.health <= 0:
            return self.enemyList.pop(self.enemyList.index(enemy))

    def isCombatOver(self, stage):
        if self.player.health <= 0 and stage.type == "Combat":
            return "Game Over"
        elif len(self.enemyList) == 0 and stage.type != "Shop" and stage.type == "Combat":
            return "Stage Over"

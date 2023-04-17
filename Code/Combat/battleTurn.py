
class combatStateMachine:
    def __init__(self, player, enemyList, cardCast, currentTurn):
        self.Turns = ["Player Turn", "Player Effects",
                      "Enemy Turn", "Enemy Attack"]
        self.player = player
        self.enemyList = enemyList
        self.turnCount = 1
        self.cardCast = cardCast
        self.currentTurn = currentTurn

    def nextTurn(self, currentTurn):
        for i in range(len(self.Turns)-1):
            if currentTurn == self.Turns[i]:
                currentTurn = self.Turns[i+1] % self.turnCount
                self.turnCount += 1
                return currentTurn
        return None

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
            self.enemylist.pop(enemy)

    def isCombatOver(self):
        if self.player.health <= 0:
            return "Game Over"
        elif len(self.enemyList) == 0:
            return "Stage Over"
        else:
            self.nextTurn(self.currentTurn)

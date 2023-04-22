

class Node:
    def __init__(self, type, visited, neighbors, row, floor):
        self.type = type
        self.visited = visited
        self.neighbors = neighbors
        self.row = row
        self.floor = floor
        self.inLevel = False

    def __repr__(self):
        return f"The node is {self.type} type and is {self.row}"

    def contents(self, player, enemyList):
        if self.type == "Shop":
            self.showShop()
        elif self.type == "Combat":
            player.instaniate()
            enemyList.instaniate()

    def showShop(self):
        pass


class Map:
    def __init__(self, NodeList, floor):
        self.NodeList = NodeList
        self.floor = floor

    def __repr__(self):
        return f"This Floor is the {self.floor}th floor"

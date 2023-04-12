class Card:
    def __init__(self, image, energyCost, skill, name, Rect):
        self.image = image
        self.energyCost = energyCost
        self.skill = skill
        self.name = name
        self.cardType = None
        self.Rect = Rect

    def __repr__(self):
        return f"The card has {self.energyCost} and {self.name}"

    def __hash__(self):
        return hash(str(self))

    def isMouseTouching(self, app, mouseX, mouseY):
        # TODO check if the card is being touched by the mouse
        if self.Rect.contains(mouseX, mouseY):
            return True
        return False

    def drawCard(self, app):
        drawRect(self.Rect.x, self.Rect.y, self.Rect.width, self.Rect.height)
        drawImage(self.image, self.Rect.x, self.Rect.y)


class SkillCard(Card):
    def __init__(self, image, energyCost, skill, name):
        super.__init__(image, energyCost, skill, name)
        super.cardType = "skill"


class AttackCard(Card):
    def __init__(self, image, energyCost, skill, name):
        super.__init__(image, energyCost, skill, name)
        super.cardType = "attack"


class ColorlessCard(Card):
    def __init__(self, image, energyCost, skill, name):
        super.__init__(image, energyCost, skill, name)
        super.cardType = "colorless"


class Deck:
    def __init__(self, cardList):
        self.cards = cardList

    def shuffle(self):
        pass

    def discard(self):
        pass

    def drawDeck(self, app):
        for c in self.cards:
            c.draw(app)

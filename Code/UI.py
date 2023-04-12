from cmu_graphics import *


class Button:
    def __init__(self, rectangle, x, y, image):
        # x is top left corner
        # y is general height
        # image is ment to fit within the rectangle of the thing being pressed
        self.rectangle = rectangle
        self.x = x
        self.y = y
        self.image = image
        self.pressed = False

    def pressButton(self):
        self.pressed = True

    def isButtonClicked(self, mouseX, mouseY):
        # only run this onMousePressed
        # check if the  mouse is within the rectangle of the button and is being pressed
        if isinstance(self.rectangle, Rect):
            if self.rectangle.contains(mouseX, mouseY):
                return True
        return False


class Banner:
    def __init__(self, alignmnet, app, List):
        self.alignmnet = alignmnet
        # group is the cmu_graphics group which allows us to create groups of
        # polygons
        # self.group = group
        self.isActive = True
        self.x = 0
        self.y = 0
        self.width = app.width
        self.height = 30
        color = "blue"
        self.List = []

    def drawBanner(self, app):
        drawRect(0, 0, self.width, self.height, fill="blue")
        for i in self.List:
            # print(i)
            for elem in i:
                # print(elem)
                print(elem[0])
                if isinstance(elem[0], str):
                    drawLabel(elem[0], elem[1], elem[2], size=20)
                elif isinstance(elem[0], int):
                    drawRect(elem[0], elem[1], 20, 20,)

    # Create banner and in the group align each element specifically to a space in the screen

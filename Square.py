from Utilities import *


class Square:
    def __init__(self, canvas, x, y):
        self.size = 6
        self.crood = Croodinate(x, y)
        self.state = Type.Empty
        self.canvas = canvas
        self.tagName = "Rectangle" + str(x) + str(y)
        self.drawRectangle(self.canvas, self.crood)

    def Switcher(self, x):
        return {
            0: "gray",
            1: "black",
            2: "white",
            3: "white",
            4: "green",
            5: "blue",
            6: "red"
        }.get(x, "gray")

    def changeStateWhenMousedownAndOver(self, event, mouseDown):
        if(mouseDown):
            if(self.state == Type.Obstacle):
                self.setState(Type.Empty)
            elif(self.state == Type.Empty):
                self.setState(Type.Obstacle)

    def mouseClick(self, event):
        if(self.state == Type.Obstacle):
            self.setState(Type.Empty)
        elif(self.state == Type.Empty):
            self.setState(Type.Obstacle)

    def setRectangleOnClick(self):
        self.canvas.tag_bind(self.tagName, "<Button-1>", self.mouseClick)

    def drawRectangle(self, canvas, crood):
        (x, y) = self.crood.getCrood()
        color = self.Switcher(self.getState().value)
        self.rectangle = canvas.create_rectangle(
            x-self.size, y-self.size, x+self.size, y+self.size, fill=color, tag=self.tagName)

    def setSize(self, size):
        self.size = size

    def getSize(self):
        return self.size

    def setState(self, state):
        self.state = state
        self.update()

    def getState(self):
        return self.state

    def update(self):
        self.canvas.delete(self.rectangle)
        self.rectangle = self.drawRectangle(self.canvas, self.crood)

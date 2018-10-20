from tkinter import *
from enum import Enum


class Type(Enum):
    Empty = 0
    Obstacle = 1
    Opened = 2
    Closed = 3
    Start = 4
    Goal = 5
    Path = 6


class Croodinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setCrood(self, x, y):
        self.x = x
        self.y = y

    def getCrood(self):
        return self.x, self.y


class Square:
    def __init__(self, canvas, x, y):
        self.size = 10
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

    def setRectangleEnter(self, isMouseDown):
        self.canvas.tag_bind(self.tagName, "<Enter>", lambda event,
                             mouseDown=isMouseDown: self.changeStateWhenMousedownAndOver(event, mouseDown))

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


class Map:
    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.grid(row=0, column=0, rowspan=100, columnspan=50)
        self.size = 40
        self.isMouseDown = False
        self.canvas = Canvas(mainFrame, bg="white", height=1500,
                             width=1300, border=1)
        self.map = []
        self.canvas.grid(row=0, column=0, rowspan=50, columnspan=50)
        self.drawMap()

        self.setSquaresOnClick()
        # self.setSquaresEnter(False)

        # self.canvas.bind("<Button-1>", self.mouseDown)
        # self.canvas.bind("<ButtonRelease-1>", self.mouseUp)

    def drawMap(self):
        y = 30
        for i in range(self.size):
            row = []
            x = 30
            for j in range(self.size):
                square = Square(self.canvas, x, y)
                row.append(square)
                x += 2*square.getSize() + 3
            y += 2*square.getSize() + 3
            self.map.append(row)

    def setSquaresEnter(self, isMouseDown):
        for i in range(self.size):
            for j in range(self.size):
                self.map[i][j].setRectangleEnter(isMouseDown)

    def setSquaresOnClick(self):
        for i in range(self.size):
            for j in range(self.size):
                self.map[i][j].setRectangleOnClick()

    def mouseDown(self, event):
        print("down")
        self.setSquaresEnter(True)

    def mouseUp(self, event):
        print("up")
        self.setSquaresEnter(False)

class Panel:
    def __inti__(self, master):
        mainFrame = Frame(master)
        mainFrame.grid(row=0, column=0, rowspan=100, columnspan=50)
root = Tk()

#root1 = Tk()

Map = Map(root)
#Panel = Panel(root1)

root.mainloop()
#root1.mainloop()
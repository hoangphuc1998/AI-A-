from tkinter import *
from Panel import *
from Square import *


class Map:
    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.grid(row=0, column=0, rowspan=100, columnspan=50)
        self.__inittializeVariable()
        self.canvas = Canvas(mainFrame, bg="white", height=1500,
                             width=980, border=1)
        self.canvas.grid(row=0, column=0, rowspan=50, columnspan=50)

        self.createButton(mainFrame)

        self.map = []
        self.drawMap()
        self.setSquaresOnClick()
        self.bindMotion()

    def run(self):
        print(self.size, self.start, self.goal, self.Heuristic, self.Algorithm)

    def update(self):
        self.canvas.delete("all")
        self.map.clear()
        self.map = []

        self.drawMap()
        self.setSquaresOnClick()
        self.bindMotion()

    def createButton(self, mainFrame):
        self.runButton = Button(mainFrame, text="Run",
                                width=20, command=self.run)
        self.runButton.grid(row=0, column=51, rowspan=2)

        self.updateButton = Button(
            mainFrame, text="Update", width=20, command=self.update)
        self.updateButton.grid(row=2, column=51, rowspan=2)

    def __inittializeVariable(self):
        self.x = 10
        self.y = 10
        self.padding = 2

        self.size = 70
        self.start = Croodinate(0, 0)
        self.goal = Croodinate(self.size - 1, self.size - 1)
        self.time = 0
        self.Algorithm = "A*"
        self.Heuristic = "Euclid"

    def drawMap(self):
        y = self.y
        for i in range(self.size):
            row = []
            x = self.x
            for j in range(self.size):
                square = Square(self.canvas, x, y)
                row.append(square)
                x += 2*square.getSize() + self.padding
            y += 2*square.getSize() + self.padding
            self.map.append(row)
        self.map[self.start.x][self.start.y].setState(Type.Start)
        self.map[self.goal.x][self.goal.y].setState(Type.Goal)

    def bindMotion(self):
        self.canvas.bind("<B1-Motion>", self.handleMotion)

    def isInside(self, x, y):
        squareSize = 2*self.map[0][0].getSize() + self.padding
        return (x >= self.x) and (y >= self.y) and (x <= squareSize*self.size) and (y <= squareSize*self.size)

    def handleMotion(self, event):
        squareSize = 2*self.map[0][0].getSize() + self.padding
        if(self.isInside(event.x, event.y)):
            self.map[int((event.y - self.x)/squareSize) + 1][int((event.x - self.y) /
                                                                 squareSize) + 1].setState(Type.Obstacle)

    def setSquaresOnClick(self):
        for i in range(self.size):
            for j in range(self.size):
                self.map[i][j].setRectangleOnClick()


def handleApply(panel, map):
    if(panel.allValid()):
        map.start = Croodinate(panel.startX.get(), panel.startY.get())
        map.goal = Croodinate(panel.goalX.get(), panel.goalY.get())
        map.size = panel.size.get()
        map.Algorithm = panel.Algorithm.get()
        map.Heuristic = panel.Heuristic.get()
        map.time = panel.time.get()
    else:
        panel.showMessageBox("Error", "Values are invalid!")


root = Tk()

root.title('Map')
Map = Map(root)


def toplevel():
    top = Toplevel()
    top.title('Panel')
    top.wm_geometry("400x200")
    top.attributes('-alpha', 0.8)
    top.configure(background="black")
    return top


Panel = Panel(toplevel(), 40)
Panel.applyButton.bind("<Button-1>", lambda event,
                       panel=Panel, map=Map: handleApply(panel, map))


root.mainloop()

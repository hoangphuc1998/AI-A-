from tkinter import *
from Panel import *
from Square import *
from AStar import A_star
from ARA_star import runARA

class MapGUI:
    def __init__(self, master):
        self.master = master
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
        heuristic = "euclidean"
        if self.Heuristic == "My heuristic":
            heuristic = "max_step"
        if self.Algorithm == "A*":
            A_star(input_method='gui', input=self,
               output_method='gui', output=self, root=self.master, heuristic=heuristic)
        else:
            runARA(10000,heuristic=heuristic,input_method='gui',input=self,output_method='gui',output=self,root=self.master)

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

        self.size = 30
        self.start = Coord(0, 0)
        self.goal = Coord(self.size - 1, self.size - 1)
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
        self.map[self.start.y][self.start.x].setState(Type.Start)
        self.map[self.goal.y][self.goal.x].setState(Type.Goal)

    def bindMotion(self):
        self.canvas.bind("<B1-Motion>", self.handleMotion)

    def isInside(self, x, y):
        squareSize = 2*self.map[0][0].getSize() + self.padding
        return (x >= self.x) and (y >= self.y) and (x <= squareSize*self.size) and (y <= squareSize*self.size)

    def handleMotion(self, event):
        squareSize = 2*self.map[0][0].getSize() + self.padding
        if(self.isInside(event.x, event.y)):
            self.map[int((event.y - self.y)/squareSize) + 1][int((event.x - self.x) /
                                                                 squareSize) + 1].setState(Type.Obstacle)

    def setSquaresOnClick(self):
        for i in range(self.size):
            for j in range(self.size):
                self.map[i][j].setRectangleOnClick()


def handleApply(panel, map):
    if(panel.allValid()):
        map.start = Coord(panel.startX.get(), panel.startY.get())
        map.goal = Coord(panel.goalX.get(), panel.goalY.get())
        map.size = panel.size.get()
        map.Algorithm = panel.Algorithm.get()
        map.Heuristic = panel.Heuristic.get()
        map.time = panel.time.get()
    else:
        panel.showMessageBox("Error", "Values are invalid!")


root = Tk()

root.title('Map')
Map = MapGUI(root)


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

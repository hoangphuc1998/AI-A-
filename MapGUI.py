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

        self.map = []
        self.drawMap()
        self.createButton(mainFrame)
        self.setSquaresOnClick()
        self.bindMotion()

    def __inittializeVariable(self):
        self.x = 10
        self.y = 10
        self.padding = 2

        self.size = 40
        self.start = Coord(0, 0)
        self.goal = Coord(self.size - 1, self.size - 1)
        self.time = 0
        self.Algorithm = "A*"
        self.Heuristic = "Euclid"

    def run(self):
        self.disableAllButton()
        heuristic = "euclidean"
        if self.Heuristic == "My Heuristic":
            heuristic = "min_step"
        #print(heuristic)
        if self.Algorithm == "A*":
            A_star(input_method='gui', input=self,
                   output_method='gui', output=self, root=self.master, heuristic=heuristic)
        else:
            #timer = self.runButton.after(int(self.time*1000),runARA,(self.time,heuristic,'gui',self,'gui',self,self.master))
            runARA(10000, heuristic=heuristic, input_method='gui',
                   input=self, output_method='gui', output=self, root=self.master,epsilon=2.5)
            # self.runButton.after_cancel(timer)
        self.enableAllButton()

    def disableAllButton(self):
        self.runButton['state'] = 'disabled'
        self.updateButton['state'] = 'disabled'
        self.resetButton['state'] = 'disabled'

    def enableAllButton(self):
        self.runButton['state'] = 'normal'
        self.updateButton['state'] = 'normal'
        self.resetButton['state'] = 'normal'

    def update(self):
        self.canvas.delete("all")
        self.map.clear()
        self.map = []

        self.drawMap()
        self.setSquaresOnClick()
        self.bindMotion()

    def reset(self):
        for i in range(self.size):
            for j in range(self.size):
                if(self.map[i][j].state != Type.Obstacle):
                    self.map[i][j].setState(Type.Empty)

    def createButton(self, mainFrame):
        row = 0
        self.runButton = Button(mainFrame, text="Run",
                                width=20, command=self.run)
        self.runButton.grid(row=row, column=50, rowspan=2, columnspan=5)

        row += 2
        self.resetButton = Button(
            mainFrame, text="Reset", width=20, command=self.reset)
        self.resetButton.grid(row=row, column=50, rowspan=2, columnspan=5)

        row += 2
        self.updateButton = Button(
            mainFrame, text="Update", width=20, command=self.update)
        self.updateButton.grid(row=row, column=50, rowspan=2, columnspan=5)

        row += 10
        typeName = ['Empty', 'Obstacle', 'Opened',
                    'Closed', 'Start', 'Goal', 'Path', 'Incons']
        for i in range(len(typeName)):
            color = self.map[0][0].Switcher(i)
            Label(mainFrame, bg=color, width="2").grid(
                row=row, column=50, rowspan=2)
            Label(mainFrame, text=typeName[i]).grid(
                row=row, column=52, rowspan=2)
            row += 1

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
        return (x >= self.x) and (y >= self.y) and (x <= squareSize*self.size + 3) and (y <= squareSize*self.size + 3)

    def handleMotion(self, event):
        squareSize = 2*self.map[0][0].getSize() + self.padding
        if(self.isInside(event.x, event.y)):
            self.map[int((event.y - self.y)/squareSize)][int((event.x - self.x) /
                                                             squareSize)].setState(Type.Obstacle)

    def setSquaresOnClick(self):
        for i in range(self.size):
            for j in range(self.size):
                self.map[i][j].setRectangleOnClick()


def handleApply(panel, map):
    if(panel.allValid()):
        panel.convertAllToInt()
        map.start = panel.istart
        map.goal = panel.igoal
        map.size = panel.isize
        map.Algorithm = panel.Algorithm.get()
        map.Heuristic = panel.Heuristic.get()
        map.time = panel.ftime
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
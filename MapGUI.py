from tkinter import *
from Panel import *
from Square import *
from AStar import A_star
from ARA_star import runARA


class MapGUI:
    def __init__(self, master):
        self.master = master
        color = "#00b0ba"
        mainFrame = Frame(master)
        mainFrame.grid(row=0, column=0, rowspan=100, columnspan=50)
        self.__inittializeVariable()
        self.canvas = Canvas(mainFrame, bg=color, height=1500,
                             width=1000, bd=1)
        self.canvas.grid(row=0, column=0, rowspan=50, columnspan=50)

        self.drawMap()
        self.createButton(mainFrame)
        self.bindCanvas()

    def __inittializeVariable(self):
        self.map = []
        self.x = 10
        self.y = 10
        self.padding = 2
        self.startFlag = False
        self.goalFlag = False

        self.size = 40
        self.start = Coord(0, 0)
        self.goal = Coord(self.size - 1, self.size-1)
        self.epsilon = 1.5
        self.oldEpsilon = 1.5
        self.Algorithm = "A*"
        self.Heuristic = "Euclid"

    def run(self):
        self.disableAllButton()
        heuristic = "euclidean"
        if self.Heuristic == "My Heuristic":
            heuristic = "min_step"
        # print(heuristic)
        if self.Algorithm == "A*":
            A_star(input_method='gui', input=self,
                   output_method='gui', output=self, root=self.master, heuristic=heuristic)
        else:
            # timer = self.runButton.after(int(self.time*1000),runARA,(self.time,heuristic,'gui',self,'gui',self,self.master))
            runARA(10000, heuristic=heuristic, input_method='gui',
                   input=self, output_method='gui', output=self, root=self.master, epsilon=self.epsilon)
            # self.runButton.after_cancel(timer)
        self.enableAllButton()

    def bindCanvas(self):
        self.canvas.bind("<Key>", self.handleKeyDown)
        self.canvas.bind("<KeyRelease>", self.handleKeyRelease)
        self.canvas.bind("<B1-Motion>", self.handleMotion)
        self.canvas.bind("<Button-1>", self.handleClick)
        self.canvas.bind("<MouseWheel>", self.handleMouseWheel)

    def handleKeyDown(self, event):
        if(event.char == 's'):
            self.startFlag = True
        if(event.char == 'g'):
            self.goalFlag = True

    def handleKeyRelease(self, event):
        if(event.char == 's'):
            self.startFlag = False
        if(event.char == 'g'):
            self.goalFlag = False

    def handleClick(self, event):
        self.canvas.focus_set()
        x, y = event.x, event.y
        if(self.startFlag):
            if(self.isInside(x, y)):
                self.changeStart(x, y)
        elif(self.goalFlag):
            if(self.isInside(x, y)):
                self.changeGoal(x, y)
        else:
            if(self.getTypeWithCoord(x, y) == Type.Obstacle):
                self.setTypeWithCoord(x, y, Type.Empty)
            elif(self.getTypeWithCoord(x, y) == Type.Empty):
                self.setTypeWithCoord(x, y, Type.Obstacle)

    def handleMotion(self, event):
        self.setTypeWithCoord(event.x, event.y, Type.Obstacle)

    def handleMouseWheel(self, event):
        if self.runButton['state'] == 'normal':
            if event.num == 5 or event.delta == -120:
                if(self.size >= 70):
                    return
                self.size += 2
                self.goal.set_coord(self.size - 1, self.size - 1)
                self.update()
            if event.num == 4 or event.delta == 120:
                if(self.size <= 4):
                    return
                self.size -= 2
                self.goal.set_coord(self.size - 1, self.size - 1)
                self.update()

    def drawMap(self):
        squareSize = self.switchSize(self.size)
        y = self.y + squareSize
        for i in range(self.size):
            row = []
            x = self.x + squareSize
            for j in range(self.size):
                square = Square(self.canvas, x, y, squareSize)
                row.append(square)
                x += 2*square.getSize() + self.padding
            y += 2*square.getSize() + self.padding
            self.map.append(row)
        self.map[self.start.y][self.start.x].setState(Type.Start)
        self.map[self.goal.y][self.goal.x].setState(Type.Goal)

    def createButton(self, mainFrame):
        row = 0
        self.runButton = Button(mainFrame, width=17, bg="#5CB85C", fg="white", bd=7, height=2, text="Run",
                                command=self.run)
        self.runButton.grid(row=row, column=50, rowspan=2, columnspan=5)

        row += 2
        self.resetButton = Button(
            mainFrame, text="Reset", width=17,  bg="#5CB85C", fg="white", bd=7, height=2, command=self.reset)
        self.resetButton.grid(row=row, column=50, rowspan=2, columnspan=5)

        row += 2
        self.updateButton = Button(
            mainFrame, text="Update", width=17,  bg="#5CB85C", fg="white", bd=7, height=2, command=self.update)
        self.updateButton.grid(row=row, column=50, rowspan=2, columnspan=5)

        row += 5
        self.epsilonLabel = Label(mainFrame, text='Epsilon: '+ str(
            self.epsilon), fg="red", font="20")
        self.epsilonLabel.grid(row=row, column=50, rowspan=2, columnspan=5)

        row += 5
        typeName = ['Empty', 'Obstacle', 'Opened',
                    'Closed', 'Start', 'Goal', 'Path', 'Incons', 'Previous Paths']
        for i in range(len(typeName)):
            color = self.map[0][0].Switcher(i)
            Label(mainFrame, bg=color, width="2").grid(
                row=row, column=50, rowspan=2)
            Label(mainFrame, text=typeName[i], font="20").grid(
                row=row, column=52, rowspan=2)
            row += 1

    def update(self):
        self.canvas.delete("all")
        self.map.clear()
        self.map = []

        self.drawMap()
        self.bindCanvas()
        self.setEpsilon(self.oldEpsilon)

    def reset(self):
        for i in range(self.size):
            for j in range(self.size):
                if(self.map[i][j].state != Type.Obstacle):
                    self.map[i][j].setState(Type.Empty)
        self.setEpsilon(self.oldEpsilon)
        

    def changeStart(self, x, y):
        self.map[self.start.y][self.start.x].setStartOrGoal(Type.Empty)
        self.setTypeWithCoord(x, y, Type.Start)
        i, j = self.getIndexWithCoord(x, y)
        self.start.set_coord(j, i)

    def changeGoal(self, x, y):
        self.map[self.goal.y][self.goal.x].setStartOrGoal(Type.Empty)
        self.setTypeWithCoord(x, y, Type.Goal)
        i, j = self.getIndexWithCoord(x, y)
        self.goal.set_coord(j, i)

    def disableAllButton(self):
        self.runButton['state'] = 'disabled'
        self.updateButton['state'] = 'disabled'
        self.resetButton['state'] = 'disabled'

    def enableAllButton(self):
        self.runButton['state'] = 'normal'
        self.updateButton['state'] = 'normal'
        self.resetButton['state'] = 'normal'

    def getIndexWithCoord(self, x, y):
        squareSize = 2*self.map[0][0].getSize() + self.padding
        return (int((y - self.y/2)/squareSize), int((x - self.x/2) / squareSize))

    def isInside(self, x, y):
        squareSize = 2*self.map[0][0].getSize() + self.padding
        return (x >= self.x) and (y >= self.y) and (x <= squareSize*self.size + 3) and (y <= squareSize*self.size + 3)

    def setTypeWithCoord(self, x, y, state):
        if(self.isInside(x, y)):
            i, j = self.getIndexWithCoord(x, y)
            self.map[i][j].setState(state)

    def getTypeWithCoord(self, x, y):
        if(self.isInside(x, y)):
            i, j = self.getIndexWithCoord(x, y)
            return self.map[i][j].state
        return 0

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon
        self.epsilonLabel['text'] = self.epsilon

    def switchSize(self, x):
        return 360/x


def handleApply(panel, map):
    if(panel.allValid()):
        panel.convertAllToInt()
        map.start = panel.istart
        map.goal = panel.igoal
        map.size = panel.isize
        map.Algorithm = panel.Algorithm.get()
        map.Heuristic = panel.Heuristic.get()
        map.epsilon = panel.fepsilon
        map.oldEpsilon = map.epsilon
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

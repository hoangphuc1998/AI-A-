from Utilities import Coord, Type


class Square:
    def __init__(self, canvas, x, y):
        self.size = 6
        self.coord = Coord(x, y)
        self.state = Type.Empty
        self.canvas = canvas
        self.tagName = "Rectangle" + str(x) + str(y)
        self.drawRectangle(self.canvas, self.coord)

    def Switcher(self, x):
        return {
            0: "gray",  # Empty
            1: "black",  # Obstacle
            2: "yellow",  # Opened
            3: "white",  # Closed
            4: "green",  # Start
            5: "blue",  # Goal
            6: "red",  # Path
            7: "purple" #Incons
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

    def drawRectangle(self, canvas, coord):
        (x, y) = self.coord.get_coord()
        color = self.Switcher(self.getState().value)
        self.rectangle = canvas.create_rectangle(
            x-self.size, y-self.size, x+self.size, y+self.size, fill=color, tag=self.tagName)

    def setSize(self, size):
        self.size = size

    def getSize(self):
        return self.size

    def setState(self, state):
        if self.state != Type.Start and self.state != Type.Goal:
            self.state = state
        self.update()

    def getState(self):
        return self.state

    def update(self):
        self.canvas.delete(self.rectangle)
        self.drawRectangle(self.canvas, self.coord)

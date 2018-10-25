from tkinter import *
from tkinter import messagebox
from Utilities import *


class Panel(Frame):
    def __init__(self, master, size):
        Frame.__init__(self, master)
        mainFrame = Frame(master, bg="black")
        mainFrame.grid(row=0, column=0, rowspan=100, columnspan=100)
        self.__initialzeVariable(size)
        self.__createForm(mainFrame)

    def __initialzeVariable(self, size):
        self.startX = StringVar(None, str(0))
        self.startY = StringVar(None, str(0))

        self.size = StringVar(None, str(size))
        self.goalX = StringVar(None, str(int(self.size.get())-1))
        self.goalY = StringVar(None, str(int(self.size.get())-1))

        self.Algorithm = StringVar(None, "A*")
        self.Heuristic = StringVar(None, "Euclid")

        self.epsilon = StringVar(None, str(1.0))

        self.istart = Coord(int(self.startX.get()), int(self.startY.get()))
        self.igoal = Coord(int(self.goalX.get()), int(self.goalY.get()))
        self.isize = int(self.size.get())
        self.fepsilon = float(self.epsilon.get())

    def __createForm(self, mainFrame):
        self.createAlgorithmField(mainFrame, 0)
        self.createHeuristicField(mainFrame, 2)

        self.createSizeField(mainFrame, 4)
        self.createStartField(mainFrame, 7)
        self.createGoalField(mainFrame, 9)
        self.createEpsilonField(mainFrame, 11)
        self.createButton(mainFrame, 14)

    def createAlgorithmField(self, mainFrame, row):
        Label(mainFrame, text="Algorithm", bg="black", fg="white").grid(
            row=row, column=0, columnspan=2, rowspan=2)
        Radiobutton(mainFrame, text="A*", activebackground="black", variable=self.Algorithm, value="A*", bg="black", fg="red").grid(
            row=row, column=2, columnspan=2)
        Radiobutton(mainFrame, text="ARA*", activebackground="black", variable=self.Algorithm, value="ARA*", bg="black", fg="red").grid(
            row=row, column=3, columnspan=2)

    def createHeuristicField(self, mainFrame, row):
        Label(mainFrame, text="Heuristic", bg="black", fg="white").grid(
            row=row, column=0, columnspan=2, rowspan=2)
        Radiobutton(mainFrame, text="Euclid", fg="red", activebackground="black", variable=self.Heuristic, value="Euclid", bg="black").grid(
            row=row, column=2, columnspan=2)
        Radiobutton(mainFrame, text="My Heuristic", activebackground="black", variable=self.Heuristic, value="My Heuristic", bg="black", fg="red").grid(
            row=row, column=3, columnspan=2)

    def createSizeField(self, mainFrame, row):
        validateInteger = (self.register(
            self.onValidateInteger), '%P')
        Label(mainFrame, text="Size ", bg="black",
              fg="white").grid(row=row, column=0, rowspan=2)
        Entry(mainFrame, textvariable=self.size, bg="black", fg="white", insertbackground="white", bd=0, validate="key", validatecommand=validateInteger).grid(
            row=row, column=1, columnspan=3)

    def createStartField(self, mainFrame, row):
        validateInteger = (self.register(
            self.onValidateInteger), '%P')
        Label(mainFrame, text="Start ", bg="black",
              fg="white").grid(row=row, column=0, rowspan=2)
        Label(mainFrame, text="X :", bg="black",
              fg="white").grid(row=row, column=1)
        Entry(mainFrame, textvariable=self.startX, bg="black", fg="white", insertbackground="white", bd=0, validate="key",
              validatecommand=validateInteger).grid(row=row, column=2)
        Label(mainFrame, text="Y :", bg="black",
              fg="white").grid(row=row, column=3)
        Entry(mainFrame, textvariable=self.startY, bg="black", fg="white", insertbackground="white", bd=0, validate="key",
              validatecommand=validateInteger).grid(row=row, column=4)

    def createGoalField(self, mainFrame, row):
        validateInteger = (self.register(
            self.onValidateInteger), '%P')
        Label(mainFrame, text="Goal ", bg="black",
              fg="white").grid(row=row, column=0, rowspan=2)
        Label(mainFrame, text="X :", bg="black",
              fg="white").grid(row=row, column=1)
        Entry(mainFrame, textvariable=self.goalX, bg="black", fg="white", insertbackground="white", bd=0, validate="key",
              validatecommand=validateInteger).grid(row=row, column=2)
        Label(mainFrame, text="Y :", bg="black",
              fg="white").grid(row=row, column=3)
        Entry(mainFrame, textvariable=self.goalY, bg="black", fg="white", insertbackground="white", bd=0, validate="key",
              validatecommand=validateInteger).grid(row=row, column=4)

    def createEpsilonField(self, mainFrame, row):
        validateFloat = (self.register(
            self.onValidateFloat), '%P')
        Label(mainFrame, text="Epsilon ", bg="black",
              fg="white").grid(row=row, column=0, rowspan=3)
        Entry(mainFrame, textvariable=self.epsilon, bg="black", fg="white", insertbackground="white", bd=0, validate="key", validatecommand=validateFloat).grid(
            row=row, column=1, columnspan=3)

    def createButton(self, mainFrame, row):
        self.applyButton = Button(
            mainFrame, text="Apply", bg="black", fg="white", bd=0, width=15, pady=10, font=(15))
        self.applyButton.grid(row=row, column=0, columnspan=4)
        Button(mainFrame, text="Reset", bg="black", fg="white", bd=0, width=15,  pady=10, font=(15), command=self.handleReset).grid(
            row=row, column=4, columnspan=4)

    def showMessageBox(self, title, message):
        messagebox.showinfo(title, message)

    def isInRange(self, value, a, b):
        for i in range(len(value)):
            if value[i] < a[i] or value[i] > b[i]:
                return False
        return True

    def allValid(self):
        if(self.isInt(self.size.get()) and self.isInt(self.startX.get()) and self.isInt(self.startY.get()) and
           self.isInt(self.goalX.get()) and self.isInt(self.goalY.get()) and self.isFloat(self.epsilon.get())):

            value = [int(self.size.get()), int(self.startX.get()), int(self.startY.get()),
                     int(self.goalX.get()), int(self.goalY.get()), float(self.epsilon.get())]
            high = [70, int(self.size.get())-1, int(self.size.get())-1,
                    int(self.size.get())-1, int(self.size.get())-1, 5.0]
            low = [2, 0, 0, 0, 0, 0.1]
            return self.isInRange(value, low, high)
        return False

    def convertAllToInt(self):
        self.istart.x = int(self.startX.get())
        self.istart.y = int(self.startY.get())
        self.igoal.x = int(self.goalX.get())
        self.igoal.y = int(self.goalY.get())

        self.isize = int(self.size.get())
        self.fepsilon = float(self.epsilon.get())

    def handleReset(self):

        self.startX.set(0)
        self.startY.set(0)

        self.size.set(40)
        self.goalX.set(self.size.get() - 1)
        self.goalY.set(self.size.get() - 1)

        self.Algorithm.set("A*")
        self.Heuristic.set("Euclid")

        self.epsilon.set(1.0)

    def onValidateInteger(self, P):
        return True

    def onValidateFloat(self, P):
        return True

    def isInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def isFloat(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

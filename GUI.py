from tkinter import *
from cmath import *


class LeftFrame:
    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.grid(row=0, column=0, rowspan=1, columnspan=1)

        self.labelHeuristic = Label(mainFrame, text="My Heuristic", fg="green")
        self.heapArray = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 0,
                          8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 0, 1, 2, 3, 4, 5, 6, 7,
                          8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 0, 1, 2, 3, 4, 5, 6, 7,
                          8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 0, 1, 2, 3, 4, 5, 6, 7,
                          8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 0, 1, 2, 3, 4, 5, 6, 7,
                          8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 0, 1, 2, 3, 4, 5, 6, 7,
                          8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 0, 1, 2, 3, 4, 5, 6, 7]

        self.button = Button(mainFrame, text="test button")

        self.button.grid(row=4, column=0)

    def button_click(self, callback):
        callback()


class RightFrame:
    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.grid(row=0, column=1, rowspan=100, columnspan=5)

        self.canvas = Canvas(mainFrame, bg="white", height=400,
                             width=400, border=1, relief=SUNKEN)
        self.canvas.grid(row=0, column=0, rowspan=100)

        self.canvas.bind('<Configure>', self.create_grid)

    def create_grid(self, event=None):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.delete('grid_line')

        for i in range(0, w, 20):
            self.canvas.create_line([(i, 0), (i, h)], tag='grid_line')

        for i in range(0, h, 20):
            self.canvas.create_line([(0, i), (w, i)], tag='grid_line')


class Tree:
    def __init__(self, master):
        mainFrame = Frame(master)
        mainFrame.grid(row=0, column=0)

        self.canvas = Canvas(mainFrame, bg="white", height=1500,
                             width=2000, border=1)

        self.canvas.grid(row=0, column=0, rowspan=50, columnspan=50)

        self.canvas.bind('<Configure>', self.drawTree)

    def drawTree(self, heapArray):
        if heapArray and isinstance(heapArray, list):
            numberOfRow = int(log(len(heapArray), 2).real) + 1
            extractedLists = self.extractLists(heapArray)
            rowNumber = 0
            for item in extractedLists:
                self.drawOvalRow(item, rowNumber, numberOfRow)
                rowNumber += 1

    def drawOvalRow(self, extractedList, rowNumber, numberOfRow):
        width = self.canvas.winfo_width()
        offsetTree = width/2 - 50
        ovalRange = 14
        if rowNumber == 0:
            self.drawOval(extractedList[0], offsetTree, 50, ovalRange)
        else:
            columnNumber = 0
            offset = 68*numberOfRow
            shiftTabSpace = 0
            parentX = 0
            parentY = 0
            for i in range(rowNumber):
                shiftTabSpace += offset
                offset /= 2
            offset *= 2
            for item in extractedList:
                x = offsetTree - (shiftTabSpace) + columnNumber*offset*2
                y = rowNumber*80 + 50
                self.drawOval(item, x, y, ovalRange)
                if columnNumber % 2 == 0:
                    parentX = x + offset
                    parentY = y - 80 + ovalRange
                    y -= ovalRange
                else:
                    parentX = x - offset
                    parentY = y - 80 + ovalRange
                    y -= ovalRange
                self.canvas.create_line(x, y, parentX, parentY)
                columnNumber += 1

    def extractLists(self, heapArray):
        numberOfRow = int(log(len(heapArray), 2).real) + 1
        extractedLists = []
        extractedLists.append([heapArray[0]])
        indexRow = []
        valueRow = []
        indexRow.append(0)
        for i in range(numberOfRow - 1):
            indexRow, valueRow = self.childs(indexRow, heapArray)
            extractedLists.append(valueRow)
        return extractedLists

    def childs(self, indexRow, heapArray):
        newIndexRow = []
        newValueRow = []
        for val in indexRow:
            if 2*val + 1 < len(heapArray):
                newIndexRow.append(2*val + 1)
                newValueRow.append(heapArray[2*val + 1])
            if 2*val + 2 < len(heapArray):
                newIndexRow.append(2*val + 2)
                newValueRow.append(heapArray[2*val + 2])
        return newIndexRow, newValueRow

    def drawOval(self, value, x, y, r=30):
        self.drawOvalWithCrood(x, y, r)
        self.drawTextWithValue(value, x, y)

    def drawOvalWithCrood(self, x, y, r):
        self.canvas.create_oval(x-r, y-r, x+r, y+r, tag="oval")

    def drawTextWithValue(self, value, x, y):
        self.canvas.create_text(x, y, text=str(value), font=15)

    def clearCanvas(self):
        self.canvas.delete("all")

    def updateCanvas(self, heapArray):
        self.clearCanvas()
        self.drawTree(heapArray)


root = Tk()

leftFrame = LeftFrame(root)
rightFrame = RightFrame(root)


root1 = Tk()
tree = Tree(root1)


def onClick():
    tree.drawTree(leftFrame.heapArray)


leftFrame.button.bind(
    "<Button-1>", lambda event: leftFrame.button_click(onClick))

root1.mainloop()
root.mainloop()


# leftFrame = Frame(root)
# leftFrame.pack(side=LEFT, fill=X)

# rightFrame = Frame(root)
# rightFrame.pack(side=RIGHT, fill=X)

# button1 = Button(leftFrame, text="My Heuristic", fg="green")
# button2 = Button(leftFrame, text="Time", fg="blue")
# label = Label(rightFrame, text="Size", bg="red", fg="white")
# button4 = Button(rightFrame, text="My Heuristic", fg="red")

# labelHeuristic = Label(root, text="My Heuristic", fg="green")
# entryHeuristic = Entry(root)

# labelSize = Label(root, text="Size", bg="red", fg="white")

# labelMaxTime = Label(root, text="Max Time")
# entryMaxTime = Entry(root)

# labelHeuristic.grid(row=0, column=0, sticky="W")
# entryHeuristic.grid(row=0, column=1)

# canvas = Canvas(root, bg="white", height=800,
#                 width=1000, border=1, relief=SUNKEN)

# labelSize.grid(row=1, column=0, sticky="W")

# labelMaxTime.grid(row=2, column=0, sticky="W")
# entryMaxTime.grid(row=2, column=1)

# canvas.grid(row=0, column=2, rowspan=100)


# def create_grid(event=None):
#     w = canvas.winfo_width()
#     h = canvas.winfo_height()
#     canvas.delete('grid_line')

#     # Creates all vertical lines at intevals of 100
#     for i in range(0, w, 100):
#         canvas.create_line([(i, 0), (i, h)], tag='grid_line')

#     # Creates all horizontal lines at intevals of 100
#     for i in range(0, h, 100):
#         canvas.create_line([(0, i), (w, i)], tag='grid_line')


# canvas.bind('<Configure>', create_grid)

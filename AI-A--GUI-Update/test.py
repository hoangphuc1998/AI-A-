import random
import time
from tkinter import *
from MapGUI import MapGUI, Type

root = Tk()
Map = MapGUI(root)
root.update()
while True:
    for i in range(Map.size):
        time.sleep(0.1)
        Map.map[i][i].setState(Type.Opened)
        root.update()

mainloop()

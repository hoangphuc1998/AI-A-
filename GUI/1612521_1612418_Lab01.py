
from MapGUI import *


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
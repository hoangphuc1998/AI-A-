from enum import Enum


class Type(Enum):
    Empty = 0
    Obstacle = 1
    Opened = 2
    Closed = 3
    Start = 4
    Goal = 5
    Path = 6
    Incons = 7
    PreviousPaths = 8


# Class Coord save coordinate of a cell
class Coord:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def set_coord(self, x, y):
        self.x = x
        self.y = y
    def get_coord(self):
        return self.x, self.y
    def __eq__(self, value):
            return self.x == value.x and self.y == value.y
    def __ne__(self, value):
            return not self.__eq__(value)
    # Calculate euclidean distance between 2 cells
    def euclidean_distance(self,c):
        return ((self.x-c.x)**2 + (self.y-c.y)**2)**(1/2)
    # Calculate heuristic by calculate max step from a cell to another cell
    # Formula for heuristic between cell a and b: max(|a.x-b.x|,|a.y-b.y)
    def min_step(self,c):
        return max(abs(self.x-c.x),abs(self.y-c.y))
    def calculate_heuristic(self,cell,heuristic ='euclidean'):
        if heuristic=='euclidean':
            return self.euclidean_distance(cell)
        if heuristic == 'min_step':
            return self.min_step(cell)
    # Get next available steps. List of cells is sort clockwise
    def get_successor_list(self,n):
        sucessor_list = []
        final_list = []
        sucessor_list.append(Coord(self.x-1,self.y-1))
        sucessor_list.append(Coord(self.x,self.y-1))
        sucessor_list.append(Coord(self.x+1,self.y-1))
        sucessor_list.append(Coord(self.x+1,self.y))
        sucessor_list.append(Coord(self.x+1,self.y+1))
        sucessor_list.append(Coord(self.x,self.y+1))
        sucessor_list.append(Coord(self.x-1,self.y+1))
        sucessor_list.append(Coord(self.x-1,self.y))
        for c in sucessor_list:
            if c.x>=0 and c.x<n and c.y>=0 and c.y<n:
                final_list.append(c)
        return final_list
    def print(self):
        print('('+str(self.x)+','+str(self.y)+')',end = ' ')
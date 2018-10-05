#Function to calculate position in heap
def parent(n):
    return (n-1)//2
def left_child(n):
    return 2*n + 1
def right_child(n):
    return 2*n + 2

class Coord:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __eq__(self, value):
            return self.x == value.x and self.y == value.y
    def __ne__(self, value):
            return not self.__eq__(value)

class Cell:
    def __init__(self,coord,g,h,parent,t):
        self.coord = coord
        self.g = g
        self.h = h
        self.parent = parent
        self.type = t
    def get_cost(self):
        return self.g + self.h

class PriorityQueue:
    def print(self):
        for i in self.heap:
            print(i.get_cost(),end = ' ')
        print()
    def __init__(self):
        self.heap = []
        self.size = 0
    #Insert new key to priority queue
    def insert_new_key(self,cell):
        self.size+=1
        i = self.size - 1
        self.heap.append(cell)
        while (i!=0 and self.heap[parent(i)].get_cost()>self.heap[i].get_cost()):
            self.heap[i],self.heap[parent(i)] = self.heap[parent(i)],self.heap[i]
            i = parent(i)
    #Extract a key from a priority queue
    def extract(self):
        if self.size==0:
            return 'Error: No element found'
        if self.size==1:
            self.size-=1
            temp = self.heap[0]
            self.heap.pop()
            return self.heap[0]
        temp = self.heap[0]
        self.heap[0] = self.heap[self.size-1]
        self.size-=1
        self.heap.pop()
        self.sift_down(0)
        return temp
    #Sift a key down
    def sift_down(self,i):
        l = left_child(i)
        r = right_child(i)
        s = i
        if (l<self.size and self.heap[l].get_cost()<self.heap[s].get_cost()):
            s = l
        if (r<self.size and self.heap[r].get_cost()<self.heap[s].get_cost()):
            s = r
        if s!=i:
            self.heap[s],self.heap[i] = self.heap[i],self.heap[s]
            self.sift_down(s)
    #Insert a key to priority queue. Update the value when already exists
    def insert_key(self,cell):
        i = 0
        while (i<self.size and self.heap[i].coord!=cell.coord):
            i+=1
        if i>=self.size:
            self.insert_new_key(cell)
        else:
            if self.heap[i].get_cost() > cell.get_cost():
                self.heap[i] = cell
                while (i!=0 and self.heap[parent(i)].get_cost()>self.heap[i].get_cost()):
                    self.heap[i],self.heap[parent(i)] = self.heap[parent(i)],self.heap[i]
                    i = parent(i)
        self.print()


open_list = PriorityQueue()
open_list.insert_key(Cell(Coord(2,3),2,1,1,2))
open_list.insert_key(Cell(Coord(4,3),0,2,1,2))
open_list.insert_key(Cell(Coord(5,3),1,0,1,2))
open_list.insert_key(Cell(Coord(6,3),5,10,1,2))
open_list.insert_key(Cell(Coord(7,3),5,0,1,2))
open_list.insert_key(Cell(Coord(8,3),1,3,1,2))
open_list.insert_key(Cell(Coord(6,3),0,0,1,2))

print(open_list.extract().get_cost())
open_list.print()

print(open_list.extract().get_cost())
open_list.print()

print(open_list.extract().get_cost())
open_list.print()

print(open_list.extract().get_cost())
open_list.print()
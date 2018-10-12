import sys
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
    def euclide_distance(self,c):
        return ((self.x-c.x)**2 + (self.y-c.y)**2)**(1/2)
    def calculate_heuristic(self,cell,type ="euclide"):
        if type=="euclide":
            return self.euclide_distance(cell)
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

class Cell:
    def __init__(self,coord,g,h,parent,t):
        self.coord = coord
        self.g = g
        self.h = h
        self.parent = parent
        self.type = t
    def get_cost(self):
        return self.g + self.h
    def trace_path(self):
        p = self
        path = []
        while p!=None:
            path.append(p.coord)
            p = p.parent
        path = reversed(path)
        return path

class Map:
    def __init__(self):
        self.grid_map = []
        self.n = 0
        self.start = None
        self.goal = None
    def import_from_file(self,filename):
        with open(filename) as f:
            self.n = int(f.readline())
            x,y = [int(i) for i in next(f).split()]
            self.start = Coord(x,y)
            x,y = [int(i) for i in next(f).split()]
            self.goal = Coord(x,y)
            for i in range(self.n):
                line = []
                for index,val in enumerate(f.readline().split()):
                    new_cell = Cell(Coord(index,i),0,0,None,int(val))
                    new_cell.h = new_cell.coord.calculate_heuristic(self.goal)
                    line.append(new_cell)
                self.grid_map.append(line)
    def get_cell(self,x,y):
        return self.grid_map[y][x]

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
            return temp
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



def init_list(n):
    open_list = PriorityQueue()
    closed_list = []
    for _ in range(n):
        closed_list.append([False for x in range(n)])
    return open_list,closed_list

def A_star():
    find_path = False
    grid_map = Map()
    grid_map.import_from_file(sys.argv[1])
    open_list,closed_list = init_list(grid_map.n)
    open_list.insert_key(grid_map.get_cell(grid_map.start.x,grid_map.start.y))
    while open_list.size>0:
        q = open_list.extract()
        if q.coord == grid_map.goal:
            print("Find path")
            path = q.trace_path()
            print(q.g)
            for c in path:
                c.print()
            print()
            find_path = True
            return
        elif closed_list[q.coord.y][q.coord.x]==False:
            successor_list = q.coord.get_successor_list(grid_map.n)
            for s in successor_list:
                cell = grid_map.get_cell(s.x,s.y)
                if cell.type == 0 and closed_list[s.y][s.x] == False:
                    cell.g = q.g + 1
                    cell.h = cell.coord.calculate_heuristic(grid_map.goal)
                    cell.parent = q
                    open_list.insert_key(cell)
        closed_list[q.coord.y][q.coord.x] = True
    if find_path == False:
        print('Can\'t find path')


A_star()
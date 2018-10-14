import sys
import time
infinity = float('inf')
# Class Coord save coordinate of a cell
class Coord:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __eq__(self, value):
            return self.x == value.x and self.y == value.y
    def __ne__(self, value):
            return not self.__eq__(value)
    # Calculate euclidean distance between 2 cells
    def euclidean_distance(self,c):
        return ((self.x-c.x)**2 + (self.y-c.y)**2)**(1/2)
    # Calculate heuristic by calculate max step from a cell to another cell
    # Formula for heuristic between cell a and b: max(|a.x-b.x|,|a.y-b.y)
    def max_step(self,c):
        return max(abs(self.x-c.x),abs(self.y-c.y))
    def calculate_heuristic(self,cell,heuristic ='euclidean'):
        if heuristic=='euclidean':
            return self.euclidean_distance(cell)
        if heuristic == 'max_step':
            return self.max_step(cell)
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

class Cell:
    def __init__(self,coord,g,h,parent,t):
        self.coord = coord
        self.g = g
        self.h = h
        self.parent = parent
        self.type = t
        self.symbol = '-'
        if self.type==1:
            self.symbol = 'o'
    def get_cost(self,epsilon = 1):
        return self.g + epsilon*self.h
    # Return a list of cells in path from start to goal
    def trace_path(self):
        p = self
        path = []
        while p!=None:
            path.append(p.coord)
            p.symbol = 'x'
            p = p.parent
        path = reversed(path)
        return path

class Map:
    def __init__(self,n = 0,start = None,goal = None):
        self.grid_map = []
        self.n = n
        self.start = start
        self.goal = goal

    #Read input file and create map
    def import_from_file(self,filename,heuristic = 'euclidean'):
        with open(filename) as f:
            self.n = int(f.readline())
            x,y = [int(i) for i in next(f).split()]
            self.start = Coord(x,y)
            x,y = [int(i) for i in next(f).split()]
            self.goal = Coord(x,y)
            for i in range(self.n):
                line = []
                for index,val in enumerate(f.readline().split()):
                    new_cell = Cell(Coord(index,i),infinity,0,None,int(val))
                    if new_cell.type!=1:
                        new_cell.h = new_cell.coord.calculate_heuristic(self.goal,heuristic=heuristic)
                    line.append(new_cell)
                self.grid_map.append(line)
            self.get_cell(self.start).g = 0

    #Get cell at coordinate (x,y)
    def get_cell(self,coord):
        return self.grid_map[coord.y][coord.x]
    #Print map to output file or console
    def print_map(self,file = None):
        self.get_cell(self.start).symbol = 'S'
        self.get_cell(self.goal).symbol = 'G'
        if file==None:
            for line in self.grid_map:
                for cell in line:
                    print(cell.symbol,end = ' ')
                    if cell.symbol == 'x':
                        cell.symbol = '-'
                print()
        else:
            for line in self.grid_map:
                for cell in line:
                    file.write(str(cell.symbol)+' ')
                    if cell.symbol == 'x':
                        cell.symbol = '-'
                file.write('\n')


#Function to calculate position in heap
def parent(n):
    return (n-1)//2
def left_child(n):
    return 2*n + 1
def right_child(n):
    return 2*n + 2
#Priority Queue class implemented by binary heap
class PriorityQueue:
    def print(self):
        for i in self.heap:
            print('('+str(i.get_cost())+','+str(i.h)+')',end = ' ')
        print()
    def __init__(self):
        self.heap = []
        self.size = 0
    #Insert new key to priority queue
    def insert_new_key(self,cell,epsilon):
        self.size+=1
        i = self.size - 1
        self.heap.append(cell)
        while (i!=0 and self.heap[parent(i)].get_cost(epsilon)>self.heap[i].get_cost(epsilon)):
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
    #Get the minimum f value in heap
    def get_min(self):
        return self.heap[0]
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
    def insert_key(self,cell,epsilon = 1):
        i = 0
        while (i<self.size and self.heap[i].coord!=cell.coord):
            i+=1
        if i>=self.size:
            self.insert_new_key(cell,epsilon)
        else:
            if self.heap[i].get_cost(epsilon) > cell.get_cost(epsilon):
                self.heap[i] = cell
                while (i!=0 and self.heap[parent(i)].get_cost(epsilon)>self.heap[i].get_cost(epsilon)):
                    self.heap[i],self.heap[parent(i)] = self.heap[parent(i)],self.heap[i]
                    i = parent(i)

# Init container used by A* and ARA* (open_list, closed_list, incons_list)
def init_list(n):
    open_list = PriorityQueue()
    closed_list = []
    incons_list = []
    for _ in range(n):
        closed_list.append([False for x in range(n)])
    return open_list,closed_list,incons_list

# Print output when find path
def print_output(grid_map,q,output_method,file):
    path = q.trace_path()
    if output_method=='console':
        print(q.g+1)
        for c in path:
            c.print()
        print()
    elif output_method=='file':
        file.write(str(q.g+1)+'\n')
        for c in path:
            file.write('('+str(c.x)+','+str(c.y)+') ')
        file.write('\n')
        grid_map.print_map(file)

# Implement A* algorithm
def A_star(heuristic = 'euclidean', input_method = 'file', input_file = 'input.txt', output_method = 'file',output_file = 'output.txt'):
    find_path = False
    grid_map = Map()
    grid_map.import_from_file(input_file,heuristic)
    open_list,closed_list,_ = init_list(grid_map.n)
    open_list.insert_key(grid_map.get_cell(grid_map.start))
    file = None
    if output_method == 'file':
        file = open(output_file,'w')
    while open_list.size>0:
        q = open_list.extract()
        if q.coord == grid_map.goal:
            print_output(grid_map,q,output_method,file)
            find_path = True
            return
        elif closed_list[q.coord.y][q.coord.x]==False:
            successor_list = q.coord.get_successor_list(grid_map.n)
            for s in successor_list:
                cell = grid_map.get_cell(s)
                # If cell is not a block and not in closed_list and have a lower cost than before
                if cell.type == 0 and closed_list[s.y][s.x] == False and cell.get_cost() > q.g + 1 + cell.h:
                    cell.g = q.g + 1
                    cell.parent = q
                    open_list.insert_key(cell)
        closed_list[q.coord.y][q.coord.x] = True
    if find_path == False:
        if output_method=='console':
            print('Can\'t find path')
        elif output_method=='file':
            file.write('-1')

def improve_path(grid_map, open_list, closed_list, incons_list, minf, heuristic = 'euclidean', epsilon = 1):
    while open_list.size>0 and grid_map.get_cell(grid_map.goal).get_cost(epsilon)>open_list.get_min().get_cost(epsilon):
        q = open_list.extract()
        closed_list[q.coord.y][q.coord.x] = True
        for s in q.coord.get_successor_list(grid_map.n):
            cell = grid_map.get_cell(s)
            if cell.type!=1 and cell.get_cost(epsilon) > q.g + 1 + epsilon*cell.h:
                cell.g = q.g+1
                cell.parent = q
                if minf>cell.get_cost(epsilon = 1):
                    minf = cell.get_cost(epsilon = 1)
                if closed_list[s.y][s.x]==False:
                    open_list.insert_key(cell,epsilon)
                else:
                    incons_list.append(cell)
    return minf

def handle_result(grid_map,epsilon,output_method = 'file',output = None):
    if output_method == 'file' and output!=None:
        output.write(str(epsilon)+'\n')
        q = grid_map.get_cell(grid_map.goal)
        print_output(grid_map,q,output_method,output)


def ARA_star(heuristic = 'euclidean',epsilon = 1.5,input_method = 'file',input = 'input.txt',output_method = 'file',output = 'output.txt'):
    e = infinity
    minf = infinity
    grid_map = Map()
    grid_map.import_from_file(input,heuristic)
    open_list,closed_list,incons_list = init_list(grid_map.n)
    open_list.insert_key(grid_map.get_cell(grid_map.start),epsilon=epsilon)
    minf = improve_path(grid_map,open_list,closed_list,incons_list,minf, heuristic,epsilon)
    if output_method=='file':
        output = open(output,'w')
    handle_result(grid_map,e,output_method,output)
    e = min(epsilon,grid_map.get_cell(grid_map.goal).g/minf)
    while e>1:
        epsilon-=0.1
        new_open_list,closed_list,_ = init_list(grid_map.n)
        for c in incons_list:
            new_open_list.insert_key(c,epsilon)
        for c in open_list.heap:
            new_open_list.insert_key(c,epsilon)
        open_list = new_open_list
        incons_list = []
        minf = improve_path(grid_map,open_list,closed_list,incons_list,minf, heuristic,epsilon)
        handle_result(grid_map,e,output_method,output)
        e = min(epsilon,grid_map.get_cell(grid_map.goal).g/minf)
start_time = time.time()
A_star(heuristic='max_step',input_file=sys.argv[1])
print('Running time: ',str(time.time()-start_time))
start_time = time.time()
ARA_star(heuristic='max_step',epsilon=1.5,input=sys.argv[1])
print('Running time: ',str(time.time()-start_time))
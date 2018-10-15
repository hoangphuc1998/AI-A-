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
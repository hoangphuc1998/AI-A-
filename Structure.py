infinity = float('inf')
from Utilities import Coord,Type

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
    
    #Read input from gui and create map
    def import_from_gui(self,map,heuristic='euclidean'):
        self.n = map.size
        self.start = map.start
        self.goal = map.goal
        for y in range(self.n):
            line = []
            for x in range(self.n):
                new_cell = Cell(Coord(x,y),infinity,0,None,map.map[y][x].state.value)
                if new_cell.type!=1:
                    new_cell.h = new_cell.coord.calculate_heuristic(self.goal,heuristic=heuristic)
                line.append(new_cell)
            self.grid_map.append(line)
        self.get_cell(self.start).g = 0
        # f = open('input.txt','w')
        # f.write(str(self.n)+'\n')
        # f.write(str(self.start.x) + ' '+ str(self.start.y)+'\n')
        # f.write(str(self.goal.x)+' '+str(self.goal.y)+'\n')
        # for y in range(self.n):
        #     for x in range(self.n):
        #         if self.grid_map[y][x].type==1:
        #             f.write('1 ')
        #         else:
        #             f.write('0 ')
        #     f.write('\n')
        # f.close()
        
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
        file.write('\n')
    elif output_method == 'gui':
        for c in path:
            file.map[c.y][c.x].setState(Type.Path)
    #print(q.g+1)
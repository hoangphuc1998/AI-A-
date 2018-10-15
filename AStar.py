import sys
from Structure import *
from PriorityQueue import *

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

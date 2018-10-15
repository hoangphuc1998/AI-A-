import sys
from Structure import Map,print_output
from PriorityQueue import PriorityQueue,init_list

# Implement A* algorithm
def A_star(heuristic = 'euclidean', input_method = 'file', input= 'input.txt', output_method = 'file',output = 'output.txt'):
    find_path = False
    grid_map = Map()
    if input_method=='file':
        grid_map.import_from_file(input,heuristic)
    else:
        grid_map.import_from_gui(input,heuristic)
    grid_map.print_map()
    open_list,closed_list,_ = init_list(grid_map.n)
    open_list.insert_key(grid_map.get_cell(grid_map.start))
    file = None
    if output_method == 'file':
        file = open(output,'w')
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
if __name__=='__main__':
    A_star(heuristic='max_step',input=sys.argv[1])
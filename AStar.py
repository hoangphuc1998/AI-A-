import sys
import time
from Structure import Map, print_output
from PriorityQueue import PriorityQueue, init_list
from Utilities import Type
# Implement A* algorithm


def A_star(heuristic='euclidean', input_method='file', input='input.txt', output_method='file', output='output.txt', root='abc'):
    find_path = False
    grid_map = Map()
    if input_method == 'file':
        grid_map.import_from_file(input, heuristic)
    elif input_method == 'gui':
        grid_map.import_from_gui(input, heuristic)
    #grid_map.print_map_value(epsilon=1)
    open_list, closed_list, _ = init_list(grid_map.n)
    open_list.insert_key(grid_map.get_cell(grid_map.start),epsilon=1)
    file = None
    if output_method == 'file':
        file = open(output, 'w')
    if output_method == 'gui':
        file = output
    while open_list.size > 0:
        q = open_list.extract(epsilon=1)
        closed_list[q.coord.y][q.coord.x] = True
        if q.coord == grid_map.goal:
            print_output(grid_map, q, output_method, file)
            find_path = True
            return
        successor_list = q.coord.get_successor_list(grid_map.n)
        for s in successor_list:
            cell = grid_map.get_cell(s)
            # If cell is not a block and not in closed_list and have a lower cost than before
            if cell.type != 1 and closed_list[s.y][s.x] == False and cell.g > q.g + 1:
                cell.g = q.g + 1
                cell.parent = q
                open_list.insert_key(cell,epsilon=1)
                if output_method == 'gui':
                    time.sleep(0.02)
                    output.map[s.y][s.x].setState(Type.Opened)
                    root.update()
        #grid_map.print_map_value(epsilon=1)
        if output_method == 'gui':
            output.map[q.coord.y][q.coord.x].setState(Type.Closed)

        
    if find_path == False:
        if output_method == 'console':
            print('Can\'t find path')
        elif output_method == 'file':
            file.write('-1')


if __name__ == '__main__':
    c = 3
    while c!=1 and c!=2:
        c = int(input('Choose heuristic (1: Euclidean, 2: Our heuristic): '))
    heuristic = 'euclidean'
    if c==2:
        heuristic = 'min_step'
    start = time.time()
    A_star(heuristic=heuristic, input=sys.argv[1],input_method='file',output_method='file',output=sys.argv[2])
    print(time.time()-start)

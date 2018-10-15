import sys
from multiprocessing import Process
import time
from Structure import *
from PriorityQueue import *

def improve_path(grid_map, open_list, closed_list, incons_list, minf, epsilon = 1):
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


def ARA_star(grid_map,epsilon = 1.5,output_method = 'file',output = 'output.txt'):
    e = infinity
    minf = infinity
    open_list,closed_list,incons_list = init_list(grid_map.n)
    open_list.insert_key(grid_map.get_cell(grid_map.start),epsilon=epsilon)
    minf = improve_path(grid_map,open_list,closed_list,incons_list,minf,epsilon)
    if output_method=='file':
        output = open(output,'w')
    handle_result(grid_map,epsilon,output_method,output)
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
        minf = improve_path(grid_map,open_list,closed_list,incons_list,minf,epsilon)
        handle_result(grid_map,epsilon,output_method,output)
        e = min(epsilon,grid_map.get_cell(grid_map.goal).g/minf)


def runARA(time_limit,heuristic='euclidean',input_method='file',input='input.txt',output_method='file',output='output.txt'):
    if __name__ == '__main__':
        grid_map = Map()
        if input_method=='file':
            grid_map.import_from_file(input,heuristic)
        action_process = Process(target=ARA_star,args=(grid_map,2,output_method,output))
        action_process.start()
        action_process.join(timeout=time_limit/1000)
        action_process.terminate()
time_limit = int(input('Enter time limit: '))
runARA(time_limit,heuristic = 'max_step',input=sys.argv[1],output=sys.argv[2])
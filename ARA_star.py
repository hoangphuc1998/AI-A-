import sys
from multiprocessing import Process
import time
from Structure import *
from PriorityQueue import *

def improve_path(grid_map, open_list, closed_list, incons_list, minf, epsilon = 1,output_method = 'file',output = 'output.txt',root = 'abc'):
    while open_list.size>0 and grid_map.get_cell(grid_map.goal).get_cost(epsilon)>open_list.get_min().get_cost(epsilon):
        q = open_list.extract()
        closed_list[q.coord.y][q.coord.x] = True
        if output_method == 'gui':
            output.map[q.coord.y][q.coord.x].setState(Type.Closed)
        for s in q.coord.get_successor_list(grid_map.n):
            cell = grid_map.get_cell(s)
            if cell.type!=1 and cell.get_cost(epsilon) > q.g + 1 + epsilon*cell.h:
                cell.g = q.g+1
                cell.parent = q
                if minf>cell.get_cost(epsilon = 1):
                    minf = cell.get_cost(epsilon = 1)
                if closed_list[s.y][s.x]==False:
                    open_list.insert_key(cell,epsilon)
                    if output_method == 'gui':
                        time.sleep(0.05)
                        output.map[cell.coord.y][cell.coord.x].setState(Type.Opened)
                        root.update()
                else:
                    incons_list.append(cell)
                    if output_method == 'gui':
                        output.map[cell.coord.y][cell.coord.x].setState(Type.Incons)
    return minf

def handle_result(grid_map,epsilon,output_method = 'file',output = None):
    q = grid_map.get_cell(grid_map.goal)
    if output_method == 'file' and output!=None:
        output.write(str(epsilon)+'\n')
        print_output(grid_map,q,output_method,output)
    elif output_method == 'gui':
        print_output(grid_map, q, output_method, output)


def ARA_star(grid_map,epsilon = 1.5,output_method = 'file',output = 'output.txt',root = 'abc'):
    e = infinity
    minf = infinity
    open_list,closed_list,incons_list = init_list(grid_map.n)
    open_list.insert_key(grid_map.get_cell(grid_map.start),epsilon=epsilon)
    minf = improve_path(grid_map,open_list,closed_list,incons_list,minf,epsilon,output_method,output,root)
    if output_method=='file':
        output = open(output,'w')
    handle_result(grid_map,epsilon,output_method,output)
    e = min(epsilon,grid_map.get_cell(grid_map.goal).g/minf)
    while e>1:
        epsilon-=0.1
        new_open_list,closed_list,_ = init_list(grid_map.n)
        for c in incons_list:
            new_open_list.insert_key(c,epsilon)
            if output_method == 'gui':
                output.map[c.coord.y][c.coord.x].setState(Type.Opened)
                root.update()
        for c in open_list.heap:
            new_open_list.insert_key(c,epsilon)
        open_list = new_open_list
        incons_list = []
        minf = improve_path(grid_map,open_list,closed_list,incons_list,minf,epsilon,output_method,output,root)
        handle_result(grid_map,epsilon,output_method,output)
        e = min(epsilon,grid_map.get_cell(grid_map.goal).g/minf)

def my_func(map1,root):
    i = 0
    map1.map[1][1].setState(Type.Path)
    root.update()
    while True:
        if map1.map[1][1].state == Type.Empty:
            map1.map[1][1].setState(Type.Closed)
        else:
            map1.map[1][1].setState(Type.Empty)
        time.sleep(1)
        print(i)
        i+=1
        root.update()
    

def runARA(time_limit,heuristic='euclidean',input_method='file',input='input.txt',output_method='file',output='output.txt',root = 'abc'):
    grid_map = Map()
    if input_method=='file':
        grid_map.import_from_file(input,heuristic)
    elif input_method == 'gui':
        grid_map.import_from_gui(input,heuristic)
    if output_method == 'gui':
        #action_process = Process(target=ARA_star,args=(grid_map,2,output_method,output, root))
        try:
            action_process = Process(target=my_func, args=(output,root))
            action_process.start()
            action_process.join(timeout=time_limit/1000)
            action_process.terminate()
        except:
            print ("a")
        #ARA_stcatchar(grid_map,10,output_method,output,root = root)
    else:
        action_process = Process(target=ARA_star,args=(grid_map,2,output_method,output))
        #action_process = Process(target=my_func)
        action_process.start()
        action_process.join(timeout=time_limit/1000)
        action_process.terminate()
if __name__ == '__main__':
    time_limit = int(input('Enter time limit: '))
    runARA(time_limit,heuristic = 'max_step',input=sys.argv[1],output=sys.argv[2])
import sys
sys.path.insert(0, '../Structure')
from os import path
from threading import Thread, Event
import time
from Structure import *
from PriorityQueue import *
stop_it = Event()
def improve_path(grid_map, open_list, closed_list, incons_list, minf, epsilon = 1,output_method = 'file',output = 'output.txt',root = 'abc'):
    while open_list.size>0 and grid_map.get_cell(grid_map.goal).get_cost(epsilon)>open_list.get_min().get_cost(epsilon):
        q = open_list.extract(epsilon=epsilon)
        closed_list[q.coord.y][q.coord.x] = True
        if output_method == 'gui':
            output.map[q.coord.y][q.coord.x].setState(Type.Closed)
        for s in q.coord.get_successor_list(grid_map.n):
            cell = grid_map.get_cell(s)
            if cell.type!=1 and cell.g > q.g + 1:
                cell.g = q.g+1
                cell.parent = q
                if minf>cell.get_cost(epsilon = 1):
                    minf = cell.get_cost(epsilon = 1)
                if closed_list[s.y][s.x]==False:
                    open_list.insert_key(cell,epsilon)
                    if output_method == 'gui':
                        time.sleep(0.02)
                        output.map[cell.coord.y][cell.coord.x].setState(Type.Opened)
                        root.update()
                else:
                    incons_list.append(cell)
                    if output_method == 'gui':
                        output.map[cell.coord.y][cell.coord.x].setState(Type.Incons)
        if stop_it.is_set():
            return minf
    return minf

def handle_result(grid_map,epsilon,output_method = 'file',output = None,closed_list=[]):
    q = grid_map.get_cell(grid_map.goal)
    if output_method == 'file' and output!=None:
        output.write('epsilon = ' + str(epsilon)+'\n')
        print_output(grid_map,q,output_method,output)
    elif output_method == 'gui':
        print_output(grid_map, q, output_method, output)
        for y in range(grid_map.n):
            for x in range(grid_map.n):
                if closed_list[y][x]==True and output.map[y][x].state !=Type.Path:
                    output.map[y][x].setState(Type.Empty)
        path = q.trace_path()
        if epsilon>1:
            for c in path:
                output.map[c.y][c.x].setState(Type.PreviousPaths)
        output.master.update()


def ARA_star(grid_map,epsilon = 1.5,output_method = 'file',output = 'output.txt',root = 'abc'):
    if output_method == 'file':
        output = open(output,'w')
    e = infinity
    minf = grid_map.get_cell(grid_map.start).get_cost(epsilon=1)
    open_list,closed_list,incons_list = init_list(grid_map.n)
    open_list.insert_key(grid_map.get_cell(grid_map.start),epsilon=epsilon)
    minf = improve_path(grid_map,open_list,closed_list,incons_list,minf,epsilon,output_method,output,root)
    if stop_it.is_set():
        return
    handle_result(grid_map,epsilon,output_method,output,closed_list)
    e = min(epsilon,grid_map.get_cell(grid_map.goal).g/minf)
    
    while e>1:
        epsilon-=0.1
        epsilon = round(epsilon,1)
        if output_method=='gui':
            output.setEpsilon(epsilon)
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
        handle_result(grid_map,epsilon,output_method,output,closed_list)
        e = min(epsilon,grid_map.get_cell(grid_map.goal).g/minf)
        if stop_it.is_set():
            break


def runARA(time_limit,epsilon = 1.5,heuristic='euclidean',input_method='file',input='input.txt',output_method='file',output='output.txt',root = 'abc'):
    grid_map = Map()
    if input_method=='file':
        grid_map.import_from_file(input,heuristic)
    elif input_method == 'gui':
        grid_map.import_from_gui(input,heuristic)
    if output_method == 'gui':
        ARA_star(grid_map= grid_map,epsilon=epsilon,output_method = output_method,output = output,root = root)
    else:
        action_process = Thread(target=ARA_star,args=(grid_map,epsilon,output_method,output,))
        action_process.start()
        action_process.join(timeout=time_limit/1000)
        stop_it.set()
        #action_process.terminate()

def main_ARA_star():
    time_limit = int(input('Enter time limit: '))
    epsilon = float(input('Enter start epsilon: '))
    c = 3
    while c!=1 and c!=2:
        c = int(input('Choose heuristic (1: Euclidean, 2: Our heuristic): '))
    heuristic = 'euclidean'
    if c==2:
        heuristic = 'min_step'
    runARA(time_limit,epsilon = epsilon,heuristic = heuristic,input=sys.argv[1],output=sys.argv[2])
    if path.getsize(sys.argv[2])==0:
        f=open(sys.argv[2],'w')
        f.write('-1')
if __name__ == '__main__':
    main_ARA_star()
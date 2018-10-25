
#Function to calculate position in heap
def parent(n):
    return (n-1)//2
def left_child(n):
    return 2*n + 1
def right_child(n):
    return 2*n + 2
#Priority Queue class implemented by binary heap
class PriorityQueue:
    def print(self,epsilon):
        for i in self.heap:
            i.coord.print()
            print(i.get_cost(epsilon),end = ' ')
    def __init__(self):
        self.heap = []
        self.size = 0
    #Insert new key to priority queue
    def insert_new_key(self,cell,epsilon):
        self.size+=1
        i = self.size - 1
        self.heap.append(cell)
        while (i>0 and self.heap[parent(i)].get_cost(epsilon)>self.heap[i].get_cost(epsilon)):
            self.heap[i],self.heap[parent(i)] = self.heap[parent(i)],self.heap[i]
            i = parent(i)
    #Extract a key from a priority queue
    def extract(self,epsilon=1):
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
        self.sift_down(0,epsilon=epsilon)
        return temp
    #Get the minimum f value in heap
    def get_min(self):
        return self.heap[0]
    #Sift a key down
    def sift_down(self,i,epsilon=1):
        l = left_child(i)
        r = right_child(i)
        s = i
        if (l<self.size and self.heap[l].get_cost(epsilon=epsilon)<self.heap[s].get_cost(epsilon=epsilon)):
            s = l
        if (r<self.size and self.heap[r].get_cost(epsilon=epsilon)<self.heap[s].get_cost(epsilon=epsilon)):
            s = r
        if s!=i:
            self.heap[s],self.heap[i] = self.heap[i],self.heap[s]
            self.sift_down(s,epsilon=epsilon)
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
                while (i>0 and self.heap[parent(i)].get_cost(epsilon)>self.heap[i].get_cost(epsilon)):
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
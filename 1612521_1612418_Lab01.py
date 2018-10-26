from AStar import main_AStar
from ARA_star import main_ARA_star
if __name__ == '__main__':
    c = 0
    while c!= 1 and c !=2:
        c = int(input('Choose program (1: A* \t 2: ARA*): '))
    if c==1:
        main_AStar()
    else:
        main_ARA_star()
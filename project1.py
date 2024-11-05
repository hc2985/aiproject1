#Hyeonung Cho & Karl Zerbe
import math
from heapq import heapify, heappush, heappop

def heuristic(index,goal):
    #calculate heuristic from index to goal
    x = index[0]
    y = index[1]

    #get difference of x and y coordinates
    xdiff = (goal[0]-x)
    ydiff = (goal[1]-y)

    #euclidian distnace
    h = math.sqrt((xdiff**2)+(ydiff**2))
    return h

def stepcost(paction ,action,k):
    #action -> (0-7 move)
    #calculate current step cost

    #angle cost, use minimum angle difference
    angle = k*(min((abs(paction - action)), (8 - abs(paction - action)))/4)

    #get dist cost
    if(action%2 == 0):
        dist = 1
    else:
        dist = math.sqrt(2)

    #cost of angle cost + dist cost
    return angle + dist

def outofbound(index,max):
    #check if out of bound
    if index[0] < 0 or index[1] < 0 or index[0] >= max[0] or index[1] >= max[1]:
        return True
    return False

def main():
    #dict to store each cell's g(n), h(n), angle, and prev
    graph = {}
    #keep track of nodes generated
    nodesgenerated = 1
    
    #line -> line by line of input
    with open("Sample_input.txt") as file:
        line = [line.strip() for line in file.readlines()]
   
    index = line[0].split(' ')
    #start index, goal index
    start = (int(index[0]),int(index[1]))
    goal = (int(index[2]),int(index[3]))

    # Removing all spaces
    for i in range(1, len(line)):
        line[i] = line[i].replace(" ", "")

    #max index of the graph
    maxy = len(line) - 1 #up down
    maxx = len(line[1]) #left right

    #update dict with start index with step cost and heuristic
    graph.update({start:(0,heuristic(start,goal),0,None)})
    
    directions = {
    0 : (1, 0),
    1 : (1,1),
    2 : (0, 1),
    3 : (-1,1),
    4 : (-1,0),
    5 : (-1,-1),
    6 : (0,-1),
    7 : (1,-1)
}
    #get k value from input
    k = int(input("Enter K value:"))
    heap = []
    heapify(heap)
    #push in (f(n),index of start)
    heappush(heap,((graph.get(start)[0]) + graph.get(start)[1],start))
    while(heap):
        #get and expand the next lowest f(n) in heap
        prev = heappop(heap)
        if(prev[1] != goal):
            #if not goal, get all 8 directions and check if valid (not in dict, not 1)
            x,y = prev[1][0], prev[1][1]
            for i in range(8):
                nx, ny = x + directions[i][0], y + directions[i][1]
                if not outofbound((nx,ny),(maxx,maxy)) and int(line[maxy-ny][nx]) != 1:
                    #if within the graph and not a wall
                    pathcost = graph.get((x,y))[0] + stepcost(graph.get((x,y))[2],i,k)
                    heur = heuristic((nx,ny),goal)
                    if (nx,ny) not in graph or graph.get((nx,ny))[0] > pathcost:
                        #if new state or have lower g(n) than exisitng, generate and put into the heap
                        nodesgenerated += 1
                        graph.update({(nx,ny):(pathcost,heur,i,prev[1])})
                        heappush(heap, ((pathcost+heur),(nx,ny)))
        else:
            #end when goal node is expanded
            break
                 
    if not graph.get(goal):
        #check if path to solution is found
        return -1

    curr = goal
    path = []
    actions = []
    f_values = []
    while(graph.get(curr) != None):
        #get the optimal path, the actions taken, and the f(n) for the cells within the path
        actions.append(graph.get(curr)[2])
        path.append(curr)
        f_values.append(graph.get(curr)[0]+graph.get(curr)[1])
        curr = graph.get(curr)[3]
        
    #minor adjustments
    actions.pop()
    actions.reverse()
    path.reverse()
    f_values.reverse()   
    depth = len(path)-1

    for pos in path:
        if(pos != start and pos != goal):
            #edit graph for cells within the path that isnt the start or goal
            x = pos[0]
            y = pos[1]
            l_index = maxy - y
            temp = line[l_index]
            line_parts = list(temp)
            line_parts[x] = "4"
            line[l_index] = line_parts
            line[l_index] = "".join(line_parts)
        
    with open("output1.txt", "w") as file:
        #create output file
        file.write(f"{depth}\n")
        file.write(f"{nodesgenerated}\n")
        file.write(f"{actions}\n")
        file.write(f"{f_values}\n")
        for i in range(1, len(line)):
            line_parts = list(line[i])
            line[i] = " ".join(line_parts)
            file.write(f"{line[i]}\n")

if __name__ == "__main__":
    main()


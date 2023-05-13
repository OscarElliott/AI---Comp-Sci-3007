from node import Node
import heapq

# AStar Search (A*)
class astar:
    def __init__(self,src,destination,X_max,Y_max,gamemap,heuristic):
        #initialize A*
        self.x0, self.y0 = src
        self.xd, self.yd = destination
        self.X_max = X_max
        self.Y_max = Y_max
        self.gamemap = gamemap
        self.counter = 0 
        self.heuristic = heuristic
        if self.heuristic == "euclidean":   
            self.heuristic = self.euclidean_distance
        elif heuristic == "manhattan":
            self.heuristic = self.manhattan_distance 
        else:
            print("Error: A* search requires valid heuristic to function, check parameters and spelling then try again")


    # Heuristic 1: Euclidean Distance
    def euclidean_distance(self, src, destination):
        heuristic1 = ((src[0]-destination[0])**2+(src[1]-destination[1])**2)**0.5
        return heuristic1

    # Heuristic 2: manhattan Distance
    def manhattan_distance(self, src, destination):
        heuristic2 = abs(src[0]-destination[0])+abs(src[1]-destination[1])
        return heuristic2

    def run(self):
        n = Node(self.x0,self.y0)
        visited = set()
        h_value = self.heuristic((self.x0,self.y0),(self.xd,self.yd))
        priority_queue = [(h_value, 0, (self.counter, n))]
        heapq.heapify(priority_queue)
        visited.add((self.x0,self.y0))
        

        while priority_queue:
            h, _, (counter, node) = heapq.heappop(priority_queue)

            if node.x == self.xd and node.y == self.yd:
                path = []
                current_node = node
                while current_node is not None:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1] 
            
            for x, y in node.get_neighbours("UDLR"):
                if 0 <= x < self.X_max and 0 <= y < self.Y_max and (x,y) not in visited and self.gamemap[x][y] != "X":
                    # find cost of move accounting for elevation
                    elevation_diffrence = int(self.gamemap[x][y]) - int(self.gamemap[node.x][node.y])
                    elevation_cost = 0 if elevation_diffrence <= 0 else elevation_diffrence
                    cost = 1 + node.cost + elevation_cost
                    heuristic_cost = cost + self.heuristic((x,y),(self.xd,self.yd))
                    self.counter += 1
                    move = self.counter
                    visited.add((x,y))
                    new_node = Node(x,y,node, cost, move)
                    heapq.heappush(priority_queue, (heuristic_cost, move, (self.counter, new_node)))
        # in case where no solution is found
        return None
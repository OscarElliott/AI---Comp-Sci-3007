from node import Node
import heapq

# Uniform Cost Search (UCS)
class ucs:
    def __init__(self,src,destination,X_max,Y_max,gamemap):
        #initialize UCS
        self.x0, self.y0 = src
        self.xd, self.yd = destination
        self.X_max = X_max
        self.Y_max = Y_max
        self.gamemap = gamemap
        self.counter = 0

    def run(self):
        n = Node(self.x0,self.y0)
        visited = set()
        priority_queue = [(0, (self.counter, n))]
        heapq.heapify(priority_queue)
        visited.add((self.x0,self.y0))


        while priority_queue:
            _, (counter, node) = heapq.heappop(priority_queue)

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
                    heuristic_cost = 0 if elevation_diffrence <= 0 else elevation_diffrence
                    cost = 1 + node.cost + heuristic_cost
                    visited.add((x,y))
                    new_node = Node(x,y,node, cost)
                    self.counter += 1
                    heapq.heappush(priority_queue, (new_node.cost, (self.counter, new_node)))
        # in case where no solution is found
        return None
from node import Node

# Breadth First Search (BFS)
class bfs:
    def __init__(self,src,destination,X_max,Y_max,gamemap):
        self.x0, self.y0 = src
        self.xd, self.yd = destination
        self.X_max = X_max
        self.Y_max = Y_max
        self.gamemap = gamemap

    def run(self):
        n = Node(self.x0,self.y0)
        visited = set()
        queue = [n]
        visited.add((self.x0,self.y0))

        while queue:
            node = queue.pop(0)

            if node.x == self.xd and node.y == self.yd:
                path = []
                current_node = node
                while current_node is not None:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1]
            
            neighbours = node.get_neighbours("UDLR")
            for neighbour in neighbours:
                x,y = neighbour
                if 0 <= x < self.X_max and 0 <= y < self.Y_max and (x,y) not in visited and self.gamemap[x][y] != "X":
                    visited.add((x,y))
                    new_node = Node(x,y,node)
                    queue.append(new_node)
        # in case where no solution is found
        return None
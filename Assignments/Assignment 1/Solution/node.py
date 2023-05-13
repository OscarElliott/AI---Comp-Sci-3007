class Node:
    #class for a "node" obnject on the map
    
    # initialize properties of node
    def __init__(self, x, y, parent=None, cost=0,move=0):
        self.x = x
        self.y = y
        self.parent = parent
        self.cost = cost
        self.move = move
    # cost comparison
    def __lt__(self, other):
        if self.cost == other.cost:
            return self.move == other.move
        return self.cost < other.cost
    
    def get_neighbours(self, move):
        move_map = {'U': (self.x-1, self.y),
                    'D': (self.x+1, self.y),
                    'L': (self.x, self.y-1),
                    'R': (self.x, self.y+1)
                    }
        neighbours = []
        for move in list(move):
            neighbours.append(move_map[move])
        return neighbours





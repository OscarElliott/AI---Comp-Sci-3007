from bfs import bfs
from ucs import ucs
from astar import astar
import sys

class Pathfinder:
    # initialize Pathfinder
    def __init__(self, src, destination, X_max, Y_max
    , gamemap, searchtype, heuristic = None):
        self.src = src
        self.destination = destination
        self.X_max = X_max
        self.Y_max = Y_max

        self.gamemap = gamemap
        self.searchtype = searchtype
        self.heuristic = heuristic

    def run(self):
        if self.searchtype == "bfs":
            model = bfs(src,destination,X_max,Y_max,gamemap)
            path = model.run()
            return path
        if self.searchtype == "ucs":
            model = ucs(src,destination,X_max,Y_max,gamemap)
            path = model.run()
            return path
        if self.searchtype == "astar":
            model = astar(src,destination,X_max,Y_max,gamemap,heuristic)
            path = model.run()
            return path
        
    def print_map(self,path):
        new_map = [row.copy() for row in self.gamemap]

        try:
            for i, j in path:
                new_map[i][j] = "*"
            
            
            for row in new_map:
                print(" ".join(row))
        except TypeError as e:
            print("null")
        
if __name__ == "__main__":
    inputfile = sys.argv[1]
    searchtype = sys.argv[2]

    if len(sys.argv) > 3:
        heuristic = sys.argv[3]
    else:
        heuristic = None

    file_ = open(inputfile)

    line = file_.readline()
    line = line.strip().split(" ")
    X_max, Y_max = int(line[0]), int(line[1])
    src = file_.readline().split()
    src = (int(src[0])-1,int(src[1])-1)
    destination = file_.readline().split()
    destination = (int(destination[0])-1, int(destination[1])-1)

    gamemap = []
    for line in file_.readlines():
        line = line.strip().split()
        gamemap.append(line)

    Search = Pathfinder(src,destination,X_max,Y_max,gamemap,searchtype,heuristic)
    path = Search.run()

    Search.print_map(path)

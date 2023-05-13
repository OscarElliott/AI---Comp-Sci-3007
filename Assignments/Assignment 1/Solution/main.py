import sys
from pathfinder import Pathfinder

if __name__ == "__main__":
    inputfile = str(sys.argv[1])
    searchtype = str(sys.argv[2])
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
    destination = (int(destination[0])-1, int(destination[1]-1))

    gamemap = []
    for line in file_.readlines():
        line = line.strip().split()
        gamemap.append(line)

    Search = Pathfinder(src,destination,X_max,Y_max,gamemap,searchtype,heuristic)
    path = Search.run()

    Search.print_map(path)
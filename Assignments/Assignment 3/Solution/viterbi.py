import sys
import numpy as np

# function to read in input file
def parse_input_file(inputfile):
    file_ = open(inputfile)
    lines = file_.readlines()
    Y_max, X_max = map(int, lines[0].strip().split(" "))
    number_of_obvs = int(lines[Y_max+1])
    error_percent = float(lines[Y_max+number_of_obvs+2])
    obvs_values = []
    for i in range(number_of_obvs):
        line = lines[Y_max+2+i].strip()
        obvs_values.append(line)
    grid = []
    for j in range(Y_max):
        line = lines[j+1].strip().split(" ")
        grid.append(line)
    return Y_max, X_max, number_of_obvs, error_percent, obvs_values, grid


class Viterbi:
    def __init__(self, Y_max, X_max, number_of_obvs, error_percent, obvs_values, grid):
        self.Y_max = Y_max
        self.X_max = X_max
        self.number_of_obvs = number_of_obvs
        self.error_percent = error_percent
        self.grid = grid
        #self.trellis = [] # list of numpy matrcies at each timestep
        self.state_space = []  # list of traversable points
        self.probabilities = [] # probabilities array
        self.Y = obvs_values
        self.K = 0  # Number of traversable points (initialized as 0)
        self.Tm = np.empty((0, 0))
        self.Em = np.empty((0, 0)) 
        #Update values
        self.initialize_state_space()
        self.K = len(self.state_space)
        self.initialize_probabilities()
        self.initialize_transition_matrix()
        self.initialize_emission_matrix()

    def initialize_probabilities(self):
        for k in range(self.Y_max):
            for j in range(self.X_max):
                if self.grid[k][j] == "0":
                    self.probabilities.append(1/self.K)
                else:
                    self.probabilities.append(0)
        

    def initialize_state_space(self):
        # add all traversable points i.e 0 to state space
        for k in range(self.Y_max):
            for j in range(self.X_max):
                if self.grid[k][j] == "0":
                    self.state_space.append((k,j))

    def initialize_transition_matrix(self):
        self.Tm = np.zeros((self.K, self.K))
        for k, state in enumerate(self.state_space):
            y, x = state
            N,S,W,E = self.get_surroundings(state)
            Valid_neighbours = 0
            Neighbours = [None,None,None,None]
            if N == '0':
                Valid_neighbours+=1
                stateN = (y-1,x)
                Neighbours[0] = self.get_transition(stateN)
            if S == '0':
                Valid_neighbours+=1
                stateN = (y+1,x)
                Neighbours[1] = self.get_transition(stateN)
            if W == '0':
                Valid_neighbours+=1
                stateN = (y,x-1)
                Neighbours[2] = self.get_transition(stateN)
            if E == '0':
                Valid_neighbours+=1
                stateN = (y,x+1)
                Neighbours[3] = self.get_transition(stateN)
            if N == '0':
                self.Tm[k, Neighbours[0]] = 1/Valid_neighbours
            if S == '0':
                self.Tm[k, Neighbours[1]] = 1/Valid_neighbours
            if W == '0':
                self.Tm[k, Neighbours[2]] = 1/Valid_neighbours
            if E == '0':
                self.Tm[k, Neighbours[3]] = 1/Valid_neighbours

    def get_transition(self,state):
        for k, state1 in enumerate(self.state_space):
            if state == state1:
                return k
            



    def get_surroundings(self, state):
        N, S, W, E = '0', '0', '0', '0'

        if state[0] > 0 and self.grid[state[0] - 1][state[1]] == 'X':
            N = '1'
        if state[0] < self.Y_max - 1 and self.grid[state[0] + 1][state[1]] == 'X':
            S = '1'
        if state[1] > 0 and self.grid[state[0]][state[1] - 1] == 'X':
            W = '1'
        if state[1] < self.X_max - 1 and self.grid[state[0]][state[1] + 1] == 'X':
            E = '1'
        if state[0] == 0:
            N = '1'
        if state[0] == self.Y_max - 1:
            S = '1'
        if state[1] == 0:
            W = '1'
        if state[1] == self.X_max - 1:
            E = '1'

        return N,S,W,E

    def initialize_emission_matrix(self):
        self.Em = np.zeros((self.K, self.number_of_obvs))
        for i, state in enumerate(self.state_space):
            state = self.state_space[i]
            N,S,W,E = self.get_surroundings(state)
            surroundings = N + S + W + E
            for j in range(self.number_of_obvs):
                error_count = 0
                for k in range(4):
                    if surroundings[k] != self.Y[j][k]:
                        error_count += 1
                emission_prob = ((1 - self.error_percent) ** (4 - error_count)) * (self.error_percent ** error_count)
                self.Em[i, j] = emission_prob


    # just useful for testing
    def SelfPrint(self):
        np.set_printoptions(threshold=np.inf)
        print(self.state_space)
        print(self.K)
        print(self.Em)
        print(self.probabilities)
        m = (X_max+X_max-1*Y_max)
        print(m)
        print(self.Tm)
        n = (self.Tm[0][1])
        print(n)
        print(self.Y)
        k = self.grid[0][4]
        print(k)
    
    def Viterbi_forward(self):
        trellis = np.zeros((self.number_of_obvs,self.Y_max,self.X_max))
        K=0
        for i in range(self.Y_max):
            for j in range(self.X_max):
                if self.probabilities[j+self.X_max*i] != 0:
                    trellis[0,i,j] = self.probabilities[j+self.X_max*i] * self.Em[K,0]
                    K+=1
                else:
                    trellis[0,i,j] = 0
        for j in range (1,self.number_of_obvs):
            for i, state in enumerate(self.state_space):
                max_prob = 0
                y,x = state
                for k in range(self.K):
                    y1,x1 = self.state_space[k]
                    prob = trellis[j-1,y1,x1] * self.Tm[k,i] * self.Em[i, j]
                    if prob > max_prob:
                        max_prob = prob
                trellis[j,y,x] = max_prob
        return trellis

    





if __name__ == "__main__":
    inputfile = sys.argv[1]

    Y_max, X_max, number_of_obvs, error_percent, obvs_values, grid = parse_input_file(inputfile)
    Solve = Viterbi(Y_max, X_max, number_of_obvs, error_percent, obvs_values, grid)
    Solve.SelfPrint()
    

    # testing
    #print(number_of_obvs)
    #print(Y_max)
    #print(X_max)
    #print(error_percent)
    #print(obvs_values)
    #print(grid)


    # given code to finish 
    maps = Solve.Viterbi_forward()
    print(*maps)
    np.savez("output.npz", *maps)
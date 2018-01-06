import numpy as np

class MealyMachineCodec(object):

    def __init__(self, states, input_symbols, output_symbols):
        self.states = states
        self.input_symbols = input_symbols
        self.output_symbols = output_symbols
        self.numofstates = len(states)
        self.numofinputs = len(input_symbols)
        self.numofoutputs = len(output_symbols)
        self.row_size = self.numofinputs * self.numofstates
        self.column_size = self.numofoutputs * self.numofstates

    def encode(self, transition, action):
        transition_matrix = np.zeros((self.row_size,  \
                self.column_size), dtype=bool)
        for i, start_state in enumerate(transition):
            for j, (input_, end_state) in enumerate(start_state.values()):
                output = action[start_state][input_]
                row = self.numofstates*i + j
                # REVIEW: For the case ends_state and output are not integers
                # Assumption: states = {0, 1, 2, ...}, output symbols = {0, 1, 2, ...}
                column = self.numofoutputs*end_state + output
                transition_matrix[row][column] = True

        return transition_matrix

    def decode(self, transition_matrix):
        transition = {}
        action = {}
        for state in self.states:
            transition[state] = {}
            action[state] = {}

        (row, column) = np.where(transition_matrix)
        for n in range(self.row_size):
            # Assumption: states, input symbols, output symbols = {0, 1, 2, ...}
            (i, j) = divmod(n, self.numofinputs)
            start_state = i
            input_ = j
            index = column[n]
            (k, l) = divmod(index, self.numofoutputs)
            end_state = k
            output = l
            transition[start_state][input_] = end_state
            action[start_state][input_] = output


        return transition, action

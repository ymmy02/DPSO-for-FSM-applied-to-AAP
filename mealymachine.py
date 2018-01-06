class MealyMachine(object):

    def __init__(self, states, init_state, input_symbols,   \
            output_symbols, transition, action):
        self.states = states
        self.input_symbols = input_symbols
        self.output_symbols = states
        self.transition = transition
        self.action = action
        self.init_state = init_state
        self.current_state = self.init_state

    def input_(self, input_symbol):
        current_state = self.current_state
        end_state = self.transition[current_state][input_symbol]
        output_symbol = self.action[current_state][input_symbol]
        self.current_state = end_state
        return output_symbol

    def run(self, inputs):
        outputs = [self.input_(i) for i in inputs]
        final_state = self.current_state
        self.current_state = self.init_state
        return outputs, final_state

    def update_functions(self, transition, action):
        self.transition = transition
        self.action = action

    def print_transition_table(self):
        print("===================================================")

        input_symbols_str = [str(i) for i in self.input_symbols]
        print("\t", "|\t".join(input_symbols_str))

        print("---------------------------------------------------")

        for state in self.states:
            end_states = self.transition[state].values()
            output_symbols = self.action[state].values()
            end_states_str = [str(state) for state in end_states]
            output_symbols_str = [str(i) for i in output_symbols]
            endstate_with_output = [end_states_str[i] + "/" + output_symbols_str[i]
                    for i in range(len(end_states_str))]
            print(str(state), "|", "\t", "|\t".join(endstate_with_output))

        print("---------------------------------------------------")
        print("===================================================")

from functions import run_simulator_with_fsm
from antsimulator import AntSimulator
from dpso import DPSOforMealyMachineConstruction

def main():

    numofstates = 5
    states = list(range(numofstates))
    input_symbols = [0, 1]  # 0:Not Found, 1:Found
    output_symbols = [0, 1, 2]  # 0:Forward, 1:Left, 2:Right

    max_moves = 600
    ant = AntSimulator(max_moves)
    with open("trialdata/santafe_trial.txt") as trial_file:
        ant.parse_matrix(trial_file)
    dpsommc = DPSOforMealyMachineConstruction(ant)

    dpsommc.construct(states, input_symbols, output_symbols, population=10, maxloop=10)

    mealymachines = dpsommc.best_mealymachines

    for mealymachine in mealymachines:
        mealymachine.print_transition_table()
        run_simulator_with_fsm(ant, mealymachine)
        ant.reset()
        ant.print_route()

if __name__ == "__main__":
    main()

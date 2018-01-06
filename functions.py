import random
import numpy as np

from particle import Particle
from mealymachine import MealyMachine
from enums import InputSymbol, OutputSymbol

def create_mealymachine(states, input_symbols,  \
        output_symbols, matrix, codec):
    init_state = states[0]
    (transition, action) = codec.decode(matrix)
    mealymachine = MealyMachine(states, init_state,     \
            input_symbols, output_symbols, transition, action)
    return mealymachine

def create_particle(states, input_symbols, output_symbols, codec):
    row_size = len(input_symbols) * len(states)
    column_size = len(output_symbols) * len(states)
    pos = np.eye(row_size, column_size, dtype=bool)
    for row in pos:
        np.random.shuffle(row)
    # REVIEW: Whether initializing vel=0  works well 
    vel = np.zeros((row_size, column_size))

    particle = Particle(pos, vel)
    particle.mealymachine = create_mealymachine(states,    \
            input_symbols, output_symbols, pos, codec)

    return particle

def run_simulator_with_fsm(antsimulator, mealymachine):
    while antsimulator.moves < antsimulator.max_moves and  \
            antsimulator.eaten < antsimulator.allfoods:
        input_ = InputSymbol.FOUND if    \
                antsimulator.sense_food() else InputSymbol.NOTFOUND
        output = mealymachine.input_(input_)
        if output == OutputSymbol.FORWARD:
            antsimulator.move_forward()
        elif output == OutputSymbol.LEFT:
            antsimulator.turn_left()
        elif output == OutputSymbol.RIGHT:
            antsimulator.turn_right()
    fitness = antsimulator.eaten
    return fitness

# TODO: Implement
def pickup_best_mealymachines(swarm):
    best_mealymachines = []
    gbest = swarm[0].gbest
    return best_mealymachines

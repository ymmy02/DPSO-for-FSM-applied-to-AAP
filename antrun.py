from enums import InputSymbol, OutputSymbol

def run_with_fsm(antsimulator, mealymachine):
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

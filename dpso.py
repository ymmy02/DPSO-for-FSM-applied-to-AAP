import random
import numpy as np

import functions as fnc
from mealymachine import MealyMachine
from codec import MealyMachineCodec

class DPSOforMealyMachineConstruction(object):

    def __init__(self, ant):
        self._best_mealymachines = []
        self.codec = None
        self.ant = ant
        self.c1 = None
        self.c2 = None
        self.best_fitness = 0

    def construct(self, states, input_symbols, output_symbols,  \
            population=10, maxloop=10, c1=2, c2=2):

        self.c1 = c1
        self.c2 = c2
        ##############
        # Initialize #
        ##############
        self.codec = MealyMachineCodec(states, input_symbols, output_symbols)
        swarm = [fnc.create_particle(states, input_symbols, output_symbols, self.codec)
                for _ in range(population)]
        # Vectorize Functions
        vadvance = np.vectorize(self._advance)
        vupdatemealymachine = np.vectorize(self._updatemealymachine)
        #vevaluate = np.vectorize(self._evaluate)
        # Evaluate Fitness
        for particle in swarm:
            self._evaluate(particle)
            particle.pbest_fitness = particle.fitness
        # Set Global Best
        self._updategbest(swarm)

        #############
        # Main Loop #
        #############
        for n in range(maxloop):
            vadvance(swarm)
            vupdatemealymachine(swarm)
            for particle in swarm:
                self._evaluate(particle)
            self._updatepbest(swarm)
            self._updategbest(swarm)
            self._printlog(swarm, n, nskip=1)

        #################
        # Output Result #
        #################
        init_state = states[0]
        gbest = swarm[0].gbest
        (transition, action) = self.codec.decode(gbest)
        bestmm = MealyMachine(states, init_state,     \
                input_symbols, output_symbols, transition, action)
        self._best_mealymachines.append(bestmm)

    def _advance(self, particle):
        pos_float = particle.pos.astype(float)
        vel = particle.vel
        pbest = particle.pbest
        gbest = particle.gbest
        r1 = random.random()
        r2 = random.random()
        vel += self.c1 * r1 * (pbest.astype(float)-pos_float)
        vel += self.c2 * r2 * (gbest.astype(float)-pos_float)
        new_pos = np.zeros(particle.pos.shape, dtype=bool)
        indices = np.argmax(vel, axis=1)
        for i, j in enumerate(indices):
            new_pos[i][j] = True
        particle.vel = vel
        particle.pos = new_pos

    def _updatepbest(self, swarm):
        for particle in swarm:
            if particle.fitness > particle.pbest_fitness:
                particle.pbest = particle.pos
                particle.pbest_fitness = particle.fitness

    # REVIEW: Consider some particle has the same fitness value
    def _updategbest(self, swarm):
        best_particles = []
        best_fitness = max(p.pbest_fitness for p in swarm)
        if best_fitness < self.best_fitness:
            return

        self.best_fitness = best_fitness
        indices = [i for i,p in enumerate(swarm) if p.pbest_fitness == best_fitness]
        index = random.choice(indices)
        for particle in swarm:
            particle.gbest = swarm[index].pbest.copy()
            particle.gbest_fitness = swarm[index].pbest_fitness

    def _evaluate(self, particle):
        antsimulator = self.ant
        mealymachine = particle.mealymachine
        fnc.run_simulator_with_fsm(antsimulator, mealymachine)
        n = float(antsimulator.eaten)
        s_max = float(antsimulator.max_moves)
        s_last = float(antsimulator.moves)
        fitness = n + (s_max-s_last-1) / s_max
        particle.fitness = fitness
        antsimulator.reset()

    def _updatemealymachine(self, particle):
        (transition, action) = self.codec.decode(particle.pos)
        particle.mealymachine.update_functions(transition, action)

    def _printlog(self, swarm, loopcount, nskip=1):
        if loopcount%nskip != 0:
            return
        gbest = swarm[0].gbest
        print("########## Time Step:", loopcount, "##########")
        # Best Fitness
        print("Best Fitness:", self.best_fitness)
        # Best Mealy Machine
        print("Best Encoded Mealy Machine")
        print(gbest.astype(int))

    #def _pick_up_best_mealymachines(self, swarm):
    #    states = self.states
    #    init_state = states[0]
    #    input_symbols = self.input_symbols
    #    output_symbols = output_symbols
    #    gbest = swarm[0].gbest
    #    (transition, action) = self.codec.decode(gbest)
    #    bestmm = MealyMachine(states, init_state,     \
    #            input_symbols, output_symbols, transition, action)
    #    self._best_mealymachines.append(bestmm)

    @property
    def best_mealymachines(self):
        return self._best_mealymachines

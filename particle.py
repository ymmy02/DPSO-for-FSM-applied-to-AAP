class Particle(object):

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.fitness = None
        self.pbest = self.pos
        self.pbest_fitness = None
        self.gbest = None
        self.gbest_fitness = None
        self.mealymachine = None

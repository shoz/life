# -*- coding: utf-8 -*-

import os
import gzip
import tempfile
import operator
import math
import logging
import sys
import random
import numpy

from deap import gp, creator, tools, base, algorithms
from deap.gp import PrimitiveSet, genFull, PrimitiveTree

def get_complexity(individual, pset):
    data = str(individual)
    temp = tempfile.NamedTemporaryFile(delete=False)
    f = gzip.open(temp.name, 'wb', 9)
    f.write(data)
    f.close()
    size = os.path.getsize(temp.name)
    os.remove(temp.name)
    return size,

pset = PrimitiveSet("main", 2)
pset.addPrimitive(max, 2)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(operator.neg, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
#pset.addTerminal(3)

pset.renameArguments(ARG0="x")

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual",
               gp.PrimitiveTree,
               fitness=creator.FitnessMin,
               pset=pset)

toolbox = base.Toolbox()
toolbox.register('expr', gp.genFull, pset=pset, min_=10, max_=15)
toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('compile', gp.compile, pset=pset)
toolbox.register('evaluate', get_complexity, pset=pset)
toolbox.register('select', tools.selTournament, tournsize=1)
toolbox.register('mate', gp.cxOnePoint)
toolbox.register('expr_mut', gp.genFull, min_=0, max_=10)
toolbox.register('mutate', gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

population = toolbox.population(n=300)
hof = tools.HallOfFame(1)
stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
stats_size = tools.Statistics(len)
mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
mstats.register('avg', numpy.mean)
mstats.register('std', numpy.std)
mstats.register('min', numpy.min)
mstats.register('max', numpy.max)

population, log = algorithms.eaSimple(population,
                                      toolbox,
                                      0.3,  # mate
                                      0.1,  # mutation
                                      50,   # Generation
                                      stats=mstats,
                                      halloffame=hof,
                                      verbose=True)

print str(hof[0])

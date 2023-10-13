from random import random
from game import testInd

from deap import algorithms, base, creator, tools
import matplotlib
matplotlib.use('TkAgg')  # Or you can use 'Agg', 'Qt5Agg', etc.
import matplotlib.pyplot as plt
import numpy as np

moves = ["C", "M", "CC", "MM", "CM"]


# Generate a random individual of length 11 made up of valid moves
def randInd():
    ind = []
    for i in range(11):
        ind.append(moves[int(random() * len(moves))])
    return ind


def mutate(ind):
    ind[int(random() * len(ind))] = moves[int(random() * len(moves))]
    return ind,


def detailInd(ind):
    print(ind)
    print("Fitness: " + str(testInd(ind)))


#detailInd(randInd())


def evoAlgorithm(verbose=False):
    ## SET UP THE EVOLUTIONARY ALGORITHM
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    toolbox.register("indices", randInd)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", testInd)

    toolbox.register("mate", tools.cxTwoPoint)

    toolbox.register("mutate", mutate)

    toolbox.register("select", tools.selTournament, tournsize=5)

    population = toolbox.population(n=600)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    stats.register("median", np.median)

    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.7, mutpb=0.9, ngen=50, stats=stats,
                                              halloffame=hof, verbose=verbose)

    return population, logbook, hof

population, logbook, hof = evoAlgorithm(True)

print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))

# Extract statistics from logbook
gen = logbook.select("gen")
avg = logbook.select("avg")
std = logbook.select("std")
min_ = logbook.select("min")
max_ = logbook.select("max")
median_ = logbook.select("median")

# Plot the statistics
plt.figure()
plt.errorbar(gen, avg, yerr=std, label="Average", linewidth=2)
plt.plot(gen, min_, label="Minimum", linewidth=2)
plt.plot(gen, max_, label="Maximum", linewidth=2)
plt.plot(gen, median_, label="Median", linewidth=2)
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend(loc="lower right")
plt.title("Fitness Statistics Across Generations")
plt.show()

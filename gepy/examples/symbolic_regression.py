from gepy.functions.linking import sum_linker
from gepy.functions.arithmetic import addition, subtraction, multiplication, division
from gepy.chromosome import StandardChromosome
from gepy.population import StandardPopulation
import random
from time import time

class DataPoint:
    SAMPLE = []
    SAMPLE_SIZE = 10
    RANGE_LOW, RANGE_HIGH = -10.0, 10.0
    RANGE_SIZE = RANGE_HIGH - RANGE_LOW

    def __init__(self, x):
        self.x = float(x)
        self.y = 4 * (x ** 3) + 2 * x + 5

    @staticmethod
    def populate():
        DataPoint.SAMPLE = []
        for _ in range(DataPoint.SAMPLE_SIZE):
            x = DataPoint.RANGE_LOW + (random.random() * DataPoint.RANGE_SIZE)
            DataPoint.SAMPLE.append(DataPoint(x))

class Regression(StandardChromosome):
    REWARD = 1000.0
    tree_functions = addition, subtraction, multiplication, division
    tree_terminals = ('x', 2, 3)

    def _fitness(self):
        total = 0
        for x in DataPoint.SAMPLE:
            try:
                guess = self(x=x.x)
                diff = min(1.0, abs((guess - x.y) / x.y))
                total += Regression.REWARD * (1 - diff)
            except ZeroDivisionError:
                return 0
        return total

    def _solved(self):
        return self.REWARD * 10 - self.fitness <= 0.1**6

if __name__ == "__main__":
    DataPoint.populate()

    p = StandardPopulation(Regression, 30, 3, 6, Regression.tree_functions, Regression.tree_terminals, sum_linker, mutation=2.5/45, inversion=0.1)
    print(p)
    print()

    start = time()
    for _ in range(150):
        if p.best.solved:
            break
        p.evolve()
        print(p.generation, p.best, p.best.fitness)
    end = time()

    if p.best.solved:
        print()
        print('SOLVED:', p.best)

    print('Took %.3fms per cycle' % (1000 * (end - start) / p.generation))

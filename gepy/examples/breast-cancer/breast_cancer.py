from gepy.functions.linking import argmax_linker
from gepy.functions.arithmetic import addition, subtraction, multiplication, division
from gepy.chromosome import StandardChromosome
from gepy.population import StandardPopulation
from time import time
import csv

SAMPLE = []
SAMPLE_SIZE = 0
TEST = []

class CsvData:
    @staticmethod
    def populate():
        global SAMPLE_SIZE
        global SAMPLE
        global TEST
        with open("breast-cancer-wisconsin.data", "r") as csvfile:
            SAMPLE_SIZE = 0
            SAMPLE = []
            TEST = []
            points = csv.DictReader(csvfile, fieldnames=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'cls'])
            for row in points:
                for field in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'cls']:
                    row[field] = int(row[field]) if row[field] != '?' else -10
                if SAMPLE_SIZE < 500:
                    SAMPLE.append(row)
                    SAMPLE_SIZE += 1
                else:
                    TEST.append(row)

class Cancer(StandardChromosome):
    tree_functions = addition, subtraction, multiplication, division
    tree_terminals = '2', '3', '4', '5', '6', '7', '8', '9', '10'

    def _fitness(self, dataset=None):
        dataset = dataset if dataset is not None else SAMPLE
        total = 0
        for x in dataset:
            try:
                guess = self(dictionary=x)
                total += 1 if guess[0] == x['cls'] / 2 - 1 else 0
            except (ZeroDivisionError, ValueError, TypeError):
                pass
        return total
    
    def _solved(self):
        return self.fitness == SAMPLE_SIZE

if __name__ == "__main__":
    CsvData.populate()
    p = StandardPopulation(Cancer, 30, 2, 6, Cancer.tree_functions, Cancer.tree_terminals, argmax_linker, mutation=2.0/25, inversion=0.1)
    print(p)

    start = time()
    for i in range(100):
        if p.best.solved:
            break

        p.cycle()
        print(i, p.best, p.best.fitness)
    end = time()
    print('Per cycle: %.3fms' % (1000 * (end - start) / i))

    if p.best.solved:
        print("SOLVED:", p.best)
    else:
        print("BEST SAMPLE:", p.best.fitness, "of", SAMPLE_SIZE, "(%.3f)" % (100 * p.best.fitness / SAMPLE_SIZE))
        
    test_fitness = p.best._fitness(dataset=TEST)
    test_length = len(TEST)
    print("EVALUATION OF BEST", test_fitness, "of", test_length, "(%.3f)" % (100 * test_fitness / test_length))

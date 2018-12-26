from gepy.chromosome import StandardChromosome
from gepy.population import StandardPopulation
from gepy.functions.linking import append_linker
from gepy.examples.subroutine_generation.functions import add, mul, sub, div, dup, swap, nop, ret, inc, dec
from time import time
from copy import deepcopy

class VM(StandardChromosome):
    tree_functions = add, mul, sub, div, dup, swap, nop, ret, inc, dec
    tree_terminals = ('stack',)

    # We try to get the function x -> x (x + 1)
    SAMPLES = [(2.0, 6.0), (-3.0, 6.0), (10.0, 110.0), (12.0, 156.0)]

    def _fitness(self):
        total = 0.0
        for x in VM.SAMPLES:
            start, target = x
            try:
                guess = self(stack=deepcopy([start])).pop()
                diff = min(1.0, abs((target - guess) / target))
                total += 1000.0 * (1.0 - diff)
            except (ZeroDivisionError, ValueError, TypeError, IndexError) as e:
                pass
        return total

    def _solved(self):
        return self.fitness == len(VM.SAMPLES) * 1000

if __name__ == "__main__":
    p = StandardPopulation(VM, 30, 1, 8, VM.tree_functions, VM.tree_terminals, append_linker, mutation=2.0/12, inversion=0.1)
    print(p)

    start = time()
    for i in range(250):
        if p.best.solved:
            break

        p.cycle()
        print(i, p.best, p.best.fitness)
    end = time()
    print('Per cycle: %.3fms' % (1000 * (end - start) / i))

    if p.best.solved:
        print('SOLVED:', p.best)
    

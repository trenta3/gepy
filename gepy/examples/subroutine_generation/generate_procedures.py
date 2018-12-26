from gepy.chromosome import StandardChromosome
from gepy.population import StandardPopulation
from gepy.functions.linking import append_linker
from gepy.examples.subroutine_generation.functions import add, mul, sub, div, dup, swap, nop, ret, inc, dec, swap3
from time import time, sleep
from copy import deepcopy

class VM(StandardChromosome):
    tree_functions = add, mul, sub, div, dup, swap, swap3, ret, inc, dec
    tree_terminals = ('stack',)

    def _fitness(self):
        total = 0.0
        for x in VM.SAMPLES:
            start, target = x
            try:
                guess = self(stack=deepcopy(start)).pop()
                diff = min(1.0, abs((target - guess) / target))
                total += 1000.0 * (1.0 - diff)
            except (ZeroDivisionError, ValueError, TypeError, IndexError) as e:
                pass
        return total

    def _solved(self):
        return abs(len(VM.SAMPLES) * 1000 - self.fitness) <= 0.1**6


def use_functions_with(samples):
    VM.SAMPLES = samples
    p = StandardPopulation(VM, 30, 1, 12, VM.tree_functions, VM.tree_terminals, append_linker, mutation=2.0/16, inversion=0.1)
    print(p)

    start = time()
    for i in range(10000):
        if p.best.solved:
            break

        p.cycle()
        print(i, p.best, p.best.fitness)
    end = time()
    print('Per cycle: %.3fms' % (1000 * (end - start) / i))

    if p.best.solved:
        print('SOLVED:', p.best)
    
if __name__ == "__main__":
    # We try to get the function x -> x (x + 1)
    FIRST_FUNCTION = [([2.0], 6.0), ([-3.0], 6.0), ([10.0], 110.0), ([12.0], 156.0)]
    use_functions_with(FIRST_FUNCTION)
    sleep(5)
    
    # x, y -> (y + 1) / x
    SECOND_FUNCTION = [([2.0, 3.0], 2.0), ([1.0, 0.0], 1.0), ([1.5, 5.0], 4.0)]
    use_functions_with(SECOND_FUNCTION)
    sleep(5)

    # x, y -> x * y / (x + y)
    # We list here some of the obtained exact solutions:
    # div.mul.swap3.add.swap3.dup.swap3.dup.stack
    # dup.div.swap3.dup.inc.div.dec.swap.swap3.dec.dup.inc.stack
    # dup.inc.div.sub.swap3.dup.inc.div.swap3.swap.swap3.dup.stack
    # inc.dup.dec.div.mul.swap3.inc.dup.div.swap3.dup.swap.stack
    # div.inc.swap.inc.inc.dec.div.swap3.dec.swap.swap3.dup.stack
    THIRD_FUNCTION = [([15.0, 5.0], 3.75), ([5.0, 5.0], 2.5), ([3.0, 7.0], 2.1), ([2.0, 8.0], 1.6), ([10.0, 10.0], 5.0)]
    use_functions_with(THIRD_FUNCTION)


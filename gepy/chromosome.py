from random import random
from math import floor
from .genes import Gene
from .exceptions import ImplementationError

class StandardChromosome:
    def __init__(self, gene_number, genes_head, tree_functions=None, tree_terminals=None, linking_function=None):
        self._cantchange = False
        self.modified_round = 0
        self.gene_number = gene_number
        self.genes_head = genes_head
        self.linking_function = linking_function if linking_function is not None else self.__class__.linking_function
        self.tree_functions = tree_functions if tree_functions is not None else self.__class__.tree_functions
        self.tree_terminals = tree_terminals if tree_terminals is not None else self.__class__.tree_terminals
        self.genes = [Gene(head_length=genes_head, tree_functions=tree_functions, tree_terminals=tree_terminals)
                      for _ in range(gene_number)]
        for gene in self.genes:
            gene.initialize()

    def _fitness(self):
        """
        User-implemented function, should return the fitness value for the chromosome
        """
        raise ImplementationError("You should provide a _fitness function for the chromosomes")
            
    def _solved(self):
        """
        If not subclassed, it always returns False.
        If it returns True, the search is stopped since an optimal chromosome has been found.
        """
        return False
    
    def __call__(self, **kwargs):
        args = []
        for gene in self.genes:
            args.append(gene(**kwargs))
        return self.linking_function(*args)

    def __len__(self):
        """
        Returns the real chromosome length as tree.

        It also counts the linking function at the start.
        """
        return 1 + sum([len(gene) for gene in self.genes])

    def __repr__(self):
        """
        Returns a representation of the chromosome.
        """
        return "|".join([repr(gene) for gene in self.genes])

    def mutate(self, rate, rnd):
        for gene in self.genes:
            if gene.mutate(rate):
                self.modified_round = rnd

    def inversion(self, rate, rnd):
        if random() <= rate:
            gene_to_invert = floor(self.gene_number * random())
            self.genes[gene_to_invert].inversion()
            self.modified_round = rnd
            return True

    def IS_transposition(self, rate, rnd):
        if random() <= rate:
            gene_to_transpose = floor(self.gene_number * random())
            self.genes[gene_to_transpose].IS_transposition()
            self.modified_round = rnd
            return True

    def RIS_transposition(self, rate, rnd):
        if random() <= rate:
            gene_to_transpose = floor(self.gene_number * random())
            self.genes[gene_to_transpose].RIS_transposition()
            self.modified_round = rnd
            return True

    @property
    def modified(self):
        return self.modified_round

    def __cmp__(self, other):
        # Returns -1 if self < other, 0 if self == other, 1 if self > other
        if self.fitness < other.fitness:
            return -1
        elif self.fitness > other.fitness:
            return 1
        elif self.modified > other.modified:
            return 1
        elif self.modified < other.modified:
            return -1
        else:
            return 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __neq__(self, other):
        return self.__cmp__(other) != 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0


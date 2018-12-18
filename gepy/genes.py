from gepy.utils import arity, list_choose_rand, choose_rand
from gepy.exceptions import InitializationError, EvaluationError
from random import random
from math import floor
from copy import deepcopy

class Gene:
    """
    Fundamental class to handle all different kind of genes.
    """
    def __init__(self, head_length, tree_functions, tree_terminals):
        self.head_length = head_length
        self.tree_functions = list(tree_functions)
        self.tree_terminals = list(tree_terminals)
        max_arity = max([arity(fn) for fn in tree_functions])
        self.tail_length = head_length * (max_arity - 1) + 1

    def initialize(self, value=None):
        """
        Perform initialization of the gene.
        If 'value' is a list of tree_functions and tree_terminals it will be copied into the gene, otherwise a random initialization will be performed.
        """
        if value is not None:
            if len(value) == self.head_length + self.tail_length:
                self.gene_head = value[:self.head_length]
                self.gene_tail = value[self.head_length:]
            else:
                raise InitializationError("The value given to the gene doesn't have the required length.")
        else:
            self.gene_head = list_choose_rand(self.tree_functions + self.tree_terminals, self.head_length)
            self.gene_tail = list_choose_rand(self.tree_terminals, self.tail_length)

    def __repr__(self):
        get_symbol = lambda x: x._symbol if x in self.tree_functions else str(x)
        return ".".join(map(get_symbol, self.gene_head + self.gene_tail))

    def __len__(self):
        """
        Returns the length of the tree represented by the gene.
        """
        # Calculated as gene_total_length - values_remaining_on_the_stack + 1
        gene = self.gene_head + self.gene_tail
        stack_elements = 0
        for element in gene[-1::-1]:
            if element in self.tree_terminals:
                stack_elements += 1
            elif element in self.tree_functions:
                stack_elements -= (arity(element) - 1)
        return self.head_length + self.tail_length - stack_elements + 1
    
    def funcdict(self):
        return {fn._symbol: fn for fn in self.gene_head + self.gene_tail}
    
    def fromstring(self, string):
        funcdict = self.funcdict()
        thelist = list(map(lambda x: funcdict.get(x, int(x)), string.split(".")))
        self.gene_head = thelist[:self.head_length]
        self.gene_tail = thelist[self.head_length:]

    def valu(self, kwargs, sp=0, collect=1):
        # PERFORMANCE: We evaluate starting from the start of the gene
        results = []
        while collect > 0:
            element = self.gene_head[sp] if sp < self.head_length else self.gene_tail[sp - self.head_length]
            collect -= 1
            sp += 1
            if element in self.tree_terminals:
                results.append(kwargs.get(element, element))
            else:
                args, sp = self.valu(kwargs, sp=sp, collect=element._arity)
                results.append(element(*args))
        return results, sp
        
    def __call__(self, **kwargs):
        """
        Evaluate the expression expressed from the gene.
        """
        return self.valu(kwargs=kwargs)[0][0]

    def tofunction(self):
        """
        Returns a python function that evaluates the current gene.
        """
        return self.__call__

    def mutate(self, rate):
        for idx in range(self.head_length):
            if random() <= rate:
                self.gene_head[idx] = choose_rand(self.tree_functions + self.tree_terminals)
        for idx in range(self.tail_length):
            if random() <= rate:
                self.gene_tail[idx] = choose_rand(self.tree_terminals)

    def inversion(self):
        initial_head_point = floor(random() * self.head_length)
        final_head_point = floor(random() * self.head_length)
        start = min(initial_head_point, final_head_point)
        end = max(initial_head_point, final_head_point) + 1
        self.gene_head[start:end] = self.gene_head[start:end][-1::-1]

    def IS_transposition(self):
        # NOTE: This only takes a part of the tail and copies it somewhere else
        initial_tail_point = floor(random() * self.tail_length)
        final_tail_point = floor(random() * self.tail_length)
        start = min(initial_tail_point, final_tail_point)
        end = max(initial_tail_point, final_tail_point)
        target_point = floor(random() * (self.head_length + self.tail_length))
        totalgene = self.gene_head + self.gene_tail
        if target_point + end - start > self.head_length + self.tail_length:
            end = self.head_length + self.tail_length - target_point + start
        totalgene[target_point:target_point + end - start] = deepcopy(self.gene_tail[start:end])
        self.gene_head = totalgene[:self.head_length]
        self.gene_tail = totalgene[self.head_length:self.head_length + self.tail_length + 1]
        assert len(self.gene_tail) == self.tail_length

    def RIS_transposition(self):
        initial_head_point = floor(random() * self.head_length)
        while initial_head_point < self.head_length:
            if self.gene_head[initial_head_point] in self.tree_functions:
                break
            initial_head_point += 1
        else:
            # No function found, we return
            return False
        # We are on a function site
        totalgene = self.gene_head + self.gene_tail
        final_point = initial_head_point + floor(random() * (self.head_length + self.tail_length - initial_head_point))
        totalgene[:final_point - initial_head_point] = deepcopy(totalgene[initial_head_point:final_point])
        self.gene_head = totalgene[:self.head_length]
        self.gene_tail = totalgene[self.head_length:self.head_length + self.tail_length + 1]
        assert len(self.gene_tail) == self.tail_length
        
# TODO: RNC Genes, ADF Genes

class StandardGene(Gene):
    """
    Class for standard genes, i.e. expression trees.
    
    Evolution operators implemented:
    - Replication
    - Mutation
    - Inversion
    - IS Transposition
    - Reproduction
    - RIS Transposition
    - Gene Transposition
    - One-point Recombination
    - Two-point Recombination
    - Gene Recombination
    """
    pass

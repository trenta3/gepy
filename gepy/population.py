from .exceptions import InitializationError, ImplementationError
from .chromosome import StandardChromosome
from .selection import RouletteWheelSelection
from .utils import argmax
from random import random

class StandardPopulation:
    """
    Handles a population of uniform chromosomes...
    """
    default_rates = dict(
        replication=0,
        mutation=0.05,
        inversion=0.1,
        IS_transposition=0.1,
        RIS_transposition=0,
        gene_transposition=0,
        one_point_recombination=0,
        two_point_recombination=0,
        gene_recombination=0
    )
    
    def __init__(self, chromosomecls, population_size, chromosome_genes, genes_head, tree_functions, tree_terminals, linking_function, selection_strategy=RouletteWheelSelection(), chromosomes=None, **kwargs):
        self.current_round = 0
        self.solved = False
        self.population_size = population_size
        self.selection_strategy = selection_strategy
        if chromosomes is not None:
            if len(chromosomes) != population_size:
                raise InitializationError("The given chromosomes' lenght is not the population size")
            self.population = chromosomes
        else:
            self.population = [chromosomecls(gene_number=chromosome_genes, genes_head=genes_head, tree_functions=tree_functions, tree_terminals=tree_terminals, linking_function=linking_function)
                               for _ in range(population_size)]
        for attr, default in StandardPopulation.default_rates.items():
            self.__dict__[attr] = default if not attr in kwargs else kwargs[attr]

    def evaluate(self):
        """
        Evaluates the fitness of all the chromosomes.
        """
        if not hasattr(self, "evaluation_round") or self.evaluation_round != self.current_round:
            # PERFORMANCE: Prevent multi-time evaluation of the current chromosomes
            self.evaluation_round = self.current_round
            for chromosome in self.population:
                chromosome.fitness = chromosome._fitness()
                chromosome.solved = chromosome._solved()

    def cycle(self):
        # For retrocompatibility with PyGEP
        self.evolve()
                
    def evolve(self, selection_strategy=None, **kwargs):
        """
        Handles a round of evolution of the population.

        This consist of:
        - The evaluation of chomosomes
        - The selection phase
        - The evolution functions
        """
        # 1. Evaluate all of the chromosomes
        self.evaluate()
        # 2. Selection phase using the strategy
        sstrategy = self.selection_strategy if selection_strategy is None else selection_strategy
        new_population = sstrategy.select(self.population)
        self.population = new_population
        # 3. Applying evolution functions
        for attr, _ in StandardPopulation.default_rates.items():
            rate = self.__dict__[attr] if not hasattr(kwargs, attr) else kwargs[attr]
            if rate > 0:
                if "action_%s" % attr in self.__class__.__dict__:
                    self.__getattribute__("action_%s" % attr)(rate=rate, rnd=self.current_round) # Perform evolution function with its rate
                else:
                    raise ImplementationError("The evolution function action_%s is not there!" % attr)
        # The population has been evolved successfully
        self.current_round += 1

    @property
    def generation(self):
        return self.current_round
        
    @property
    def best(self):
        self.evaluate()
        return self.population[argmax(self.population, lambda x: x.fitness)]

    def __repr__(self):
        """
        Returns a representation for the population suitable for printing.
        """
        rep = "[Size: %d | Round: %d | Best fitness: %f]\n" % (self.population_size, self.current_round, self.best.fitness)
        for order, chromosome in enumerate(self.population, 1):
            rep += "%d - %s [%d] (%f)\n" % (order, repr(chromosome), len(chromosome), chromosome.fitness)
        return rep

    def __len__(self):
        """
        Returns the number of individuals in the population.
        """
        return self.population_size

    def action_mutation(self, rate, rnd):
        """
        Mutates the chromosomes...
        """
        for chromosome in self.population[1:]:
            chromosome.mutate(rate, rnd)
        
    def action_inversion(self, rate, rnd):
        """
        Inverts the chromosomes' genes' head...
        """
        for chromosome in self.population[1:]:
            chromosome.inversion(rate, rnd)
        
    def action_IS_transposition(self, rate, rnd):
        """
        Transposes a random sequence at a random point of a chromosome...
        """
        for chromosome in self.population[1:]:
            chromosome.IS_transposition(rate, rnd)

"""
Selection strategies for populations.

- Roulette-wheel with simple elitism
"""
from .exceptions import SelectionError
from itertools import accumulate
from random import random
from bisect import bisect
from copy import deepcopy

class RouletteWheelSelection:
    """
    Selection strategy of the roulette-wheel:

    - First save the best 'simple_elitism' individuals.
    - Then assign a different probability of beign extracted based on fitness.
    - Then extract randomly some of those individuals
    """
    def __init__(self, simple_elitism=1):
        self.simple_elitism = simple_elitism

    def select(self, population):
        population_size = len(population)
        population.sort(reverse=True)
        new_population = []
        # Perform the simple elitism selection
        if self.simple_elitism <= population_size:
            new_population = [deepcopy(el) for el in population[:self.simple_elitism]]
            assert len(new_population) == self.simple_elitism, "Population size should be the same as simple elitism"
            for chromosome in new_population:
                chromosome._cantchange = True # Cause are the best
        else:
            raise SelectionError("The population size is less than the simple elitism...")
        # Perform the roulette-wheel selection
        cumulative_fitness = list(accumulate(map(lambda x: x.fitness, population)))
        for _ in range(population_size - len(new_population)):
            extracted_value = random() * cumulative_fitness[-1]
            extracted_index = bisect(cumulative_fitness, extracted_value)
            assert extracted_index >= 0 and extracted_index < len(population), "Extracted index was out of bounds"
            new_individual = deepcopy(population[extracted_index])
            new_individual._cantchange = False
            new_population.append(new_individual)
            assert id(new_population[-1]) != id(population[extracted_index]), "The population element was not deepcopied"
        assert len(new_population) == len(population), "The new population has not the same size as before"
        return new_population

from random import sample
from Domain.Individual import Individual

class Population:  # Population of individuals
    def __init__(self, individuals):
        self.individuals = individuals

    @staticmethod
    def genIndividuals(sz, genes):
        individuals = []
        for _ in range(sz):
            individuals.append(Individual(sample(genes, len(genes))))
        return Population(individuals)

    def add(self, route):
        self.individuals.append(route)

    def rmv(self, route):
        self.individuals.remove(route)

    def getFittest(self):
        fittest = self.individuals[0]
        for route in self.individuals:
            if route.fitness > fittest.fitness:
                fittest = route

        return fittest


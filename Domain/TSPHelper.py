from Domain.ExecutionParameters import ExecutionParameters
from random import random, randint, sample
from Domain.Individual import Individual
from Domain.Population import Population
from sys import maxsize
from time import time


class GeneticAlgorithmRunner:
    def __init__(self, parameters: ExecutionParameters, genes):
        self.genes = genes
        self.pop_size = parameters.PopSize
        self.n_gen = parameters.NGen
        self.tourn_size = parameters.TournSize
        self.mut_rate = parameters.MutRate
        self.verbose = 1

    def run(self):
        population = Population.genIndividuals(self.pop_size, self.genes)
        history = {'cost': [population.getFittest().travel_cost]}
        counter, generations, min_cost = 0, 0, maxsize

        print("Caxiero Viajante => Iniciando execução...")

        start_time = time()
        while counter < self.n_gen:
            population = self.evolve(population, self.tourn_size, self.mut_rate)
            cost = population.getFittest().travel_cost

            if cost < min_cost:
                counter, min_cost = 0, cost
            else:
                counter += 1

            generations += 1
            history['cost'].append(cost)

        total_time = round(time() - start_time, 6)

        print("Caxiero Viajante => Evolução demorou {} gerações e encontrou a menor distância em {} KM".format(generations, min_cost))

        history['generations'] = generations
        history['total_time'] = total_time
        history['route'] = population.getFittest()

        return history


    def evolve(self, pop, tourn_size, mut_rate):
        new_generation = Population([])
        pop_size = len(pop.individuals)
        elitism_num = pop_size // 2

        # Elitism
        for _ in range(elitism_num):
            fittest = pop.getFittest()
            new_generation.add(fittest)
            pop.rmv(fittest)

        # Crossover
        for _ in range(elitism_num, pop_size):
            parent_1 = self.selection(new_generation, tourn_size)
            parent_2 = self.selection(new_generation, tourn_size)
            child = self.crossover(parent_1, parent_2)
            new_generation.add(child)

        # Mutation
        for i in range(elitism_num, pop_size):
            self.mutate(new_generation.individuals[i], mut_rate)

        return new_generation


    def crossover(self, parent_1, parent_2):
        def FillWithFirstParentGenes(child, parent, genes_n):
            start_at = randint(0, len(parent.genes)-genes_n-1)
            finish_at = start_at + genes_n
            for i in range(start_at, finish_at):
                child.genes[i] = parent_1.genes[i]

        def FillWithSecondParentGenes(child, parent):
            j = 0
            for i in range(0, len(parent.genes)):
                if child.genes[i] == None:
                    while parent.genes[j] in child.genes:
                        j += 1
                    child.genes[i] = parent.genes[j]
                    j += 1

        genes_n = len(parent_1.genes)
        child = Individual([None for _ in range(genes_n)])
        FillWithFirstParentGenes(child, parent_1, genes_n // 2)
        FillWithSecondParentGenes(child, parent_2)

        return child

    def mutate(self, individual, rate):
        for _ in range(len(individual.genes)):
            if random() < rate:
                sel_genes = sample(individual.genes, 2)
                individual.swap(sel_genes[0], sel_genes[1])


    def selection(self, population, competitors_n):
        return Population(sample(population.individuals, competitors_n)).getFittest()

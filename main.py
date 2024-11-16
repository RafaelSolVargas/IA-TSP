from Domain.ExecutionParameters import ExecutionParameters
from Domain.TSPHelper import GeneticAlgorithmRunner
from View.Plotter import Plotter
from datetime import datetime
import Utils.utils as utils
import random


def run(parameters: ExecutionParameters):
    genes = utils.readCitiesFile(parameters.FilePath)

    print(f"-- Executando algoritmo genético para {len(genes)} cidades --")

    runner = GeneticAlgorithmRunner(parameters, genes)

    history = runner.run()

    Plotter.plotGeneticResult(history['cost'], history['route'])


if __name__ == "__main__":
    parameters = ExecutionParameters(
        popSize=500,         # Tamanho da população
        tournSize=50,        # Tamanho do torneio
        mutRate=0.02,        # Taxa de mutação
        nGen=20,             # Número de gerações
        filePath='./InputData/cities.csv'  # Caminho para o arquivo de cidades
    )

    # Verificação de consistência entre os parâmetros
    if parameters.TournSize > parameters.PopSize:
        raise ValueError("Tournament size cannot be bigger than population size.")

    random.seed(int(datetime.now().timestamp()))

    run(parameters)

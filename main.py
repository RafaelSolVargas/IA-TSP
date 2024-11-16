from Domain.ExecutionParameters import ExecutionParameters
from Domain.TSPHelper import GeneticAlgorithmRunner
from View.Plotter import Plotter
from datetime import datetime
import Utils.utils as utils
import random

if __name__ == "__main__":
    parameters = ExecutionParameters(
        popSize=500,         # Tamanho da população
        tournSize=50,        # Tamanho do torneio
        mutRate=0.02,        # Taxa de mutação
        nGen=20,             # Gerações necessárias consecutivas e estáveis para parar
        maxGen=80,            # Número máximo de gerações possíveis
        filePath='./InputData/cidades.csv'
    )

    random.seed(int(datetime.now().timestamp()))

    genes = utils.readCitiesFile(parameters.FilePath)

    print(f"-- Executando algoritmo genético para {len(genes)} cidades --")

    runner = GeneticAlgorithmRunner(parameters, genes)

    history = runner.run()

    Plotter.plotGeneticResult(history['cost'], history['route'])

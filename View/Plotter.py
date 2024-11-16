import matplotlib.pyplot as plt # type: ignore
from mpl_toolkits.basemap import Basemap # type: ignore

class Plotter:
    @classmethod
    def plotGeneticResult(cls, costs, individual, save_to=None):
        plt.figure(1)
        plt.subplot(121)
        cls.plotGaConvergence(costs)

        plt.subplot(122)
        cls.plotRoute(individual)

        if save_to is not None:
            plt.savefig(save_to)
            plt.close()
        else:
            plt.show()

    def plotGaConvergence(costs):
        x = range(len(costs))
        plt.title("Convergência")
        plt.xlabel('Geração')
        plt.ylabel('Custo (KM)')
        plt.text(x[len(x) // 2], costs[0], 'Custo mínimo: {} KM'.format(costs[-1]), ha='center', va='center')
        plt.plot(x, costs, '-')


    def plotRoute(individual):
        m = Basemap(projection='lcc', resolution=None,
                    width=5E6, height=5E6,
                    lat_0=-15, lon_0=-56)

        plt.axis('off')
        plt.title("Menor caminho encontrado")

        for i in range(0, len(individual.genes)):
            x, y = m(individual.genes[i].lng, individual.genes[i].lat)

            plt.plot(x, y, 'ob', markersize=5)
            if i == len(individual.genes) - 1:
                x2, y2 = m(individual.genes[0].lng, individual.genes[0].lat)
            else:
                x2, y2 = m(individual.genes[i+1].lng, individual.genes[i+1].lat)

            plt.plot([x, x2], [y, y2], '-', color='blue')  # Define a linha vermelha

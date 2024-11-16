import matplotlib.pyplot as plt  # type: ignore
from mpl_toolkits.basemap import Basemap  # type: ignore


class Plotter:
    @classmethod
    def plotGeneticResult(cls, costs, individual, save_to=None):
        plt.figure(figsize=(10, 8))

        # Plot da convergência (Gráfico superior)
        plt.subplot(211)
        cls.plotGaConvergence(costs)

        # Plot do menor caminho encontrado (Gráfico inferior)
        plt.subplot(212)
        cls.plotRoute(individual)

        if save_to is not None:
            plt.savefig(save_to)
            plt.close()
        else:
            plt.tight_layout()
            plt.show()

    def plotGaConvergence(costs):
        x = range(len(costs))
        plt.title("Evolução do Custo ao Longo das Gerações", fontsize=12)
        plt.xlabel('Geração', fontsize=10)
        plt.ylabel('Custo (KM)', fontsize=10)
        plt.grid(alpha=0.5)
        plt.text(x[len(x) // 2], costs[0], 'Custo mínimo: {} KM'.format(costs[-1]),
                 ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.7))
        plt.plot(x, costs, '-o', color='purple', markersize=4, linewidth=1.5)

    def plotRoute(individual):
        m = Basemap(projection='lcc', resolution=None,
                    width=5E6, height=5E6,
                    lat_0=-15, lon_0=-56)

        plt.axis('off')
        plt.title("Rota Otimizada Encontrada", fontsize=12)

        for i in range(0, len(individual.genes)):
            x, y = m(individual.genes[i].lng, individual.genes[i].lat)

            # Ponto como estrela verde
            plt.plot(x, y, marker='*', color='green', markersize=6, label='Cidade' if i == 0 else "")

            if i == len(individual.genes) - 1:
                x2, y2 = m(individual.genes[0].lng, individual.genes[0].lat)
            else:
                x2, y2 = m(individual.genes[i+1].lng, individual.genes[i+1].lat)

            # Linhas conectando as cidades em cinza claro
            plt.plot([x, x2], [y, y2], '-', color='green', alpha=0.7, linewidth=1.5)

        # Legenda opcional
        plt.legend(loc='upper right', fontsize=8)

import pandas as pd
import math
import numpy as np
import pygad
from datetime import datetime
import matplotlib.pyplot as plt

# obtém os dados da cidade
# TSP = pd.read_csv('tsp1.csv', index_col=0, header=0)
TSP = pd.read_csv('tsp3.csv', index_col=0, header=0)

# obtém o número máximo de cidades
MAX_CIDADES = len(TSP.index)

# distância entre duas cidades
def distancia_euclidiana(A, B):
    A = np.array(A)
    B = np.array(B)
    
    return np.sqrt(np.sum((A - B) ** 2))

# gera uma solução aleatória
def solucao():
    lista_solucao = np.arange(1, MAX_CIDADES + 1)
    np.random.shuffle(lista_solucao)
    return lista_solucao.tolist()

# função de aptidão
# '-1' é usado para mudar o índice da cidade de base 1 para o array de base 0
def distancia_viagem(ga_instance, solucao, solution_idx):
    solucao = np.array(solucao, dtype=np.int64)
    indices = solucao - 1
    distancias = LOOKUP[indices[:-1], indices[1:]]
    distancia = np.sum(distancias)
    distancia += LOOKUP[indices[-1], indices[0]]
    return 1 / distancia

# chamado após cada geração
# retornar a string "parar" irá terminar o algoritmo genético
def ao_gerar(g):
    # comentar para múltiplas execuções para reduzir a quantidade de informações de saída
    print(datetime.now(), "Geração:", g.generations_completed, "\tÚltima Solução:", round(1/g.last_generation_fitness[0], 4))

    # determina se deve ou não parar (sem melhoria após x iterações)
    x = 500
    if parar_geracao(g, x):
        return "parar"

# determina se deve parar uma geração após x iterações sem melhoria
def parar_geracao(g, x):
    if g.generations_completed > x:
        indice_maximo = g.generations_completed - 1
        aptidao_atual = g.best_solutions_fitness[indice_maximo]
        aptidao_x_atras = g.best_solutions_fitness[indice_maximo - x]
        if np.isclose(aptidao_atual, aptidao_x_atras, atol=0.00003):
            return True
    return False

# imprime a solução
def imprimir_solucao(g):
    distancia = distancia_viagem(g, 1, 1)
    print("Aptidão = {} Distância = {}".format(distancia, 1/distancia))

# calcula a distância entre cada cidade
# cria um array 2d para o número de cidades
# precisa usar -1 para converter entre o intervalo indexado em 0 e o sistema de numeração de cidades indexado em 1
def todas_distancias():
    coords = TSP.values
    num_cidades = len(coords)
    distancias = np.zeros((num_cidades, num_cidades))
    for i in range(num_cidades):
        for j in range(num_cidades):
            distancias[i, j] = distancia_euclidiana(coords[i], coords[j])
    return distancias

# imprime a melhor rota em um gráfico
# modificado de https://www.kite.com/python/answers/how-to-make-a-connected-scatter-plot-in-matplotlib-in-python
def imprimir_rota(s):
    coordenadas_x = []
    coordenadas_y = []
    nomes = []
    for i in range(MAX_CIDADES + 1):  # +1 porque adicionamos a primeira cidade ao final antes de chamar
        cidade = TSP.iloc[int(s[i]) - 1]
        coordenadas_x.append(cidade.iloc[0])
        coordenadas_y.append(cidade.iloc[1])
        if 'name' in TSP.columns:
            nomes.append(cidade['name'])

    plt.scatter(coordenadas_x, coordenadas_y)
    plt.plot(coordenadas_x, coordenadas_y)

    if nomes:
        for i, nome in enumerate(nomes):
            plt.annotate(nome, (coordenadas_x[i], coordenadas_y[i]))

    plt.xlabel("distância x")
    plt.ylabel("distância y")
    plt.title("Rota da Melhor Solução")
    plt.show()

# array 2D com todas as distâncias entre cidades
LOOKUP = todas_distancias()

def algoritmo_genetico():
   # atribui a função de aptidão
   funcao_aptidao = distancia_viagem

   # quantas gerações iterar
   # defina este valor alto e deixe a função parar_geracao determinar se deve terminar
   # certifique-se de definir o número de iterações em parar_geracao suficientemente alto para seu conjunto de dados
   num_geracoes = len(TSP) * 1000

   # tamanho da população
   solucoes_por_populacao = 2000

   # espaço de solução
   num_genes = MAX_CIDADES

   # intervalo de solução
   espaco_gene = range(1, MAX_CIDADES + 1)

   # acasalar com os melhores x% da população
   # 25% tem sido uma boa média
   percentual_acasalamento = 25
   num_pais_acasalando = math.ceil(solucoes_por_populacao * percentual_acasalamento / 100)
   
   # manter os melhores x% da população para a próxima geração
   # 1% funciona bem para populações maiores (>1000), caso contrário, 5% é bom
   percentual_manutencao = 1
   manter_pais = math.ceil(solucoes_por_populacao * percentual_manutencao / 100)

   # escolher como selecionar os pais
   tipo_selecao_pais = "sss"
   # tipo_selecao_pais = "rank"

   # o cruzamento dos dados de ponto único e dois pontos era indistinguível
   # mas dois pontos era mais intensivo em recursos
   # tipo_cruzamento = "single_point"
   tipo_cruzamento = "two_points"

   # como implementar a mutação
   tipo_mutacao = "adaptive"

   # irá gerar um aviso se percentual * MAX_CIDADES < 1 (ou seja, em tsp1.csv)
   # [20, 5] produziu os melhores resultados
   percentual_mutacao_genes = [20, 5]
   
   # inicializa os parâmetros do algoritmo genético
   ga_instance = pygad.GA(num_generations=num_geracoes,
                        num_parents_mating=num_pais_acasalando,
                        fitness_func=funcao_aptidao,
                        sol_per_pop=solucoes_por_populacao,
                        num_genes=num_genes,
                        parent_selection_type=tipo_selecao_pais,
                        keep_parents=manter_pais,
                        crossover_type=tipo_cruzamento,
                        mutation_type=tipo_mutacao,
                        mutation_percent_genes=percentual_mutacao_genes,
                        gene_space=espaco_gene,
                        on_generation=ao_gerar,
                        allow_duplicate_genes=False)

   # executa uma instância do algoritmo genético
   ga_instance.run()

   # plota a aptidão ao longo do tempo
   ga_instance.plot_fitness()

   # salva o melhor resultado
   s, fit, s_i = ga_instance.best_solution()

   # modifica o array do melhor resultado para impressão (precisa adicionar a última cidade = primeira cidade para ser exibido corretamente)
   s_print = s
   s_print = np.append(s_print, s_print[0])

   # imprime um mapa da rota da melhor solução
   imprimir_rota(s_print)

   # imprime a melhor rota
   print("Melhor Rota:\n",s_print,"\n")

   # retorna a melhor solução
   return s

if __name__ == '__main__':
    algoritmo_genetico()
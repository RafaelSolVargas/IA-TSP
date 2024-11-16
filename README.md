Para executar esse código baixe as dependências necessárias via:


``` python
pip install -r requirements.txt
```

E depois, estando no root do projeto, execute:

``` python
python main.py
```

Para trocar os parâmetros utilizados no código, modifique-os manualmente no arquivo main.py na linha:
```
    parameters = ExecutionParameters(
        popSize=500,         # Tamanho da população
        tournSize=50,        # Tamanho do torneio
        mutRate=0.02,        # Taxa de mutação
        nGen=20,             # Gerações para estabilizar
        filePath='./InputData/cidades.csv'
    )
```
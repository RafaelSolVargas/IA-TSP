class ExecutionParameters:
    def __init__(self, popSize: int, tournSize: int, mutRate: float, nGen: int, maxGen: int, filePath: str):
        self.PopSize = popSize
        self.TournSize = tournSize
        self.MutRate = mutRate
        self.NGen = nGen
        self.FilePath = filePath
        self.MaxGen = maxGen
import pandas as pd # type: ignore
from Domain.Gene import Gene
from random import sample


def readCitiesFile(fn, sample_n=0):
    df = pd.read_csv(fn)
    genes = [Gene(row['city'], row['latitude'], row['longitude'])
             for _, row in df.iterrows()]

    return genes if sample_n <= 0 else sample(genes, sample_n)

# Python 2.7
from savReaderWriter import SavReader
import pandas as pd
with SavReader('file.sav') as reader:
    chunk = 20000
    N = reader.shape.nrows
    lista = range(0,N+chunk, chunk)
    rangos = [lista[i-1:i+1] for i in range(1,len(lista))]
    pisa = pd.DataFrame([], columns=reader.header)
    pisa.to_csv('filename.csv', index=False)
    for r in rangos:
        records = []
        for line in reader[r[0]:r[1]]:
            records.append(line)
        pisa = pd.DataFrame(records)
        pisa.to_csv('filename.csv', index=False, mode='a', header=False)

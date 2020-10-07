import os
from simpledbf import Dbf5

def dbf_to_csv(inputfile, outputfile='output.csv', replace=False):
    existe = os.path.exists(outputfile)
    if (existe and replace) or (not existe):
        Dbf5(inputfile, codec='latin-1').to_dataframe().to_csv(outputfile, sep=',', index=False)
        print('Archivo', inputfile, 'exitosamente convertido a', outputfile)        
    else:
        print(f'El archivo {outputfile} ya existe. Para reemplazarlo use la opción replace=True')

dbf_to_csv(f'archivo.dbf', 'archivo_convertido.csv')
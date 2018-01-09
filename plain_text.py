def plain(x):
    '''Esta función convierte en minúscula los caracteres de una cadena de texto y remueve acentos de las vocales. 
    El input es una cadena de texto'''
    return x.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó',u'o').replace('ú',u'u').replace('ñ',u'n').replace('\t','').replace('\n','')

def html_to_text(url):
    """Esta función extrae el texto principal de una página web html"""
    if url[-4:] not in ['.pdf','.mp4']:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
        test = BS(requests.get(url, headers=headers).content, 'lxml')                    
        tags_excl = ['select','script','style','a','ul','ol','span','form','footer','div[class="gg728"]','div[class="post-comments"]']
        for tag in tags_excl:
            while test.select(tag):
                test.select_one(tag).extract()
        output = '\n'.join([x for x in test.body.get_text().splitlines() if x.replace(' ','')!=''])
    else:
        output = ''
    return output
def html_to_text2(url_test):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    test = BS(requests.get(url_test, headers=headers).content, 'lxml').body
    # tags que se deben excluir
    tags_drop = ['select','script','style','a','ul','ol','li','form','footer','div[class="gg728"]','div[class="post-comments"]']
    # tags que no se deben excluir: solo se mantendrán los elementos atributos-valores listados, se borrarán otros elementos con el mismo tag pero diferentes atributos-valores
    tags_keep = ['span[itemprop="articleBody"]','span[style="font-weight: 400;"]']
    tags_all = [];atts_all = [];vals_all = []
    # Enlista todos los tags, atributos y valores de tags_keep
    for tag_att_val in tags_keep: 
        tags_all = [re.findall(r'\w+(?=\[)',tag_att_val)[0]]
        att_val = re.findall(r'(?<=\[).*(?=\])',tag_att_val)[0].split('=') # lista, pos0=atributo, pos1:valor_atrib
        atts_all += [att_val[0]]; vals_all += [att_val[1].replace('"','')]
    # Extrae todos los de la lista de exclusión
    for tag in tags_drop: 
        while test.select(tag):
            test.select_one(tag).extract()
    #Mantenemos algunos tags
    if test.find_all(tags_all):# verificamos que la página tenga alguno de los tags en keep
        for tag_att_val in tags_keep: # iteramos sobre los elementos en keep
            tag = re.findall(r'\w+(?=\[)',tag_att_val)[0]
            att_val = re.findall(r'(?<=\[).*(?=\])',tag_att_val)[0].split('=') # lista, pos0=atributo, pos1:valor_atrib
            att = att_val[0]; val = att_val[1].replace('"','')
            if sum([len(test.select(x)) for x in tags_all]): # si tiene alguno de los atributos-valores, procede a mantener algunos
                for I in test.find_all(tag): # iteramos sobre los tags
                    if not set(atts_all).intersection(set(I.attrs.keys())): # si no tiene el atributo, extráelo
                        I.extract()
                    else: # si tiene el atributo, verifica si es el valor
                        if not set(vals_all).intersection({z for z in I.attrs.values() if type(z)==str}): # si el valor no es el indicado, extrae
                            I.extract()
            else: # si la página no tiene alguno de los atributos-valores, procede a eliminar todos los que tienen el tag
                for I in test.find_all(tag): # iteramos sobre los tags
                    I.extract()
    # Eliminimos todos los hipervínculos <a>, excepto si están dentro de un parrafo <p>
    for A in test.find_all('a'):
        if not A.parent.name=='p':
            A.extract()
    output = '\n'.join([x.strip() for x in test.get_text().splitlines() if x.replace(' ','')!=''])
    return output

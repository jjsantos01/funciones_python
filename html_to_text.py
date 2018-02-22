ddef html_to_text(url_test):
    if url_test[-4:] not in ['.pdf','.mp4']:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
        test = BS(requests.get(url_test, headers=headers).content, 'lxml').body
        # tags que se deben excluir
        tags_drop = ['select','button','script','noscript','style','a','ul','ol','li','form','nav','footer','header','aside','div[class*="sidebar"]','div[class*="footer"]','div[class*="comments"]',
            'div[id*="footer"]','div[id*="relacionadas"]','div[class*="relacionadas"]','div[class*="related"]','div[id*="comentarios"]','div[class="header"]','div[id="sidebar"]',
            'div[id="dslc-module-61c2a8ea276"]','div[id="dslc-module-b4f99a563f3"]','div[class="row notas-destacados-int"]','div[class="row notas-local-int"]',
             'div[class="modal fade base_modal"]','div[id="zonaactiva"]','div[id="clasificados"]','div[id="npie"]','div[class="gg728"]',
            'div[class="teaser "]','div[id="pie"]','div[class="author-box"]','div[class="relevantes"]','section[id="sp-top"]','div[class="custom yoexpreso-whatsapp"]',
            'div[class="view-header"]', 'h2[class="element-invisible"]','h2[class="pane-title"]','div[class="pum-content popmake-content"]',
            'section[class="header-en-portada"]','article[class="hidden-xs hidden-sm col-md-4 col-lg-4 text-center"]',
            'div[id="comScoreData"]','div[class="visible-xs-block box-destacadas-mobile hide-box"]','div[id="ultimaHora"]',
            'div[class="visible-xs-block box-compartidas-mobile hide-box"]','div[id="Login"]','div[id="box_tools2"]','div[id="head"]',
            'section[id="sp-seccion-3-articulos"]','section[id="sp-pre-footer"]','div[id="dynamic_box_right"]','a','span']
        # tags que no se deben excluir: solo se mantendrán los elementos atributos-valores listados, se borrarán otros elementos con el mismo tag pero diferentes atributos-valores
        tags_keep = ['span[itemprop="articleBody"]','span[style="font-weight: 400;"]','span[style="font-size: medium;"]',
        'div[class="l-page has-one-sidebar has-sidebar-second"]','div[class="vw-page-wrapper clearfix vw-sidebar-position-right"]',
        'div[class="container layout-2-col layout-right-sidebar post-template-10"]','div[class="eltdf-two-columns-75-25 eltdf-content-has-sidebar clearfix"]',
        'div[class="eltdf-column1 eltdf-content-left-from-sidebar"]','span[style="font-family: arial, helvetica, sans-serif; font-size: large;"]',
        'div[class="sidebar_content"]','header[class="has-second-menu"]']
        tags_all = [];atts_all = [];vals_all = []
        # Enlista todos los tags, atributos y valores de tags_keep
        for tag_att_val in tags_keep: 
            tags_all += [re.findall(r'\w+(?=\[)',tag_att_val)[0]]
            att_val = re.findall(r'(?<=\[).*(?=\])',tag_att_val)[0].split('=') # lista, pos0=atributo, pos1:valor_atrib
            atts_all += [att_val[0]]; vals_all += [att_val[1].replace('"','')]
        # lista drop todos los de la lista de exclusión
        lista_drop = [ele for tag in tags_drop for ele in test.select(tag)]   
        # mantenemos todos los tags <a> y <span> si están dentro de un parrafo <p>
        for ele in lista_drop:
            if ((ele.name=='a') or (ele.name=='span')) & ((ele.parent.name=='p')):
                lista_drop.remove(ele)
        # lista de los elementos que no se van a eliminar
        set_vals_all = set(vals_all)
        lista_keep = []
        for x in lista_drop:
            if (x.name in tags_all) & bool(set(x.attrs.keys()).intersection(set(atts_all))):
                set_val = {' '.join(z) if isinstance(z,list) else z for z in x.attrs.values()}
                if bool(set_vals_all.intersection(set_val)):
                    lista_keep += [x]
         ### Casos especiales:
        if 'jornadaveracruz' in url_test:
            for x in lista_drop:
                if x.name=='form':
                    if x['id']=='form1':
                        lista_keep+=[x]
                    
        # Mantenemos los ques están en la lista_keep
        for ele in lista_keep:
            lista_drop.remove(ele)
        #eliminamos los que quedan en la lista drop
        for ele in lista_drop:
            ele.extract()
            output = '\n'.join([x.strip() for x in test.get_text().splitlines() if x.replace(' ','')!=''])
    else:
        output = ''
    return output
def html_to_text2(url):
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

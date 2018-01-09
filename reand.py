def reand(reg):
  import re
  '''Esta función genera el operador & en una expresión regular.
  El input de la función son las palabras o re que quieren ser encontradas en conjunto, separadas por el símbolo &.
  También pueden estar separadas por |'''
  out = ''
  for x in reg.replace(' ','').split('&'):
    inte = '|'.join(['.*'+y for y in x.split('|')])
    out += '(?={})'.format(inte)
  return out

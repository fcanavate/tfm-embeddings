import rdflib
import openpyxl
g=rdflib.Graph()
#g.load('http://dbpedia.org/resource/Semantic_Web')
#g.parse("prueba.ttl", format="ttl")
g.parse("long_abstracts_es.ttl", format="ttl")
libro=openpyxl.load_workbook(file="wikipedia.xlsx")
hoja=libro.worksheets(Hoja1)
n=0
for s,p,o in g:
    n+=1
    hoja.append([s,p,o])
    print (s,p,o)
    if n%1000==0:
        libro.save("wikipedia.xlsx")
libro.save("wikipedia.xlsx")        
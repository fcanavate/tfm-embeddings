

# =============================================================================
# obtiene fichero que hay que convertir a  separado por tabuladores y renonbrar con extension tsv 
# =============================================================================



#!pip install google.colab
#!pip install openpyxl
#!pip install os
#!pip install rdflib
#!pip install listdir
#!pip install scandir
#!pip install xlrd
#!pip install urllib
#!pip install scipy
#!pip install pandas
import rdflib
import openpyxl
from os import listdir
from os import scandir
import xlrd
#from google.colab import drive
from openpyxl import load_workbook
from openpyxl import Workbook
from urllib import request
import numpy as np
from scipy import sparse
from scipy.sparse import coo_matrix
from scipy import stats
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
#from sparsesvd import sparsesvd
from scipy.sparse.linalg import svds
#https://pypi.org/project/sparsesvd/
#drive.mount('/content/gdrive')
#root_dir = "/content/gdrive/My Drive/"
#def ls2(path): 
#    return [obj.name for obj in scandir(path) if obj.is_file()]


base_verb_pd=pd.read_excel("base_verb_fusion.xlsx",names=['index_verb','verbostd','verbo'])
base_noun_pd=pd.read_excel("base_noun_fusion.xlsx",names=['index_noun','nombrestd','nombre'])
coord_nounsuj_verb_pd=pd.read_excel("coord_nounsuj_verb_fusion.xlsx",names=['noun_suj_index','verbindex','coordenada'])
coord_nounsuj_verb_pd.index = np.arange(1, len(coord_nounsuj_verb_pd)+1)
#construimos matriz COO a partir de coord_nounsuj_verb_pd
coord_nounsuj_verb_matrix=coo_matrix((coord_nounsuj_verb_pd.loc[:,'coordenada'],(coord_nounsuj_verb_pd.loc[:,'noun_suj_index'],coord_nounsuj_verb_pd.loc[:,'verbindex'])),dtype=int)                                     
coord_nounsuj_verb_matrix.sum_duplicates() 


                            
def indexnombre(nombre):
    filanombre=base_noun_pd[(base_noun_pd['nombrestd']==nombre)]
    indexn=filanombre.iloc[0][0]
    return(indexn)    
def indexverbo(verbo):
    filaverbo=base_verb_pd[(base_verb_pd['verbostd']==verbo)]
    indexv=filaverbo.iloc[0][0]
    return(indexv)
    
def nombre(indicenombre):
    filanombre=base_noun_pd[(base_noun_pd['index_noun']==indicenombre)]
    nombre=filanombre.iloc[0][1]
    return(nombre)    
        
#obtenemso el vector correspondiente a un nombre dado
def vector_noun_suj(nombre):
    index_noun=indexnombre(nombre)+1
    vectornombre=coord_nounsuj_verb_matrix.getrow(index_noun)
    vector_noun_dense=vectornombre.todense()
    return(vector_noun_dense)

def vector_noun_suj_index(index):
    index_noun=index
    vectornombre=coord_nounsuj_verb_matrix.getrow(index_noun)
    vector_noun_dense=vectornombre.todense()
    return(vector_noun_dense)

def noceros(indexnombre3):
    vectornombre=vector_noun_suj_index(indexnombre3)
    noceros=np.count_nonzero(vectornombre)
    return (noceros)
def distanciasuj(nombre1,nombre2):
    vector1=np.squeeze(np.asarray((vector_noun_suj(nombre1))))
    modulovector1=np.linalg.norm(vector1)
    if modulovector1==0:
        modulovector1=1
    vector1n=vector1/modulovector1
    vector2=np.squeeze(np.asarray((vector_noun_suj(nombre2))))
    modulovector2=np.linalg.norm(vector2)
    if modulovector2==0:
        modulovector2=1
    vector2n=vector2/modulovector2
    angulo=np.dot(vector1n,vector2n)
    diferencia=vector1n-vector2n
    distancia=np.linalg.norm(diferencia)
    return([distancia,angulo])

def distanciasuj_index(indexnombre1,indexnombre2):
    vector1=np.squeeze(np.asarray((vector_noun_suj_index(indexnombre1))))
    modulovector1=np.linalg.norm(vector1)
    if modulovector1==0:
        modulovector1=1
    vector1n=vector1/modulovector1
    vector2=np.squeeze(np.asarray((vector_noun_suj_index(indexnombre2))))
    modulovector2=np.linalg.norm(vector2)
    if modulovector2==0:
        modulovector2=1
    vector2n=vector2/modulovector2
    angulo=np.dot(vector1n,vector2n)
    diferencia=vector1n-vector2n
    distancia=np.linalg.norm(diferencia)
    return([distancia,angulo])
def distancias(nombre1,nombre2):
    distanciasuj1=distanciasuj(nombre1,nombre2)
    print ("suj:",distanciasuj1[0])


## buscar grupos de 100 elementos mas cercanos a un nombre dado
#buscamos indice el nombre

matriznombres=[]
for indexnombre in range (1,10000):
    noceros1=noceros(indexnombre)
    matriznombres.append([indexnombre,nombre(indexnombre),noceros1])
matriznombres_pd=pd.DataFrame(matriznombres,columns=['index','nombres','noceros'])
nombresnozeros = matriznombres_pd.sort_values('noceros',ascending=False)
vectores=pd.DataFrame ()
nombres_vectores=[]
# elegimos las primeras 100 palabras dendro de la lista de nozeros que estará formada por elementos con el mayor número de coordnadas respecto a la bse no ceros
for nom1 in range (1,4000):
    indice_nombre=(nombresnozeros.iloc[nom1]['index'])
    #nombres_vectores.append([indice_nombre,nombre(indice_nombre),nom1])
    nombres_vectores.append([nom1,nombre(indice_nombre)])
    vector1=pd.DataFrame(vector_noun_suj_index(nombresnozeros.iloc[nom1]['index']))
    #vector2= (df - df.mean()) / (df.max() - df.min())
    vector2=np.squeeze(np.asarray(vector1))
    modulovector2=np.linalg.norm(vector2)
    if modulovector2==0:
        modulovector2=1
    vector2n=vector2/modulovector2
    vector2=pd.DataFrame(vector2n)
    print (nom1)
    vectores=pd.concat([vectores, vector2.transpose()], axis=0)
nombres_vectores_pd=pd.DataFrame(nombres_vectores,columns=['count','word'])
#print (vectores)
print (nombres_vectores)
vectores.to_csv("vectores_completo_4000.csv")
nombres_vectores_pd.to_csv("nombres_vectores_4000.csv",encoding="utf_8_sig")
#seleccion de columnas
vector_columna_nozeros=(vectores != 0).any(axis=0)
print (vector_columna_nozeros)
#bas-verb_pd=base_verb_500=base_verb_pd[pd.concat([pd.DataFrame([True]), vector_columna_nozeros.transpose()], axis=0)]
base_verb_pd=base_verb_pd.drop(len(base_verb_pd)-1,axis=0)
#print(base_verb_pd)
base_verb_500=base_verb_pd[vector_columna_nozeros]
base_verb_500.to_csv("base_verb_4000.csv")
vectores=vectores.loc[:, vector_columna_nozeros]
vectores.to_csv("vectores_4000.csv")
print("fin1")
#clusterizamos con Kmeans
kmeans=KMeans(n_clusters=50)
kmeans.fit(vectores)
labels = kmeans.predict(vectores)
centroids = kmeans.cluster_centers_
nombres_vectores_pd['clases']=labels
nombres_vectores_pd.to_csv("nombres_vectores_4000_labels.csv",encoding="utf_8_sig")
#print(labels)
#print(centroids)



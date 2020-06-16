

# =============================================================================
# busca grupo de 100 palabras mas cercano a un elemento dado las ordenas de menor distanca a mayor
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
import sklearn
#from sparsesvd import sparsesvd
from scipy.sparse.linalg import svds
#https://pypi.org/project/sparsesvd/
#drive.mount('/content/gdrive')
#root_dir = "/content/gdrive/My Drive/"
#def ls2(path): 
#    return [obj.name for obj in scandir(path) if obj.is_file()]


base_verb_pd=pd.read_excel("base_verb_fusion.xlsx",names=['index_verb','verbostd','verbo'])
base_verb_pd.index = np.arange(1, len(base_verb_pd)+1)
base_noun_pd=pd.read_excel("base_noun_fusion.xlsx",names=['index_noun','nombrestd','nombre'])
base_noun_pd.index = np.arange(1, len(base_noun_pd)+1)
coord_nounsuj_verb_pd=pd.read_excel("coord_nounsuj_verb_fusion.xlsx",names=['noun_suj_index','verbindex','coordenada'])
coord_nounsuj_verb_pd.index = np.arange(1, len(coord_nounsuj_verb_pd)+1)
#construimos matriz COO a partir de coord_nounsuj_verb_pd
coord_nounsuj_verb_matrix=coo_matrix((coord_nounsuj_verb_pd.loc[:,'coordenada'],(coord_nounsuj_verb_pd.loc[:,'noun_suj_index'],coord_nounsuj_verb_pd.loc[:,'verbindex'])),dtype=int)                                     
coord_nounsuj_verb_matrix.sum_duplicates() 

#procedemos a aplicar TruncatedSDV para reducir su dimensionalidad
print ("shape1",coord_nounsuj_verb_matrix.shape)
coord_nounsuj_verb_matrix=sklearn.preprocessing.normalize(coord_nounsuj_verb_matrix, norm='l2', axis=1, copy=True, return_norm=False)
coord_nounsuj_verb_matrix_asf=coord_nounsuj_verb_matrix.asfptype()
u,s,v=svds(coord_nounsuj_verb_matrix_asf,5000)
matrizdim1000=u.dot(np.diag(s))
print ("shape2",matrizdim1000.shape)

                            
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
    vectornombre=matrizdim1000[index_noun]
    return(vectornombre)

def vector_noun_suj_index(index):
    index_noun=index
    vectornombre=matrizdim1000[index_noun]
    return(vectornombre)
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
def obtener_nombres_relacionados(index_argumentonombre):
    for j in range (1,5000):
        indexnombre=nombresnozeros.iloc[j][0]
        distancia=distanciasuj_index (index_argumentonombre,indexnombre)
        matrizdistancias.append([nombre(indexnombre),distancia[0],])

## buscar grupos de 100 elementos mas cercanos a un nombre dado
#buscamos indice el nombre

matriznombres=[]
for indexnombre in range (1,10000):
    noceros1=noceros(indexnombre)
    matriznombres.append([indexnombre,nombre(indexnombre),noceros1])
matriznombres_pd=pd.DataFrame(matriznombres,columns=['index','nombres','noceros'])
nombresnozeros = matriznombres_pd.sort_values('noceros',ascending=False)
nombres_global_red=df = pd.DataFrame ()
nombres_global_normal=df = pd.DataFrame ()
for i in range(1,5000):
    index_argumento_nombre=nombresnozeros.iloc[i][0]
    argumento_nombre=nombresnozeros.iloc[i][1]
    print (i,index_argumento_nombre,nombresnozeros.iloc[i][1])
    matrizdistancias=[]
    obtener_nombres_relacionados(index_argumento_nombre)
    matrizdistancias_pd=pd.DataFrame(matrizdistancias,columns=['nombres','distancia'])
    nombres = matrizdistancias_pd.sort_values('distancia')   
    #nombres_global['nombres_'+argumento_nombre]=nombres['nombres_'+argumento_nombre]
    #nombres_global['distancia_'+argumento_nombre]=nombres['distancia_'+argumento_nombre]
    nombres_global_red=pd.concat([nombres_global_red, nombres[0:9]], axis=0)
    nombres_global_normal=pd.concat([nombres_global_normal, nombres[0:99]], axis=0)
    #nombres_global=pd.merge(nombres_global, nombres)
    if i%5==0:
        #nombresnozeros.to_csv("nombrenozeros.csv",encoding='utf_8_sig')
        nombres_global_red.to_csv("nombres_global_fusion_red_dimension1000.csv",encoding="utf_8_sig")
        nombres_global_normal.to_csv("nombres_global_fusion_normal_dimension1000.csv",encoding="utf_8_sig")
#nombresnozeros.to_csv("nombrenozeros.csv",encoding='utf_8_sig')
nombres_global_red.to_csv("nombres_global_fusion_red_dimension1000.csv",encoding="utf_8_sig")
nombres_global_normal.to_csv("nombres_global_fusion_normal_dimension1000.csv",encoding="utf_8_sig")
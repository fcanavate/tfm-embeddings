

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
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

#from sparsesvd import sparsesvd
from scipy.sparse.linalg import svds
#https://pypi.org/project/sparsesvd/
#drive.mount('/content/gdrive')
#root_dir = "/content/gdrive/My Drive/"
#def ls2(path): 
#    return [obj.name for obj in scandir(path) if obj.is_file()]


base_verb_pd=pd.read_excel("base_verb_fusion.xlsx",names=['index_verb','verbostd','verbo'])
base_noun_pd=pd.read_excel("base_noun_fusion.xlsx",names=['index_noun','nombrestd','nombre'])

vectores_completo_pd=pd.read_csv("vectores_completo_500.csv")
nombres_vectores_pd=pd.read_csv("nombres_vectores_500.csv")
vectores_pd=pd.read_csv("vectores_500.csv")
base_verb_pd_reducido=pd.read_csv("base_verb_500.csv")

#clusterizamos con Kmeans
kmeans=KMeans(n_clusters=50)
kmeans.fit(vectores_pd)
labels = kmeans.predict(vectores_pd)
centroids = kmeans.cluster_centers_
nombres_vectores_pd['clases']=labels
nombres_vectores_pd.to_csv("nombres_vectores_500_2_labels.csv",encoding="utf_8_sig")
#print(labels)
#print(centroids)
#Clustering jerárquico
# Creamos el dendograma para encontrar el número óptimo de clusters
label_palabras=nombres_vectores_pd['word']
print (vectores_pd)
R=dendrogram = sch.dendrogram(sch.linkage(vectores_pd, method = 'ward'),p=100,truncate_mode="lastp",orientation='top')
temp = {R["leaves"][ii]: labels[ii] for ii in range(len(R["leaves"]))}
def llf(xx):
    return (label_palabras.iloc[temp[xx]])
dendrogram = sch.dendrogram(sch.linkage(vectores_pd, method = 'ward'),p=100,leaf_label_func=llf,truncate_mode="lastp",orientation='top')
plt.title('Dendrograma')
plt.xlabel('Distancias')
plt.ylabel('Palabras')
plt.show()



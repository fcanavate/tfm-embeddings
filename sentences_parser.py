import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook
import nltk, re, pprint
nltk.download('punkt')
from nltk import word_tokenize	
from nltk.tokenize import sent_tokenize
from urllib import request
import parserV3
nltk.download('averaged_perceptron_tagger')
url = "http://www.gutenberg.org/files/2554/2554-0.txt"
texto = request.urlopen(url)
raw = texto.read()
#print (type(raw))
#print (raw)
#print (len(raw))
raw1=raw.decode('utf-8')
sentences=sent_tokenize(raw1)
#print (sentences[:10])
wb=load_workbook(filename="verbnoun.xlsx")
ws=wb.active
n=0
for sentence in sentences[:10000]:
    sentence1=sentence.strip("\r\n")
    sentence2=sentence1.replace("\r\n"," ")
    sentence3=sentence2.replace("  "," ")
        #llamada al parse
    analisis=parserV3.parse(sentence3)
    #print (analisis)
    npalabra=1
    for palabra in analisis:
        if len(palabra)>6:
            if palabra[3]=='VERB':
                verbnoun=["","","","","","","","","","",""]
                verbnoun[0]=palabra[2]
                verbnoun[10]=sentence3
                ordenverbo=palabra[0]
                npalabra1=0
                npalabrasuj=1
                npalabraobj=5
                for palabra1 in analisis:
                    npalabra1=npalabra1+1
                    if len(palabra1)>6:             
                        if palabra1[6]==ordenverbo and palabra1[3]=="NOUN" and palabra1[7]=="nsubj":
                            verbnoun[npalabrasuj]=palabra1[2]
                            npalabrasuj=npalabrasuj+1
                        if palabra1[6]==ordenverbo and palabra1[3]=="NOUN" and palabra1[7]=="obj":
                            verbnoun[npalabraobj]=palabra1[1]
                            npalabraobj=npalabraobj+1
                print (sentence3)
                print (verbnoun)
                if npalabrasuj>1 and npalabraobj>5:
                    ws.append(verbnoun)
                    wb.save("verbnoun.xlsx") 
    

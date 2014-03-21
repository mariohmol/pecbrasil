''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
#from pecbrasil.politica.models import Politico, Partido, TimeCandidato,Time, Rodada, RodadaPontos,Candidatura,Pontuacao

''' Connect to DB '''
#db = MySQLdb.connect(host="localhost", user=environ["DATAMINAS_DB_USER"], 
#
#db = MySQLdb.connect(host="localhost", user="root",    passwd="", db="pecbrasil",charset="utf8",init_command="SET NAMES UTF8")




#db = MySQLdb.connect(host="supremait.com", user="pecbrasil",    passwd="pecbrasil321", db="pecbrasil")

#db.autocommit(1)
#cursor = db.cursor()
def pegaIdLinha(linha):
    resp= linha.split(" ")
    i=0
    for item in resp:
        if item is not None and len(item)>3:
            
            return item


       
def tiraIdLinha(linha,item):
    if item is not None:
        #item=pegaIdLinha(linha)
        if item is not None and len(item)>1 and item[1]=='n':
            linha=linha.replace(item,"").strip()

    final=""
    valores=linha.split(" ")
    for val in valores:
        val=val.strip()
        
        if len(val)==3 and final=="":
            continue
        final=final+ " "+val
    linha=final
    return linha
##############
# UTILS

# ts = '2013-01-12 15:27:43'
# f = '%Y-%m-%d %H:%M:%S'
def formatDate(ts,f=None):
    if ts is None:
        return None
    if f is None:
        f='%d/%m/%Y'
    a = datetime.datetime.strptime(ts, f)
    return a.strftime('%Y-%m-%d %H:%M:%S')


    
def openCSV(filename):  
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.abspath(os.path.join(basedir, '..', filename))
    input_f = codecs.open(file_path, "rU")
    csv_reader = csv.reader(input_f, delimiter=",", quotechar='"')
    csv_reader.next()
    return csv_reader

def writefile(filename,text):  
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.abspath(os.path.join(basedir, '..', filename))  
    f = open(file_path,'w')
    f.write(text)
  

def runCoding():         
    csv_reader = utils.openCSV('data/Coding.csv')
    i=0
    depara=[]
    for line in csv_reader:
        i=i+1
        if line[1] and i>2:      
            #Unicode   
            # "Windows1252"   
            # Expected  
            Coding_DE= line[3]  
            #Actual
            Coding_PARA= line[2]  
            addCoding(Coding_DE,Coding_PARA,depara)
              
                        
            #Unicode    
            #"Windows1252"    
            #Expected 
            Coding_DE= line[9]  
            #Actual
            Coding_PARA= line[8]  
            
            addCoding(Coding_DE,Coding_PARA,depara)

    return depara


def addCoding(de,para,depara):
    if de is None or para is None or de == '':
        return
    print de + "-"+para
    depara.append([de,para])

def applyCoding(entrada,de_para):
    #print entrada
    for valor in de_para:
        #print valor
        
        if valor[0] in entrada:
            #print 'encontrou'+valor[1]+'oi'
            encontrou=1
            entrada=entrada.replace(valor[0] ,valor[1] )
    #print entrada
    return entrada

def runQuery(query):
    print query
    cursor.execute(query)

def hasNumbers(inputString):
    if inputString is not None:
        return any(char.isdigit() for char in inputString)   

import re
import unicodedata as ud
    
def remove_non_ascii_1(text):

    return ''.join(i for i in text if ord(i)<128)
def remove_non_ascii_2(text):
    
    return re.sub(r'[^\x00-\x7F]',' ', text)

parentescos={"Sn": None, "Pn": None, "Bn": None, "Tn": None, "Qn": None , "Hn": None, "On": None}
nomeparentescos={"Sn": None, "Pn": None, "Bn": None, "Tn": None, "Qn": None, "Hn": None, "On": None }

def atualizaParentesco(id,nome=None):
    if id is not None:
        #if parentescos[id[0:2]] is not None:
            #print "possivel aerro atualiza parentesco"
        parentescos[id[0:2]]=id
        nomeparentescos[id[0:2]]=nome


 
def encontraParentesco(anteriorParentescos,id):
    if id is not None:
        ante = anteriorParentescos[id[0:2]]
        return parentescos[ante]

def iniciar(arq):
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.abspath(os.path.join(basedir, '..',arq))
    file = open(file_path, 'r')
    refile=file.read()
    resp= refile.split(".\n")
    anterior=None
    nomeAnterior=None
    idAnterior=None
    paiAnterior=None
    i=0
    pula=0
    paiId=None
    id=None
    
   
    anteriorParentescos={"Bn": None,
                          "Tn": "Bn",
                         "Qn": "Tn" ,
                          "Pn": "Qn",
                          "Sn": "Pn",
                          "Hn": "Sn",
                          "On": "Hn"
                       
                           }
    for item in resp:
        i=i+1
        
        if pula==1:
            pula=0
            continue
        
        if i>1 and len(resp)>i:
            if item[len(item)-1]=='n' and resp[i][0]=='a': 
                item=item+" "+resp[i] 
                pula=1
        else:
            anterior=item
        if item=='Sem filhos':
            continue    
        
        
        #if anterior[len(item)-1]=='n' and resp[i+1][0]=='a':            
            #print 'achou'
        
        anterior=item
        

        #item = item.encode("utf8")
        item= item.replace("\n"," ").strip()
        #item=item.trim()
        item = item.replace("0n",'Qn').replace("8n",'Hn')
        item = item.replace("- ",'').replace("=",'')
        item = item.replace("_",'').replace('"','')
        
        atualizaPais=0
        if item.startswith('Pais de:'):
            item = item.replace("Pais de:",'').strip()
            if id is not None:
                print "Paisde:"+id
                atualizaPais=1
        
        id=pegaIdLinha(item)
        if not hasNumbers(id):
            id=None
            
       
        
        
        item=tiraIdLinha(item,id)
       
        
        
        
        nome = item.split(",")[0]
        if atualizaPais==1:
            atualizaParentesco(idAnterior,nomeAnterior)
            
        atualizaPais=0
        
        
        paiId=encontraParentesco(anteriorParentescos,id)
         
        desc=item.replace(nome,"")
        
        
            
        if id is None and nomeAnterior[0:5]==nome[0:5]:
            id=idAnterior
            paiId=paiAnterior
        
        if id is None:
            for value in nomeparentescos:
                if nomeparentescos[value] is not None and nomeparentescos[value][0:5]==nome[0:5]:
                    id=parentescos[value]
            
        if id is not None:
            print "ID:"+id.strip()
        if nome is not None:
            print "Nome:"+nome.strip()
        if paiId is not None:
            print "Pai:"+paiId.strip()
        print "------------"
        
            
        nomeAnterior=nome
        idAnterior=id
        paiAnterior=paiId
    #print resp

    
    
iniciar( 'data/1esq.txt')
iniciar( 'data/2dir.txt')

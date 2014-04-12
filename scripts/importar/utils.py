''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
#from pecbrasil.politica.models import Politico, Partido, TimeCandidato,Time, Rodada, RodadaPontos,Candidatura,Pontuacao

''' Connect to DB '''
def getConnection(tipo=None):
    if tipo is None:
        passwd="123456"
        db = MySQLdb.connect(host="localhost", user="root",    passwd=passwd, db="sisfocus_pec",charset="utf8",init_command="SET NAMES UTF8")
    elif tipo=='L':
        db = MySQLdb.connect(host="localhost", user="root",    passwd="", db="sisfocus_pec",charset="utf8",init_command="SET NAMES UTF8")
    elif tipo=='D': #dummy
        db = MySQLdb.connect(host="localhost", user="root",    passwd="123456", db="sisfocus_pec",charset="utf8",init_command="SET NAMES UTF8")
 
    else:
        passwd="pec2014"
        db = MySQLdb.connect(host="politicaesporteclube.com", user="sisfocus_pec",    passwd=passwd, db="sisfocus_pec",charset="utf8",init_command="SET NAMES UTF8")
   
    db.autocommit(1)
    return db
    #db = MySQLdb.connect(host="localhost", user=environ["DATAMINAS_DB_USER"], 
    #db = MySQLdb.connect(host="supremait.com", user="pecbrasil",    passwd="pecbrasil321", db="pecbrasil")

def getCursorConnection(tipo=None):
    db = getConnection(tipo)
    cursor = db.cursor()
    return cursor

#cursor=getCursorConnection()    
   

##############
# UTILS

# ts = '2013-01-12 15:27:43'
# f = '%Y-%m-%d %H:%M:%S'
#%d/%m/%Y %H:%M:%S'
def formatDate(ts,f=None,saida=None):
    if ts is None:
        return None
    if f is None:
        f='%d/%m/%Y'
    if saida is None:
        saida='%Y-%m-%d %H:%M:%S'
    if len(ts) < 10:
        f=f[0:8]
    a = datetime.datetime.strptime(ts, f)
    return a.strftime(saida)


    
def openCSV(filename):  
    basedir = os.path.abspath(os.path.dirname(__file__))
    print basedir

    file_path = os.path.abspath(os.path.join(basedir, '../..', filename)) #../..
    print file_path
    input_f = codecs.open(file_path, "rU") #rU
    csv_reader = csv.reader(input_f, delimiter=",", quotechar='"')

    try:
        print "reading"
        csv_reader.next()
    except csv.Error, e:
        print "Error %s - %s" % (filename,e)
    except StopIteration:
        print "Iteration End"
    return csv_reader

def writefile(filename,text):  
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.abspath(os.path.join(basedir, '..', filename))  
    f = open(file_path,'w')
    f.write(text)
 
       
def cleanAll():
    cursor.execute("delete from candidatura" )
    cursor.execute("ALTER TABLE candidatura AUTO_INCREMENT =1" )
    
    cursor.execute("delete from politico" )
    cursor.execute("ALTER TABLE politico AUTO_INCREMENT =1" )
    
    cursor.execute("delete from partido" )
    cursor.execute("ALTER TABLE partido AUTO_INCREMENT =1" )
    
    #cursor.execute("delete FROM `candidatura` WHERE partido NOT IN ( SELECT id FROM partido )" )
    cursor.execute("delete FROM `pontuacao` where candidatura not in (select id from candidatura)" )
    cursor.execute("delete FROM `politico` where candidatura not in (select id from candidatura)" )
    cursor.execute("delete from rodadapontos")
    
 
 
 

def runCoding():         
    csv_reader = openCSV('data/Coding.csv')
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
    #print de + "-"+para
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
    

def processosTest(depara):  
    cursor.execute("SELECT * FROM `despesacandidato`")
    rows = cursor.fetchall()
    for row in rows:
        descOriginal=row[1]
       
        
        desc=applyCoding(descOriginal,depara)
        print desc
        return 


def proposicaoTest(depara):  
    cursor.execute("SELECT `id`,`desc` FROM `proposicao`")
    rows = cursor.fetchall()
    for row in rows:
        descOriginal=row[1]
        id=row[0] 
        
        
        desc=applyCoding(descOriginal,depara)
        
        #print descOriginal
        #print desc
        
        #if desc == descOriginal:
        #    continue
        
        desc=desc.replace("'"," ")
        #cursor.execute("UPDATE `pecbrasil`.`proposicao` SET `desc` = %s where `proposicao`.`id` = "+id,[desc])
        #print "UPDATE `pecbrasil`.`proposicao` SET `desc` = %s where `proposicao`.`id` = "+id,[desc]
        
        #cursor.execute("UPDATE `pecbrasil`.`proposicao` SET `desc` = '"+desc+"' where `proposicao`.`id` = "+id)
        query= "UPDATE `pecbrasil`.`proposicao` SET `desc` = '"+desc+"' where `proposicao`.`id` = "+str(id)
        cursor.execute(query)
        #return
          

def updatePontuacaoPartidosSQL():           
    sql="update partido p set "+ \
    "total_votacao = ( select sum(total_votacao) from candidatura where partido = p.id ),"+\
     "pontuacao_total = ( select sum(pontuacao_total) from candidatura where partido = p.id ),"+\
    "pontuacao_ultima = ( select sum(pontuacao_ultima) from candidatura where partido = p.id ),"+\
    "pontuacao_tendencia = ( select sum(pontuacao_tendencia) from candidatura where partido = p.id ),"+\
    "total_votacao = ( select sum(total_votacao) from candidatura where partido = p.id ),"+\
    "total_presenca = ( select sum(total_presenca) from candidatura where partido = p.id ),"+\
    "total_processo = ( select sum(total_processo) from candidatura where partido = p.id ),"+\
    "total_proposicao = ( select sum(total_proposicao) from candidatura where partido = p.id ),"+\
    "total_despesa = ( select sum(total_despesa) from candidatura where partido = p.id ),"+\
    "politico_total = ( select count(1) from candidatura where partido = p.id )"
    cursor.execute(sql)
      
    sql="update proposicao p set p.favor = (select count(1) from votacaocandidato where voto=1 and p.id=proposicao)," + \
    "p.contra = (select count(1) from votacaocandidato where voto=3 and p.id=proposicao)," + \
    "p.abstencao = (select count(1) from votacaocandidato where voto=2 and p.id=proposicao)"
    cursor.execute(sql)


def trataPontoString(pontos):
    result=trataPonto(pontos)
    if result is None:
        return 0
    return result

def trataPonto(pontos):
    if pontos=='' or pontos is None:
        return None
    pontos=str(pontos)
    pontos = pontos.replace(",",".")
    resultado=round(float(pontos),2) 
    return  resultado 


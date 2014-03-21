''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
import utils

#cursor = utils.getCursorConnection(ambiente)

##################
#    PARTIDO
###########
def addPartido(nome,sigla=None,codigo=None,cursor=None):    
    row = getPartido(nome)  
    if row is None:
        row = getPartidoByCodigo(codigo,cursor=cursor)
    if row is None:
        cursor.execute("insert into partido (name_en,name_pt,sigla,codigo,id) values (%s,%s,%s,%s,%s)",[nome,nome, sigla,codigo,codigo])
        print "Inserido partido "            
    else:
        cursor.execute("update partido set name_pt = '"+nome+"',name_en = '"+nome+"' where codigo = %s",[codigo] )
        print "update partido set name_pt = '"+nome+"',name_en = '"+nome+"' where codigo = "+str(codigo) + ";"
    return getPartido(nome,cursor=cursor)

def getPartido(nome,cursor=None):   
    cursor.execute("select id from partido where name_en = %s or sigla=%s",[nome,nome] )
    rows = cursor.fetchall()
    for row in rows:
        return row    
    return None

def getPartidoByCodigo(codigo,cursor=None):   
    cursor.execute("select id from partido where codigo = %s",[codigo] )
    rows = cursor.fetchall()
    for row in rows:
        return row    
    return None

def runPartido(cursor=None):         
    csv_reader = utils.openCSV('data/ExpPartido.csv')
    for line in csv_reader:
        if line[1]:     
            ExpPartido_Codigo= line[0]  
            ExpPartido_Sigla= line[1]  
            ExpPartido_Nome= line[2]  
            
            addPartido(codigo=ExpPartido_Codigo,sigla=ExpPartido_Sigla,nome=ExpPartido_Nome,cursor=cursor)
            
def runPartidoCores(cursor=None):         
    csv_reader = utils.openCSV('data/Cores.csv')
    for line in csv_reader:
        if line[1]:     
            ExpPartido_Codigo= line[0]  
            ExpPartido_Sigla= line[1]  
            ExpPartido_Nome= line[2]  
            ExpPartido_Cor= line[3] 
            cursor.execute("update partido set color=%s where id=%s"
                       ,[ExpPartido_Cor,ExpPartido_Codigo])
    



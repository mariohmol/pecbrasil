''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
import utils
import partido

#cursor = utils.getCursorConnection()

##################
#    POLITICO E CANDIDATOS
###########

def addPolitico(nome,nascimento=None,desc_pt=None,partido=None,id_original=None,cursor=None):    
    row = getPolitico(nome,id_original,cursor=cursor)    
    nascimento = utils.formatDate(nascimento)
    if row is None:
        cursor.execute("insert into politico (nome,nascimento,desc_pt,partido,id_original) values (%s,%s,%s,%s,%s)",[nome,nascimento,desc_pt,partido,id_original])
        print "Inserido politico "           
    else:
        cursor.execute("update politico set id_original = "+id_original+",desc_pt='"+desc_pt+"',nome='"+nome+"' , nascimento='"+nascimento+"' where id = "+str(row[0])+ ";")
        print "Atualizado politico"
        #nascimento=STR_TO_DATE('"+nascimento+"', '%d/%m/%Y')
    return getPolitico(nome,id_original,cursor=cursor) 

def getPolitico(nome=None,id_original=None,cursor=None):   
    if nome is None:
        cursor.execute("select id from politico where id_original = %s",[id_original] )
        #print "select id from politico where id_original = %s",[id_original]
        rows = cursor.fetchall()
        for row in rows:
            return row  
    
    
    cursor.execute("select id from politico where nome = %s",[nome] )
    #print "select id from politico where nome = %s",[nome]
    rows = cursor.fetchall()
    for row in rows:
        return row  
    
    return None


def addCandidatura(titulo,nome,partidoNome=None,uf=None,cidade=None,cargo=None,situacao=None,nascimento=None,id_original=None,cursor=None):  
    rowPartido = partido.getPartido(partidoNome,cursor=cursor)
    if rowPartido is None:
        #print "Partido "+partido+ " nao encontrado"
        #return
        rowPartido = partido.addPartido(nome=partidoNome,sigla=partidoNome,codigo=1,cursor=cursor)  
    
    rowPolitico = getPolitico(nome,id_original,cursor=cursor)  
    if rowPolitico is None:
        #print "Politico "+nome+ " nao encontrado"
        return
        #addPolitico(nome,nascimento,None,None,ExpPolitico_ID)
   
    row = getCandidatura(nome,politico=rowPolitico[0],cursor=cursor)   
    if row is None and rowPolitico is not None:
        cursor.execute("insert into candidatura (name_en,name_pt, uf,cidade,cargo,situacao,politico,partido,id_original) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                       ,[titulo,nome,uf,cidade,cargo,situacao,rowPolitico[0],rowPartido[0],id_original])
        print "Inserido Candidatura"            
    else:
        cursor.execute("update candidatura set name_en=%s,name_pt=%s, uf=%s,cidade=%s,cargo=%s,situacao=%s,partido=%s where politico=%s"
                       ,[titulo,nome,uf,cidade,cargo,situacao,rowPartido[0],rowPolitico[0]])
        print "update candidatura set name_en='"+titulo+"',name_pt='"+nome+"', uf='"+uf+"',cidade='"+cidade \
            +"',cargo='"+cargo+"',situacao='"+situacao+"',partido='"+str(rowPartido[0])+"' where politico="+str(rowPartido[0])+";"
        #print "Atualizado Candidatura"
    return getCandidatura(nome,cursor=cursor)

def getCandidatura(nome=None,politico=None,id_original=None,cursor=None):
    
    if nome is not None:   
        cursor.execute("select id from candidatura where name_pt = %s or name_en = %s",[nome,nome] )
        rows = cursor.fetchall()
        for row in rows:
            return row 
    if id_original is not None:
        cursor.execute("select id from candidatura where  id_original = %s",[id_original] )
        rows = cursor.fetchall()
        for row in rows:
            return row
        
    if nome is not None and politico is not None and isinstance(nome,int) and isinstance(politico,int):       
        cursor.execute("select id from candidatura where  id_original = %s or id_original = %s",[politico,nome] )
        rows = cursor.fetchall()
        for row in rows:
            return row   
    
    cursor.execute("select id from candidatura where politico = %s",[politico] )
    rows = cursor.fetchall()
    for row in rows:
        return row   
    return None    
    
def runPolitico(cursor=None):         
    csv_reader = utils.openCSV('data/ExpPolitico2010.csv')
    for line in csv_reader:
        if line[1]:     
            NOME_CANDIDATO= line[0]  #ANTONIA LUCILEIA CRUZ RAMOS CAMARA - ExpPolitico_Nome
            ExpPolitico_ID= line[1]  #123756 - ExpPolitico_ID
            ExpPolitico_UF= line[2] 
            ExpPolitico_Titulo= line[3] 
            ExpPolitico_Partido= line[4] 
            ExpPolitico_Sexo= line[5]  #4
            ExpPolitico_DescSexo= line[6]  #FEMININO
            ExpPolitico_NomeReduzido= line[7] #ANTONIA LUCIA
            ExpPolitico_DataNascimento= line[8] #17/07/1970
            ExpPolitico_Cidade= line[9] 
            ExpPolitico_Ano= line[10] 
            ExpPolitico_Cargo= line[11] 
            ExpPolitico_DescSituacao= line[12] 
            ExpPolitico_Nome= line[13] 
  
            addPolitico(NOME_CANDIDATO,ExpPolitico_DataNascimento,ExpPolitico_Nome,ExpPolitico_Partido,ExpPolitico_ID,cursor=cursor)


''' Open CSV file '''
def runCandidaturas(cursor=None):         
    csv_reader = utils.openCSV('data/ExpCandidaturas2010.csv')
    
    for line in csv_reader:
            
        print line[7]
        
        #id = int(line[1])   #keywords = line[4] or None     
        print line[0]  
        ExpCandidaturas_Titulo   = line[0] 
        ExpCandidaturas_Nome   = line[1]  
        ExpCandidaturas_Ano    = line[2] 
        ExpCandidaturas_UF    = line[3] 
        ExpCandidaturas_Cidade  = line[4]   
        ExpCandidaturas_Cargo     = line[5]
        ExpCandidaturas_Partido   = line[6]  
        ExpCandidaturas_DescSituacao     = line[7]
        ExpCandidaturas_ID = line[8]
        

        if ExpCandidaturas_Nome and ExpCandidaturas_Ano=="2010": # and ExpCandidaturas_DescSituacao == "ELEITO": 
            addCandidatura(titulo=ExpCandidaturas_Titulo,nome=ExpCandidaturas_Nome,
                           partidoNome=ExpCandidaturas_Partido,
                           uf=ExpCandidaturas_UF,
                           cidade=ExpCandidaturas_Cidade,    cargo=ExpCandidaturas_Cargo,
                           situacao=ExpCandidaturas_DescSituacao
                           , nascimento = None,id_original=ExpCandidaturas_ID,cursor=cursor)
#             return


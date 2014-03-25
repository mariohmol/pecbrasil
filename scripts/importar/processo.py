''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
import utils
import politico

##################
#    PROCESSOS
###########
def addProcessos(processo,candidatura=None,status=None,desc=None,categoria=None,processosSQL=None): 
    if isinstance(candidatura, tuple):
        candidatura=int(candidatura[0])   
    row = getProcessos(processo,candidatura) 
    if row is None:
        print "Inserido processocandidato "   
        query="INSERT INTO `pecbrasil`.`processocandidato` (`processo`, `candidatura`, `desc`, `status`,`categoria`) VALUES ("
        query=query+"'"+processo+"','"+str(candidatura)+"','"+desc+"','"+status+"','"+categoria+"')"
        print query
        cursor.execute(query)
                 
    else:
        print "Atualizando processocandidato "   + desc
        query="update processocandidato set `desc` = '"+desc+"',status = '"+status+"',categoria = '"+categoria+"' where processo ='"+processo+"'"
        if candidatura is not None:
            query=query+" and candidatura = "+str(candidatura) 
        processosSQL=processosSQL+query
        print query
        cursor.execute(query)
    return processosSQL #getProcessos(processo,candidatura)

def getProcessos(processo,candidatura):  
    query= "select * from processocandidato where processo = '"+processo+"'"
    if candidatura is not None:
        query= query+" and candidatura = '"    +str(candidatura)+ "'"
    
    print query
    cursor.execute(query )
    rows = cursor.fetchall()
    for row in rows:
        return row    
    return None


def runProcessos():         
    csv_reader = utils.openCSV('data/ExpProcessosAbertos.csv')
    processosSQL=""
    for line in csv_reader:
        if line[1]:      
            Processo_Id = line[0]     
            Processo_Origem   = line[1]
            Processos_Status   = line[2]   
            Processos_Identificacao = line[3]     
            Processos_CodigoUnico = line[4]     
            Processos_TRE    = line[5]  
            Processos_Nome   = line[6]  
            ideCadastro= line[7]  
            Processos_Assunto = line[8]     
            Processos_Categoria=  line[8][0:49]
            
            politico = politico.getCandidatura(politico=ideCadastro)
         
            # desc="Origem: %s ,  Identificacao: %s , TRE: %s , Nome: %s",[Processo_Origem,Processos_Identificacao,Processos_TRE,Processos_Nome]
            desc="Origem: "+Processo_Origem+" ,  Identificacao: "+Processos_Identificacao+" , TRE: "+Processos_TRE+" , Nome: "+Processos_Nome\
            + " Assunto: "+Processos_Assunto
 
            processosSQL=addProcessos(processo=Processo_Id,candidatura=politico,desc=desc,processosSQL=processosSQL
                         ,status=Processos_Status,categoria=Processos_Categoria)
            
    utils.writefile('data/Processos.sql',processosSQL)
            




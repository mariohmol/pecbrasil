''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
import utils
import politico


#cursor = utils.getCursorConnection()

##################
#    RODADAS E PONTUACOES
###########

def addRodada(semana,ano,inicio=None,fim=None,cursor=None):    
    row = getRodada(semana,ano,cursor=cursor)    
    if row is None:
        cursor.execute("insert into rodada (semana,ano,inicio,fim) values (%s,%s,%s,%s)",[semana,ano,inicio,fim])
        print "Inserido Rodada " + semana + " / " + ano            
    elif inicio is not None and fim is not None:
        query= "update rodada set inicio=STR_TO_DATE('"+inicio+"', '%d/%m/%Y'), fim=STR_TO_DATE('"+fim+"', '%d/%m/%Y') where semana="+ semana+" and ano="+ str(ano)
        #print query
        #cursor.execute(query)
        
        print "Atualizado Rodada " + semana + " / " + ano
    return getRodada(semana,ano,cursor=cursor)

def updateRodadaMaxMin(semana,ano,max_presenca=None,min_presenca=None,max_proposicao=None, \
                       min_proposicao=None,max_processo=None,min_processo=None, \
                       max_votacao=None,min_votacao=None,max_despesa=None,min_despesa=None,cursor=None): 
   
        
    max_presenca= utils.trataPontoString(max_presenca)
    min_presenca= utils.trataPontoString(min_presenca)
    max_proposicao= utils.trataPontoString(max_proposicao)
    min_proposicao= utils.trataPontoString(min_proposicao)
    max_processo= utils.trataPontoString(max_processo)
    min_processo= utils.trataPontoString(min_processo)
    max_votacao= utils.trataPontoString(max_votacao)
    min_votacao= utils.trataPontoString(min_votacao)
    max_despesa= utils.trataPontoString(max_despesa)
    min_despesa= utils.trataPontoString(min_despesa)
    
    query= "update rodada set max_presenca = '"+str(max_presenca)+"',min_presenca = '"+str(min_presenca)+"',"+ \
    " max_proposicao = '"+str(max_proposicao)+"',min_proposicao = '"+str(min_proposicao)+"',"+ \
    " max_processo = '"+str(max_processo)+"',min_processo = '"+str(min_processo)+"',"+ \
    " max_votacao = '"+str(max_votacao)+"',min_votacao = '"+str(min_votacao)+"',"+ \
     " max_despesa = '"+str(max_despesa)+"',min_despesa = '"+str(min_despesa)+"'"+ \
    "  where semana="+ semana+" and ano="+ str(ano)
    print query
    cursor.execute(query)

def getRodada(semana,ano,cursor=None):   
    cursor.execute("select id from rodada where semana = %s and ano=%s",[semana,ano] )
    rows = cursor.fetchall()
    for row in rows:
        return row    
    return None

''' Open CSV file '''
def runRodadas(cursor=None):         
    csv_reader = utils.openCSV('data/Rodada.csv')    
    for line in csv_reader:
        if line[1]: 
            #id = int(line[1])   #keywords = line[4] or None   
            Ano = line[0] 
            Id = line[1]
            Inicio = line[2]
            Fim = line[3]
            addRodada(semana=Id,ano=Ano,inicio=Inicio,fim=Fim,cursor=cursor)
            

 
        
def addPontuacao(cursor=None,semana=None,ano=None,candidatura=None,pontos=None,presenca=None ,tendenciapresenca=None,
                 totalpresenca=None,proposicao=None,tendenciaproposicao=None,totalproposicao=None
                 ,nascimento=None,
                  processo=None,tendencia_processo=None,total_processo=None,
      votacao=None,tendencia_votacao=None,total_votacao=None,
       despesa=None,tendencia_despesa=None,total_despesa=None
                 ):    
    
    
    if candidatura is None:
        return None
    rowRodada = addRodada(semana,ano,cursor=cursor)
    rowCandidato = politico.getCandidatura(id_original=candidatura,cursor=cursor)   
    if rowCandidato is None:
        print 'Pontuacao: Candidato '+candidatura+" nao encontrado"
        return None
    row = getPontuacao(rowRodada[0],rowCandidato[0],cursor=cursor)    
   
    pontos=utils.trataPonto(pontos)
    presenca=utils.trataPonto(presenca)
    tendenciapresenca=utils.trataPonto(tendenciapresenca)
    totalpresenca=utils.trataPonto(totalpresenca)
    proposicao=utils.trataPonto(proposicao)
    tendenciaproposicao=utils.trataPonto(tendenciaproposicao)
    totalproposicao=utils.trataPonto(totalproposicao)    
    
    #processo=utils.trataPonto(totalproposicao)
    #tendencia_processo=utils.trataPonto(totalproposicao)
    #total_processo=utils.trataPonto(totalproposicao)
    #votacao=utils.trataPonto(totalproposicao)
    #tendencia_votacao=utils.trataPonto(totalproposicao)
    #total_votacao=utils.trataPonto(totalproposicao)
    atualizado = datetime.datetime.now()
    
    #print pontos
    #print "----"
    
    tendencia_processo=utils.trataPonto(tendencia_processo)
    processo=utils.trataPonto(processo)
    total_processo=utils.trataPonto(total_processo)
    tendencia_despesa=utils.trataPonto(tendencia_despesa)
    votacao=utils.trataPonto(votacao)
    despesa=utils.trataPonto(despesa)
    tendencia_despesa=utils.trataPonto(tendencia_despesa)
    total_despesa=utils.trataPonto(total_despesa)
    tendencia_votacao=utils.trataPonto(tendencia_votacao)
    totalproposicao=utils.trataPonto(totalproposicao)
    
    if row is None and semana is not None:
        cursor.execute("insert into pontuacao (rodada,candidatura,pontos,presenca ,tendencia_presenca,total_presenca,proposicao,tendencia_proposicao,total_proposicao,processo,tendencia_processo,total_processo,votacao,tendencia_votacao,total_votacao,despesa,tendencia_despesa,total_despesa,rodada_numero,rodada_ano,atualizado) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                       [rowRodada[0],rowCandidato[0],
                        pontos,presenca ,tendenciapresenca,totalpresenca,
                        proposicao,tendenciaproposicao,totalproposicao,
                        processo,tendencia_processo,total_processo,
                        votacao,tendencia_votacao,total_votacao,
                        despesa,tendencia_despesa,total_despesa,semana,ano,atualizado])
        print "Inserido Pontuacao" 
        print rowRodada[0]
        print rowCandidato[0]           
    else:
        if total_votacao is None or total_votacao =='':
            total_votacao=0
        
        cursor.execute("update pontuacao set pontos=%s,presenca=%s ,tendencia_presenca=%s,total_presenca=%s,proposicao=%s,tendencia_proposicao=%s,total_proposicao=%s , processo=%s,tendencia_processo=%s,total_processo=%s,votacao=%s,tendencia_votacao=%s,total_votacao=%s,despesa=%s,tendencia_despesa=%s,total_despesa=%s,rodada_numero=%s,rodada_ano=%s,atualizado=%s where rodada=%s and candidatura=%s",
                       [pontos,presenca ,tendenciapresenca,totalpresenca,
                        proposicao,   tendenciaproposicao,totalproposicao,
                        processo,tendencia_processo,total_processo,
                        votacao,tendencia_votacao,total_votacao,
                        despesa,tendencia_despesa,total_despesa,semana,ano,atualizado,
                        rowRodada[0],rowCandidato[0]])
        
        print "Atualizado Pontuacao " + semana + " / " + ano + " : " +str(rowCandidato[0])
    return getPontuacao(rowRodada[0],rowCandidato[0],cursor=cursor)

def getPontuacao(rodada,candidatura,cursor=None):   
    cursor.execute("select rodada,candidatura from pontuacao where rodada = %s and candidatura=%s",[rodada,candidatura] )
    rows = cursor.fetchall()
    for row in rows:
        return row    
    return None



''' Open CSV file '''
def runPontuacao(cursor=None,anoFilter=None, semanaFilter=None):         
    csv_reader = utils.openCSV('data/ExpPontuacaoTotal.csv')
    print "runPontuacao"
    for line in csv_reader:

        if line[1]: 
            
         
                        #id = int(line[1])   #keywords = line[4] or None   
                        
                        
            ExpPontuacao_ideCadastro     = line[0] 
            ExpPontuacao_Semana    = line[1]  
            
            ExpPontuacao_UltimoPresenca     = line[2] 
            #ExpPontuacao_TendenciaPresenca    = line[3]  
            ExpPontuacao_TotalPresenca     = line[3] 
            
            ExpPontuacao_UltimoProposicao     = line[4] 
            #ExpPontuacao_TendenciaProposicao    = line[6]  
            ExpPontuacao_TotalProposicao = line[5] 
       
     
            ExpPontuacao_UltimoDespesa     = line[6] 
            #ExpPontuacao_TendenciaDespesa    = line[9]  
            ExpPontuacao_TotalDespesa = line[7] 
                                    
            ExpPontuacao_UltimoVotacao     = line[8] 
            #ExpPontuacao_TendenciaVotacao    = line[12]  
            ExpPontuacao_TotalVotacao = line[9] 
            
            ExpPontuacao_PontoPresenca  = line[10]
            ExpPontuacao_PontoProposicao = line[11]
            ExpPontuacao_PontoDespesa  = line[12]
            ExpPontuacao_PontoVotacao  = line[13]
            ExpPontuacao_Pontuacao= line[14]
            ano= line[15] #ExpPontuacao_Ano

	    if ((anoFilter is None or anoFilter==ano) and (semanaFilter is None or semanaFilter==ExpPontuacao_Semana)):
            	addPontuacao(cursor=cursor, semana=ExpPontuacao_Semana,ano=ano,candidatura=ExpPontuacao_ideCadastro,
            
		        pontos=ExpPontuacao_Pontuacao,
		    
		        presenca=ExpPontuacao_UltimoPresenca ,
		        #tendenciapresenca=ExpPontuacao_TendenciaPresenca,
		        totalpresenca=ExpPontuacao_TotalPresenca,
		    
		        proposicao=ExpPontuacao_UltimoProposicao,
		        #tendenciaproposicao=ExpPontuacao_TendenciaProposicao,
		        totalproposicao=ExpPontuacao_TotalProposicao, 
		    
		    
		        votacao=ExpPontuacao_UltimoVotacao ,            
		        #tendencia_votacao=ExpPontuacao_TendenciaVotacao,
		        total_votacao=ExpPontuacao_TotalVotacao,
		    
		        despesa=ExpPontuacao_UltimoDespesa ,
		        #tendencia_despesa=ExpPontuacao_TendenciaDespesa,
		        total_despesa=ExpPontuacao_TotalDespesa
            
            
            )
              
            ''' 
            ExpPontuacao_ideCadastro     = line[0] 
            ExpPontuacao_UltimaSemana    = line[1]  
            ExpPontuacao_Semana     = line[2] 
            ExpPontuacao_TituloPolitico     = line[3] 
            ExpPontuacao_Titulo     = line[4] 
            ExpPontuacao_Cidade     = line[5] 
            ExpPontuacao_Cargo     = line[6] 
            ExpPontuacao_DataNascimento   = line[7]   
            ExpPontuacao_AnoEleicao     = line[8] 
            ExpPontuacao_Sexo     = line[9] 
            ExpPontuacao_Partido     = line[10] 
            ExpPontuacao_nome     = line[11] 
            ExpPontuacao_uf     = line[12] 
            
                      
            ExpPontuacao_UltimoPresenca     = line[13] 
            ExpPontuacao_TendenciaPresenca    = line[14]  
            ExpPontuacao_TotalPresenca     = line[15] 
            
            ExpPontuacao_UltimoProposicao     = line[16] 
            ExpPontuacao_TendenciaProposicao    = line[17]  
            ExpPontuacao_TotalProposicao = line[18] 
       
     
            ExpPontuacao_UltimoDespesa     = line[19] 
            ExpPontuacao_TendenciaDespesa    = line[20]  
            ExpPontuacao_TotalDespesa = line[21] 
            
            
            ExpPontuacao_UltimoProcesso     = line[22] 
            ExpPontuacao_TendenciaProcesso    = line[23]  
            ExpPontuacao_TotalProcesso = line[24] 
            
            ExpPontuacao_UltimoVotacao     = line[25] 
            ExpPontuacao_TendenciaVotacao    = line[26]  
            ExpPontuacao_TotalVotacao = line[27] 
            
            ExpPontuacao_MaxTotalPresenca = line[28]  
            ExpPontuacao_MaxUltimoPresenca  = line[29]
            ExpPontuacao_MaxTendenciaPresenca   = line[30]
            ExpPontuacao_MaxTotalProposicao = line[31]
            ExpPontuacao_MaxUltimoProposicao = line[32]
            ExpPontuacao_MaxTendenciaProposicao  = line[33]
            ExpPontuacao_MaxTotalDespesa   = line[34]
            ExpPontuacao_MaxUltimoDespesa  = line[35]
            ExpPontuacao_MaxTendenciaDespesa  = line[36]
            ExpPontuacao_MaxTotalVotacao= line[37]
            ExpPontuacao_MaxUltimoVotacao  = line[38]
            ExpPontuacao_MaxTendenciaVotacao  = line[39]
            ExpPontuacao_MaxTotalProcesso   = line[40]
            ExpPontuacao_MaxUltimoProcesso = line[41]
            ExpPontuacao_MaxTendenciaProcesso  = line[42]
            
            ExpPontuacao_MinTotalPresenca   = line[43] 
            ExpPontuacao_MinUltimoPresenca  = line[44] 
            ExpPontuacao_MinTendenciaPresenca  = line[45]
            ExpPontuacao_MinTotalProposicao   = line[46]
            ExpPontuacao_MinUltimoProposicao  = line[47] 
            ExpPontuacao_MinTendenciaProposicao = line[48]
            ExpPontuacao_MinTotalDespesa = line[49]
            ExpPontuacao_MinUltimoDespesa  = line[50]
            ExpPontuacao_MinTendenciaDespesa = line[51]
            ExpPontuacao_MinTotalVotacao= line[52]
            ExpPontuacao_MinUltimoVotacao = line[53]
            ExpPontuacao_MinTendenciaVotacao = line[54]
            ExpPontuacao_MinTotalProcesso  = line[55]
            ExpPontuacao_MinUltimoProcesso = line[56]
            ExpPontuacao_MinTendenciaProcesso = line[57]
            
            ExpPontuacao_PontoPresenca  = line[58]
            ExpPontuacao_PontoProposicao = line[59]
            ExpPontuacao_PontoDespesa  = line[60]
            ExpPontuacao_PontoVotacao  = line[61]
            ExpPontuacao_PontoProcesso = line[62]
            ExpPontuacao_Pontuacao= line[63]
            ExpPontuacao_Ano= line[64]
            
               
            addPontuacao(semana=ExpPontuacao_Semana,ano=ExpPontuacao_Ano,candidatura=ExpPontuacao_Titulo,
                 pontos=ExpPontuacao_Pontuacao,
                 presenca=ExpPontuacao_UltimoPresenca ,tendenciapresenca=ExpPontuacao_TendenciaPresenca,
                 totalpresenca=ExpPontuacao_TotalPresenca,
                 proposicao=ExpPontuacao_UltimoProposicao,tendenciaproposicao=ExpPontuacao_TendenciaProposicao
                 ,totalproposicao=ExpPontuacao_TotalProposicao, nascimento = ExpPontuacao_DataNascimento,
                 
            processo=ExpPontuacao_UltimoProcesso,
            tendencia_processo=ExpPontuacao_TendenciaProcesso,
            total_processo=ExpPontuacao_TotalProcesso ,
            votacao=ExpPontuacao_UltimoVotacao ,
            
            tendencia_votacao=ExpPontuacao_TendenciaVotacao,
            total_votacao=ExpPontuacao_TotalVotacao,
            
            despesa=ExpPontuacao_UltimoDespesa ,
            tendencia_despesa=ExpPontuacao_TendenciaDespesa,
            total_despesa=ExpPontuacao_TotalDespesa)
            
            updateRodadaMaxMin(semana=ExpPontuacao_Semana,ano=ano,max_presenca=ExpPontuacao_MaxUltimoPresenca,min_presenca=ExpPontuacao_MinUltimoPresenca, \
                               max_proposicao=ExpPontuacao_MaxUltimoProposicao, \
                       min_proposicao=ExpPontuacao_MinUltimoProposicao,max_processo=ExpPontuacao_MaxUltimoProcesso,min_processo=ExpPontuacao_MinUltimoProcesso, \
                       max_votacao=ExpPontuacao_MaxUltimoVotacao,min_votacao=ExpPontuacao_MinUltimoVotacao, \
                       max_despesa=ExpPontuacao_MaxUltimoDespesa,min_despesa=ExpPontuacao_MinUltimoDespesa)
 '''
    cursor.execute("update pontuacao p set p.rodada_ano = (select ano from rodada WHERE id = p.rodada);")

    cursor.execute("update pontuacao p set p.rodada_numero = (select semana from rodada WHERE id = p.rodada);")
          
            
                     
def getMaxRodada(cursor=None):
    cursor.execute("SELECT max(id) from rodada")
    rows = cursor.fetchall()
    for row in rows:
        return row[0]
    

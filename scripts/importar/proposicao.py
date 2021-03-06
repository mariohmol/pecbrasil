''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
import utils
import politico
import orgao

''' Connect to DB '''
#cursor = utils.getCursorConnection()

depara=utils.runCoding()

##################
#    Proposicao
###########
def addProposicao(sigla,status=None,desc=None,candidatura=None,proposicaoSQL=None,data=None,autor=None,tipo=None,originalid=None,cursor=None):    
    
    row = getProposicao(sigla,cursor=cursor)   
    desc=utils.applyCoding(desc,depara) 
    desc=desc.replace("'" ,'"' )
    autor=autor.replace("'" ,'"' )
    if autor is not None and len(autor)>490:
        autor=autor[:490]
    data=utils.formatDate(data,'%d/%m/%Y %H:%M:%S','%Y-%m-%d')
    if isinstance(candidatura, tuple):
        candidatura=int(candidatura[0]) 
    if candidatura is None:
        candidatura=0
    if row is None:
        cursor.execute("INSERT INTO `proposicao` (`status`,  `sigla`, `desc`,candidatura,autor,data,tipo,originalid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",[status,sigla,desc,str(candidatura),autor,data,tipo,originalid])
        print "Inserido Proposicao "            
    else:
        query = "update proposicao set `desc` = '"+desc+"',`status` = '"+status +        "',`autor` = '"+autor+"',`data` = '"+data+"',`tipo` = '"+tipo+"',`candidatura` = '"+ \
        str(candidatura)+"',originalid='"+originalid+"' where sigla = '"+sigla+ "';"
        print "Atualizando Proposicao "+sigla
        print query
        cursor.execute(query )
        proposicaoSQL=proposicaoSQL+query
        
    #return getProposicao(sigla)
    return proposicaoSQL

def getProposicao(sigla,cursor=None):
    #print "select id from proposicao where sigla = %s",[sigla]
    cursor.execute("select id from proposicao where sigla = %s",[sigla] )
    rows = cursor.fetchall()
    for row in rows:
        return row    
    #print "select id from proposicao where sigla like '%"+sigla+"'"
    cursor.execute("select id from proposicao where sigla like '%"+sigla+"'" )
    rows = cursor.fetchall()
    for row in rows:
        return row
    return None

def getProposicaoByOriginal(id,cursor=None):
    cursor.execute("select id from proposicao where originalid = %s",[id] )
    rows = cursor.fetchall()
    for row in rows:
        return row

##################
# STATUS
#####################
def getStatusProposicao(id=None,nome=None,cursor=None):
    print str(nome)+" get status"+str(id)
    cursor.execute("select id_statusproposicao from statusproposicao where originalid_statusproposicao = %s",[id] )
    rows = cursor.fetchall()
    for row in rows:
        return str(row[0]) 
    
    cursor.execute("select id_statusproposicao from statusproposicao where nome_statusproposicao = %s",[nome] )
    rows = cursor.fetchall()
    for row in rows:
        return str(row[0]) 
    return addStatusProposicao(id=id,nome=nome,cursor=cursor)

def addStatusProposicao(id=None,nome=None,cursor=None):
    cursor.execute("INSERT INTO `statusproposicao` (`nome_statusproposicao`, `originalid_statusproposicao`) VALUES (%s,%s)",[nome,id])
    return getTipoProposicao(id=id,nome=nome,cursor=cursor)





##################
# TIPO
#####################
def getTipoProposicao(id=None,nome=None,sigla=None,cursor=None):
    if not sigla:
        sigla=nome
    print str(id)+" gettipo "+str(nome)+" -  sigla: "+str(sigla)
    cursor.execute("select id_tipoproposicao from tipoproposicao where sigla_tipoproposicao = %s",[sigla] )
    rows = cursor.fetchall()
    for row in rows:
        return str(row[0])
    return addTipoProposicao(id,nome,sigla,cursor=cursor)
  
def addTipoProposicao(id=None,nome=None,sigla=None,cursor=None):
    if not nome:
        nome=sigla
    cursor.execute("INSERT INTO `tipoproposicao` (`nome_tipoproposicao`, `sigla_tipoproposicao`,originalid_tipoproposicao) VALUES (%s,%s,%s)",[nome,sigla,id])
    print str(sigla)+"ADD TIPO PROPOSICAO"+str(nome)
    return getTipoProposicao(id=id,nome=nome,sigla=sigla,cursor=cursor)



##################
# ACAO
#####################
def getProposicaoAcao(id=None,proposicao=None,data=None,cursor=None):
    print str(id)+" proposicaoacao "+str(proposicao)
    if id:      
        cursor.execute("select id_proposicaoacao from proposicaoacao where originalid_proposicaoacao = %s",[id] )
        rows = cursor.fetchall()
        for row in rows:
            return str(row[0])
    if proposicao and data:
        cursor.execute("select id_proposicaoacao from proposicaoacao where proposicao_proposicaoacao = %s and data_proposicaoacao = %s",[proposicao,data] )
        rows = cursor.fetchall()
        for row in rows:
            return str(row[0])    
  
def addProposicaoAcao(id=None,nome=None,siglaProposicao=None,data=None,status=None,orgao=None,candidatura=None,cursor=None):
    
    proposicao_proposicaoacao=getProposicao(siglaProposicao,cursor=cursor)
    status_proposicaoacao=getStatusProposicao(nome=status,cursor=cursor)
    print "Proposicao A Encontrada:"+str(proposicao_proposicaoacao[0])
    sql="select id_proposicaoacao from proposicaoacao where data_proposicaoacao='"+str(data)+"' and proposicao_proposicaoacao='"+ str(proposicao_proposicaoacao[0])+ "'"
    print sql
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        return str(row[0])
    
    cursor.execute("INSERT INTO `proposicaoacao` (`nome_proposicaoacao`, `originalid_proposicaoacao`,data_proposicaoacao,proposicao_proposicaoacao,"
                   +"status_proposicaoacao,candidatura_proposicaoacao,orgao_proposicaoacao) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                   [nome,id,data,proposicao_proposicaoacao[0],status_proposicaoacao[0],candidatura,orgao[0]])
    return getProposicaoAcao(proposicao=proposicao_proposicaoacao[0],data=data,cursor=cursor)


##################
# RUN PROPOSICAO ACAO
#####################
def runProposicaoAcao(cursor=None,anoFilter=None,semanaFilter=None):         
    csv_reader = utils.openCSV('data/TramitacaoOrgaoProposicao.csv')
    proposicaoSQL=""
    siglaAtual=None
    for line in csv_reader:
        if line[1]:      
            
            ProposicaoAcao_tipo    = line[0]
            ProposicaoAcao_numero   = line[1]
            ProposicaoAcao_ano    = line[2]
            ProposicaoAcao_situacao    = line[3]
            ProposicaoAcao_ementa    = line[4]
            ProposicaoAcao_idProposicao = line[5]   
            ProposicaoAcao_data    = line[6]
            ProposicaoAcao_codOrgao = line[7]   
            ProposicaoAcao_orgao    = line[8]
            ProposicaoAcao_descricao = line[9]   
            
            ProposicaoAcao_Sigla= ProposicaoAcao_tipo + " " + ProposicaoAcao_numero + "/"+ ProposicaoAcao_ano 
            ProposicaoAcao_data=utils.formatDate(ProposicaoAcao_data)
            
            
            id = getProposicao(sigla=ProposicaoAcao_Sigla,cursor=cursor)
            if not id:
                id = getProposicaoByOriginal(id=ProposicaoAcao_idProposicao,cursor=cursor)
            
            if not id:
                print "Proposicao Nao Encontrada:"+ProposicaoAcao_Sigla
                continue
            
            #ProposicaoAcao_situacao
            
            orgaoId = orgao.addOrgao(sigla=ProposicaoAcao_orgao,original_cf=ProposicaoAcao_codOrgao,desc=ProposicaoAcao_orgao,cursor=cursor) 
            
            proposicaoSQL=addProposicaoAcao(nome=ProposicaoAcao_ementa,data=ProposicaoAcao_data,siglaProposicao=ProposicaoAcao_Sigla,
                                            status=ProposicaoAcao_situacao,orgao=orgaoId,cursor=cursor)
    


##################
# RUN PROPOSICAO
#####################
def runProposicao(cursor=None,anoFilter=None,semanaFilter=None):         
    csv_reader = utils.openCSV('data/ExpProposicao.csv')
    proposicaoSQL=""
    siglaAtual=None
    for line in csv_reader:
        if line[1]:      
            
            
            Proposicao_numero    = line[0] 
            Proposicao_ano   = line[1]  
            Proposicao_Id= line[2]  
            Proposicao_nomePolitico  = line[3]   
            Proposicao_datApresentacao  = line[4]   
            Proposicao_txtEmenta   = line[5]  
            Proposicao_txtExplicacaoEmenta = line[6]    
            Proposicao_qtdAutores    = line[7] 
            Proposicao_indGenero    = line[8] 
            Proposicao_qtdOrgaosComEstado    = line[9] 
            Proposicao_situacao    = line[10] 
            Proposicao_descricao    = line[11] 
            Proposicao_codProposicaoPrincipal = line[12]    
            Proposicao_proposicaoPrincipal = line[13]    
            Proposicao_codOrgaoEstado    = line[14] 
            Proposicao_siglaOrgaoEstado  = line[15]   
            Proposicao_datDespacho    = line[16] 
            Proposicao_txtDespacho= line[17] 


            Proposicao_txtNomeAutor= line[18] 
            ideCadastro= line[19] 
            Proposicao_codPartido= line[20] 
            Proposicao_txtSiglaPartido= line[21] 
            Proposicao_txtSiglaUF= line[22] 
            Proposicao_apreciacaoId= line[23] 
            Proposicao_txtApreciacao= line[24] 
            Proposicao_codRegime= line[25] 
            Proposicao_txtRegime= line[26] 
            Proposicao_orgaoNumeradorId= line[27] 
            Proposicao_orgaoNumeradorSigla= line[28] 
            Proposicao_orgaoNumeradorNome= line[29] 
            Proposicao_tipoProposicaoId= line[30] 
            TipoProposicao_tipoSigla= line[31] 
            Proposicao_tipoProposicaoNome= line[32] 
            ProposicaoVotada_codProposicao= line[33] 
            ProposicaoVotada_nomeProposicao= line[34] 
            ProposicaoVotada_tipo= line[35] 
            ProposicaoVotada_ano= line[36] 
            ProposicaoVotada_id= line[37] 


            ExpVotacao_Sigla= TipoProposicao_tipoSigla + " " + Proposicao_numero + "/"+ Proposicao_ano  
            
            ExpVotacao_Desc= Proposicao_txtEmenta
            if Proposicao_nomePolitico:
                ExpVotacao_Desc=ExpVotacao_Desc+ " -- Ementa " + Proposicao_txtExplicacaoEmenta 
            if Proposicao_nomePolitico:
                ExpVotacao_Desc=ExpVotacao_Desc+ " -- Orgao do estado: " +  Proposicao_codOrgaoEstado 
            if Proposicao_nomePolitico:
                ExpVotacao_Desc=ExpVotacao_Desc+ " -- Apreciacao: " +              Proposicao_txtApreciacao 
            #  ?? CONGRESSO NACIONAL,
            if Proposicao_nomePolitico:
                ExpVotacao_Desc=ExpVotacao_Desc+ " -- Nome politico: " + Proposicao_nomePolitico 
            # Aviso (CN) , Emenda na Comissao
            if Proposicao_orgaoNumeradorNome:
                ExpVotacao_Desc=ExpVotacao_Desc+ " -- Orgao Numeraodor: " + Proposicao_orgaoNumeradorNome
            ExpVotacao_Autor = Proposicao_txtNomeAutor + " - " + Proposicao_txtSiglaPartido
            ExpVotacao_Data = Proposicao_datApresentacao
            ExpVotacao_Tipo = Proposicao_tipoProposicaoNome
                

            ExpVotacao_Status= Proposicao_situacao  + " - " + Proposicao_descricao
            
            if siglaAtual is None:
                siglaAtual=ExpVotacao_Sigla
            elif siglaAtual == ExpVotacao_Sigla:
                continue
            else:
                siglaAtual = ExpVotacao_Sigla 
            row = politico.getCandidatura(id_original=ideCadastro,cursor=cursor)
            
            tipo = getTipoProposicao(id=Proposicao_tipoProposicaoId , sigla=TipoProposicao_tipoSigla,
                                     nome=Proposicao_tipoProposicaoNome,cursor=cursor)
            
            status = getStatusProposicao(id=Proposicao_situacao ,   nome=Proposicao_descricao,cursor=cursor)
            
            proposicaoSQL=addProposicao(status=status,sigla=ExpVotacao_Sigla, autor=ExpVotacao_Autor,
                                        data=ExpVotacao_Data,tipo=tipo,originalid=Proposicao_Id,
                                        desc=ExpVotacao_Desc,candidatura=row,proposicaoSQL=proposicaoSQL,cursor=cursor)
    #utils.writefile('data/Proposicoes.sql',proposicaoSQL)
            #addVotacaoCandidato(votacao,candidatura=politico,voto=None)
            
########################
# UTILS
####################

def separaSiglaNumeroAnoProposicao(entrada):
    #PL 6025/2005
    entrada=trim(entrada)


def propostaVinculada(sigla):
    sigla = trim(sigla)
    siglas = sigla.split("=>")
    for sig in siglas:
        sigla=trim(sig)
    return sigla   
   
#Fazer script para verifica proposicoes com data de votacao mas sem registros de votacaocandidato (jWEB)
#Fazer script no qlikview para baixar proposicoes q foram votadas mas ainda nao extraidas (qlikview)

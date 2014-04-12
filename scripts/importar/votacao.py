''' Import statements '''
import utils
import politico
import proposicao
from mako.filters import trim

''' Connect to DB '''
#cursor = utils.getCursorConnection()
logflag=True
depara=utils.runCoding()
def addVotacaoCandidato(proposicao,candidatura,voto=None,cursor=None): 
    if   candidatura is None:
        print "addVotacaoCandidato candidatura retornou"
        return
    if proposicao is None:
        print "addVotacaoCandidato proposicao retornou"
        return
    
    print "Iniciando addVotacaoCandidato"
    if voto == 'Sim':
        votoInt = 1;
    elif len(voto)>3:
        votoInt = 2; #obstrucao
    else:        
        votoInt = 3;
    #print str(votoInt) + " - " + voto
    
    if isinstance(candidatura, tuple):
        candidatura=int(candidatura[0]) 
        
    if isinstance(proposicao, tuple):
        proposicao=int(proposicao[0]) 
         
    row = getVotacaoCandidato(proposicao,candidatura,cursor=cursor)  
    
    if row is None:
        cursor.execute("insert into votacaocandidato (proposicao,candidatura,voto) values (%s,%s,%s)",[proposicao,candidatura, votoInt])
        if logflag: print "Inserido votacaocandidato "            
    else:
        cursor.execute("update votacaocandidato set voto = '"+str(votoInt)+"' where  candidatura = %s and proposicao = %s",[candidatura,proposicao] )
        if logflag: print "Atualizando votacaocandidato " 
    return getVotacaoCandidato(proposicao,candidatura,cursor=cursor)

def getVotacaoCandidato(proposicao,candidatura,cursor=None): 
    print "select voto,candidatura from votacaocandidato where proposicao = %s and candidatura = %s",[proposicao,candidatura]
    cursor.execute("select voto,candidatura from votacaocandidato where proposicao = %s and candidatura = %s",[proposicao,candidatura] )
    rows = cursor.fetchall()
    for row in rows:
        return row    
    return None

def limparVotacaoCandidato(cursor=None): 
    cursor.execute("delete from votacaocandidato " )
    return None

def runVotacaoCandidato(cursor=None):         
    csv_reader = utils.openCSV('data/ExpVotacaoDeputado.csv')
    #"update proposicao set favor=null, contra=null , abstencao=null where id>0"
    for line in csv_reader:
        if line[1]:      
            
            #VotacaoDeputado_Nome = line[0]   
            ideCadastro    = line[1]
            #VotacaoDeputado_Partido  = line[2]  
            #VotacaoDeputado_UF    = line[3]
            VotacaoDeputado_Voto   = line[4] 
            VotacaoDeputado_Numero  = line[5]  
            VotacaoDeputado_Ano    = line[6]
            #VotacaoDeputado_Resumo= line[7]
            print ideCadastro
            politicoCand = politico.getCandidatura(id_original=ideCadastro,cursor=cursor)
            print VotacaoDeputado_Numero+"/"+VotacaoDeputado_Ano
            proposicaoCand=proposicao.getProposicao(" " + VotacaoDeputado_Numero+"/"+VotacaoDeputado_Ano,cursor=cursor)
            print proposicaoCand
            addVotacaoCandidato(proposicao=proposicaoCand,
                                candidatura=politicoCand,voto=VotacaoDeputado_Voto,cursor=cursor)

def runVotacaoProposicao(cursor=None):         
    csv_reader = utils.openCSV('data/VotacoesProposicoes.csv')
    #"update proposicao set favor=null, contra=null , abstencao=null where id>0"
    print "runVotacaoProposicao:"
    for line in csv_reader:
        if line[1]:      
             
            codProposicao    = line[0]
            nomeProposicao  = line[1]  
            dataVotacao    = line[2]
            dataVotacao=utils.formatDate(dataVotacao,'%d/%m/%Y','%Y-%m-%d')
            
            nomeProposicao= proposicao.propostaVinculada(nomeProposicao)
            print "Proposicao:"+nomeProposicao
            id = proposicao.getProposicao(sigla=nomeProposicao,cursor=cursor)
            if not id:
                id = proposicao.getProposicaoByOriginal(id=codProposicao,cursor=cursor)
            
            if not id:
                continue
            id=id[0]
            print "Proposicao Encontrada:"+str(id)
            cursor.execute("UPDATE proposicao SET datavotacao=%s where id = %s",[dataVotacao,id])
         


#runVotacaoCandidato()




''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
import utils
import politico
import rodada

#cursor = utils.getCursorConnection()

##################
#    DESPESAS
# 
#
###########
def addDespesas(candidatura=None,categoria=None,valor=None,rodada=None,despesasSQL=None,cursor=None):    
    row = getDespesas(candidatura=candidatura,categoria=categoria,rodada=rodada,valor=valor,cursor=cursor)    
    if isinstance(candidatura, tuple):
        candidatura=int(candidatura[0])
    if isinstance(categoria, tuple):
        categoria=int(categoria[0])   
    #print categoria
    #categoria = applyCoding(categoria,depara)
    
    #return

    if row is None:
        query="insert into despesacandidato (ativo,categoria,candidatura,valor,rodada) values (1,'"+ \
        str(categoria)+"',"+ str(candidatura) + ",'"+valor+"',"+str(rodada)+");"
        print "Inserido DESPESAS "  +query   
        cursor.execute(query)
    else:
        
        query="update despesacandidato set ativo=1, categoria = '"+str(categoria)+"',valor = '"+valor+ \
        "' where rodada = "+str(rodada)+" and candidatura = "+ str(candidatura)+ ";"
        despesasSQL=despesasSQL+query
        print query
        print "Atualizando DESPESAS: "+query
        cursor.execute(query )
    return despesasSQL #getDespesas(candidatura=candidatura,rodada=rodada,categoria=categoria,valor=valor)

def getDespesas(rodada,candidatura,categoria,valor,cursor=None):   
    #categoria='ola'
    #candidatura='1'
    if isinstance(candidatura, tuple):
        candidatura=int(candidatura[0])
    if isinstance(categoria, tuple):
        categoria=int(categoria[0])
    
    #print "select * from despesacandidato where rodada = %s and candidatura = %s and categoria = %s",   [rodada,candidatura,categoria]
    
    query="select * from despesacandidato where rodada = "+str(rodada)+ \
          " and candidatura = "+str(candidatura)+" and categoria = '"+ str(categoria) + "'"
    print query
    cursor.execute(query )
    
    rows = cursor.fetchall()
    for row in rows:
        return row 
    
    query="select * from despesacandidato where rodada = "+str(rodada)+ \
          " and candidatura = "+str(candidatura)+" and valor = '"+ valor + "'"
    print query
    cursor.execute(query )
    
    rows = cursor.fetchall()
    for row in rows:
        return row    
    return None

def getDespesaTipo(nome,cursor=None):
    print "Nome Antes" + nome
    if nome[0:6] == 'ASSINATURA'[0:6]:
        nome='ASSINATURA DE PUBLICACOES'
        
    if nome[0:6] == 'COMBUSTIVEIS E LUBRIFICANTES'[0:6]:
        nome='COMBUSTIVEIS E LUBRIFICANTES'    

    if nome[0:6] == 'CONSULTORIAS'[0:6]:
        nome='CONSULTORIAS'             
         
    if trim(nome)[8:12] == 'SERVICOS POSTAIS'[7:11]:
        nome='SERVICOS POSTAIS' 
    if nome[0:5].upper() == 'EMISSAO BILHETE AEREO'[0:5]:
        nome='EMISSAO BILHETE AEREO'      
    
    if nome[0:6] == 'DIVULGACAO'[0:6]:
        nome='DIVULGACAO DA ATIVIDADE PARLAMENTAR'            
  
    if nome[0:6] == 'MANUTENCAO DE ESCRITORIO DE APOIO A ATIVIDADE'[0:6]:
        nome='MANUTENCAO DE ESCRITORIO DE APOIO A ATIVIDADE'        
    
    if nome[0:6] == 'FORNECIMENTO DE ALIMENTACAO DO PARLAMENTAR'[0:6]:
        nome='FORNECIMENTO DE ALIMENTACAO DO PARLAMENTAR'         
    
    if nome[0:4] == 'LOCACAO DE VEICULOS AUTOMOTORES OU FRETAMENTO'[0:4]:
        nome='LOCACAO DE VEICULOS AUTOMOTORES OU FRETAMENTO' 
         
    if nome[0:6] == 'PASSAGENS AEREAS E FRETAMENTO DE AERONAVES'[0:6]:
        nome='PASSAGENS AEREAS E FRETAMENTO DE AERONAVES' 
 
    if nome[22:27] == 'SERVICO DE SEGURANCA PRESTADO POR EMPRESA ESPECIALIZADA'[20:25]:
        nome='SERVICO DE SEGURANCA PRESTADO POR EMPRESA ESPECIALIZADA' 
    if nome[30:44]=="ESTACIONAMENTO":   
        nome='SERVICO DE TAXI, PEDAGIO E ESTACIONAMENTO'
    
    #nome = applyCoding(nome,depara)
    print "Nome Depois" + nome
    
    query="select * from despesatipo where nome_despesatipo = '"+str(nome)+ "'"
    print query
    cursor.execute(query )
    rows = cursor.fetchall()
    for row in rows:
        return row    
    
    query="insert into despesatipo (nome_despesatipo) values ('"+str(nome)+"');"
    print "Inserido DESPESAS "  +query   
    cursor.execute(query)
    
    return getDespesaTipo(nome,cursor=cursor)

def runDespesas(cursor=None,anoFilter=None, semanaFilter=None):         
    csv_reader = utils.openCSV('data/ExpDespesas.csv')
    despesasSQL=""
    max=100
    i=0
    for line in csv_reader:
        i=i+1
        
        Despesas_semanaInicio  = line[2]  
        ano=  Despesas_semanaInicio[-4:]
            
        if (line[1] and len(line)>=5 and ((anoFilter is None or anoFilter==ano) and (semanaFilter is None or semanaFilter==Despesas_semana))):  
            #if i > max:
            #    break
             
            Despesas_semana  = line[1]   
            Despesas_semanaFim    = line[3]    
          
            #addRodada(semana=Despesas_semana,ano=ano,inicio=Despesas_semanaInicio,fim=Despesas_semanaFim)
            rodadaRetorno=rodada.addRodada(semana=Despesas_semana,ano=ano,cursor=cursor) 
     
            if isinstance(rodadaRetorno, tuple):
                rodadaRetorno=int(rodadaRetorno[0])
  
            ideCadastro  = line[0] 
            politicoRetorno = politico.getCandidatura(id_original=ideCadastro,cursor=cursor)
            
            Despesas_txtDescricao  = line[4]  
            Despesas_txtDescricao=getDespesaTipo(Despesas_txtDescricao,cursor=cursor)
            #Despesas_txtDescricao = Despesas_txtDescricao.decode("utf-8")
            Despesas_vlrLiquido= line[5]
            Despesas_vlrLiquido = Despesas_vlrLiquido.replace(",",".")

            if politicoRetorno is not None:
                despesasSQL=addDespesas(candidatura=politicoRetorno,categoria=Despesas_txtDescricao,  
                            valor=Despesas_vlrLiquido,rodada=rodadaRetorno,despesasSQL=despesasSQL,cursor=cursor)
            
    #runDespesasCoding()
    #utils.writefile('data/Despesas.sql',despesasSQL)

def runDespesasCoding(cursor=None):         
    csv_reader = utils.openCSV('data/CodingDespesas.csv')
    #SELECT DISTINCT categoria, idcategoria FROM `despesacandidato`
    #delete FROM `despesacandidato`
    cursor.execute("update  `despesacandidato` set idcategoria=md5(categoria)")
    
    return
    for line in csv_reader:
        if line[1]:      
            
            Coding_DE= line[0]  
            CodingMD5= line[1]
            #Actual
            Coding_PARA= line[2]  
            #addCoding(Coding_DE,Coding_PARA,depara)
            query="update despesacandidato set categoria='"+Coding_PARA+ \
            "' where idcategoria = '"+CodingMD5+"';"
            print query
            cursor.execute(query)  
            
         

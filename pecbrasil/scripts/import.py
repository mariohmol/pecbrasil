''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
from importar import utils
from optparse import OptionParser





#Exemplo de Chamada
# python import.py -o runPontuacao -a L
parser = OptionParser()
parser.add_option("-o", "--opcao", dest="opcao",
                  help="escolha qual passo do processamento", metavar="OPCAO")

parser.add_option("-r", "--rodada", dest="rodada",
                  help="distribua os pontos nas ligas e times de acordo com nova pontuacao da rodada", metavar="RODADA")

parser.add_option("-a", "--ambiente", dest="ambiente",
                  help="define o ambiente de conexao com o banco (L = Local,P=Producao), se vazio local, ", metavar="AMBIENTE")

parser.add_option("-y", "--ano", dest="ano",
                  help="define o ano que deseja processar, descartando dados dos demais ", metavar="ANO")

parser.add_option("-s", "--semana", dest="semana",
                  help="define a semana que deseja processar, descartando dados dos demais ", metavar="SEMANA")


(options, args) = parser.parse_args()


opcao=None
rodadaOption=None
ambiente=None
ano="2014"
semana=None
if options.opcao is not None:    
    opcao=trim(options.opcao)
if options.rodada is not None:    
    rodadaOption=trim(options.rodada)
if options.ambiente is not None:    
    ambiente=trim(options.ambiente)
if options.ano is not None:    
    ano=trim(options.ano)
if options.semana is not None:    
    ambiente=trim(options.semana)

''' Connect to DB '''
cursor = utils.getCursorConnection(ambiente)

depara=utils.runCoding()
logflag=True


from importar import politico
from importar import proposicao
from importar import partido
from importar import despesa
from importar import processo
from importar import repasse
from importar import votacao
from importar import rodada
import pontos

    

#Scripts de criacao de Base
if opcao=="runPartido":
    partido.runPartido(cursor=cursor)    
if opcao=="runPolitico":
    politico.runPolitico(cursor=cursor)
if opcao=="runCandidaturas":
    politico.runCandidaturas(cursor=cursor)


#Detalhes das informacoes usadas em pontuacao
if opcao=="runDespesas":
    despesa.runDespesas(cursor=cursor,anoFilter=ano,semanaFilter=semana)
if opcao=="runProposicao":
    proposicao.runProposicao(cursor=cursor,anoFilter=ano,semanaFilter=semana)
if opcao=="runVotacaoCandidato":
    votacao.runVotacaoCandidato(cursor=cursor)


#Scripts de Pontuacao
if opcao=="runPontuacao":
    rodada.runPontuacao(cursor=cursor,anoFilter=ano,semanaFilter=semana)
    
    
###################################
# ESSES METODOS SAO EXECUTADOS PELA WEB
####################################
#if opcao=="updatePontuacaoCandidatosSQL":
#    pontos.updatePontuacaoCandidatosSQL(cursor=cursor)
#if opcao=="updatePontuacaoTimesSQL":
#    pontos.updatePontuacaoTimesSQL(cursor=cursor)
#if opcao=="updatePontuacaoPartidosSQL":
#    pontos.updatePontuacaoPartidosSQL(cursor=cursor)
#if opcao=="updateRodadaMaxMinAutomatic":
#    pontos.updateRodadaMaxMinAutomatic(cursor=cursor)
#if rodadaOption is not None and rodadaOption.is_digit():
#    rodada.buildRodada(rodadaOption,2013)
###################################


#runDespesasCoding()
#processosTest(depara)

#runPartidoCores()
#runRodadas()


#---------------------------------------------------------------------
#Nao utilizar , verificar melhor (utilizar o ..SQL() no lugar)
#updatePontuacaoCandidatos()
#updatePontuacaoTimes()

#runDespesasCoding()
#processosTest(depara) 
#proposicaoTest(depara)

#DESCONTINUADO
#runPontuacaoTotal()
#runProcessos()
#runPresenca() ?? A desenvolver

#cleanAll()  

#Rodar apenas em testes, para gerar todas as rodadas de uma vez
#buildRodadas();

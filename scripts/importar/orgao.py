''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
import utils
import politico

''' Connect to DB '''
#cursor = utils.getCursorConnection()

depara=utils.runCoding()

##################
#    Orga
###########
def addOrgao(sigla,original_cf=None,desc=None,cursor=None):    
    row=None
    if not original_cf:
        row=getOrgaoByOriginal(id=original_cf,cursor=cursor)
    if not row:
        row=getOrgao(sigla=sigla,cursor=cursor)
        
    
    if row is None:
        cursor.execute("INSERT INTO `orgao` (`original_cf`,  `sigla`, `desc`) VALUES (%s,%s,%s)",[original_cf,sigla,desc])
        print "Inserido Orga "            
    else:
        query = "update orgao set `desc` = '"+desc+"',`sigla` = '"+sigla +        "' where original_cf = '"+original_cf+ "';"
        print "Atualizando Orga "+sigla
        cursor.execute(query )
        
    return getOrgaoByOriginal(id=original_cf,cursor=cursor)

def getOrgao(sigla=None,original_cf=None,cursor=None):

    cursor.execute("select id from orgao where sigla = %s",[sigla] )
    rows = cursor.fetchall()
    for row in rows:
        return row    

    return getOrgaoByOriginal(id=original_cf,cursor=cursor)

def getOrgaoByOriginal(id,cursor=None):
    if not id:
        return None
    cursor.execute("select id from orgao where  original_cf = %s",[id] )
    rows = cursor.fetchall()
    for row in rows:
        return row

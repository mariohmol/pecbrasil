''' Import statements '''
import csv, sys, MySQLdb, os
from os import environ
import datetime
import codecs 
from mako.filters import trim
import utils
import partido

##################
#    REPASSE
###########
def addRepasses(processo,candidatura=None,status=None,desc=None):    
    row = getRepasses(processo,candidatura)    
    if row is None:
        cursor.execute("insert into processocandidato (processo,candidatura,status,desc) values (%s,%s,%s,%s,%s)",[processo,candidatura,status,desc])
        print "Inserido processocandidato "            
    else:
        cursor.execute("update processocandidato set desc = '"+desc+"',status = '"+status+"' sigla processo = %s and candidatura = %s",[processo,candidatura] )
    return getRepasses(processo,candidatura)

def getRepasses(processo,candidatura):   
    cursor.execute("select processo,candidatura from processocandidato where processo = %s and candidatura = %s",[processo,candidatura] )
    rows = cursor.fetchall()
    for row in rows:
        return row    
    return None


def runRepasses():         
    csv_reader = utils.openCSV('data/ExpRepasses.csv')
    for line in csv_reader:
        if line[1]:      
            ExpProcessos_processo= line[0]  
            ExpProcessos_candidatura= line[1]  
            ExpProcessos_Status= line[2] 
            ExpProcessos_desc= line[3]  
            
            addProcessos(processo=ExpProcessos_processo,candidatura=ExpProcessos_candidatura,desc=ExpProcessos_desc,status=ExpProcessos_Status)







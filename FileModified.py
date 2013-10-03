#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Description: Script to check if exists one file and ctime
#  usage: scritp.py file [-m minutes -h hours -d days]
#
# Con valor "old" dara critico cuando el mtime sea más viejo del valor de rango(cw)
# con valor "new" dara critico si el mtime es menor a los parametros de rango 

import os
import sys
import time
from string import lower
from optparse import OptionParser
from sys import exit
scriptname = sys.argv[0]

#NAGIOS VALUES:
OK = 0
WARN = 1
CRIT = 2
UKN = 3


def help():
    print """
    Usage: %s -p path/file [ [-t old | new] -c critical -w warning ]
    
    Example:  %s /var/log/messages -m -t old -c 10 -w 7
           If the mtime is older than 7 minutes, return Warning.
           If mtime is older than 10 minutes, return critical.
           
           %s /var/log/messages 
           If file exists return OK
           If file not exists return critical
    """   % (scriptname,scriptname,scriptname)
def ficheroexiste(pathfile):
    return os.path.exists(pathfile)
def mtime(filename):
    return os.stat(filename).st_mtime
def timeolder(timesec):
    x = time.mktime(time.localtime()) - timesec
    return x
parser = OptionParser()
usage = ""

parser.add_option("-p", "--path",type="string", 
                   help="Path of the file.", dest="file")
                   
parser.add_option("-t","--type", type="string", 
                  help="Type of evaluation.{old | new}",dest="type")
                  
parser.add_option("-w", "--warning", type="int", 
                  help="integer - minutes", dest="warning_value") 

parser.add_option("-c","--critical", type="int", 
                  help="integer - minutes", dest="critical_value")
                                    
(options, args) = parser.parse_args()
# CASE 1: Test the existence of 1 file
file = options.file
if options.file and not options.type:
    existe = ficheroexiste(file)
    if existe :
        print "OK: File %s Exists"%file 
        exit(OK)
    else :
        print "CRITICAL: %s NOT FOUND"%file  
        exit(CRIT)
elif not options.file  :
    help()
    exit(UKN)
    
#CASE 2: Test mtime of the file

#check params
if options.type and options.critical_value and options.warning_value :
    # getting "timebreak" values
    warnval = timeolder((options.warning_value * 60))
    critval = timeolder((options.critical_value * 60))
    if lower(options.type) == "old" :
        if mtime(file) <= critval :

            print "CRITICAL: File %s not modified in %d seconds!!"% (file, time.mktime(time.localtime()) - mtime(file))
            
            exit(CRIT)
        if mtime(file) <= warnval :
            print "WARNING: File %s not modified in %d seconds!!"% (file, time.mktime(time.localtime()) - mtime(file))
            exit(WARN)
        else :
            print "OK: File modification time is in tresholds"
            exit(OK)
    elif  lower(options.type) == "new" :
        if not ficheroexiste(file) :
            print "CRITICAL: %s NOT FOUND"%file  
            exit(CRIT)
        
        if mtime(file) >= critval :
            print "CRITICAL: File %s not modified in %d seconds!!"% (file, time.mktime(time.localtime()) - mtime(file))
            exit(CRIT)
        if mtime(file) >= warnval :
            print "WARNING: File %s not modified in %d seconds!!"% (file, time.mktime(time.localtime()) - mtime(file))
            exit(WARN)
        else :
            print "OK: File modification time is in tresholds"
            exit(OK)
    else :   
        print "UKNOWN: type of evaluation not correctly defined"
        exit(UKN)
        
    if not existe :
        print "CRITICAL: %s NOT FOUND"%file  
        exit(CRIT)
else :
    help()
    exit(UKN)

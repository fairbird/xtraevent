# -*- coding: utf-8 -*-
# ------------------- von Python ------------------------------------
import json
import re
import os
import socket
import sys
import requests
import inspect                 # um zu schauen von wem ist die funktion aufgerufen worden
import time
import inspect
# --------------------------- Logfile -------------------------------


from datetime import datetime, timedelta
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraevent_name.log"

## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
############################## File copieren ############################################
# fuer py2 die int und str anweisung raus genommen und das Grad zeichen

###########################  log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus
from Plugins.Extensions.xtraEvent.skins.xtraSkins import *

logstatus = "off"
if config.plugins.xtraEvent.logFiles.value == True:
    logstatus = "on"
else:
    logstatus = "off"

#logstatus = "on"


# ________________________________________________________________________________

def write_log(msg):
    if logstatus == ('on'):
        with open(myfile, "a") as log:

            log.write(datetime.now().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")

            return
    return

# ****************************  test ON/OFF Logfile ************************************************


def logout(data):
    if logstatus == ('on'):
        write_log(data)
        return
    return


# ----------------------------- so muss das commando aussehen , um in den file zu schreiben  ------------------------------
logout(data="start")






REGEX = re.compile(
        r'([\(\[]).*?([\)\]])|'
        r'(: odc.\d+)|'
        r'(\d+: odc.\d+)|'
        r'(\d+ odc.\d+)|(:)|'
        r'( -(.*?).*)|(,)|'
        r'!|'
        r'/.*|'
        r'\|\s[0-9]+\+|'
        r'[0-9]+\+|'
        r'\s\d{4}\Z|'
        r'([\(\[\|].*?[\)\]\|])|'
        r'(\"|\"\.|\"\,|\.)\s.+|'
        r'\"|:|'
        r'Премьера\.\s|'
        r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
        r'(х|Х|м|М|т|Т|д|Д)/с\s|'
        r'\s(с|С)(езон|ерия|-н|-я)\s.+|'
        r'\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
        r'\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
        r'\s(ч|ч\.|с\.|с)\s\d{1,3}.+|'
        r'\d{1,3}(-я|-й|\sс-н).+|', re.DOTALL)

logout(data="parameter ende xxx")



# --------------------------------------------------------------------------------------------------------------------





def eventname(Name):
    logout(data="")
    logout(data="start eventname")
    logout(data=">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> name aus der json in eventname start umwandelen")
    caller_frame = inspect.currentframe().f_back
    caller_name = inspect.getframeinfo(caller_frame).function
    log_message = "Die Funktion getText() wurde von {} aufgerufen.".format(caller_name)
    logout(data=log_message)

    logout(data=Name)
    # hier live: entfernen
    Name = Name.replace('\xc2\x86', '').replace('\xc2\x87', '').replace("live: ", "").replace("LIVE ", "")
    Name = Name.replace("live: ", "").replace("LIVE ", "").replace("LIVE: ", "").replace("live ", "")
    logout(data="name live rausnehmen")
    logout(data=Name)

    # hier versuch name nur vor dem :
    #name1 = Name.split(": ", 1)
    #Name = name1[0]
    #logout(data="name   : abtrennen ")
    #logout(data=Name)

    Name = REGEX.sub('', Name).strip()
    logout(data=Name)

    Name = Name.replace("&", "und")
    Name = Name.replace("ß", "ss")
    Name = Name.lower()
    logout(data=Name)
    logout(data=">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> name aus der json in eventname ende umgewandelt")
    logout(data="")
    return Name  # liefert dem aufruf das zurueck


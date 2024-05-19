# -*- coding: utf-8 -*-
# by digiteng...07.2020 - 08.2020 - 10.2021
# <widget source="Service" render="xtraEmcBackdrop" position="0,0" size="1280,720" zPosition="0"
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, loadJPG
from Components.Sources.ServiceEvent import ServiceEvent
from Components.Sources.CurrentService import CurrentService
from Components.config import config
import os
import re

# --------------------------- Logfile -------------------------------

from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraEmcBackdrop.log"

## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
############################## File copieren ############################################
# fuer py2 die int und str anweisung raus genommen und das Grad zeichen

###########################  log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus

logstatus = "on"


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


try:
    pathLoc = config.plugins.xtraEvent.loc.value
except:
    pathLoc = ""


REGEX = re.compile(
        r'([\(\[]).*?([\)\]])|'
        r'(: odc.\d+)|'
        r'(\d+: odc.\d+)|'
        r'(\d+ odc.\d+)|(:)|'
        
        r'!|'
        r'/.*|'
        r'\|\s[0-9]+\+|'
        r'[0-9]+\+|'
        r'\s\d{4}\Z|'
        r'([\(\[\|].*?[\)\]\|])|'
        r'(\"|\"\.|\"\,|\.)\s.+|'
        r'\"|:|'
        r'\*|'
        r'Премьера\.\s|'
        r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
        r'(х|Х|м|М|т|Т|д|Д)/с\s|'
        r'\s(с|С)(езон|ерия|-н|-я)\s.+|'
        r'\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
        r'\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
        r'\s(ч|ч\.|с\.|с)\s\d{1,3}.+|'
        r'\d{1,3}(-я|-й|\sс-н).+|', re.DOTALL)

class xtraEmcBackdrop(Renderer):

    def __init__(self):
        Renderer.__init__(self)

    GUI_WIDGET = ePixmap
    def changed(self, what):
        if not self.instance:
            return
        else:
            if what[0] != self.CHANGED_CLEAR:
                movieNm = ""
                try:
                    service = self.source.getCurrentService()
                    if service:
                        evnt = service.getPath()
                        movieNm = evnt.split('-')[-1].split(".")[0].strip()
                        movieNm = REGEX.sub('', movieNm).strip()
                        pstrNm = "{}xtraEvent/EMC/{}-backdrop.jpg".format(pathLoc, movieNm.strip())
                        logout(data=str(pstrNm))
                        if os.path.exists(pstrNm):
                            self.instance.setScale(2)
                            self.instance.setPixmap(loadJPG(pstrNm))
                            self.instance.show()
                        else:
                            self.instance.setScale(2)
                            self.instance.setPixmap(loadJPG("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/noMovie.jpg"))
                            self.instance.show()
                    else:
                        self.instance.hide()
                except:
                    pass
            else:
                self.instance.hide()
                return

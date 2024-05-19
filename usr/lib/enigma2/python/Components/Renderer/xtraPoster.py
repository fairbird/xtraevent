# -*- coding: utf-8 -*-
# by digiteng...08.2020 - 11.2021
# <widget source="session.Event_Now" render="xtraPoster" position="0,0" size="185,278" zPosition="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eEPGCache, loadJPG
from Components.config import config
import requests
from requests.utils import quote
import os
import re
import json

# --------------------------- Logfile -------------------------------

from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraPoster.log"

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
if config.plugins.xtraEvent.tmdbAPI.value != "":
    tmdb_api = config.plugins.xtraEvent.tmdbAPI.value
else:
    tmdb_api = "3c3efcf47c3577558812bb9d64019d65"
if config.plugins.xtraEvent.tvdbAPI.value != "":
    tvdb_api = config.plugins.xtraEvent.tvdbAPI.value
else:
    tvdb_api = "a99d487bb3426e5f3a60dea6d3d3c7ef"

try:
    import sys
    PY3 = sys.version_info[0]
    if PY3 == 3:
        from builtins import str
        from builtins import range
        from builtins import object
        from configparser import ConfigParser
        from _thread import start_new_thread
    else:
        from ConfigParser import ConfigParser
        from thread import start_new_thread
except:
    pass

try:
    from Components.Language import language
    lang = language.getLanguage()
    lang = lang[:2]
except:
    try:
        lang = config.osd.language.value[:-3]
    except:
        lang = "en"

lang_path = r"/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/languages"
try:
    lng = ConfigParser()
    if PY3 == 3:
        lng.read(lang_path,  encoding='utf8')
    else:
        lng.read(lang_path)
    lng.get(lang, "0")
except:
    try:
        lang="en"
        lng = ConfigParser()
        if PY3 == 3:
            lng.read(lang_path,  encoding='utf8')
        else:
            lng.read(lang_path)
    except:
        pass

epgcache = eEPGCache.getInstance()
pathLocDown =  "{}xtraEvent/".format(config.plugins.xtraEvent.loc.value)


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

class xtraPoster(Renderer):

    def __init__(self):
        Renderer.__init__(self)

    GUI_WIDGET = ePixmap
    def changed(self, what):
        logout(data="changed")
        if not self.instance:
            return
        else:
            logout(data="changed ist jpg vorhanden")

            
            if what[0] != self.CHANGED_CLEAR:
                evnt = ''
                pstrNm = ''
                evntNm = ''
                try:
                    event = self.source.event
                    logout(data=str(event))
                    if event:
                        logout(data="if event")
                        evnt = event.getEventName()
                        logout(data=str(evnt))
                        evntNm = REGEX.sub('', evnt).strip()
                        logout(data=str(evntNm))
                        pstrNm = "{}xtraEvent/poster/{}.jpg".format(pathLoc, evntNm)
                        logout(data=str(pstrNm))
                        if os.path.exists(pstrNm):
                            logout(data="jpg vorhanden")
                            self.instance.setPixmap(loadJPG(pstrNm))
                            self.instance.setScale(1)
                            self.instance.show()
                            logout(data="changed ende jpg vorhanden ")
                        else:
                            logout(data="jpg nicht vorhanden")
                            pstrNmno = "{}xtraEvent/poster/dummy/{}.jpg".format(pathLoc, evntNm)
                            if os.path.exists(pstrNmno):
                                logout(data="jpg dummy vorhanden")
                                self.instance.setPixmap(loadJPG(pstrNmno))
                                self.instance.setScale(1)
                                self.instance.show()
                                logout(data="changed ende jpg dummy vorhanden ")

                            else:
                                self.instance.hide()
                    else:
                        logout(data="no event")
                        self.instance.hide()
                    return
                except:
                    logout(data="no ")
                    self.instance.hide()
                    return
            else:
                logout(data="nichts changed")
                self.instance.hide()
                return

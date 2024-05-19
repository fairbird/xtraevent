# -*- coding: utf-8 -*-
# by digiteng
# v1 07.2020, 11.2021

# <ePixmap pixmap="xtra/star_b.png" position="560,367" size="200,20" alphatest="blend" zPosition="2" transparent="1" />
# <widget render="xtraStar" source="session.Event_Now" pixmap="xtra/star.png" position="560,367" size="200,20" alphatest="blend" transparent="1" zPosition="3" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from Components.VariableValue import VariableValue
from enigma import eSlider
from Components.config import config
import os
import re
import json

# --------------------------- Logfile -------------------------------

from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraStarEmc.log"

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
    logout(data="start pathloc")
    logout(data=str(pathLoc))
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

class xtraStarEmc(VariableValue, Renderer):
    def __init__(self):
        logout(data="init")
        Renderer.__init__(self)
        VariableValue.__init__(self)
        self.__start = 0
        self.__end = 100

    GUI_WIDGET = eSlider
    def changed(self, what):
        logout(data="changed")
        rtng = 0
        if what[0] == self.CHANGED_CLEAR:
            (self.range, self.value) = ((0, 1), 0)
            return
        try:
            event = ""
            evntNm = ""
            evnt = ""
            event = self.source.event
            if event:
                evnt = event.getEventName()
                logout(data="Eventname-evnt")
                logout(data=str(evnt))
                evntNm = REGEX.sub('', evnt).strip()
                logout(data=str(evntNm))
                logout(data="start pathloc")
                logout(data=str(pathLoc))
                rating_json = "{}xtraEvent/EMC/{}-info.json".format(pathLoc, evntNm)
                logout(data="path json")
                logout(data=str(rating_json))
                if os.path.exists(rating_json):
                    logout(data="json vorhanden")

                    with open(rating_json) as f:
                        logout(data="json vorhanden open file")
                        #rating = json.load(f)['imdbRating']
                        data = json.load(f)
                        #logout(data=str(data))
                        logout(data="json vorhanden open file 1")
                        rating = data['results'][0]['vote_average']
                        logout(data="json vorhanden open file 2")
                        logout(data=str(rating))

                    if rating:
                        logout(data="json wert vorhanden")
                        rtng = int(10*(float(rating)))
                        logout(data=str(rtng))
                    else:
                        logout(data="json wert nicht vorhanden")
                        rtng = 0
                else:
                    logout(data="json nicht vorhanden")

                    rtng = 0
            else:
                rtng = 0
        except:
            pass
        range = 100
        value = rtng

        (self.range, self.value) = ((0, range), value)

    def postWidgetCreate(self, instance):
        logout(data="postWidgetCreate")
        instance.setRange(self.__start, self.__end)

    def setRange(self, range):
        logout(data="setrange")
        (self.__start, self.__end) = range
        if self.instance is not None:
            self.instance.setRange(self.__start, self.__end)

    def getRange(self):
        logout(data="getRange")
        return self.__start, self.__end

    range = property(getRange, setRange)

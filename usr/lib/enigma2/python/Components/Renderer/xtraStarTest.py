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

from Plugins.Extensions.xtraEvent.skins.xtraSkins import *

import inspect



###########################  log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus


# --------------------------- Logfile -------------------------------


from datetime import datetime, timedelta
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

import os
########################### log file loeschen ##################################
dir_path = "/tmp/xtraevent"

try:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print("Verzeichnis wurde erstellt:", dir_path)
    else:
        print("Verzeichnis existiert bereits:", dir_path)
except Exception as e:
    print("Fehler beim Erstellen des Verzeichnisses:", e)




myfile=dir_path + "/starTest.log"
## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
############################## File copieren ############################################
# hier darf keine import zeile rein sonst geht logfile in py2 nicht

###########################  log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus , beide if gehen in py2
logstatus = "off"
#if config.plugins.xtraEvent.logFiles.value == True:
if config.plugins.xtraEvent.logFiles.value:
    logstatus = "on"
else:
    logstatus = "off"

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
        r'\d{1,3}(-я|-й|\sс-н).+|'
        r'\sح\s*\d+|'                # Entfernt Episodennummern in arabischen Serien
        r'\sج\s*\d+|'                # Entfernt Staffelangaben in arabischen Serien
        r'\sم\s*\d+|'                # Entfernt weitere Staffelangaben in arabischen Serien
        r'\d+$'                     # Entfernt Zahlen am Ende
        , re.DOTALL)

# erst 3 mal init schleife 1 dann what 1  die 2 schleife ca 6 mal

class xtraStarTest(VariableValue, Renderer):
    def __init__(self):
        logout(data="----------------------------------------------------------------------------- init")
        #                                                                                                  1   von processWidget aufgerufen.
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        log_message = "Die Funktion getText() wurde von {} aufgerufen.".format(caller_name)
        logout(data=str(log_message))

        Renderer.__init__(self)
        VariableValue.__init__(self)
        self.__start = 0
        self.__end = 100



    GUI_WIDGET = eSlider
    def changed(self, what):
        logout(data="---------------------------------------------------------------------------- changed start")
        #                                                                                              1   von connectUpstream aufgerufe ,  ist what 0
        #                                                                                              2   von __call__ aufgerufen , ist what 1
        logout(data="what")
        logout(data=str(what))
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        log_message = "Die Funktion getText() wurde von {} aufgerufen.".format(caller_name)
        logout(data=str(log_message))

        rtng = 0
        if what[0] == self.CHANGED_CLEAR:
            logout(data=str(what))
            logout(data="---------------------------------------------------------------------  channed_clear")
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
                rating_json = "{}xtraEvent/infossterne/{}.json".format(pathLoc, evntNm)
                rating2_json = "{}xtraEvent/infosomdbsterne/{}.json".format(pathLoc, evntNm)
                logout(data="path json")
                logout(data=str(rating_json))

                logout(data="path json tmdb abfrage")
                if os.path.exists(rating_json):
                    logout(data="json vorhanden tmdb")
                    with open(rating_json) as f:
                        logout(data="json vorhanden open file tmdb")
                        data = json.load(f)
                        logout(data=str(data))
                        logout(data="json vorhanden open file 1 tmdb")
                        #rating = data['results'][0]['vote_average']
                        rating = data['vote_average']
                        logout(data="json vorhanden open file 2 tmdb")
                        logout(data=str(rating))

                    if rating:
                        logout(data="json wert vorhanden")
                        rtng = int(10*(float(rating)))
                        logout(data=str(rtng))


                    else:
                        logout(data="json wert nicht vorhanden")
                        rtng = 0
                else:
                    logout(data="path json tmdb nicht vorhanden")
                    logout(data="path json 2")
                    logout(data=str(rating2_json))
                    if os.path.exists(rating2_json):
                        logout(data="json vorhanden omdb")
                        with open(rating2_json) as f:
                            logout(data="json vorhanden open file")
                            data = json.load(f)
                            logout(data=str(data))
                            logout(data="json vorhanden open file 1")
                            rating = data['vote_average']
                            logout(data="json vorhanden open file 2")
                            logout(data=str(rating))

                        if rating:
                            logout(data="json wert vorhanden")
                            rtng = int(10 * (float(rating)))
                            logout(data=str(rtng))
                        else:
                            logout(data="json wert nicht vorhanden")
                            rtng = 0
                    else:
                        #default_json = "{}xtraEvent/default.json".format(pathLoc)
                        default_json = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/default.json"
                        if os.path.exists(default_json):
                            logout(data="----------------------- json default")
                            with open(default_json) as f:
                                logout(data="json vorhanden open file tmdb")
                                data = json.load(f)
                                logout(data=str(data))
                                logout(data="json vorhanden open file 1 tmdb")
                                # rating = data['results'][0]['vote_average']
                                rating = data['vote_average']
                                logout(data="json vorhanden open file 2 tmdb")
                                logout(data=str(rating))
                            if rating:
                                logout(data="json wert vorhanden")
                                rtng = int(10 * (float(rating)))
                                logout(data=str(rtng))
                            else:
                                logout(data="json wert nicht vorhanden")
                                rtng = 0

                        else:
                            logout(data="json nicht vorhanden omdb")
                            rtng = 0
            else:
                rtng = 0
        except:
            pass
        logout(data="ende")
        range = 100
        value = rtng
        logout(data=str(value))

        (self.range, self.value) = ((0, range), value)

    def postWidgetCreate(self, instance):
        logout(data="----------------------------------------------------------------------- postWidgetCreate")
        #                                                                                                             1  von GUIcreate aufgerufen
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        log_message = "Die Funktion getText() wurde von {} aufgerufen.".format(caller_name)
        logout(data=str(log_message))

        instance.setRange(self.__start, self.__end)

    def setRange(self, range):
        logout(data="----------------------------------------------------------------------- setrange fertig")
        #                                                                                                             1   von changed aufgerufen.
        #                                                                                                             2   von changed aufgerufen.

        logout(data=str(range))
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        log_message = "Die Funktion getText() wurde von {} aufgerufen.".format(caller_name)
        logout(data=str(log_message))

        (self.__start, self.__end) = range
        if self.instance is not None:
            self.instance.setRange(self.__start, self.__end)

    def getRange(self):
        logout(data="------------------------------------------------------------------------ getRange")
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        log_message = "Die Funktion getText() wurde von {} aufgerufen.".format(caller_name)
        logout(data=str(log_message))

        return self.__start, self.__end

    range = property(getRange, setRange)
    logout(data="fertig ende")
    logout(data=str(range))

# -*- coding: utf-8 -*-
# by digiteng...06.2020, 11.2020, 11.2021
from __future__ import absolute_import
from Components.AVSwitch import AVSwitch
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.ActionMap import ActionMap
from enigma import eEPGCache, eTimer, getDesktop, ePixmap, ePoint, eSize, loadJPG, loadPNG
from Components.config import config
from ServiceReference import ServiceReference
from Screens.MessageBox import MessageBox
import Tools.Notifications

from Components.Converter.Converter import Converter
from Components.Element import cached

import requests
from requests.utils import quote
import os
import re
import sys
import json
from PIL import Image
import socket
from . import xtra
from datetime import datetime
import time
import threading
from Components.ProgressBar import ProgressBar
import io
from Plugins.Extensions.xtraEvent.skins.xtraSkins import *

from .xtra import version
import shutil
import inspect
# --------------------------- Logfile -------------------------------


from datetime import datetime, timedelta
from shutil import copyfile
from os import remove
from os.path import isfile

downloadrunning = 0

########################### log file loeschen ##################################

myfile="/tmp/xtraevent-Download.log"

## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
############################## File copieren ############################################
# fuer py2 die int und str anweisung raus genommen und das Grad zeichen

###########################  log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus
logstatus = "off"
if config.plugins.xtraEvent.logFiles.value == True:
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

logout(data=str(config.plugins.xtraEvent.logFiles.value))
# ----------------------------- so muss das commando aussehen , um in den file zu schreiben  ------------------------------
#logout(data="start 6.77")
logout(data=str(version))

#                                    bei 1570 google abfrage einbauen

if config.plugins.xtraEvent.tmdbAPI.value != "":
    tmdb_api = config.plugins.xtraEvent.tmdbAPI.value
else:
    tmdb_api = "3c3efcf47c3577558812bb9d64019d65"
if config.plugins.xtraEvent.tvdbAPI.value != "":
    tvdb_api = config.plugins.xtraEvent.tvdbAPI.value
else:
    tvdb_api = "a99d487bb3426e5f3a60dea6d3d3c7ef"
if config.plugins.xtraEvent.fanartAPI.value != "":
    fanart_api = config.plugins.xtraEvent.fanartAPI.value
else:
    fanart_api = "6d231536dea4318a88cb2520ce89473b"

try:
    import sys
    PY3 = sys.version_info[0]
    if PY3 == 3:
        from builtins import str
        from builtins import range
        from builtins import object
        from configparser import ConfigParser
        from _thread import start_new_thread
        from urllib.parse import quote, urlencode
        from urllib.request import urlopen, Request
        from _thread import start_new_thread


    else:
        from ConfigParser import ConfigParser
        from thread import start_new_thread
        from urllib2 import urlopen, quote
        from thread import start_new_thread
except:
    pass

try:
    from Components.Language import language
    logout(data="language try")
    lang = language.getLanguage()
    lang = lang[:2]
    logout(data=str(lang))
except:
    try:
        lang = config.osd.language.value[:-3]
        logout(data="config.osd")
        logout(data=str(lang))
    except:
        logout(data="default")
        lang = "en"
        logout(data=str(lang))

logout(data="------------------------------------------------- language is -------------------------------------------")
logout(data=str(lang))

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
pathLoc =  "{}xtraEvent/".format(config.plugins.xtraEvent.loc.value)
logout(data="-------------------------------------------------------------- pathLoc ----------------------------------")
logout(data=str(pathLoc))
desktop_size = getDesktop(0).size().width()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
REGEX = re.compile(
    r'([\(\[]).*?([\)\]])|'       # Entfernt Text in Klammern
    r'(: odc.\d+)|'              # Entfernt : odc.x Muster
    r'(\d+: odc.\d+)|'           # Entfernt x: odc.y Muster
    r'(\d+ odc.\d+)|(:)|'        # Entfernt x odc.y oder nur ':'
    r'!|'                        # Entfernt Ausrufezeichen
    r'/.*|'                      # Entfernt alles nach '/'
    r'\|\s[0-9]+\+|'             # Entfernt '| x+' Muster
    r'[0-9]+\+|'                 # Entfernt 'x+' Muster
    r'\s\d{4}\Z|'                # Entfernt Jahresangaben am Ende
    r'([\(\[\|].*?[\)\]\|])|'    # Entfernt Text in verschiedenen Klammern
    r'(\"|\"\.|\"\,|\.)\s.+|'    # Entfernt Text nach Anführungszeichen
    r'\"|:|'                     # Entfernt einfache Anführungszeichen und Doppelpunkte
    r'\*|'                       # Entfernt Sternchen
    r'Премьера\.\s|'             # Entfernt 'Премьера. ' Muster
    r'(х|Х|м|М|т|Т|д|Д)/ф\s|'   # Entfernt kyrillische Muster für Filme
    r'(х|Х|м|М|т|Т|д|Д)/с\s|'   # Entfernt kyrillische Muster für Serien
    r'\s(с|С)(езон|ерия|-н|-я)\s.+|'  # Entfernt Staffel- oder Episodenangaben
    r'\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|' # Entfernt x ч Muster
    r'\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|' # Entfernt '. x ч' Muster
    r'\s(ч|ч\.|с\.|с)\s\d{1,3}.+|' # Entfernt 'ч x' Muster
    r'\d{1,3}(-я|-й|\sс-н).+|'   # Entfernt weitere Staffelangaben
    r'\sح\s*\d+|'                # Entfernt Episodennummern in arabischen Serien
    r'\sج\s*\d+|'                # Entfernt Staffelangaben in arabischen Serien
    r'\sم\s*\d+|'                # Entfernt weitere Staffelangaben in arabischen Serien
    r'\d+$'                      # Entfernt Zahlen am Ende
    , re.DOTALL
)
#  r'[\u0600-\u06FF]+'  # Arabische Schrift

class downloads(Screen):
    logout(data="------------------------------------------------------------------------------- class download screen")
    caller_frame = inspect.currentframe().f_back
    caller_name = inspect.getframeinfo(caller_frame).function
    #log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
    log_message = "Die Funktion getText() wurde von %s aufgerufen." % caller_name
    logout(data=str(log_message))
    # --------------------------------------------------------------------------- wird von module aufgerufen

    def __init__(self, session):
        logout(data="init")
        Screen.__init__(self, session)
        self.session = session
        if desktop_size <= 1280:
            if config.plugins.xtraEvent.skinSelect.value == 'skin_1':
                self.skin = download_720
            if config.plugins.xtraEvent.skinSelect.value == 'skin_2':
                self.skin = download_720_2
        else:
            if config.plugins.xtraEvent.skinSelect.value == 'skin_1':
                self.skin = download_1080
            if config.plugins.xtraEvent.skinSelect.value == 'skin_2':
                self.skin = download_1080_2
        self.titles = ""
        self['status'] = Label()
        self['status2'] = Label()
        self['info'] = Label()
        self['infoposter'] = Label()
        self['infobackdrop'] = Label()
        self['infobanner'] = Label()
        self['infoinfos'] = Label()
        self['infologo'] = Label()
        self['infocasts'] = Label()
        self['downloadcount'] = Label()
        self['info2'] = Label()
        self['Picture'] = Pixmap()
        self['Picture2'] = Pixmap()
        self['int_statu'] = Label()
        self['key_red'] = Label(_('Back'))
        self['key_green'] = Label(_('Download'))
        # self['key_yellow'] = Label(_('Show'))
        self['key_yellow'] = Label(_('Delete All'))
        self['key_1'] = Label(_('Delete Poster             :1'))
        self['key_2'] = Label(_('Delete Backdrop        :2'))
        self['key_3'] = Label(_('Delete Banner            :3'))
        self['key_4'] = Label(_('Delete Infos               :4'))
        self['key_5'] = Label(_('Delete Noinfos           :5'))
        self['key_blue'] = Label(_(lng.get(lang, '66')))
        self['actions'] = ActionMap(['xtraEventAction'],

        {
        'cancel': self.close,
        'red': self.close,
        'ok':self.save,
        'green':self.save,
        # 'yellow':self.ir,
        'yellow': self.deletfilesall,
        '1': self.deletfilesposter,
        '2': self.deletfilesbackdrop,
        '3': self.deletfilesbanner,
        '4': self.deletfilesinfos,
        '5': self.deletfilesnoinfos,
        'blue':self.showhide
        }, -2)
        # ---------------------------- hier anzahl der dateien einbauen anzahl bei 1540 ----------------------------------

        self.countposter = 0
        self['infoposter'].setText(str(self.countposter))
        self.countbackdrop = 0
        self['infobackdrop'].setText(str(self.countbackdrop))
        self.countbanner = 0
        self['infobanner'].setText(str(self.countbanner))
        self.countinfos = 0
        self['infoinfos'].setText(str(self.countinfos))
        self.countlogo = 0
        self['infologo'].setText(str(self.countlogo))
        self.countcasts = 0
        self['infocasts'].setText(str(self.countcasts))
        self.downloadcount = 0
        self['downloadcount'].setText(str(self.downloadcount))
        # -----------------------------------------------------------------------------------------------
        self['progress'] = ProgressBar()
        self['progress'].setRange((0, 100))
        self['progress'].setValue(0)
        self.setTitle(_("░ {}".format(lng.get(lang, '45'))))
        self.screen_hide = False
        # -------------------------------------------------------------------------------------------------
        # ------------------------------------------------------------ hier anzahl files abrufen
        self.anzahlfiles_in_poster()
        self['infoposter'].setText(str(self.countposter))
        self.anzahlfiles_in_backdrop()
        self['infobackdrop'].setText(str(self.countbackdrop))
        self.anzahlfiles_in_banner()
        self['infobanner'].setText(str(self.countbanner))
        self.anzahlfiles_in_infos()
        self['infoinfos'].setText(str(self.countinfos))
        self.anzahlfiles_in_logo()
        self['infologo'].setText(str(self.countlogo))
        self.anzahlfiles_in_casts()
        self['infocasts'].setText(str(self.countcasts))
        # --------------------------------------------------------------------------------------------------
        testver = version
        self.testver = testver
        self["testver"] = Label()
        self["testver"].setText("%s " % (self.testver))
        self.onLayoutFinish.append(self.showFilm)
        self.onLayoutFinish.append(self.intCheck)


    def anzahlfiles_in_poster(self):
        logout(data="anzahl poster ")
        directory = "{}poster".format(pathLoc)
        count = 0
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                count += 1
        self.countposter = count
        logout(data=str(self.countposter))
        self['infoposter'].setText(str(self.countposter))

    def anzahlfiles_in_backdrop(self):
        logout(data="anzahl backdrop")
        directory = "{}backdrop".format(pathLoc)
        count = 0
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                count += 1
        self.countbackdrop = count
        logout(data=str(self.countbackdrop))
        self['infobackdrop'].setText(str(self.countbackdrop))


    def anzahlfiles_in_banner(self):
        logout(data="anzahl banner")
        directory = "{}banner".format(pathLoc)
        count = 0
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                count += 1
        self.countbanner = count
        logout(data=str(self.countbanner))
        self['infobanner'].setText(str(self.countbanner))

    def anzahlfiles_in_infos(self):
        logout(data="anzahl infos")
        directory = "{}infos".format(pathLoc)
        count = 0
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                count += 1
        self.countinfos = count
        logout(data=str(self.countinfos))
        self['infoinfos'].setText(str(self.countinfos))

    def anzahlfiles_in_logo(self):
        logout(data="anzahl logo ")
        directory = "{}logo".format(pathLoc)
        count = 0
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                count += 1
        self.countlogo = count
        logout(data=str(self.countlogo))
        self['infologo'].setText(str(self.countlogo))

    def anzahlfiles_in_casts(self):
        logout(data="anzahl casts ")
        directory = "{}casts".format(pathLoc)
        count = 0
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isdir(filepath):
                count += 1
        self.countcasts = count
        logout(data=str(self.countcasts))
        self['infocasts'].setText(str(self.countcasts))

    def intCheck(self):
        logout(data="intCheck")
        try:
            socket.setdefaulttimeout(2)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            self['int_statu'].setText("☻")
            return True
        except:
            self['int_statu'].hide()
            self['status'].setText(lng.get(lang, '68'))
            return False

    def searchLanguage(self):
        logout(data="searchLanguage")
        try:
            from Components.Language import language
            lang = language.getLanguage()
            lang = lang[:2]
        except:
            try:
                lang = config.osd.language.value[:-3]
            except:
                lang = "en"
        return lang

    def showhide(self):
        logout(data="showhide")
        if self.screen_hide:
            Screen.show(self)
        else:
            Screen.hide(self)
        self.screen_hide = not (self.screen_hide)

    def save(self):
        logout(data="------------------------------ save -------------------------------------------------------------")
        # ---------------------------------------------------------- wird von xtra startDownload augerufen
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        #log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
        log_message = "Die Funktion getText() wurde von %s aufgerufen." % caller_name
        logout(data=str(log_message))

        if config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '14'):
            logout(data="-------------------------- save - gehe zu currentCHEpgs -------------------------------------")
            self.currentChEpgs()
        if config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '13'):
            logout(data="-------------------------- save ende - gehe zu selBouquets ----------------------------------")
            self.selBouquets()

    def deletfilesall(self):
        logout(data="delete Files")
        self.deletfilesposter()
        self.deletfilesbackdrop()
        self.deletfilesbanner()
        self.deletfilesinfos()
        self.deletfilesnoinfos()
        self.deletfileslogo()
        self.deletfilescasts()
        self.deletfilesinfossterne()
        self.deletfilesinfosomdbsterne()
        self.deletfilesinfosomdb()

    def deletfilesposter(self):
        logout(data="deletfilesposter")
        directoryposter = "{}poster".format(pathLoc)
        files = os.listdir(directoryposter)
        for file in files:
            file_path = os.path.join(directoryposter, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_poster()

    def deletfileslogo(self):
        logout(data="deletfileslogo")
        directoryposter = "{}logo".format(pathLoc)
        files = os.listdir(directoryposter)
        for file in files:
            file_path = os.path.join(directoryposter, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_logo()

    def deletfilescasts(self):
        logout(data="deletfilescasts")
        directoryposter = "{}casts".format(pathLoc)
        files = os.listdir(directoryposter)
        for file in files:
            file_path = os.path.join(directoryposter, file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
        self.anzahlfiles_in_casts()

    def deletfilesbackdrop(self):
        logout(data="deletfilesbackdrop")
        directorybackdrop = "{}backdrop".format(pathLoc)
        files = os.listdir(directorybackdrop)
        for file in files:
            file_path = os.path.join(directorybackdrop, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_backdrop()

    def deletfilesbanner(self):
        logout(data="deletfilesbanner")
        directorybanner = "{}banner".format(pathLoc)
        files = os.listdir(directorybanner)
        for file in files:
            file_path = os.path.join(directorybanner, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_banner()

    def deletfilesinfos(self):
        logout(data="deletfilesinfos")
        directoryinfos = "{}infos".format(pathLoc)
        files = os.listdir(directoryinfos)
        for file in files:
            file_path = os.path.join(directoryinfos, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_infos()

    def deletfilesnoinfos(self):
        logout(data="deletfilesinfos")
        directoryinfos = "{}noinfos".format(pathLoc)
        files = os.listdir(directoryinfos)
        for file in files:
            file_path = os.path.join(directoryinfos, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_infos()

    def deletfilesinfosomdb(self):
        logout(data="deletfilesinfosomdb")
        directoryinfos = "{}infosomdb".format(pathLoc)
        files = os.listdir(directoryinfos)
        for file in files:
            file_path = os.path.join(directoryinfos, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_infos()

    def deletfilesinfosomdbsterne(self):
        logout(data="deletfilesinfosomdbsterne")
        directoryinfos = "{}infosomdbsterne".format(pathLoc)
        files = os.listdir(directoryinfos)
        for file in files:
            file_path = os.path.join(directoryinfos, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_infos()

    def deletfilesinfossterne(self):
        logout(data="deletfilesinfossterne")
        directoryinfos = "{}infossterne".format(pathLoc)
        files = os.listdir(directoryinfos)
        for file in files:
            file_path = os.path.join(directoryinfos, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_infos()

    def deletfiles(self):
        logout(data="deletfiles")
        directoryposter = "{}poster".format(pathLoc)
        files = os.listdir(directoryposter)
        for file in files:
            file_path = os.path.join(directoryposter, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        directorybackdrop = "{}backdrop".format(pathLoc)
        files = os.listdir(directorybackdrop)
        for file in files:
            file_path = os.path.join(directorybackdrop, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        directorybanner = "{}banner".format(pathLoc)
        files = os.listdir(directorybanner)
        for file in files:
            file_path = os.path.join(directorybanner, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        directoryinfos = "{}infos".format(pathLoc)
        files = os.listdir(directoryinfos)
        for file in files:
            file_path = os.path.join(directoryinfos, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        directorylogo = "{}logo".format(pathLoc)
        files = os.listdir(directorylogo)
        for file in files:
            file_path = os.path.join(directorylogo, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        directorycasts = "{}casts".format(pathLoc)
        files = os.listdir(directorycasts)
        for file in files:
            file_path = os.path.join(directorycasts, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        directoryinfosomdb = "{}infosomdb".format(pathLoc)
        files = os.listdir(directoryinfosomdb)
        for file in files:
            file_path = os.path.join(directoryinfosomdb, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        directoryinfossterne = "{}infossterne".format(pathLoc)
        files = os.listdir(directoryinfossterne)
        for file in files:
            file_path = os.path.join(directoryinfossterne, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        directoryinfosomdbsterne = "{}infosomdbsterne".format(pathLoc)
        files = os.listdir(directoryinfosomdbsterne)
        for file in files:
            file_path = os.path.join(directoryinfosomdbsterne, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        directoryinfosomdbrated = "{}infosomdbrated".format(pathLoc)
        files = os.listdir(directoryinfosomdbrated)
        for file in files:
            file_path = os.path.join(directoryinfosomdbrated, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_poster()
        self.anzahlfiles_in_backdrop()
        self.anzahlfiles_in_banner()
        self.anzahlfiles_in_infos()
        self.anzahlfiles_in_logo()
        self.anzahlfiles_in_casts()
        logout(data="------------------ def delet")


    def currentChEpgs(self):
        logout(data="currentChEpgs")
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        #log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
        log_message = "Die Funktion getText() wurde von %s aufgerufen." % caller_name
        logout(data=str(log_message))

        events = None
        import NavigationInstance
        ref = NavigationInstance.instance.getCurrentlyPlayingServiceReference().toString()
        events = epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
        if events:
            try:
                n = config.plugins.xtraEvent.searchNUMBER.value
                titles = []
                for i in range(int(n)):
                    try:
                        title = events[i][4]
                        title = REGEX.sub('', title).strip()
                        titles.append(title)
                    except:
                        continue
                    if i == n:
                        break
                self.titles = list(dict.fromkeys(titles))
                start_new_thread(self.downloadEvents, ())
            except Exception as err:
                with open("/tmp/xtraEvent.log", "a+") as f:
                    f.write("currentChEpgs, %s\n"%(err))

    def selBouquets(self):
        logout(data="--------------------------------------------------- selBouquets ---------------------------------")
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        #log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
        log_message = "Die Funktion getText() wurde von %s aufgerufen." % caller_name
        logout(data=str(log_message))

        if os.path.exists("{}bqts".format(pathLoc)):
            logout(data="----------------------------------------------- 641 Bouquets file exits ---------------------")
            with open("{}bqts".format(pathLoc), "r") as f:
                logout(data="selBouquets open file")
                refs = f.readlines()
            nl = len(refs)

            def extract_year_from_text(text):
                """Extrahiert das Jahr aus dem Text (z. B. Beschreibung)."""
                # Regulärer Ausdruck zum Finden eines Jahres im Format 4 Ziffern (z.B. 2020)
                year_match = re.search(r'\b(\d{4})\b', text)
                if year_match:
                    return year_match.group(1)  # Gibt das gefundene Jahr zurück
                return None  # Kein Jahr gefunden

            eventlist=[]
            yearlist = []  # Neue Liste für Jahre
            for i in range(nl):
                ref = refs[i]
                try:
                    events = epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
                    n = config.plugins.xtraEvent.searchNUMBER.value
                    for i in range(int(n)):
                        title = events[i][4]
                        logout(data="----------- Title")
                        logout(data=str(title))
                        #description = events[i][5]  # Beschreibung der Sendung (Short/Extended Description)
                        description = events[i][6]  # Erweiterte Beschreibung der Sendung
                        logout(data="----------- Info")
                        #logout(data=str(description))
                        logout(data="----------------")
                        fd = description
                        fd = fd.replace(',', '').replace('(', '').replace(')', '')
                        fdl = ['\d{4} [A-Z]+', '[A-Z]+ \d{4}', '[A-Z][a-z]+\s\d{4}', '\+\d+\s\d{4}']
                        logout(data=str(fd))
                        for i in fdl:
                            logout(data="Year 685 ")
                            year = re.findall(i, fd)
                            logout(data=str(year))
                            if year:
                                logout(data="Year ok 689")
                                year = re.sub(r'\(.*?\)|\.|\+\d+', ' ', year[0]).strip()
                                logout(data=str(year))
                                year_mit = year
                                # Entferne alles außer der 4-stelligen Jahreszahl
                                year = re.search(r'\b\d{4}\b', year_mit)
                                year = year.group(0)  # Extrahiere die gefundene Jahreszahl
                                logout(data=str(year))
                                break
                        # Jahr extrahieren, falls in der Beschreibung vorhanden
                        #year = extract_year_from_text(description)
                        if not year:  # Falls kein Jahr in der Beschreibung gefunden wird
                            year = 0  # Falls kein Jahr gefunden wird, 0 setzen


                        # Titel bereinigen (z. B. "live" entfernen)
                        name = title.replace('\xc2\x86', '').replace('\xc2\x87', '').replace("live: ", "").replace(
                            "LIVE ", "")
                        name = REGEX.sub('', name).strip()  # Bereinigung des Titels

                        # Eventliste mit Titel und Jahr füllen
                        eventlist.append(name)
                        yearlist.append(year)
                        logout(data="712 ende naechste sendung ")
                except:
                    pass
            self.titles = list(dict.fromkeys(eventlist))
            self.year = [yearlist[eventlist.index(title)] for title in self.titles]  # Jahre entsprechend den Titeln
            logout(data="---------------------------- Title mit Year  ------------------------------")
            logout(data=str(self.titles))
            logout(data=str(self.year))
            logout(data="---------------------------------------------------------------------------")
            #----------------------------------------------- sollte ja thread sein -------------------------
            logout(data="---------------------------- 680 selBouquets zu downloadEvents ------------------------------")
            start_new_thread(self.downloadEvents, ())
            #import _thread
            #_thread.start_new_thread(self.downloadEvents, ())
            logout(data="-----------------------------684  selBouquets von downloadEvents zurueck --------------------")
            # ----------------------------------------------------------------------------------------------
        else:
            logout(data="----------------------------- 687 selBouquets file not exits --------------------------------")

########################################################################################################################
    def downloadEvents(self):
        logout(data="")
        logout(data="------------------------------------------------------------------------------ downloadEvents 691")
        # geht wohl im thread nicht ----------------------------------------------------
        #caller_frame = inspect.currentframe().f_back
        #caller_name = inspect.getframeinfo(caller_frame).function
        #log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
        #logout(data=str(log_message))

        dwnldFile=""
        self.title = ""
        self['progress'].setValue(0)
        lang = None
        now = datetime.now()
        st = now.strftime("%d/%m/%Y %H:%M:%S ")
        tmdb_poster_downloaded = 0
        tvdb_poster_downloaded = 0
        maze_poster_downloaded = 0
        fanart_poster_downloaded = 0
        tmdb_backdrop_downloaded = 0
        tvdb_backdrop_downloaded = 0
        fanart_backdrop_downloaded = 0
        banner_downloaded = 0
        extra_downloaded = 0
        extra2_downloaded = 0
        self.extra3_poster_downloaded = 0
        self.extra3_info_downloaded = 0
        info_downloaded = 0
        self.anzahldownloads = 0
        title_search = 0
        title = ""
        infs = {}
        imdb_id = None
        Year = ""
        Rating=""
        Rated=""
        glist=""
        Duration=""
        description=""
        Type=""

        # ------------------------------------------  hier def delete files einbauen
        logout(data="---------------------------------- 732 zu delete old files bei  1842 --------------------------- ")
        self.delete_oldfilesposter()
        self.delete_oldfilesbackdrop()
        self.delete_oldfilesbanner()
        self.delete_oldfilesinfos()
        self.delete_oldfilesnoinfos()
        self.delete_oldfilesinfosomdb()
        self.delete_oldfilesinfosomdbsterne()
        self.delete_oldfilesinfossterne()
        self.delete_old_dirs_casts()
        logout(data="----------------------------------- 741 zurueck von delete old files ----------------------------")
        logout(data="")
########################################################################################################################
        logout(data="----------------------------------------------------------------------------------------------- 744 abfrage xtraEvent download JA/NEIN")
        if config.plugins.xtraEvent.onoff.value:
            logout(data="------------------------------------------------------------------------------------------- 746 xtraEvent alle downloads ist aktiv ist JA ")
            logout(data="747 abfrage ist xtraEvent3 download JA/NEIN ")
            if config.plugins.xtraEvent.extra3.value == True:
                logout(data="Extra 3 Download ist JA ")
                # elcinema(en) #################################################################

                Type = ""
                Genre = ""
                Language = ""
                Country = ""
                imdbRating = ""
                Rated = ""
                Duration = ""
                Year = ""
                Director = ""
                Writer = ""
                Actors = ""
                Plot = ""
                setime = ""
                try:
                    logout(data="extra3 true1")
                    if not os.path.exists("/tmp/urlo.html"):
                        logout(data="extra3 true1a")
                        url = "https://elcinema.com/en/tvguide/"
                        logout(data="extra3 true1a URL")
                        logout(data=str(url))
                        urlo = requests.get(url)
                        urlo = urlo.text.replace('&#39;', "'").replace('&quot;', '"').replace('&amp;', 'and').replace('(', '').replace(')', '')
                        #logout(data=str(urlo))             # info jede menge
                        with io.open("/tmp/urlo.html", "w", encoding="utf-8") as f:
                            f.write(urlo)
                            logout(data="extra3 true1a URL fertig")
                    if os.path.exists("/tmp/urlo.html"):
                        logout(data="extra3 true 1b")
                        with io.open("/tmp/urlo.html", "r", encoding="utf-8") as f:
                            urlor = f.read()
                            logout(data="extra3 urlor")
                            #logout(data=str(urlor))
                        titles = re.findall('<li><a title="(.*?)" href="/en/work', urlor)
                        #logout(data="extra3 true 1c")
                        logout(data="extra3 true 1c, Anzahl der Titel: " + str(len(titles)))
                    n = len(titles)
                except Exception as err:
                    logout(data="extra3 true 2")
                    with open("/tmp/xtraEvent.log", "a+") as f:
                        f.write("elcinema urlo, %s, %s\n"%(title, err))
                for title in titles:

                    try:
                        logout(data="download try")
                        title = REGEX.sub('', title).strip()
                        logout(data="download try title ")
                        logout(data=str(title))
                        dwnldFile = "{}poster/{}.jpg".format(pathLoc, title)
                        logout(data="download try dwnldFile save poster jpg")
                        logout(data=str(dwnldFile))
                        info_files = "{}infos/{}.json".format(pathLoc, title)
                        logout(data="download try info files save json ")
                        logout(data=str(info_files))
                        tid = re.findall('title="%s" href="/en/work/(.*?)/"'%title, urlor)[0]
                        logout(data="download try tid ist wohl die id aber nur fuers poster kein logo")
                        logout(data=str(tid))
                        self.setTitle(_("{}".format(title)))

                        if not os.path.exists(dwnldFile):
                            logout(data="download poster 370")
                            turl =	"https://elcinema.com/en/work/{}/".format(tid)
                            logout(data=str(turl))
                            jurlo = requests.get(turl.strip(), stream=True, allow_redirects=True, headers=headers)
                            jurlo = jurlo.text.replace('&#39;', "'").replace('&quot;', '"').replace('&amp;', 'and').replace('(', '').replace(')', '')
                            # poster elcinema
                            img = re.findall('<img src="(.*?).jpg" alt=""', jurlo)[0]
                            open(dwnldFile, "wb").write(requests.get("{}.jpg".format(img), stream=True, allow_redirects=True).content)
                            self['info'].setText("► {}, EXTRA3, POSTER".format(title.upper()))
                            self.extra3_poster_downloaded += 1
                            downloaded = self.extra3_poster_downloaded
                            self.prgrs(downloaded, n)
                            self.showPoster(dwnldFile)
                    except Exception as err:
                        with open("/tmp/xtraEvent.log", "a+") as f:
                            f.write("elcinema poster, %s, %s\n"%(title, err))
                    #info elcinema,
                    if not os.path.exists(info_files):
                        logout(data="download json 388")
                        turl =	"https://elcinema.com/en/work/{}/".format(tid)
                        logout(data=str(turl))
                        jurlo = requests.get(turl.strip(), stream=True, allow_redirects=True, headers=headers)
                        jurlo = jurlo.text.replace('&#39;', "'").replace('&quot;', '"').replace('&amp;', 'and').replace('(', '').replace(')', '')
                        try:
                            setime = urlor.partition('title="%s"'%title)[2].partition('</ul>')[0].strip()
                            setime = re.findall("(\d\d\:\d\d) (.*?) - (\d\d\:\d\d) (.*?)</li>", setime)
                            setime = setime[0][0]+setime[0][1]+" - "+setime[0][2]+setime[0][3]
                        except:
                            pass
                        try:
                            Category = jurlo.partition('<li>Category:</li>')[2].partition('</ul>')[0].strip()
                            Category = Category.partition('<li>')[2].partition('</li>')[0].strip()
                        except:
                            pass
                        try:
                            glist=[]
                            Genre = (jurlo.partition('<li>Genre:</li>')[2].partition('</ul>')[0]).strip().split("</a> </li>")
                            for i in range(len(Genre)-1):
                                Genre = (jurlo.partition('<li>Genre:</li>')[2].partition('</ul>')[0]).strip().split("</a> </li>")[i]
                                Genre = Genre.partition('">')[2].strip()
                                glist.append(Genre)
                        except:
                            pass
                        try:
                            llist=[]
                            Language = (jurlo.partition('<li>Language:</li>')[2].partition('</ul>')[0]).strip().split("</a> </li>")
                            for i in range(len(Language)-1):
                                Language = (jurlo.partition('<li>Language:</li>')[2].partition('</ul>')[0]).strip().split("</a> </li>")[i]
                                Language = Language.partition('">')[2].strip()
                                llist.append(Language)
                        except:
                            pass
                        try:
                            clist=[]
                            Country = (jurlo.partition('<li>Country:</li>')[2].partition('</ul>')[0]).strip().split("</a> </li>")
                            for i in range(len(Country)-1):
                                Country = (jurlo.partition('<li>Country:</li>')[2].partition('</ul>')[0]).strip().split("</a> </li>")[i]
                                Country = Country.partition('">')[2].strip()
                                clist.append(Country)
                        except:
                            pass
                        try:
                            Rating = re.findall("class='fa fa-star'></i> (.*?) </span><div", jurlo)[0]
                            Rated = jurlo.partition('<li>MPAA</li><li>')[2].partition('</li></ul></li>')[0].strip()
                            if Rated =="":
                                Rated = jurlo.partition('class="censorship purple" title="Censorship:')[2].partition('"><li>')[0].strip()
                        except:
                            pass
                        try:
                            Year = jurlo.partition('href="/en/index/work/release_year/')[2].partition('/"')[0].strip()
                        except:
                            pass
                        try:
                            Duration = re.findall("<li>(.*?) minutes</li>", jurlo)[0]
                        except:
                            pass
                        try:
                            dlist=[]
                            Director = (jurlo.partition('<li>Director:</li>')[2].partition('</ul>')[0]).strip().split('</a>')
                            for i in range(len(Director)-1):
                                Director = (jurlo.partition('<li>Director:</li>')[2].partition('</ul>')[0]).strip().split('</a>')[i]
                                Director = Director.partition('/">')[2].strip()
                                dlist.append(Director)
                        except:
                            pass
                        try:
                            wlist=[]
                            Writer = (jurlo.partition('<li>Writer:</li>')[2].partition('</ul>')[0]).strip().split('</a>')
                            for i in range(len(Writer)-1):
                                Writer = (jurlo.partition('<li>Writer:</li>')[2].partition('</ul>')[0]).strip().split('</a>')[i]
                                Writer = Writer.partition('/">')[2].strip()
                                wlist.append(Writer)
                        except:
                            pass
                        try:
                            calist=[]
                            Cast = (jurlo.partition('<li>Cast:</li>')[2].partition('</ul>')[0]).strip().split("</a> </li>")
                            for i in range(len(Cast)-1):
                                Cast = (jurlo.partition('<li>Cast:</li>')[2].partition('</ul>')[0]).strip().split("</a> </li>")[i]
                                Cast = Cast.partition('">')[2].strip()
                                calist.append(Cast)
                        except:
                            pass
                        try:
                            Description1 = re.findall("<p>(.*?)<a href='#' id='read-more'>...Read more</a><span class='hide'>", jurlo)[0]
                            Description2 = re.findall("<a href='#' id='read-more'>...Read more</a><span class='hide'>(.*?)\.", jurlo)[0]
                            Description = "{}{}".format(Description1, Description2)
                        except:
                            try:
                                Description = re.findall("<p>(.*?)</p>", jurlo)[0]
                            except:
                                pass
                        try:
                            ej = {
                            "Title": "%s"%title,
                            "Start-End Time": "%s"%setime,
                            "Type": "%s"%Category,
                            "Year": "%s"%Year,
                            "imdbRating": "%s"%Rating,
                            "Rated": "%s"%Rated,
                            "Genre": "%s"%(', '.join(glist)),
                            "Duration": "%s min."%Duration,
                            "Language": "%s"%(', '.join(llist)),
                            "Country": "%s"%(', '.join(clist)),
                            "Director": "%s"%(', '.join(dlist)),
                            "Writer": "%s"%(', '.join(wlist)),
                            "Actors": "%s"%(', '.join(calist)),
                            "Plot": "%s"%Description,
                            }
                            open(info_files, "w").write(json.dumps(ej))

                            if os.path.exists(info_files):
                                self.extra3_info_downloaded += 1
                                downloaded = self.extra3_info_downloaded
                                self.prgrs(downloaded, n)
                                self['info'].setText("► {}, EXTRA3, INFO".format(title.upper()))
                            if os.path.exists(dwnldFile):
                                self.showPoster(dwnldFile)

                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("elcinema ej, %s, %s\n"%(title, err))
                    logout(data=" hier timeout von 1 sec ")
                    time.sleep(1)  # war 5 sec mal neuer versuch
            else:
                logout(data="956 xtraEvent3 download ist NEIN ")

            logout(data="")
########################################################################################################################
            logout(data=" ---------------------------------------------------------------------------------------------- sendungen ,  anzahl und liste der sendungen zum downloaden")
            n = len(self.titles)
            self.anzahldownloads = n
            logout(data=str(n))
            logout(data=" ---------------------------------------------------------------------------------------------- liste der titel zum downloaden")
            logout(data=str(self.titles))  # Hier wird die gesamte Liste self.titles ausgegeben , sind nicht doppelt drin
            # in selBouquets wir : split gemacht und alles zu Live
########################################################################################################################
            downloadrunning = 1
            logout(data=str(downloadrunning))
########################################################################################################################
            logout(data=" ")
            downloadcount=0
            id_nummer_gefunden = 0
            self.id_nummer_gefunden = id_nummer_gefunden
            for i in range(n):
                logout(data=" Title in List und Year")
                title = self.titles[i]
                title = title.strip()
                logout(data=str(title))
                logout(data=" Title")
                self.setTitle(_("{}".format(title)))

                logout(data=" Year")
                year = self.year[i]
                logout(data=" Year2")
                #year_new = year.strip()
                year_new = year.strip() if year else ""
                logout(data=" Year3")
                year = year_new
                logout(data=" Year4")
                logout(data=str(year))
                logout(data=" Year5")
                downloadcount += 1  # Zähler erhöhen
                self.prgrs2(n, downloadcount)
#######################################################  Poster ########################################################
                logout(data="")
                logout(data=" ---------------------------------------------------------------------------------------- 975 abfrage  ist Poster download auf JA/NEIN ")
                logout(data=str(config.plugins.xtraEvent.poster.value))
                if config.plugins.xtraEvent.poster.value == True:
                    logout(data=" Poster download ist JA")
                    dwnldFile = "{}poster/{}.jpg".format(pathLoc, title)
                    logout(data=" Poster download path")
                    logout(data=str(dwnldFile))
                    ####################################################################################################
                    # ----------------------------------------  hier anfang neuer ablauf ----------------------
                    ####################################################################################################
                    logout(data=" Title und Year zum suchen")
                    evntNm=title
                    logout(data=str(evntNm))
                    evntYear=year
                    logout(data=str(evntYear))
                    pstrNm = "{}poster/{}.jpg".format(pathLoc, title) # solange suchen bis er auch poster hat
                    #pstrNm = "{}infos/{}.json".format(pathLoc, title) # mit json kann es sein das keine poster info drin ist , ist null
                    logout(data=" --------------------------------------------------------------------------------------- 1028 abfrage tmdb download neuer ablauf JA/NEIN  ")
                    if config.plugins.xtraEvent.tmdb.value == True:  # abfrage tmdb ja/nein wegen postersize
                        logout(data=" ------------------------------------------------------------------------------------- 1030 zu neue tmdb ablauf bei 2500  ")
                        self.download_tmdb(evntNm, pstrNm, evntYear)
                        logout(data=" -------------------------------------------------------------------------------------- 1032 von neue tmdb ablauf zurueck ")
                        logout(data=" ")
                        logout(data=" ")
                    else:
                        logout(data="994 neuer ablauf off")
                    ########################################################################################################################
                    logout(data="")
                    logout(data=" -------------------------------------------------------------------------------------- 994 abfrage vom TMDB alt download ja/nein ")
                    if config.plugins.xtraEvent.tmdb.value == True:         # abfrage soll von tmdb geholt werden
                        logout(data=" Poster von Tmdb alt download auf JA ")
                        if not os.path.exists(dwnldFile):                   # ist das poster schon vorhanden
                            logout(data="------------------------------- Poster file ist nicht vorhanden also download")



                            # --------------------------------------  suchen json info ---------------------------------------------------------------------------------------------------
                            try:                                            # das poster ist nicht vorhanden
                                srch = "movie"                              # wie gesucht wird , es gibt auch tv und movie
                                #srch = config.plugins.xtraEvent.searchType.value
                                logout(data="------------------------------------- Poster download mit movie 1 versuch")
                                logout(data=str(srch))
                                url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
                                url_tmdbnew=url_tmdb
                                logout(data=" URL 1 title ")
                                logout(data=str(url_tmdb))

                                if config.plugins.xtraEvent.searchLang.value == True:
                                    logout(data=" URL ")
                                    url_tmdb += "&language={}".format(self.searchLanguage())          # nochmal anfragen mir language
                                    url_tmdblng = url_tmdb
                                    logout(data=" URL language")
                                    logout(data=str(url_tmdblng))

                                    # abfrage ist total result 0 keine json vorhanden dann nochmal anfragen
                                    response = requests.get(url_tmdblng)
                                    data = response.json()
                                    total_results = data.get("total_results", 0)
                                else:
                                    response = requests.get(url_tmdbnew)
                                    data = response.json()
                                    total_results = data.get("total_results", 0)

                                # abfrage ist total result 0 keine json vorhanden dann nochmal anfragen

                                if total_results == 0:
                                    logout(data=" json  total results ist 0 keine daten im tv json")
                                    url_tmdb= "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote)
                                    url_tmdblng = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote)
                                    logout(data=" URL 2 ohne title")
                                    logout(data=str(url_tmdb))
                                # ------------------------  check od daten ok sind total resulst muss groesser 0 sein

                                    response = requests.get(url_tmdblng)
                                    data = response.json()
                                    total_results = data.get("total_results", 0)
                                    logout(data=" json total results vom json")
                                    logout(data=str(total_results))


                                    if total_results == 0:
                                        logout(data=" json total results ist 0 keine daten im json")
                                        response = requests.get(url_tmdb)
                                        data = response.json()
                                        total_results = data.get("total_results", 0)
                                        logout(data=" json total results vom json")
                                        logout(data=str(total_results))
                                        if total_results == 0:
                                            logout(data=" json total results ist 0 keine daten im json")
                                    else:
                                        logout(data=" json total results daten im json")


                                    # ------------------------------------------------- wenn mit multi nichts gefunden dann nochmal mit tv suchen -----------------------------------------------
                                    if srch == "multi":
                                        logout(data=" nochmal anfragen mit tv")
                                        srch = "tv"
                                        logout(data="-------------------------------- Poster download mit tv 2 versuch")
                                        logout(data=str(srch))
                                        url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
                                        url_tmdbnew = url_tmdb
                                        logout(data=" URL 1 title ")
                                        logout(data=str(url_tmdb))

                                        if config.plugins.xtraEvent.searchLang.value == True:
                                            logout(data=" URL ")
                                            url_tmdb += "&language={}".format(
                                                self.searchLanguage())  # nochmal anfragen mir language
                                            url_tmdblng = url_tmdb
                                            logout(data=" URL language")
                                            logout(data=str(url_tmdblng))

                                            # abfrage ist total result 0 keine json vorhanden dann nochmal anfragen
                                            response = requests.get(url_tmdblng)
                                            data = response.json()
                                            total_results = data.get("total_results", 0)
                                        else:
                                            response = requests.get(url_tmdbnew)
                                            data = response.json()
                                            total_results = data.get("total_results", 0)

                                        # abfrage ist total result 0 keine json vorhanden dann nochmal anfragen

                                        if total_results == 0:
                                            logout(data=" json  total results ist 0 keine daten im tv json")
                                            url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(
                                                srch, tmdb_api, quote)
                                            url_tmdblng = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(
                                                srch, tmdb_api, quote)
                                            logout(data=" URL 2 ohne title")
                                            logout(data=str(url_tmdb))
                                            # ------------------------  check od daten ok sind total resulst muss groesser 0 sein

                                            response = requests.get(url_tmdblng)
                                            data = response.json()
                                            total_results = data.get("total_results", 0)
                                            logout(data=" json total results vom json")
                                            logout(data=str(total_results))

                                            if total_results == 0:
                                                logout(data=" json total results ist 0 keine daten im json")
                                                response = requests.get(url_tmdb)
                                                data = response.json()
                                                total_results = data.get("total_results", 0)
                                                logout(data=" json total results vom json")
                                                logout(data=str(total_results))
                                                if total_results == 0:
                                                    logout(data=" json total results ist 0 keine daten im json")
                                            else:
                                                logout(data=" json total results daten im json")

                                # -------------------------------------------------------------------------------------------------------------------------------------------

                                else:
                                    # -----------------------   als json datei speichern
                                    response = requests.get(url_tmdb)
                                    if response.status_code == 200:
                                        logout(data=" json json info OK titel und path")
                                        # Dateipfad im temporären Verzeichnis erstellen
                                        #file_path = os.path.join('/tmp', 'poster.json')
                                        logout(data=str(title))
                                        logout(data=str(pathLoc))
                                        file_path = "{}infos/{}.json".format(pathLoc, title)
                                        logout(data=" json path kpl zum schreiben ")
                                        logout(data=str(file_path))

                                        # JSON-Daten speichern
                                        with open(file_path, 'w') as file:
                                            json.dump(response.json(), file)
                                            logout(data=" json geschrieben ")
                                    # --------------------------  file geschrieben wenn auch keine info drin ist -------------------------------
                                    # -------------------------- jetzt poster url suchen  wird aus dem results 0 geholt --------------------------------------------------------
                                    poster = ""
                                    id_nummer = ""

                                    poster = requests.get(url_tmdb).json()['results'][0]['poster_path']
                                    id_nummer = requests.get(url_tmdb).json()['results'][0]['id']
                                    #abfrage logo download , wenn nein id nummer auf None dadurch kein download

                                    logout(data=" poster url aus json holen ")
                                    logout(data=str(poster))
                                    #original_title = requests.get(url_tmdb).json()['results'][0]['poster_path']
                                    #logout(data=str(original_title))
                                    p_size = config.plugins.xtraEvent.TMDBpostersize.value
                                    logout(data=str(p_size))
                                    logout(data=" URL start download poster")
                                    url = "https://image.tmdb.org/t/p/{}{}".format(p_size, poster)
                                    logout(data=str(url))
                                    logout(data=" URL ende download von dieser url poster  ")


                                    if poster != "":
                                        logout(data="------------------------------------------- poster url vorhanden ")
                                        open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                                        #time.sleep (5)
                                    if os.path.exists(dwnldFile):
                                        logout(data="--------------------------- if os.path exist download hochzaehlen")
                                        self['info'].setText("►  {}, TMDB, POSTER".format(title.upper()))
                                        tmdb_poster_downloaded += 1
                                        downloaded = tmdb_poster_downloaded
                                        self.prgrs(downloaded, n)


                                    backdrop = ""
                                    backdrop = requests.get(url_tmdb).json()['results'][0]['backdrop_path']
                                    p_size = 300
                                    logout(data=" URL start download backdrop")
                                    url = "https://image.tmdb.org/t/p/w{}{}".format(p_size, backdrop)
                                    logout(data=str(url))
                                    logout(data=" URL ende download von dieser url backdrop ")

                                    dwnldFile_backdrop = "{}backdrop/{}.jpg".format(pathLoc, title)
                                    logout(data=str(dwnldFile_backdrop))
                                    if backdrop != "":
                                        logout(data="------------------------------------------------ poster vorhanden ")
                                        open(dwnldFile_backdrop, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)


                                    if os.path.exists(dwnldFile):
                                        logout(data="------------------------------------------------ if os.path exist")
                                        self['info'].setText("►  {}, TMDB, POSTER".format(title.upper()))
                                        tmdb_backdrop_downloaded += 1
                                        downloaded = tmdb_backdrop_downloaded
                                        self.prgrs(downloaded, n)



                                    try:
                                        logout(data=" poster try ")
                                        img = Image.open(dwnldFile)
                                        img.verify()
                                    except Exception as err:
                                        with open("/tmp/xtraEvent.log", "a+") as f:
                                            logout(data=" poster deleted xtraEvent file ")
                                            f.write("deleted tmdb poster: %s.jpg\n"%title)
                                        try:
                                            logout(data=" poster remove ")
                                            os.remove(dwnldFile)
                                        except:
                                            pass


                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    f.write("tmdb poster, %s, %s\n"%(title, err))
                        else:
                            logout(data="----------------------------------------------------------------------------------------- 1215 Poster file vorhanden download fertig ")
                    else:
                        logout(data="1284 TMDB ist off")

                    # ---------------------- abfrage if file schon vorhanden ein download reicht ja ---------------------------------------------
                    # tvdb_Poster() ######################## wenn file vorhanden hier nicht mehr noetig #########################################
                    logout(data="")
                    logout(data=" --------------------------------------------------------------------------------------- 1222 abfrage Poster tvdb Download auf ja/nein")
                    if config.plugins.xtraEvent.tvdb.value == True:
                        logout(data=" Poster download tvdb ist JA")
                        try:
                            img = Image.open(dwnldFile)
                            logout(data=" Poster img tvdb")
                            img.verify()
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                logout(data=" Poster tvdb deleted 659")
                                f.write("deleted : %s.jpg\n"%title)
                            try:
                                logout(data=" Poster tvdb remove")
                                os.remove(dwnldFile)
                            except:
                                pass
                        if not os.path.exists(dwnldFile):
                            logout(data="1303 file ist nicht vorhanden")
                            try:
                                logout(data="url 1305")
                                url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(title))
                                logout(data=str(url_tvdb))
                                logout(data="url tvdb")
                                url_read = requests.get(url_tvdb).text
                                series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
                                if series_id:
                                    logout(data="url id")
                                    url_tvdb = "https://thetvdb.com/api/{}/series/{}/{}".format(tvdb_api, series_id, self.searchLanguage())
                                    logout(data=str(url_tvdb))
                                    logout(data="url tvdb")
                                    url_read = requests.get(url_tvdb).text




                                    poster = ""
                                    poster = re.findall('<poster>(.*?)</poster>', url_read)[0]

                                    if poster != '':
                                        logout(data="url artworks ")
                                        url = "https://artworks.thetvdb.com/banners/{}".format(poster)
                                        logout(data=str(url))
                                        logout(data="url ")
                                        if config.plugins.xtraEvent.TVDBpostersize.value == "thumbnail":
                                            url = url.replace(".jpg", "_t.jpg")
                                            logout(data=str(url))
                                        open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                                        if os.path.exists(dwnldFile):
                                            self['info'].setText("►  {}, TVDB, POSTER".format(title.upper()))
                                            tvdb_poster_downloaded += 1
                                            downloaded = tvdb_poster_downloaded
                                            self.prgrs(downloaded, n)
                                            self.showPoster(dwnldFile)
                                            #continue
                                            try:
                                                img = Image.open(dwnldFile)
                                                img.verify()
                                            except Exception as err:
                                                with open("/tmp/xtraEvent.log", "a+") as f:
                                                    f.write("deleted tvdb poster: %s.jpg\n"%title)
                                                try:
                                                    os.remove(dwnldFile)
                                                except:
                                                    pass
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    f.write("tvdb poster, %s, %s\n"%(title, err))
                        logout(data="1353 file ist vorhanden")
                    else:
                        logout(data=" --------------------------------------------------------------------------------------- 1291 Poster tvdb Download ist nein")
                    ##########################################                Maze          ##########################################################
                    logout(data=" --------------------------------------------------------------------------------------- 1293 abfrage Maze Download auf ja/nein")
                    if config.plugins.xtraEvent.maze.value == True:

                        logout(data="maze download ist JA")
                        try:
                            img = Image.open(dwnldFile)
                            img.verify()
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("deleted : %s.jpg\n"%title)
                            try:
                                os.remove(dwnldFile)
                            except:
                                pass
                        if not os.path.exists(dwnldFile):
                            logout(data="file ist nicht vorhanden")
                            url_maze = "http://api.tvmaze.com/search/shows?q={}".format(quote(title))
                            logout(data=str(url_maze))
                            try:
                                url = requests.get(url_maze).json()[0]['show']['image']['medium']
                                logout(data=str(url))
                                open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                                if os.path.exists(dwnldFile):
                                    self['info'].setText("►  {}, MAZE, POSTER".format(title.upper()))
                                    maze_poster_downloaded += 1
                                    downloaded = maze_poster_downloaded
                                    self.prgrs(downloaded, n)
                                    self.showPoster(dwnldFile)
                                    try:
                                        img = Image.open(dwnldFile)
                                        img.verify()
                                    except Exception as err:
                                        with open("/tmp/xtraEvent.log", "a+") as f:
                                            f.write("deleted maze poster: %s.jpg\n"%title)
                                        try:
                                            os.remove(dwnldFile)
                                        except:
                                            pass
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    f.write("maze poster, %s, %s\n"%(title, err))
                        logout(data="file ist vorhanden")
                    logout(data=" --------------------------------------------------------------------------------------- 1335 abfrage maze  Download  ist nein")

                    #############################################  fanart_Poster   #######################################################
                    logout(data=" --------------------------------------------------------------------------------------- 1338 abfrage Fanart Download auf ja/nein")
                    if config.plugins.xtraEvent.fanart.value == True:
                        logout(data="fanart download ist JA")
                        try:
                            img = Image.open(dwnldFile)
                            img.verify()
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("deleted : %s.jpg\n"%title)
                            try:
                                os.remove(dwnldFile)
                            except:
                                pass
                        if not os.path.exists(dwnldFile):
                            logout(data="1416 file ist nicht vorhanden")
                            try:
                                url = None
                                #srch = "multi"
                                srch = config.plugins.xtraEvent.searchType.value
                                logout(data="fanart tmdb 810")
                                url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
                                logout(data=str(url_tmdb))
                                bnnr = requests.get(url_tmdb, verify=False).json()
                                tmdb_id = (bnnr['results'][0]['id'])
                                if tmdb_id:
                                    m_type = (bnnr['results'][0]['media_type'])
                                    if m_type == "movie":
                                        m_type = (bnnr['results'][0]['media_type'])
                                        m_type = "{}+s".format(m_type)
                                    else:
                                        mm_type = m_type
                                    logout(data="fanart maze 822")
                                    url_maze = "http://api.tvmaze.com/singlesearch/shows?q={}".format(quote(title))
                                    logout(data=str(url_maze))
                                    mj = requests.get(url_maze, verify=False).json()
                                    tvdb_id = (mj['externals']['thetvdb'])
                                    if tvdb_id:
                                        logout(data="fanart fanart 828")
                                        url_fanart = "https://webservice.fanart.tv/v3/{}/{}?api_key={}".format(m_type, tvdb_id, fanart_api)
                                        logout(data=str(url_fanart))
                                        fjs = requests.get(url_fanart, verify=False).json()
                                        if fjs:
                                            if m_type == "movies":
                                                mm_type = (bnnr['results'][0]['media_type'])
                                            else:
                                                mm_type = m_type
                                            if mm_type == "tv":
                                                url = fjs['tvposter'][0]['url']
                                            elif mm_type == "movies":
                                                url = fjs['movieposter'][0]['url']
                                            if url:
                                                open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True, verify=False).content)
                                            if os.path.exists(dwnldFile):
                                                self['info'].setText("►  {}, FANART, POSTER".format(title.upper()))
                                                fanart_poster_downloaded += 1
                                                downloaded = fanart_poster_downloaded
                                                self.prgrs(downloaded, n)
                                                self.showPoster(dwnldFile)
                                                try:
                                                    img = Image.open(dwnldFile)
                                                    img.verify()
                                                except Exception as err:
                                                    with open("/tmp/xtraEvent.log", "a+") as f:
                                                        f.write("deleted fanart poster: %s.jpg\n"%title)
                                                    try:
                                                        os.remove(dwnldFile)
                                                    except:
                                                        pass
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    f.write("fanart poster, %s, %s\n"%(title, err))
                        logout(data="1473 file ist vorhanden")
                    else:
                        logout(data="---------------------------------------------------------------------------------------- 1411 abfrage Fanart Download ist nein")
                else:
                    logout(data="---------------------------------------------------------------------------------------- 1413 abfrage Poster Download ist nein")
                    logout(data="")
############################################# backdrop #################################################################
                logout(data="")
                logout(data="---------------------------------------------------------------------------------------- 1417 abfrage ist Backdrop download auf JA/NEIN")
                logout(data=str(config.plugins.xtraEvent.backdrop.value))
                if config.plugins.xtraEvent.backdrop.value == True:
                    logout(data="1478 backdrop downloaden ist JA")
                    dwnldFile = "{}backdrop/{}.jpg".format(pathLoc, title)
                    if config.plugins.xtraEvent.extra.value == True:
                        logout(data="1481 extra downloaden ist ON ")
                        if not os.path.exists(dwnldFile):
                            logout(data="1483 file ist nicht vorhanden")
                            try:
                                logout(data="backdrop extra url ")
                                url = "http://capi.tvmovie.de/v1/broadcasts/search?q={}&page=1&rows=1".format(title.replace(" ", "+"))
                                logout(data=str(url))
                                logout(data="backdrop extra url ")
                                try:
                                    logout(data="url ")
                                    url = requests.get(url).json()['results'][0]['images'][0]['filepath']['android-image-320-180']
                                    logout(data=str(url))
                                    logout(data="url ")
                                except:
                                    pass
                                open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                                if os.path.exists(dwnldFile):
                                    self['info'].setText("►  {}, EXTRA, BACKDROP".format(title.upper()))
                                    extra_downloaded += 1
                                    downloaded = extra_downloaded
                                    self.prgrs(downloaded, n)
                                    self.showBackdrop(dwnldFile)
                                    try:
                                        img = Image.open(dwnldFile)
                                        img.verify()
                                    except Exception as err:
                                        with open("/tmp/xtraEvent.log", "a+") as f:
                                            f.write("deleted extra poster: %s.jpg\n"%title)
                                        try:
                                            os.remove(dwnldFile)
                                        except:
                                            pass
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    f.write("extra, %s, %s\n"%(title, err))
                        logout(data="1516 file ist vorhanden")

                    if config.plugins.xtraEvent.tmdb_backdrop.value == True:
                        logout(data="1518 backdrop tmdb ON")
                        try:
                            img = Image.open(dwnldFile)
                            img.verify()
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("deleted : %s.jpg\n"%title)
                            try:
                                os.remove(dwnldFile)
                            except:
                                pass
                        if not os.path.exists(dwnldFile):
                            logout(data="1530 file ist nicht vorhanden")
                            #srch = "multi"
                            srch = config.plugins.xtraEvent.searchType.value
                            logout(data="url ")
                            url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
                            logout(data="url ")
                            logout(data=str(url_tmdb))
                            if config.plugins.xtraEvent.searchLang.value:
                                logout(data="url ")
                                url_tmdb += "&language={}".format(self.searchLanguage())
                                logout(data="url ")
                                logout(data=str(url_tmdb))
                            try:
                                backdrop = requests.get(url_tmdb).json()['results'][0]['backdrop_path']
                                if backdrop:
                                    backdrop_size = config.plugins.xtraEvent.TMDBbackdropsize.value
                                    # backdrop_size = "w300"
                                    logout(data="url ")
                                    url = "https://image.tmdb.org/t/p/{}{}".format(backdrop_size, backdrop)
                                    logout(data="url ")
                                    logout(data=str(url))
                                    open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                                    if os.path.exists(dwnldFile):
                                        self['info'].setText("►  {}, TMDB, BACKDROP".format(title.upper()))
                                        tmdb_backdrop_downloaded += 1
                                        downloaded = tmdb_backdrop_downloaded
                                        self.prgrs(downloaded, n)
                                        self.showBackdrop(dwnldFile)
                                        try:
                                            img = Image.open(dwnldFile)
                                            img.verify()
                                        except Exception as err:
                                            with open("/tmp/xtraEvent.log", "a+") as f:
                                                f.write("deleted tmdb backdrop: %s.jpg\n"%title)
                                            try:
                                                os.remove(dwnldFile)
                                            except:
                                                pass
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    f.write("tmdb-backdrop, %s, %s\n"%(title, err))
                        logout(data="1571 file ist vorhanden")

                    if config.plugins.xtraEvent.tvdb_backdrop.value == True:
                        logout(data="1518 backdrop tvdb ON")
                        try:
                            img = Image.open(dwnldFile)
                            img.verify()
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("deleted : %s.jpg\n"%title)
                            try:
                                os.remove(dwnldFile)
                            except:
                                pass
                        if not os.path.exists(dwnldFile):
                            logout(data="1585 file nicht vorhanden")
                            try:
                                logout(data="url ")
                                url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(title))
                                logout(data="url ")
                                logout(data=str(url_tvdb))
                                url_read = requests.get(url_tvdb).text
                                series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
                                if series_id:
                                    logout(data="url ")
                                    url_tvdb = "https://thetvdb.com/api/{}/series/{}/{}.xml".format(tvdb_api, series_id, self.searchLanguage())
                                    logout(data="url ")
                                    logout(data=str(url_tvdb))
                                    url_read = requests.get(url_tvdb).text
                                    backdrop = re.findall('<fanart>(.*?)</fanart>', url_read)[0]
                                    if backdrop:
                                        logout(data="url ")
                                        url = "https://artworks.thetvdb.com/banners/{}".format(backdrop)
                                        logout(data="url ")
                                        logout(data=str(url))
                                        if config.plugins.xtraEvent.TVDBbackdropsize.value == "thumbnail":
                                            url = url.replace(".jpg", "_t.jpg")
                                        open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                                        if os.path.exists(dwnldFile):
                                            self['info'].setText("►  {}, TVDB, BACKDROP".format(title.upper()))
                                            tvdb_backdrop_downloaded += 1
                                            downloaded = tvdb_backdrop_downloaded
                                            self.prgrs(downloaded, n)
                                            self.showBackdrop(dwnldFile)
                                            try:
                                                img = Image.open(dwnldFile)
                                                img.verify()
                                            except Exception as err:
                                                with open("/tmp/xtraEvent.log", "a+") as f:
                                                    f.write("deleted tvdb backdrop: %s.jpg\n"%title)
                                                try:
                                                    os.remove(dwnldFile)
                                                except:
                                                    pass
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    f.write("tvdb-backdrop, %s, %s\n"%(title, err))
                        logout(data="1627 file ist vorhanden")

                    if config.plugins.xtraEvent.extra2.value == True:
                        logout(data="1633 download Extra2 ist ON")
                        try:
                            img = Image.open(dwnldFile)
                            img.verify()
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("deleted : %s.jpg\n"%title)
                            try:
                                os.remove(dwnldFile)
                            except:
                                pass
                        if not os.path.exists(dwnldFile):
                            logout(data="1645 file ist nicht vorhanden")
                            try:
                                logout(data="---------------------------------------------------- extra2 download bing")
                                logout(data="url ")
                                url = "https://www.bing.com/images/search?q={}".format(title.replace(" ", "+"))
                                logout(data="url ")
                                logout(data=str(url))
                                if config.plugins.xtraEvent.PB.value == "posters":
                                    logout(data="url ")
                                    url += "+poster"
                                else:
                                    logout(data="url ")
                                    url += "+backdrop"
                                logout(data="url hier ca 500 ms 1000")
                                ff = requests.get(url, stream=True, headers=headers).text
                                logout(data="url ")
                                p = ',&quot;murl&quot;:&quot;(.*?)&'
                                logout(data="url ")
                                url = re.findall(p, ff)[0]
                                logout(data="url ")
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    logout(data="url 1009")
                                    f.write("bing-backdrop, %s, %s\n"%(title, err))
                                try:
                                    logout(data="---------------------------------------------- extra2 download google")
                                    logout(data="url ")
                                    url = "https://www.google.com/search?q={}&tbm=isch&tbs=sbd:0".format(title.replace(" ", "+"))
                                    logout(data="url 1014")
                                    logout(data=str(url))
                                    if config.plugins.xtraEvent.PB.value == "posters":
                                        logout(data="url 1017")
                                        url += "+poster"
                                    else:
                                        logout(data="url ")
                                        url += "+backdrop"
                                    logout(data="url 1022")
                                    ff = requests.get(url, stream=True, headers=headers).text
                                    logout(data="url 1024")
                                    p = re.findall('\],\["https://(.*?)",\d+,\d+]', ff)[0]
                                    logout(data="url 1026")
                                    url = "https://{}".format(p)
                                    logout(data="url 1028")
                                except Exception as err:
                                    with open("/tmp/xtraEvent.log", "a+") as f:
                                        logout(data="google open ")
                                        f.write("google-backdrop, %s, %s\n"%(title, err))
                            try:
                                logout(data="try extra2 ")
                                with open(dwnldFile, 'wb') as f:
                                    f.write(requests.get(url, stream=True, allow_redirects=True).content)
                                if os.path.exists(dwnldFile):
                                    logout(data="try extra2 ")
                                    self['info'].setText("►  {}, EXTRA2, BACKDROP".format(title.upper()))
                                    logout(data="try extra2 ")
                                    extra2_downloaded += 1
                                    downloaded = extra2_downloaded
                                    self.prgrs(downloaded, n)
                                    logout(data="try extra2 ")
                                    self.showBackdrop(dwnldFile)
                                    logout(data="try extra2 ")
                                    try:
                                        img = Image.open(dwnldFile)
                                        logout(data="verivy extra2 ")
                                        img.verify()
                                    except Exception as err:
                                        with open("/tmp/xtraEvent.log", "a+") as f:
                                            logout(data="deleted extra2 ")
                                            f.write("deleted extra2 backdrop: %s.jpg\n"%title)
                                        try:
                                            logout(data="remove extra2 ")
                                            #os.remove(dwnldFile)
                                        except:
                                            pass
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                   f.write("extra2 backdrop, %s, %s\n"%(title, err))
                        logout(data="1722 file ist vorhanden")
                else:
                    logout(data=" --------------------------------------------------------------------------------------- 1665 abfrage Backdrop Download ist nein")
                    logout(data="")
############################################ banner() #################################################################
                logout(data=" --------------------------------------------------------------------------------------- 1668 abfrage Banner Download JA/NEIN")
                logout(data=str(config.plugins.xtraEvent.banner.value))
                if config.plugins.xtraEvent.banner.value == True:
                    logout(data="Banner download ist JA")
                    dwnldFile = "{}banner/{}.jpg".format(pathLoc, title)
                    try:
                        img = Image.open(dwnldFile)
                        img.verify()
                    except Exception as err:
                        with open("/tmp/xtraEvent.log", "a+") as f:
                            f.write("deleted : %s.jpg\n"%title)
                        try:
                            os.remove(dwnldFile)
                        except:
                            pass
                    if config.plugins.xtraEvent.tvdb_banner.value == True:
                        logout(data="Banner tvdb download ist JA")
                        if not os.path.exists(dwnldFile):
                            try:
                                banner_img = ""
                                url = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(title))
                                url = requests.get(url).text
                                banner_img = re.findall('<banner>(.*?)</banner>', url, re.I)[0]
                                if banner_img:
                                    url = "https://artworks.thetvdb.com{}".format(banner_img)
                                    if url:
                                        open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                                        if os.path.exists(dwnldFile):
                                            self['info'].setText("►  {}, TVDB, BANNER".format(title.upper()))
                                            banner_downloaded += 1
                                            downloaded = banner_downloaded
                                            self.prgrs(downloaded, n)
                                            self.showBanner(dwnldFile)
                                            try:
                                                img = Image.open(dwnldFile)
                                                img.verify()
                                            except Exception as err:
                                                with open("/tmp/xtraEvent.log", "a+") as f:
                                                    f.write("deleted extra2 backdrop: %s.jpg\n"%title)
                                                try:
                                                    os.remove(dwnldFile)
                                                except:
                                                    pass
                                            scl = 1
                                            im = Image.open(dwnldFile)
                                            scl = config.plugins.xtraEvent.TVDB_Banner_Size.value
                                            im1 = im.resize((im.size[0] // int(scl), im.size[1] // int(scl)), Image.ANTIALIAS)
                                            im1.save(dwnldFile)
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    f.write("tvdb banner, %s, %s\n"%(title, err))
                    if config.plugins.xtraEvent.fanart_banner.value == True:
                        logout(data="Banner download fanart ist JA")
                        try:
                            img = Image.open(dwnldFile)
                            img.verify()
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("deleted : %s.jpg\n"%title)
                            try:
                                os.remove(dwnldFile)
                            except:
                                pass
                        if not os.path.exists(dwnldFile):
                            try:
                                url = "https://api.themoviedb.org/3/search/multi?api_key={}&query={}".format(tmdb_api, quote(title))
                                jp = requests.get(url, verify=False).json()
                                tmdb_id = (jp['results'][0]['id'])
                                print(tmdb_id)
                                if tmdb_id:
                                    m_type = (jp['results'][0]['media_type'])
                                    if m_type == "movie":
                                        m_type = (jp['results'][0]['media_type'])
                                        m_type = "{}+s".format(m_type)
                                    else:
                                        mm_type = m_type
                                if m_type == "movies":
                                    url = "https://webservice.fanart.tv/v3/{}/{}?api_key={}".format(m_type, tmdb_id, fanart_api)
                                    fjs = requests.get(url, verify=False, timeout=5).json()
                                    url = fjs["moviebanner"][0]["url"]
                                    if url:
                                        open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True, verify=False, timeout=5).content)
                                        if os.path.exists(dwnldFile):
                                            self['info'].setText("►  {}, FANART, BANNER".format(title.upper()))
                                            banner_downloaded += 1
                                            downloaded = banner_downloaded
                                            self.prgrs(downloaded, n)
                                            self.showBanner(dwnldFile)
                                            try:
                                                img = Image.open(dwnldFile)
                                                img.verify()
                                            except Exception as err:
                                                with open("/tmp/xtraEvent.log", "a+") as f:
                                                    f.write("deleted fanart banner: %s.jpg\n"%title)
                                                try:
                                                    os.remove(dwnldFile)
                                                except:
                                                    pass
                                            scl = 1
                                            im = Image.open(dwnldFile)
                                            scl = config.plugins.xtraEvent.FANART_Banner_Size.value
                                            im1 = im.resize((im.size[0] // int(scl), im.size[1] // int(scl)), Image.ANTIALIAS)
                                            im1.save(dwnldFile)
                                else:
                                    try:
                                        url_maze = "http://api.tvmaze.com/singlesearch/shows?q={}".format(quote(title))
                                        mj = requests.get(url_maze, verify=False).json()
                                        tvdb_id = mj['externals']['thetvdb']
                                    except Exception as err:
                                        with open("/tmp/xtraEvent.log", "a+") as f:
                                            f.write("fanart maze banner2, %s, %s\n"%(title, err))
                                    try:
                                        if tvdb_id:
                                            url = "https://webservice.fanart.tv/v3/tv/{}?api_key={}".format(tvdb_id, fanart_api)
                                            fjs = requests.get(url, verify=False, timeout=5).json()
                                            url = fjs["tvbanner"][0]["url"]
                                    except Exception as err:
                                        with open("/tmp/xtraEvent.log", "a+") as f:
                                            f.write("fanart banner3, %s, %s\n"%(title, err))
                                    try:
                                        if url:
                                            open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True, verify=False).content)
                                            if os.path.exists(dwnldFile):
                                                self['info'].setText("►  {}, FANART, BANNER".format(title.upper()))
                                                banner_downloaded += 1
                                                downloaded = banner_downloaded
                                                self.prgrs(downloaded, n)
                                                self.showBanner(dwnldFile)
                                                try:
                                                    img = Image.open(dwnldFile)
                                                    img.verify()
                                                except Exception as err:
                                                    with open("/tmp/xtraEvent.log", "a+") as f:
                                                        f.write("deleted fanart banner: %s.jpg\n"%title)
                                                    try:
                                                        os.remove(dwnldFile)
                                                    except:
                                                        pass
                                                scl = 1
                                                im = Image.open(dwnldFile)
                                                scl = config.plugins.xtraEvent.FANART_Banner_Size.value
                                                im1 = im.resize((im.size[0] // int(scl), im.size[1] // int(scl)), Image.ANTIALIAS)
                                                im1.save(dwnldFile)
                                    except Exception as err:
                                        with open("/tmp/xtraEvent.log", "a+") as f:
                                            f.write("fanart banner4 end, %s, %s\n"%(title, err))
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    f.write("fanart maze banner1, %s, %s\n"%(title, err))
                else:
                    logout(data=" --------------------------------------------------------------------------------------- 1818  abfrage Banner Download ist nein")
                    logout(data="")


################################################ infos #################################################################
                logout(data=" --------------------------------------------------------------------------------------- 1823 abfrage Infos Download ist JA/NEIN")
                logout(data=str(config.plugins.xtraEvent.info.value))
                if config.plugins.xtraEvent.info.value == True:
                    logout(data="download info ist JA")
                    Title=None
                    Type = None
                    Genre = None
                    Language = None
                    Country = None
                    imdbRating = None
                    imdbID = None
                    Rated = None
                    Duration = None
                    Year = None
                    Released=None
                    Director = None
                    Writer = None
                    Actors = None
                    Awards=None
                    Plot = ""
                    Description = None
                    Rating = ""
                    glist=[]
                    data = {}



                    info_files = "{}infosomdb/{}.json".format(pathLoc, title)
                    if config.plugins.xtraEvent.omdbAPI.value:
                        omdb_api_input = config.plugins.xtraEvent.omdbAPI.value
                        logout(data="omdb_apis Eingabe")
                        logout(data=str(omdb_api_input))
                        omdb_apis = [str(omdb_api_input)]
                        logout(data=str(omdb_apis))
                    else:
                        logout(data="omdb_apis default")
                        omdb_apis = ["a8834925", "550a7c40", "8ec53e6b"]                 # kann schnell sein das limit erreicht zum download weil alle nutzen

                    if not os.path.exists(info_files):
                        logout(data=" -----------------  info no json 1184 -----------------------------------")
                        try:
                            try:
                                #srch = "multi"
                                srch = config.plugins.xtraEvent.searchType.value
                                logout(data="url")
                                url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
                                logout(data="url")
                                logout(data=str(url_tmdb))
                                title = requests.get(url_tmdb).json()['results'][0]['original_title']   # ?????? warum
                            except:
                                pass
                            for omdb_api in omdb_apis:                                              # kann schnell sein das limit erreicht zum download weil alle nutzen
                                try:
                                    logout(data="urlstartomdb")
                                    logout(data=str(omdb_apis))
                                    logout(data=str(omdb_api))
                                    url = "http://www.omdbapi.com/?apikey={}&t={}".format(omdb_api, title)
                                    logout(data="url ombd ")
                                    logout(data=str(url))
                                    info_omdb = requests.get(url, timeout=5)
                                    if info_omdb.status_code == 200:
                                        logout(data=" -----------------  omdb json gefunden --------------------------")
                                        Title = info_omdb.json()["Title"]
                                        Year = info_omdb.json()["Year"]
                                        Rated = info_omdb.json()["Rated"]
                                        Duration = info_omdb.json()["Runtime"]
                                        Released = info_omdb.json()["Released"]
                                        logout(data="url variablen ")
                                        Genre = info_omdb.json()["Genre"]
                                        Director = info_omdb.json()["Director"]
                                        Writer = info_omdb.json()["Writer"]
                                        Actors = info_omdb.json()["Actors"]
                                        if not config.plugins.xtraEvent.searchLang.value:
                                            Plot = info_omdb.json()["Plot"]
                                        logout(data="url variablen 2")
                                        Country = info_omdb.json()["Country"]
                                        Awards = info_omdb.json()["Awards"]
                                        imdbRating = info_omdb.json()["imdbRating"]
                                        imdbID = info_omdb.json()["imdbID"]
                                        Type = info_omdb.json()["Type"]
                                        logout(data="url variablen 3")
                                        #                                                      save json datei in infosomdb

                                        # Speichere die JSON-Datei in infosomdb
                                        info_files = "{}infosomdb/{}.json".format(pathLoc, title)
                                        logout(data=str(info_files))
                                        # Stelle sicher, dass der Zielordner existiert
                                        os.makedirs(os.path.dirname(info_files), exist_ok=True)

                                        # Schreibe die Daten in die Ausgabedatei
                                        with open(info_files, "w") as f:
                                            json.dump(info_omdb.json(), f, indent=4)
                                            logout(data="url ombd json schreiben")

                                        if Rated != "N/A":
                                            rated_files = "{}infosomdbrated/{}.json".format(pathLoc, title)
                                            rated_data = {
                                                "Rated": Rated
                                            }
                                            os.makedirs(os.path.dirname(rated_files), exist_ok=True)
                                            with open(rated_files, "w") as f:
                                                json.dump(rated_data, f, indent=4)

                                        if float(imdbRating) > 1.0:
                                            sterne_files = "{}infosomdbsterne/{}.json".format(pathLoc, title)
                                            sterne_data = {
                                                "vote_average": imdbRating
                                            }
                                            os.makedirs(os.path.dirname(sterne_files), exist_ok=True)
                                            with open(sterne_files, "w") as f:
                                                json.dump(sterne_data, f, indent=4)

                                except:
                                    pass
                            logout(data="--------------------------------------------------------------- url imbd 1937")
                            url_find = 'https://m.imdb.com/find?q={}'.format(title)
                            logout(data=str(url_find))
                            ff = requests.get(url_find).text
                            rc = re.compile('<a href="/title/(.*?)/"', re.DOTALL)
                            imdbID = rc.search(ff).group(1)
                            logout(data="url 1159")
                            url= "https://m.imdb.com/title/{}/?ref_=fn_al_tt_0".format(imdbID)
                            logout(data=str(url))
                            ff = requests.get(url).text
                            try:
                                rtng = re.findall('"aggregateRating":{(.*?)}',ff)[0] #ratingValue":8.4
                                imdbRating = rtng.partition('ratingValue":')[2].partition('}')[0].strip()
                                if Rated == None:
                                    Rated = ff.partition('contentRating":"')[2].partition('","')[0].replace("+", "").strip() # "contentRating":"18+","genre":["Crime","Drama","Thriller"],"datePublished":"2019-10-04"
                                glist=[]
                                genre = ff.partition('genre":[')[2].partition('],')[0].strip().split(",")
                                for i in genre:
                                    genre=(i.replace('"',''))
                                    glist.append(genre)
                                if Genre == None:
                                    Genre = ", ".join(glist)
                                if Year == None:
                                    Year = ff.partition('datePublished":"')[2].partition('"')[0].strip()
                                if Type == None:
                                    Type = ff.partition('class="ipc-inline-list__item">')[2].partition('</li>')[0].strip().split(" ")
                                    if Type[0].lower() == "tv":
                                        Type = "Tv Series"
                                    else:
                                        Type = "Movie"
                            except:
                                pass
                            try:
                                if Duration == None:
                                    Duration = re.findall('\d+h \d+min', ff)[0]
                            except:
                                try:
                                    if Duration == None:
                                        Duration = re.findall('\d+min', ff)[0]
                                except:
                                    pass
                            try:
                                if config.plugins.xtraEvent.searchLang.value == True:
                                    #srch = "multi"
                                    srch = config.plugins.xtraEvent.searchType.value
                                    logout(data="url 1198")
                                    url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}&language={}".format(srch, tmdb_api, quote(title), self.searchLanguage())
                                    logout(data=str(url_tmdb))
                                    Plot = requests.get(url_tmdb).json()['results'][0]['overview']
                                    if Plot == "":
                                        logout(data="url 1203")
                                        url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(title)
                                        logout(data=str(url_tvdb))
                                        url_read = requests.get(url_tvdb).text
                                        series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
                                        if series_id:
                                            logout(data="url 1209")
                                            url_tvdb = "https://thetvdb.com/api/{}/series/{}/{}".format(tvdb_api, series_id, self.searchLanguage())
                                            logout(data=str(url_tvdb))
                                            url_read = requests.get(url_tvdb).text
                                            Plot = re.findall('<Overview>(.*?)</Overview>', url_read)[0]
                            except:
                                pass
                            data = {
                            "Title": Title,
                            "Year": Year,
                            "imdbRating": imdbRating,
                            "Rated": Rated,
                            "Released":Released,
                            "Genre": Genre,
                            "Duration": Duration,
                            "Country": Country,
                            "Director": Director,
                            "Writer": Writer,
                            "Actors": Actors,
                            "Awards": Awards,
                            "Type": Type,
                            "Plot": Plot,
                            "imdbID": imdbID,
                            }
                            js = json.dumps(data, ensure_ascii=False)
                            with open(info_files, "w") as f:
                                f.write(js)

                            if os.path.exists(info_files):
                                info_downloaded += 1
                                downloaded = info_downloaded
                                self.prgrs(downloaded, n)
                                self['info'].setText("►  {}, IMDB, INFO".format(title.upper()))
                                #logout(data="info ende")
                            continue
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("infos, %s, %s\n"%(title, err))
                else:
                    logout(data=" --------------------------------------------------------------------------------------- 2032 abfrage Info Download ist nein")
                    logout(data="")

# --------------------------------  report nach dem download ---------------------------------------------------------
            logout(data="")
            logout(data="")
            logout(data="---------------------------------------------------------------------------------------- 2038  report ausgabe ")
            logout(data="idnummergefunden fuer logo und casts , downloadrunning , tmdb poster download")
            logout(data=str(self.id_nummer_gefunden))
            downloadrunning=0
            logout(data=str(downloadrunning))
            logout(data=str(tmdb_poster_downloaded))
            posterdownloads = tmdb_poster_downloaded + tvdb_poster_downloaded + maze_poster_downloaded + fanart_poster_downloaded
            backdropdownloads = tmdb_backdrop_downloaded + tvdb_backdrop_downloaded + fanart_backdrop_downloaded + extra_downloaded + extra2_downloaded
            self.anzahlfiles_in_poster()
            self.anzahlfiles_in_backdrop()
            self.anzahlfiles_in_banner()
            self.anzahlfiles_in_infos()
            self.anzahlfiles_in_logo()
            self.anzahlfiles_in_casts()
            logout(data="zu datetime")
            now = datetime.now()
            logout(data="zurueck datetime")
            extra3_poster_downloaded=self.extra3_poster_downloaded
            extra3_info_downloaded = self.extra3_info_downloaded
            dt = now.strftime("%d/%m/%Y %H:%M:%S")
            report = "\n\nSTART : {}\nEND : {}\
                \n\nDownloads All             :    {}\
                \nDownloads Poster      :    {}\
                \nDownloads Backdrop :    {}\
                \n \
                \nPOSTER; Tmdb :{}, Tvdb :{}, Maze :{}, Fanart :{}\
                \nBACKDROP; Tmdb :{}, Tvdb :{}, Fanart :{}, Extra :{}, Extra2 :{}\
                \nBANNER :{}\
                \nINFOS :{}\
                \nEXTRA3 ; Poster :{}, Info :{}".format(st, dt,
                str(self.anzahldownloads),str(posterdownloads),str(backdropdownloads),
                str(tmdb_poster_downloaded), str(tvdb_poster_downloaded), str(maze_poster_downloaded), str(fanart_poster_downloaded),
                str(tmdb_backdrop_downloaded), str(tvdb_backdrop_downloaded), str(fanart_backdrop_downloaded),
                str(extra_downloaded), str(extra2_downloaded),
                str(banner_downloaded),
                str(info_downloaded),
                str(extra3_poster_downloaded), str(extra3_info_downloaded))

            self['info2'].setText(report)
            self.report = report
            logout(data=" report ")
            try:
                if os.path.exists("/tmp/urlo.html"):
                    os.remove("/tmp/urlo.html")
            except:
                pass
            with open("/tmp/xtra_report", "a+") as f:
                f.write("%s"%report)
            logout(data="report ausgabe ende 1")
            Screen.show(self)
            logout(data="report ausgabe ende 2")
            self.brokenImageRemove()
            logout(data="report ausgabe ende 3")
            self.brokenInfoRemove()
            logout(data="report ausgabe ende 4")
            self.cleanRam()
            return
# ---------------------------------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------------------------------
    def delete_oldfilesposter(self):
        # --------  hier alte files loeschen poster -------------------------
        logout(data="------------------------------------------------ delete old files - poster")
        #logout(data=str(config.plugins.xtraEvent.deletFiles.value))
        # Verzeichnispfad angeben
        if config.plugins.xtraEvent.deletFiles.value == True:
            directory = "{}poster".format(pathLoc)
            logout(data=str(directory))
            # Aktuelles Datum erhalten
            heute = datetime.today().date()
            zwei_tage_ago = heute - timedelta(days=2)
            # Alle Dateien im Verzeichnis durchlaufen
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                logout(data=str(filepath))
                # Überprüfen, ob es sich um eine Datei handelt
                if os.path.isfile(filepath):
                    # Das Änderungsdatum der Datei abrufen
                    mtime = os.path.getmtime(filepath)
                    modified_date = datetime.fromtimestamp(mtime).date()
                    # Überprüfen, ob das Änderungsdatum älter als das aktuelle Datum ist

                    if modified_date < zwei_tage_ago:
                        # Datei löschen
                        os.remove(filepath)
                        logout(data="delete files ende poster")
        else:
            logout(data="delete files off")


    def delete_oldfilesbackdrop(self):
        # --------  hier alte files loeschen backdrop -------------------------
        logout(data="------------------------------------------------ delete old files - backdrop")
        if config.plugins.xtraEvent.deletFiles.value == True:
            # Verzeichnispfad angeben
            directory = "{}backdrop".format(pathLoc)
            logout(data=str(directory))

            # Aktuelles Datum erhalten
            heute = datetime.today().date()
            zwei_tage_ago = heute - timedelta(days=2)
            # Alle Dateien im Verzeichnis durchlaufen
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                logout(data=str(filepath))
                # Überprüfen, ob es sich um eine Datei handelt
                if os.path.isfile(filepath):
                    # Das Änderungsdatum der Datei abrufen
                    mtime = os.path.getmtime(filepath)
                    modified_date = datetime.fromtimestamp(mtime).date()
                    # Überprüfen, ob das Änderungsdatum älter als das aktuelle Datum ist

                    if modified_date < zwei_tage_ago:
                        # Datei löschen
                        os.remove(filepath)
                        logout(data="delete old files ende backdrop")
        else:
            logout(data="delete old files off")

    def delete_oldfilesbanner(self):
        # --------  hier alte files loeschen backdrop -------------------------
        logout(data="--------------------------------------------- delete old files - banner")
        if config.plugins.xtraEvent.deletFiles.value == True:
            # Verzeichnispfad angeben
            directory = "{}banner".format(pathLoc)
            logout(data=str(directory))

            # Aktuelles Datum erhalten
            heute = datetime.today().date()
            zwei_tage_ago = heute - timedelta(days=2)
            # Alle Dateien im Verzeichnis durchlaufen
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                logout(data=str(filepath))
                # Überprüfen, ob es sich um eine Datei handelt
                if os.path.isfile(filepath):
                    # Das Änderungsdatum der Datei abrufen
                    mtime = os.path.getmtime(filepath)
                    modified_date = datetime.fromtimestamp(mtime).date()
                    # Überprüfen, ob das Änderungsdatum älter als das aktuelle Datum ist

                    if modified_date < zwei_tage_ago:
                        # Datei löschen
                        os.remove(filepath)
                        logout(data="delete old files ende banner")

        else:
            logout(data="delete old files off")

    def delete_oldfilesinfos(self):
        # --------  hier alte files loeschen infos json -------------------------
        logout(data="------------------------------------------ delete old files - infos")
        if config.plugins.xtraEvent.deletFiles.value == True:
            # Verzeichnispfad angeben
            directory = "{}infos".format(pathLoc)
            logout(data=str(directory))

            # Aktuelles Datum erhalten
            heute = datetime.today().date()
            zwei_tage_ago = heute - timedelta(days=2)

            # Alle Dateien im Verzeichnis durchlaufen
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                logout(data=str(filepath))
                # Überprüfen, ob es sich um eine Datei handelt
                if os.path.isfile(filepath):
                    # Das Änderungsdatum der Datei abrufen
                    mtime = os.path.getmtime(filepath)
                    modified_date = datetime.fromtimestamp(mtime).date()
                    # Überprüfen, ob das Änderungsdatum älter als das aktuelle Datum ist

                    if modified_date < zwei_tage_ago:
                        # Datei löschen
                        os.remove(filepath)
                        logout(data="delete old files ende infos")

        else:
            logout(data="delete old files off")

    def delete_oldfilesnoinfos(self):
            # --------  hier alte files loeschen infos json -------------------------
            logout(data="------------------------------------------------ delete files start infos")
            if config.plugins.xtraEvent.deletFiles.value == True:
                # Verzeichnispfad angeben
                directory = "{}noinfos".format(pathLoc)
                logout(data=str(directory))

                # Aktuelles Datum erhalten
                heute = datetime.today().date()
                zwei_tage_ago = heute - timedelta(days=2)

                # Alle Dateien im Verzeichnis durchlaufen
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    logout(data=str(filepath))
                    # Überprüfen, ob es sich um eine Datei handelt
                    if os.path.isfile(filepath):
                        # Das Änderungsdatum der Datei abrufen
                        mtime = os.path.getmtime(filepath)
                        modified_date = datetime.fromtimestamp(mtime).date()
                        # Überprüfen, ob das Änderungsdatum älter als das aktuelle Datum ist

                        if modified_date < zwei_tage_ago:
                            # Datei löschen
                            os.remove(filepath)
                            logout(data="delete files ende infos")

            else:
                logout(data="delete files off")

    def delete_oldfilesinfosomdb(self):
        # --------  hier alte files loeschen infos json -------------------------
        logout(data="------------------------------------------ delete old files - infosomdb")
        if config.plugins.xtraEvent.deletFiles.value == True:
            # Verzeichnispfad angeben
            directory = "{}infosomdb".format(pathLoc)
            logout(data=str(directory))

            # Aktuelles Datum erhalten
            heute = datetime.today().date()
            zwei_tage_ago = heute - timedelta(days=2)

            # Alle Dateien im Verzeichnis durchlaufen
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                logout(data=str(filepath))
                # Überprüfen, ob es sich um eine Datei handelt
                if os.path.isfile(filepath):
                    # Das Änderungsdatum der Datei abrufen
                    mtime = os.path.getmtime(filepath)
                    modified_date = datetime.fromtimestamp(mtime).date()
                    # Überprüfen, ob das Änderungsdatum älter als das aktuelle Datum ist

                    if modified_date < zwei_tage_ago:
                        # Datei löschen
                        os.remove(filepath)
                        logout(data="delete old files ende infosomdb")

        else:
            logout(data="delete old files off")

    def delete_oldfilesinfossterne(self):
        # --------  hier alte files loeschen infos json -------------------------
        logout(data="------------------------------------------ delete old files - infossterne")
        if config.plugins.xtraEvent.deletFiles.value == True:
            # Verzeichnispfad angeben
            directory = "{}infossterne".format(pathLoc)
            logout(data=str(directory))

            # Aktuelles Datum erhalten
            heute = datetime.today().date()
            zwei_tage_ago = heute - timedelta(days=2)

            # Alle Dateien im Verzeichnis durchlaufen
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                logout(data=str(filepath))
                # Überprüfen, ob es sich um eine Datei handelt
                if os.path.isfile(filepath):
                    # Das Änderungsdatum der Datei abrufen
                    mtime = os.path.getmtime(filepath)
                    modified_date = datetime.fromtimestamp(mtime).date()
                    # Überprüfen, ob das Änderungsdatum älter als das aktuelle Datum ist

                    if modified_date < zwei_tage_ago:
                        # Datei löschen
                        os.remove(filepath)
                        logout(data="delete old files ende infossterne")

        else:
            logout(data="delete old files off")

    def delete_oldfilesinfosomdbsterne(self):
        # --------  hier alte files loeschen infos json -------------------------
        logout(data="------------------------------------------ delete old files - infosomdbsterne")
        if config.plugins.xtraEvent.deletFiles.value == True:
            # Verzeichnispfad angeben
            directory = "{}infosomdbsterne".format(pathLoc)
            logout(data=str(directory))

            # Aktuelles Datum erhalten
            heute = datetime.today().date()
            zwei_tage_ago = heute - timedelta(days=2)

            # Alle Dateien im Verzeichnis durchlaufen
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                logout(data=str(filepath))
                # Überprüfen, ob es sich um eine Datei handelt
                if os.path.isfile(filepath):
                    # Das Änderungsdatum der Datei abrufen
                    mtime = os.path.getmtime(filepath)
                    modified_date = datetime.fromtimestamp(mtime).date()
                    # Überprüfen, ob das Änderungsdatum älter als das aktuelle Datum ist

                    if modified_date < zwei_tage_ago:
                        # Datei löschen
                        os.remove(filepath)
                        logout(data="delete old files ende infosomdbsterne")

        else:
            logout(data="delete old files off")

    def delete_old_dirs_casts(self):
        # --------  hier alte Directories loeschen backdrop -------------------------
        logout(data="------------------------------------------------ delete old directories - cast")

        if config.plugins.xtraEvent.deletFiles.value:
            # Verzeichnispfad angeben
            directory = "{}casts".format(pathLoc)
            logout(data=str(directory))

            # Aktuelles Datum erhalten
            heute = datetime.today().date()
            zwei_tage_ago = heute - timedelta(days=2)

            # Alle Verzeichnisse im angegebenen Ordner durchlaufen
            for dirname in os.listdir(directory):
                dirpath = os.path.join(directory, dirname)
                logout(data=str(dirpath))

                if os.path.isdir(dirpath):  # Prüfen, ob es ein Verzeichnis ist
                    mtime = os.path.getmtime(dirpath)
                    modified_date = datetime.fromtimestamp(mtime).date()

                    if modified_date < zwei_tage_ago:
                        shutil.rmtree(dirpath)  # Verzeichnis und Inhalt löschen
                        logout(data=f"Deleted old directory: {dirpath}")

        else:
            logout(data="delete old directories off")

#########################################################################################################################################
    def prgrs(self, downloaded, n):
        logout(data="--------------------------------------------------------------------------------------- 2387 def prgrs start")
        self['status'].setText("Download : {} / {}".format(downloaded, n))


    def prgrs2(self, n, downloadcount):
        logout(data="--------------------------------------------------------------------------------------- 2387 def prgrs start")
        downloadzeit = n * 3.0 / 60
        logout(data="downloadzeit dezimal")
        logout(data=str(downloadzeit))
        #downloadzeit = round(downloadzeit, 1)
        #self['status2'].setText("Download : {} / {}      min : {}".format(n, downloadcount, downloadzeit))

        # Berechnung von Minuten und Sekunden
        minuten = int(downloadzeit)  # Ganze Minuten
        sekunden = int((downloadzeit % 1) * 60)  # Sekunden aus dem Dezimalrest
        logout(data=str(minuten))
        logout(data=str(sekunden))

        # Text in Minuten:Sekunden-Format oder als Dezimalminuten
        zeit_dezimal = round(downloadzeit, 1)
        zeit_format = "{}:{:02d}".format(minuten, sekunden)

        # Update des Status-Textes
        self['status2'].setText("Download : {} / {}      min : {} ".format(n, downloadcount, zeit_format))


        self['progress'].setValue(int(100 * downloadcount // n))


    def showPoster(self, dwnldFile):
        logout(data="-------------------------------------------------------------------------------------- 2392 def showPoster start")
        if config.plugins.xtraEvent.onoff.value:
            if not config.plugins.xtraEvent.timerMod.value:
                self["Picture2"].hide()
                self["Picture"].setPixmap(loadJPG(dwnldFile))
                self["Picture"].setScale(1)
                self["Picture"].show()
                if desktop_size <= 1280:
                    self["Picture"].resize(eSize(185,278))
                    self["Picture"].move(ePoint(955,235))
                    self["Picture"].setScale(1)
                else:
                    self["Picture"].setScale(1)
                    self["Picture"].resize(eSize(185,278))
                    self["Picture"].move(ePoint(1450,400))

    def showBackdrop(self, dwnldFile):
        logout(data="---------------------------------------------------------------------------------------- 2409 def showBackdrop start")
        if config.plugins.xtraEvent.onoff.value:
            if not config.plugins.xtraEvent.timerMod.value:
                self["Picture2"].hide()
                self["Picture"].setPixmap(loadJPG(dwnldFile))
                if desktop_size <= 1280:
                    self["Picture"].resize(eSize(300,170))
                    self["Picture"].move(ePoint(895,280))
                    self["Picture"].setScale(1)
                else:
                    self["Picture"].setScale(1)
                    self["Picture"].resize(eSize(300,170))
                    self["Picture"].move(ePoint(1400,400))

    def showBanner(self, dwnldFile):
        logout(data="----------------------------------------------------------------------------------------- 2424 def showBanner start")
        if config.plugins.xtraEvent.onoff.value:
            if not config.plugins.xtraEvent.timerMod.value:
                self["Picture2"].hide()
                self["Picture"].setPixmap(loadJPG(dwnldFile))
                if desktop_size <= 1280:
                    self["Picture"].resize(eSize(400,80))
                    self["Picture"].move(ePoint(845,320))
                    self["Picture"].setScale(1)
                    self["Picture"].setZPosition(10)
                else:
                    self["Picture"].setScale(1)
                    self["Picture"].resize(eSize(400,90))
                    self["Picture"].move(ePoint(1400,400))

    def showFilm(self):
        logout(data="------------------------------------------------------------------------------------------------------- def showFilm start")
        self["Picture2"].instance.setPixmapFromFile("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film2.png")
        self["Picture2"].instance.setScale(1)
        self["Picture2"].show()

    def brokenImageRemove(self):
        logout(data="------------------------------------------------------------------------------------------------------- def brokenImageRemove start")
        b = os.listdir(pathLoc)
        rmvd = 0
        try:
            for i in b:
                bb = "{}{}/".format(pathLoc, i)
                fc = os.path.isdir(bb)
                if fc != False:
                    for f in os.listdir(bb):
                        if f.endswith('.jpg'):
                            try:
                                img = Image.open("{}{}".format(bb, f))
                                img.verify()
                            except:
                                try:
                                    os.remove("{}{}".format(bb, f))
                                    rmvd += 1
                                except:
                                    pass
        except:
            pass

    def brokenInfoRemove(self):
        logout(data="------------------------------------------------------------------------------------------------------- def brokenInfoRemove start")
        try:
            infs = os.listdir("{}infos".format(pathLoc))
            for i in infs:
                with open("{}infos/{}".format(pathLoc, i)) as f:
                    rj = json.load(f)
                if rj["Response"] == "False":
                    os.remove("{}infos/{}".format(pathLoc, i))
        except:
            pass

    def cleanRam(self):
        logout(data="------------------------------------------------------------------------------------------------------- def cleanRam")
        os.system("echo 1 > /proc/sys/vm/drop_caches")
        os.system("echo 2 > /proc/sys/vm/drop_caches")
        os.system("echo 3 > /proc/sys/vm/drop_caches")


    def savePoster(self, dwn_path, url):
        
        logout(data="")
        logout(data="")
        logout(data="------------------------------------------------------------------------------------------------------- def saveposter start")
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        #log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
        log_message = "Die Funktion getText() wurde von %s aufgerufen." % caller_name
        logout(data=log_message)
        logout(data="save poster - open file")
        logout(data=str(dwn_path))
        logout(data=str(url))

        with open(dwn_path, 'wb') as f:
            logout(data="with open")
            f.write(urlopen(url).read())
            logout(data="write ")
            # Überprüfe, ob das Schreiben abgeschlossen ist
            f.flush()
            f.close()
            # Überprüfe die Dateigröße
            file_size = os.path.getsize(dwn_path)
            if file_size == 0:
                # Lösche die Datei, wenn sie 0 Byte groß ist
                os.remove(dwn_path)
                logout(data="wurde geloescht, da sie 0 Byte war.")
            else:
                logout(data="Datei wurde erfolgreich gespeichert ")
        logout(data="-------------------------------------------------------------------------------------------------------  def saveposter ende")
        logout(data="")
        return

    def showLogo(self, dwnldFile):
        logout(data="------------------------------------------------------------------------------------------------------- def showLogo")
        #if config.plugins.xtraEvent.onoff.value:
        if not config.plugins.xtraEvent.timerMod.value:
            self["Picture2"].hide()
            self["Picture"].setPixmap(loadPNG(dwnldFile))
            if desktop_size <= 1280:
                self["Picture"].resize(eSize(300, 170))
                self["Picture"].move(ePoint(895, 280))
                self["Picture"].setScale(1)
            else:
                self["Picture"].setScale(1)
                self["Picture"].resize(eSize(300, 170))
                self["Picture"].move(ePoint(1400, 400))


#########################################################################################################################################


    def download_tmdb(self, evntNm, pstrNm, evntYear):
        logout(data="")
        logout(data="")
        logout(data=" 2554 ------------------------------------------------- def download tmdb  ablauf start ------------------------------------------- ")
        start_time = time.time()
        logout(data="")
        logout(data=str(evntNm))
        logout(data=str(pstrNm))
        logout(data=str(evntYear))
        self.anfrageohne=0
        logout(data="2560 ***********************************************************************************************************************************")
        logout(data="----------------------------------- Sendungsname :         '{}' ".format(evntNm))
        logout(data="2562 ************************************************************************************************************************************")
        if '-' in evntNm:
            evntNm_orginal = evntNm  # damit man anfragen machen kann ohne untertitle nach dem - , name - xxxxxxx
            logout(data=str(pstrNm))
            anfrageohne = 1  # auf 1 gesetzt das wir beim save dann den evntNm_orginal nehmen
            # hier versuch name nur vor dem -
            name1 = evntNm.split("- ", 1)
            Name = name1[0].strip()
            logout(data="name   - abtrennen ")
            logout(data=Name)
            #Name=evntNm
            evntNm_minus = Name  # jetzt suchen wir nur mit dem vor dem - , wir muessen aber den save mit machen
        else:
            evntNm_minus=evntNm
            evntNm_orginal=evntNm


        lng = '{}'.format(self.searchLanguage())
        logout(data=str(lng))
        download_doch = 0
        if config.plugins.xtraEvent.castsFiles.value != False:
            logout(data="2610 casts ist on download ")
            download_doch = 1
        if config.plugins.xtraEvent.logoFiles.value != False:
            logout(data="2613 logo ist on download ")
            download_doch = 1


        if not os.path.exists(pstrNm) or download_doch == 1:


            logout(data="---------------------------------------------------------------------------------------------- file nicht vorhanden start multi")
            self.multi(evntNm, pstrNm, start_time, lng, evntNm_minus, evntNm_orginal, evntYear)
            if not os.path.exists(pstrNm):
                logout(data="------------------------------------------------------------------------------------------- file nicht vorhanden start movie")
                self.movie(evntNm, pstrNm, start_time, lng, evntYear)
                if not os.path.exists(pstrNm):
                    logout(data="--------------------------------------------------------------------------------------- file nicht vorhanden start tv")
                    self.tv(evntNm, pstrNm, start_time, lng, evntYear)
                    if not os.path.exists(pstrNm):
                        logout(data="****************** download_tmdb - vom download zurueck keine json gefunden *******************")
                        logout(data="")




                        return
                    else:
                        logout(data="*************************************************** download_tmdb tv - ist vorhanden *******************")
                        return
                else:
                    logout(data="******************************************************* download_tmdb movie - ist vorhanden *******************")
                    return
            else:
                logout(data="********************************************************* download_tmdb multi - ist vorhanden *******************")
                return
        else:

            return

    def movie(self, evntNm, pstrNm, start_time, lng, evntYear):
        srch = "movie"
        logout(data="")
        logout(data="------------------- movie ------------------ download_tmdb -  gehe zu download , mit srch movie , language")
        logout(data="")
        url_tmdb_lng = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}&language={}".format(srch, tmdb_api, quote(evntNm), lng)
        logout(data=(url_tmdb_lng))
        logout(data="")
        anfrageohne = 0
        evntNm_orginal = evntNm
        self.download_json(evntNm, url_tmdb_lng, start_time, anfrageohne, evntNm_orginal, evntYear)

        if not os.path.exists(pstrNm):
            logout(data="**************** movie ********************************* ist nicht vorhanden von movie ohne language")
            url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(evntNm))
            logout(data=(url_tmdb))
            logout(data="")
            anfrageohne = 0
            evntNm_orginal = evntNm
            self.download_json(evntNm, url_tmdb, start_time, anfrageohne, evntNm_orginal, evntYear)

            logout(data="-------------------------------------------------------------------------------------------------------  download_tmdb - vom download movie zurück")


        if os.path.exists(pstrNm):
            logout(data="*************** movie ************************************************************** ist vorhanden von movie")

        # --------------------------------- hier url download einbauen und url uebergeben

    def tv(self, evntNm, pstrNm, start_time, lng, evntYear):
        srch = "tv"
        logout(data="")
        logout(data="------------------ tv ------------    download_tmdb - Poster nicht vorhanden , gehe zu download , mit srch tv , language")
        url_tmdb_lng = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}&language={}".format(srch, tmdb_api, quote(evntNm), lng)
        logout(data=(url_tmdb_lng))
        logout(data="")
        anfrageohne = 0
        evntNm_orginal = evntNm
        self.download_json(evntNm, url_tmdb_lng, start_time, anfrageohne, evntNm_orginal, evntYear)

        if not os.path.exists(pstrNm):
            logout(data="*************** tv ******************************************************************* ist nicht vorhanden von tv , ohne language")
            logout(data="")
            url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(evntNm))
            logout(data=(url_tmdb))
            logout(data="")
            anfrageohne = 0
            evntNm_orginal = evntNm
            self.download_json(evntNm, url_tmdb, start_time, anfrageohne, evntNm_orginal, evntYear)

            logout(data="--------------------------------------------------------------------------------------------------- download_tmdb - vom download tv zurueck")

        if os.path.exists(pstrNm):
            logout(
                data="download_tmdb Poster *********** tv ************************** ist vorhanden von tv")


    def multi(self, evntNm, pstrNm, start_time, lng, evntNm_minus, evntNm_orginal, evntYear):
        srch = "multi"
        logout(data="")
        logout(data="------------- multi --------------    download_tmdb - Poster nicht vorhanden , gehe zu download , mit srch multi , language")
        url_tmdb_lng = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}&language={}".format(srch, tmdb_api, quote(evntNm), lng)
        logout(data=(url_tmdb_lng))
        logout(data="")
        anfrageohne = 0
        evntNm_orginal = evntNm
        self.download_json(evntNm, url_tmdb_lng, start_time, anfrageohne, evntNm_orginal, evntYear)

        logout(data="**************** multi *************************************************************** ende 1 anfrage mit language")
        logout(data=str(pstrNm))

        if not os.path.exists(pstrNm):
            logout(data="**************** multi *************************************************************** ist nicht vorhanden , neue anfrage ohne language")
            url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(evntNm))
            logout(data=(url_tmdb))
            logout(data="")
            anfrageohne = 0
            evntNm_orginal = evntNm
            self.download_json(evntNm, url_tmdb, start_time, anfrageohne, evntNm_orginal, evntYear)
            logout(data="----------------------------------------------------------------------------------------------- download_tmdb - vom download movie zurueck")

            if os.path.exists(pstrNm):
                logout(data="download_tmdb Poster ************* multi ************** ist vorhanden von multi language")
                logout(data="")

            else:

                logout(data="**************** multi ********************** minus ***************************** ist nicht vorhanden von multi , mit kurzem name mit lng")
                url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}&language={}".format(srch, tmdb_api, quote( evntNm_minus), lng)
                logout(data=(url_tmdb))
                logout(data="")
                anfrageohne = 1
                self.download_json(evntNm_minus, url_tmdb, start_time, anfrageohne, evntNm_orginal, evntYear)
                logout(data="----------------------------------------------------------------------------------------------- download_tmdb - vom download movie zurueck")

                if os.path.exists(pstrNm):
                    logout(data="download_tmdb Poster ************* multi ******* minus ******* ist vorhanden von multi")
                    logout(data="")

                else:
                    logout(data="**************** multi **************** minus *********************************** ist nicht vorhanden von multi , mit kurzem namen ohne language")
                    url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(evntNm_minus))
                    logout(data=(url_tmdb))
                    logout(data="")
                    anfrageohne = 1
                    self.download_json(evntNm_minus, url_tmdb, start_time, anfrageohne, evntNm_orginal, evntYear)
                    logout(data="----------------------------------------------------------------------------------------------- download_tmdb - vom download movie zurueck")

                    if os.path.exists(pstrNm):
                        logout(data="download_tmdb Poster ************* multi ************** ist vorhanden von multi")
                        logout(data="")
                    else:
                        logout(data="download ************* multi ************** json file nicht gefunden zum download")
                        logout(data="")

        logout(data="download_tmdb Poster ************* multi ************** file ist doch vorhanen , kein download")
        logout(data="")

    ########################################################################################################################



    def download_json(self, evntNm, url, start_time, anfrageohne, evntNm_orginal, evntYear):
        logout(data="")
        logout(data=" 2742 -------------------------------------- def download json start ----------------------------------- ")
        logout(data="")
        pathPoster = "{}poster/".format(pathLoc)
        pathBackdrop = "{}backdrop/".format(pathLoc)
        pathLogo = "{}logo/".format(pathLoc)
        pathJsonTmdb = "{}infos/".format(pathLoc)
        pathJsonOmdb = "{}infosomdb/".format(pathLoc)
        pathBanner = "{}banner/".format(pathLoc)

        #postersize = "w185"
        postersize = config.plugins.xtraEvent.TMDBpostersize.value
        #backdropsize = "w300"
        backdropsize = config.plugins.xtraEvent.TMDBbackdropsize.value
        logosize = "300"

        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        #log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
        log_message = "Die Funktion getText() wurde von %s aufgerufen." % caller_name
        logout(data=log_message)

        #if url = "NONE"
        # Anfrage senden und Daten abrufen
        response = requests.get(url)
        data = response.json()

        total_results = data["total_results"]  # Gesamtzahl der Ergebnisse erhalten
        logout(data="download json 2 total results anzahl")
        logout(data=str(total_results))
        json_data = data
        time_url = time.time() - start_time
        #log_time = f" zeit von start bis json download :{time_url} sekunden."
        log_time = " zeit von start bis json download %s sekunden." % time_url
        logout(data=log_time)
        logout(data="")

        if total_results == 0:
            logout(data="Keine Informationen gefunden.")
        else:
            logout(data="2781 Results gefunden")
            match_gefunden = False
            # Neues Attribut für Veröffentlichungsjahr
            release_date = "none"
            #year = 0
            year=evntYear
            # Durch alle Ergebnisse iterieren
            for index, result in enumerate(data.get("results", [])):
                name = "none"
                original_name = "none"
                title = "none"
                original_title = "none"
                release_date = "none"
                release_year = "none"

                # Überprüfung der relevanten Felder
                if "name" in result:
                    name = result["name"]
                    name = self.eventname(name)
                    logout(data="name aus result[{}]: {}".format(index, name))
                else:
                    logout(data="kein name in result.")

                if "original_name" in result:
                    original_name = result["original_name"]
                    original_name = self.eventname(original_name)
                    logout(data="original_name aus result[{}]: {}".format(index, original_name))
                else:
                    logout(data="kein orginal_name in result.")

                if "title" in result:
                    title = result["title"]
                    title = self.eventname(title)
                    logout(data="title aus result[{}]: {}".format(index, title))
                else:
                    logout(data="kein title in result.")

                if "original_title" in result:
                    original_title = result["original_title"]
                    original_title = self.eventname(original_title)
                    logout(data="original_title aus result[{}]: {}".format(index, original_title))
                else:
                    logout(data="kein orginal_title in result.")

                if "release_date" in result and result["release_date"]:
                    # Extrahiere Jahr aus release_date
                    release_date = result["release_date"]
                    release_year = release_date.split("-")[0]  # Nur das Jahr extrahieren
                    logout(data="release_date aus result[{}]: {}".format(index, release_date))
                else:
                    # Fallback, wenn kein release_date vorhanden ist
                    logout(data="release_date fehlt in result[{}], versuche first_air_date.".format(index))

                    # Wenn kein release_date vorhanden ist, überprüfe first_air_date
                    if "first_air_date" in result and result["first_air_date"]:
                        first_air_date = result["first_air_date"]
                        release_year = first_air_date.split("-")[0]  # Extrahiere auch hier das Jahr
                        logout(data="first_air_date aus result[{}]: {}".format(index, first_air_date))
                    else:
                        # Wenn weder release_date noch first_air_date vorhanden sind, setze release_year auf 0
                        release_year = 0
                        logout(data="Kein release_date oder first_air_date gefunden in result[{}], setze release_year auf 0.".format(index))
                        continue  # Überspringe dieses Ergebnis, da kein Jahr vorhanden ist

                # Teile den Sendungsnamen an den Trennzeichen "-" auf
                evntNm_erster_namen = evntNm.split(" - ")
                evntNmkurz = evntNm_erster_namen[0]  # Nimm den ersten Teil als Titel
                logout(data="2848 name von der sendung kurz: {}".format(evntNmkurz))

                # bestimmte namen anpassen
                if evntNm.lower() == "navy cis".lower():
                    evntNmkurz = "ncis"
                    logout(data="2853 bestimmte namen umgewandelt fuer TMDB")
                    logout(data=str(evntNmkurz))
                elif evntNm.lower() == "the legend of the lone ranger".lower():
                    evntNmkurz = "der lone ranger"
                    logout(data="2878 bestimmte namen umgewandelt fuer TMDB")
                    logout(data=str(evntNmkurz))



                # ------------------------------------ Prüfung auf Übereinstimmung -------------------------
                from difflib import SequenceMatcher

                def strings_aehnlich(string1, string2, schwelle=0.8):
                    """Prüft, ob zwei Strings ähnlich sind, basierend auf einem Schwellenwert."""
                    return SequenceMatcher(None, string1.lower(), string2.lower()).ratio() >= schwelle

                def jahr_nahe(release_year, year):
                    """Prüft, ob das Jahr innerhalb von ±2 Jahr liegt."""
                    try:
                        return abs(int(release_year) - int(year)) <= 2
                    except (ValueError, TypeError):
                        return False  # Falls release_year ungültig ist

                # Schwellenwert für die Ähnlichkeit
                testschwelle = 0.8
                logout(data="------------------------------------- was suchen wir ----------------------------------- ")
                logout(data="2897 name sendung und jahr ")
                logout(data=str(evntNm))
                logout(data=str(year))
                logout(data="----------------------------------------------------------------------------------------")

                # Bedingung für Übereinstimmung
                name_match = (
                        evntNm.lower() == name.lower() or
                        evntNm.lower() == original_name.lower() or
                        evntNm.lower() == original_title.lower() or
                        evntNm.lower() == title.lower() or
                        evntNmkurz.lower() == name.lower() or
                        evntNmkurz.lower() == original_name.lower() or
                        evntNmkurz.lower() == title.lower() or
                        evntNmkurz.lower() == original_title.lower() or
                        strings_aehnlich(evntNm, name, testschwelle) or
                        strings_aehnlich(evntNm, original_name, testschwelle) or
                        strings_aehnlich(evntNm, original_title, testschwelle) or
                        strings_aehnlich(evntNm, title, testschwelle) or
                        strings_aehnlich(evntNmkurz, name, testschwelle) or
                        strings_aehnlich(evntNmkurz, original_name, testschwelle) or
                        strings_aehnlich(evntNmkurz, title, testschwelle) or
                        strings_aehnlich(evntNmkurz, original_title, testschwelle)
                )
                logout(data=str(name_match))
                # wenn der name ok ist und nur ein result da ist nehmen wir es , kann sein das das jahr nicht stimmt
                if  total_results == 1:
                    logout(data="name ist richtig aber nur ein result , year auf 0 gesetzt")
                    year = 0


                logout(data="year ist, wenn es 0 ist wird es nicht geprueft , year ist gesetzt es wird name mit year gesucht")
                logout(data=str(year))
                # Überprüfung mit oder ohne Jahr
                if year == 0:  # Keine Jahr-Überprüfung
                    logout(data="year ist 0 , es wird nicht geprueft")
                    if name_match:
                        logout(data="match ist true")
                        match_gefunden = True
                        logout(data="Match gefunden in result[{}] ohne Jahr-Überprüfung.".format(index))
                        self.passendes_result = result
                        break  # Schleife beenden
                else:  # Jahr-Überprüfung aktiv
                    logout(data="2906 year ist xxxx , also wird geprueft")
                    if name_match and release_year is not None and jahr_nahe(release_year, year):
                        match_gefunden = True
                        logout(data="Match gefunden in result[{}] mit Jahr {} (±1 Jahr)".format(index, release_year))
                        self.passendes_result = result
                        break
                    elif name_match:
                        logout(data="Namensübereinstimmung in result[{}], aber Jahr passt nicht.".format(index))
                    else:
                        logout(data="Keine Namensübereinstimmung in result[{}]".format(index))

            if not match_gefunden:
                    logout(data="Kein passender Name mit passendem Jahr (±1 Jahr) in den Ergebnissen gefunden.")
                    return
            else:
                logout(data="")
                logout(data=" 2922 ************************************ name von der sendung ist gleich mit json *****************")
                logout(data="")
                poster_url = ""
                backdrop_url = ""
                id_nummer = ""
                media_type = ""
                id_nummer_found = ""
                logout(data="result nummer")
                logout(data=str(self.passendes_result))
                passendes_result = self.passendes_result  # Speichere das passende Resultat
                logout(data="result nummer")
                logout(data=str(passendes_result))
                if anfrageohne == 1:  # auf 1 gesetzt das wir beim save dann den evntNm_orginal nehmen
                    evntNm = evntNm_orginal
                    logout(
                        data="***************** suche war mit name minus / kurz ,  name von der sendung wieder auf orginal gemacht *****************")
                    logout(data=str(evntNm))

                if passendes_result:
                    logout(data="------------- Passendes Result vorhanden")
                    if "known_for" in passendes_result:
                        logout(
                            data="------------- passendes result vorhanden known_for --------------------------------------")
                        known_for = passendes_result["known_for"]
                        if len(known_for) > 0:
                            item = known_for[0]
                            if "poster_path" in item:
                                poster_url = item["poster_path"]
                                logout(data="------------- known_for poster")
                                logout(data=str(poster_url))
                            if "backdrop_path" in item:
                                backdrop_url = item["backdrop_path"]
                                logout(data="------------- known_for backdrop")
                                logout(data=str(backdrop_url))
                            if "id" in item:
                                id_nummer = item["id"]
                                logout(data="------------- known_for id")
                                logout(data=str(id_nummer))
                            if "media_type" in passendes_result:
                                media_type = passendes_result["media_type"]
                                logout(data="------------- media_type")
                                logout(data=str(media_type))
                    else:
                        logout(
                            data="------------- passendes result vorhanden standard ---------------------------------------")
                        if "poster_path" in passendes_result:
                            poster_url = passendes_result["poster_path"]
                            logout(data="------------- poster")
                            logout(data=str(poster_url))
                        if "backdrop_path" in passendes_result:
                            backdrop_url = passendes_result["backdrop_path"]
                            logout(data="------------- backdrop")
                            logout(data=str(backdrop_url))
                        if "id" in passendes_result:
                            id_nummer = passendes_result["id"]
                            logout(data="------------- id")
                            logout(data=str(id_nummer))
                            id_nummer_found = id_nummer
                        if "vote_average" in passendes_result:
                            vote_average = passendes_result["vote_average"]
                            logout(data="------------- vote_average")
                            logout(data=str(vote_average))
                        if "media_type" in passendes_result:
                            media_type = passendes_result["media_type"]
                            logout(data="------------- media_type")
                            logout(data=str(media_type))



                            if float(vote_average) > 1.0:
                                logout(data="------------- path sterne save")
                                sterne2_files = "{}infossterne/{}.json".format(pathLoc, evntNm)
                                sterne2_path = "{}infossterne".format(pathLoc)
                                logout(data="------------- path json sterne")
                                logout(data=str(sterne2_files))
                                sterne_data = {
                                    "vote_average": vote_average
                                }
                                logout(data=str(sterne_data))
                                #os.makedirs(os.path.dirname(sterne2_files), exist_ok=True)
                                logout(data="------------- path check")
                                logout(data=str(sterne2_path))
                                if not os.path.exists(sterne2_path):
                                    os.makedirs(sterne2_path)
                                    logout(data="------------- path sterne makedir")
                                with open(sterne2_files, "w") as file:
                                    logout(data="------------- path sterne save file")
                                    json.dump(sterne_data, file, indent=4)
                                #f.close()  # Datei schließen
                                logout(data="------------- path sterne close")
                    logout(data="------------- dwn json")
                    # Schreibe den JSON-Inhalt in die Datei
                    dwn_json = pathJsonTmdb + "{}.json".format(evntNm)
                    logout(data="------------- path json save")
                    logout(data=str(dwn_json))

                    with open(dwn_json, "w") as file:
                        json.dump(json_data, file, indent=4)
                        time_nameok = time.time() - start_time
                        #log_time = f" zeit von start bis json geschrieben :{time_nameok} sekunden."
                        log_time = " zeit von start bis json geschrieben %s sekunden." % time_nameok
                        logout(data=log_time)
                        logout(data="")

                else:
                    logout(
                        data="********************************** Name in josn nicht gleich , mann kann es doch nicht nehmen ???")
                    logout(data="")

                    return


                logout(data="****************************** sendungsname save datei ************************************ ")
                logout(data=str(evntNm))
                logout(data="2950 ******************************* save json und sterne , jetzt poster , backdrop download********")

                logout(data="%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% download poster url:")
                if poster_url is not None:
                    if poster_url != "null":
                        logout(data="")
                        # Poster-Pfad gefunden, nicht null
                        logout(data="%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Gefundene poster url:")
                        logout(data=str(poster_url))
                        logout(data=str(postersize))
                        url_poster = "https://image.tmdb.org/t/p/{}{}".format(postersize, poster_url)
                        logout(data=(url_poster))
                        logout(data="poster_path - open file")
                        dwn_poster = pathPoster + "{}.jpg".format(evntNm)
                        logout(data=(dwn_poster))
                        logout(data="poster_path - down poster name file")
                        logout(data="poster_path - zu save ")
                        self.savePoster(dwn_poster, url_poster)
                        logout(data="poster_path - von save zurueck ")

                        time_url = time.time() - start_time
                        #log_time = f" zeit von start bis save poster :{time_url} sekunden."
                        log_time = " zeit von start bis save poster %s sekunden." % time_url
                        logout(data=log_time)
                        logout(data="%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% save Poster ende")
                        logout(data="")
                    else:
                        logout(data="%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Poster-Url: ist Null")
                        #break
                else:
                    logout(data="%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Poster-Url: ist None")
                    #break

                logout(data="<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< download backdrop url:")
                if backdrop_url is not None:
                    if backdrop_url != "null":
                        # backdrop-Pfad gefunden, nicht null
                        logout(data="<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Gefundene backdrop url:")
                        logout(data=str(backdrop_url))
                        logout(data=str(backdropsize))
                        url_poster = "https://image.tmdb.org/t/p/{}{}".format(backdropsize, backdrop_url)
                        logout(data=(url_poster))
                        logout(data="backdrop_path - open file")
                        dwn_poster = pathBackdrop + "{}.jpg".format(evntNm)
                        logout(data=(dwn_poster))
                        logout(data="backdrop_path - down poster name file")
                        logout(data="backdrop_path - zu save ")
                        self.savePoster(dwn_poster, url_poster)
                        logout(data="backdrop_path - von save zurueck")
                        time_url = time.time() - start_time
                        #log_time = f" zeit von start bis save backdrop :{time_url} sekunden."
                        log_time = " zeit von start bis save backdrop %s sekunden." % time_url
                        logout(data=log_time)
                        logout(data="<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< save Backdrop ende")
                        logout(data="")
                    else:
                        logout(data="<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Backdrop-Url: ist null")
                        #break
                else:
                    logout(data="<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Backdrop-Url: ist None")
                    #break
                # break in poster und backdrop aus damit er noch mit der id schaut

                logout(data="3015 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< download logo und cats mit id_nummer:")
                if id_nummer is not None:
                    self.id_nummer_gefunden += 1
                    logout(data=str(config.plugins.xtraEvent.logoFiles.value))
                    logout(data="3018 abfrage download logo:")
                    if config.plugins.xtraEvent.logoFiles.value == False:
                        logout(data="3020 logo ist off kein download ")
                    else:
                        logout(data="3022 zu logo download:")
                        self.download_logo(id_nummer, evntNm_orginal, pathLogo, logosize, start_time, media_type)
                        logout(data="3024 zurueck von logo download:")
                    logout(data="")
                    logout(data="3021 abfrage download casts:")
                    if config.plugins.xtraEvent.castsFiles.value == False:
                        logout(data="3023 casts ist off kein download ")

                    else:
                        logout(data="3031 zu casts download:")
                        self.download_casts(id_nummer, evntNm_orginal, media_type)
                        logout(data="3033 zurueck von casts download:")

                    logout(data="3035 ------------------------------------------------ neuer Ablauf ende -------------------------------- ")
                    return

                else:
                    logout(data="2995 ------------------------------------------------ neuer Ablauf keine ID----------------------------- ")
                    return

    ############################################################# logo casts ################################################################################

    def download_logo(self, id_nummer, evntNm_orginal, pathLogo, logosize, start_time, media_type):
        evntNm=evntNm_orginal
        logout(data=" ------------------------------------------------ abfrage Logo Download 3042 -------------------------------- ")
        logout(data=" id nummer ist ")
        logout(data=str(id_nummer))
        id_nummer_save = id_nummer
        logout(data=" id save nummer  ")
        logout(data=str(id_nummer_save))

        if id_nummer is not None:
            if id_nummer != "null":
                start_time2 = time.time()
                logout(data="")
                # Poster-Pfad gefunden, nicht null
                logout(data="3054 =================================================================================== Gefundene id nummer:")
                logout(data=str(id_nummer))
                url_tmdb = "https://api.themoviedb.org/3/{}/{}/images?api_key={}".format(media_type, id_nummer, tmdb_api)
                logout(data=(url_tmdb))
                # so url - http://api.themoviedb.org/3/movie/672/images?api_key=3c3efcf47c3577558812bb9d64019d65
                # json laden in data
                response = requests.get(url_tmdb)
                data = response.json()
                logout(data="check json daten")
                time_url = time.time() - start_time2
                #log_time = f" zeit id 1:{time_url} sekunden."
                log_time = " zeit id 1 %s sekunden." % time_url
                logout(data=log_time)
                if "id" in data and data["id"] == id_nummer:
                    logout(data="json hat eine id")
                    logout(data=str(lng))
                    if not data["logos"]:
                        logout(data="json hat keine logo daten")
                        return
                    else:
                        logout(data="json hat infos daten")
                        for file_path in data["logos"]:
                            if file_path["iso_639_1"] == lng:
                                url_logo = file_path["file_path"]
                                logout(data="logo")
                                logout(data="url logo lng gefunden")
                                logout(data=url_logo)
                                break
                        else:
                            # Wenn kein deutsches logo gefunden wurde, nach einem ohne Sprachcode suchen
                            for file_path in data["logos"]:
                                if file_path["iso_639_1"] == "en":
                                    url_logo = file_path["file_path"]
                                    # Weitere Verarbeitung des Datei-Pfads
                                    logout(data="url Logo en sprache gefunden")
                                    logout(data=url_logo)
                                    break
                            else:
                                url_logo = None
                                logout(data="Kein deutsches oder sprachunabhaengiges logo gefunden.")
                                return
                        time_url = time.time() - start_time2
                        #log_time = f" zeit id 2:{time_url} sekunden."
                        log_time = " zeit id 2 %s sekunden." % time_url
                        logout(data=log_time)

                        if not url_logo == None:
                            url_logo_down = "https://image.tmdb.org/t/p/w{}{}".format(logosize, url_logo)
                            logout(data=str(url_logo_down))
                            logout(data="logo - open file")
                            dwn_logo = pathLogo + "{}.png".format(evntNm)
                            logout(data=str(dwn_logo))
                            logout(
                                data="====================================================================== zu save")
                            self.savePoster(dwn_logo, url_logo_down)
                            logout(data="====================================================================== von save zurueck ende logo_path")

                            time_url = time.time() - start_time2
                            #log_time = f" json ca 200 ms save pmg ca 170 ms - zeit id ende :{time_url} sekunden."
                            log_time = "json ca 200 ms save pmg ca 170 ms - zeit id ende %s sekunden." % time_url
                            logout(data=log_time)
                            time_url = time.time() - start_time
                            #log_time = f"1 x json ca 200 ms - 2 x save jpg ca 45 ms id json und save ca 375 ms - zeit von start bis save logo :{time_url} sekunden."
                            log_time = "1 x json ca 200 ms - 2 x save jpg ca 45 ms id json und save ca 375 ms - zeit von start bis save logo %s sekunden." % time_url
                            logout(data=log_time)
                            logout(data="")
                            return
                        else:
                            return
                else:
                    logout(data="=============================================================================== json hat keine id daten")
                    return
            else:
                logout(data="=================================================================================== json id ist null")
                return
        else:
            logout(data="======================================================================================= Logo download ist off 3058")

#################################################################################################################################################

    def download_casts(self, id_nummer, evntNm_orginal, media_type):
        evntNm=evntNm_orginal
        logout(data=" id nummer ist name ist")
        logout(data=str(id_nummer))
        logout(data=str(evntNm))

        logout(data=" ------------------------------------------------ Download  Casts auf on 3074 -------------------------------- ")
        logout(data=" id nummer ist ")
        logout(data=str(id_nummer))
        logout(data=str(evntNm))
        logout(data=str(pathLoc))
        name_dir = pathLoc + "casts/" + evntNm
        logout(data=str(name_dir))

        if id_nummer != "":
            logout(data="--------------------------------------------- Gefundene id nummer:")
            logout(data=str(id_nummer))
            lng = self.searchLanguage()
            logout(data=str(lng))
            url_tmdb = "https://api.themoviedb.org/3/{}/{}/credits?api_key={}".format(media_type, id_nummer, tmdb_api)
            logout(data=(url_tmdb))
            # API-Anfrage
            response = requests.get(url_tmdb)
            #data = response.json()

            #data = json.loads(response.text)
            logout(data="check json daten")
            #logout(data=str(data))

            # Prüfen, ob die Daten gültig sind
           # if not data.get("success", False):
            #    logout(data="Keine gültigen JSON-Daten erhalten. Prozess wird abgebrochen.")
            #    return  # Bricht den aktuellen Prozess ab

            try:
                # JSON-Daten parsen
                data = json.loads(response.content)
            except ValueError:
                # JSON ungültig
                logout(data="Ungueltige JSON-Daten erhalten. Prozess wird abgebrochen.")
                return

                # Sicherstellen, dass `data` ein Dictionary ist
            if not isinstance(data, dict):
                logout(data="1 Keine gueltigen JSON-Daten erhalten. Prozess wird abgebrochen.")
                return

            # Prüfen, ob "cast" vorhanden ist und Daten enthält
            if "cast" not in data or not data["cast"]:
                logout(data="Schlüssel 'cast' nicht gefunden oder leer. Prozess wird abgebrochen.")
                return

                # Wenn alles ok, fahre mit dem Prozess fort
            logout(data="JSON-Daten gueltig. Prozess wird fortgesetzt.")
##########################################################################################################
            # ueberpruefen, ob das Verzeichnis existiert, und erstellen, wenn nicht
            if not os.path.exists(name_dir):
                try:
                    os.makedirs(name_dir)
                    logout(data="Verzeichnis erstellt:")
                except OSError as e:
                    logout(data="Fehler beim Erstellen des Verzeichnisses:")
                    return
            else:
                logout(data="Verzeichnis existiert bereits:")

            # JSON-Dateiname
            #name_json = name_dir + "/" + evntNm + ".json"
            name_json = os.path.join(name_dir, "{}.json".format(evntNm))
            logout(data="namejson")
            logout(data=str(name_json))

            if response.status_code == 200:
                logout(data="response")

                # JSON-Datei speichern so in info geht auch in py2

                with open(name_json, "w") as file:
                    json.dump(data, file, indent=4)

                # with open(name_json, "w", encoding="utf-8") as f:
                #with io.open(name_json, "w", encoding="utf-8") as f:
                    logout(data="save")
                    #json.dump(data, f, ensure_ascii=False, indent=4)
                logout(data="Besetzung wurde erfolgreich gespeichert!")
            else:
                #logout(data="Fehler beim Abrufen der Daten:")
                logout(data="Fehler beim Abrufen der Daten: {}".format(response.status_code))
                return

            # infos holen aus der json , "profile_path": "/1ZuljeZSIDnS3EJSfwX0Gck9fAc.jpg", "name": "Michael B. Jordan"
            logout(data="zu open")
            try:
                logout(data="open")
                with open(name_json, "r") as f:
                    logout(data="open1")
                    data = json.load(f)

                logout(data="cast")
                cast = data.get("cast", [])  # Die Liste der Schauspieler holen

                # Variablen initialisieren
                darsteller0 = None
                darsteller0bild = None
                filmdarsteller0 = None
                darsteller1 = None
                darsteller1bild = None
                filmdarsteller1 = None
                darsteller2 = None
                darsteller2bild = None
                filmdarsteller2 = None
                darsteller3 = None
                darsteller3bild = None
                filmdarsteller3 = None
                darsteller4 = None
                darsteller4bild = None
                filmdarsteller4 = None
                darsteller5 = None
                darsteller5bild = None
                filmdarsteller5 = None
                darsteller6 = None
                darsteller6bild = None
                filmdarsteller6 = None
                darsteller7 = None
                darsteller7bild = None
                filmdarsteller7 = None
                darsteller8 = None
                darsteller8bild = None
                filmdarsteller8 = None
                darsteller9 = None
                darsteller9bild = None
                filmdarsteller9 = None
                darsteller10 = None
                darsteller10bild = None
                filmdarsteller10 = None

                logout(data="none")
                darsteller0_ok = False
                if len(cast) > 0:
                    darsteller0bild = cast[0].get("profile_path")
                    if darsteller0bild is not None:
                        logout(data="Darsteller 0 Bild: " + darsteller0bild)

                        darsteller0 = cast[0].get("name")
                        if darsteller0:  # Überprüfen, ob der Wert nicht None ist
                            darsteller0 = darsteller0.split("/")[0].strip()
                            logout(data="Darsteller 0: " + darsteller0)
                        else:
                            darsteller0 = ""
                            logout(data="kein Darsteller 0:" + darsteller0)

                        filmdarsteller0 = cast[0].get("character")
                        if filmdarsteller0:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller0 = filmdarsteller0.split("/")[0].strip()
                            logout(data="FilmDarsteller 0: " + filmdarsteller0)
                        else:
                            darsteller1 = ""
                            logout(data="kein FilmDarsteller 0:" + filmdarsteller0)

                        if darsteller0 and darsteller0bild:
                            # if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller0_ok = True
                            logout(data="Darsteller 0 True")
                            logout(data="Darsteller 0:" + darsteller0)
                            logout(data="FilmDarsteller 0:" + filmdarsteller0)
                            logout(data="Darsteller 0 Bild:" + darsteller0bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 0")

                darsteller1_ok = False
                if len(cast) > 1:
                    logout(data="Darsteller 1 daten holen")
                    darsteller1bild = cast[1].get("profile_path")
                    if darsteller1bild is not None:
                        logout(data="Darsteller 1 Bild: " + darsteller1bild)

                        darsteller1 = cast[1].get("name")
                        if darsteller1:  # Überprüfen, ob der Wert nicht None ist
                            darsteller1 = darsteller1.split("/")[0].strip()
                            logout(data="Darsteller 1: " + darsteller1)
                        else:
                            darsteller1 = ""
                            logout(data="kein Darsteller 1:" + darsteller1)

                        filmdarsteller1 = cast[1].get("character")
                        if filmdarsteller1:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller1 = filmdarsteller1.split("/")[0].strip()
                            logout(data="FilmDarsteller 1: " + filmdarsteller1)
                        else:
                            darsteller1 = ""
                            logout(data="kein FilmDarsteller 1:" + filmdarsteller1)


                        if darsteller1 and darsteller1bild:
                        #if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller1_ok = True
                            logout(data="Darsteller 1 True")
                            logout(data="Darsteller 1:" + darsteller1)
                            logout(data="FilmDarsteller 1:" + filmdarsteller1)
                            logout(data="Darsteller 1 Bild:" + darsteller1bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 1")

                darsteller2_ok = False
                if len(cast) > 2:
                    darsteller2bild = cast[2].get("profile_path")
                    if darsteller2bild is not None:
                        logout(data="Darsteller 2 Bild: " + darsteller2bild)

                        darsteller2 = cast[2].get("name")
                        if darsteller2:  # Überprüfen, ob der Wert nicht None ist
                            darsteller2 = darsteller2.split("/")[0].strip()
                            logout(data="Darsteller 2: " + darsteller2)
                        else:
                            darsteller2 = ""
                            logout(data="kein Darsteller 2:" + darsteller2)

                        filmdarsteller2 = cast[2].get("character")
                        if filmdarsteller2:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller2 = filmdarsteller2.split("/")[0].strip()
                            logout(data="FilmDarsteller 2: " + filmdarsteller2)
                        else:
                            darsteller2 = ""
                            logout(data="kein FilmDarsteller 2:" + filmdarsteller2)

                        if darsteller2 and darsteller2bild:
                            # if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller2_ok = True
                            logout(data="Darsteller 2 True")
                            logout(data="Darsteller 2:" + darsteller2)
                            logout(data="FilmDarsteller 2:" + filmdarsteller2)
                            logout(data="Darsteller 2 Bild:" + darsteller2bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 2")

                darsteller3_ok = False
                if len(cast) > 3:
                    darsteller3bild = cast[3].get("profile_path")
                    if darsteller3bild is not None:
                        logout(data="Darsteller 3 Bild: " + darsteller3bild)

                        darsteller3 = cast[3].get("name")
                        if darsteller3:  # Überprüfen, ob der Wert nicht None ist
                            darsteller3 = darsteller3.split("/")[0].strip()
                            logout(data="Darsteller 3: " + darsteller3)
                        else:
                            darsteller3 = ""
                            logout(data="kein Darsteller 3:" + darsteller3)

                        filmdarsteller3 = cast[3].get("character")
                        if filmdarsteller3:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller3 = filmdarsteller3.split("/")[0].strip()
                            logout(data="FilmDarsteller 3: " + filmdarsteller3)
                        else:
                            darsteller1 = ""
                            logout(data="kein FilmDarsteller 3:" + filmdarsteller3)

                        if darsteller3 and darsteller3bild:
                            # if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller3_ok = True
                            logout(data="Darsteller 3 True")
                            logout(data="Darsteller 3:" + darsteller3)
                            logout(data="FilmDarsteller 3:" + filmdarsteller3)
                            logout(data="Darsteller 3 Bild:" + darsteller3bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 3")

                # -------------------------------------------------------------------------------------------------------------

                darsteller4_ok = False
                if len(cast) > 4:
                    logout(data="Darsteller 4 daten holen")
                    darsteller4bild = cast[4].get("profile_path")
                    if darsteller4bild is not None:
                        logout(data="Darsteller 4 Bild: " + darsteller4bild)

                        darsteller4 = cast[1].get("name")
                        if darsteller4:  # Überprüfen, ob der Wert nicht None ist
                            darsteller4 = darsteller4.split("/")[0].strip()
                            logout(data="Darsteller 4: " + darsteller4)
                        else:
                            darsteller4 = ""
                            logout(data="kein Darsteller 4:" + darsteller4)

                        filmdarsteller4 = cast[4].get("character")
                        if filmdarsteller4:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller4 = filmdarsteller4.split("/")[0].strip()
                            logout(data="FilmDarsteller 4: " + filmdarsteller4)
                        else:
                            darsteller4 = ""
                            logout(data="kein FilmDarsteller 4:" + filmdarsteller4)

                        if darsteller4 and darsteller4bild:
                            # if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller4_ok = True
                            logout(data="Darsteller 4 True")
                            logout(data="Darsteller 4:" + darsteller4)
                            logout(data="FilmDarsteller 4:" + filmdarsteller4)
                            logout(data="Darsteller 4 Bild:" + darsteller4bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 4")

                # -----------------------------------------------------------------------------------------

                darsteller5_ok = False
                if len(cast) > 5:
                    logout(data="Darsteller 5 daten holen")
                    darsteller5bild = cast[5].get("profile_path")
                    if darsteller5bild is not None:
                        logout(data="Darsteller 5 Bild: " + darsteller5bild)

                        darsteller5 = cast[5].get("name")
                        if darsteller5:  # Überprüfen, ob der Wert nicht None ist
                            darsteller5 = darsteller5.split("/")[0].strip()
                            logout(data="Darsteller 5: " + darsteller5)
                        else:
                            darsteller5 = ""
                            logout(data="kein Darsteller 5:" + darsteller5)

                        filmdarsteller5 = cast[5].get("character")
                        if filmdarsteller5:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller5 = filmdarsteller5.split("/")[0].strip()
                            logout(data="FilmDarsteller 5: " + filmdarsteller5)
                        else:
                            darsteller5 = ""
                            logout(data="kein FilmDarsteller 5:" + filmdarsteller5)

                        if darsteller5 and darsteller5bild:
                            # if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller5_ok = True
                            logout(data="Darsteller 5 True")
                            logout(data="Darsteller 5:" + darsteller5)
                            logout(data="FilmDarsteller 5:" + filmdarsteller5)
                            logout(data="Darsteller 5 Bild:" + darsteller5bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 5")

                darsteller6_ok = False
                if len(cast) > 6:
                    darsteller6bild = cast[6].get("profile_path")
                    if darsteller6bild is not None:
                        logout(data="Darsteller 6 Bild: " + darsteller6bild)

                        darsteller6 = cast[6].get("name")
                        if darsteller6:  # Überprüfen, ob der Wert nicht None ist
                            darsteller6 = darsteller6.split("/")[0].strip()
                            logout(data="Darsteller 6: " + darsteller6)
                        else:
                            darsteller6 = ""
                            logout(data="kein Darsteller 6:" + darsteller6)

                        filmdarsteller6 = cast[6].get("character")
                        if filmdarsteller6:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller6 = filmdarsteller6.split("/")[0].strip()
                            logout(data="FilmDarsteller 6: " + filmdarsteller6)
                        else:
                            darsteller6 = ""
                            logout(data="kein FilmDarsteller 6:" + filmdarsteller6)

                        if darsteller6 and darsteller6bild:
                            # if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller6_ok = True
                            logout(data="Darsteller 6 True")
                            logout(data="Darsteller 6:" + darsteller6)
                            logout(data="FilmDarsteller 6:" + filmdarsteller6)
                            logout(data="Darsteller 6 Bild:" + darsteller6bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 6")

                darsteller7_ok = False
                if len(cast) > 7:
                    darsteller7bild = cast[7].get("profile_path")
                    if darsteller7bild is not None:
                        logout(data="Darsteller 7 Bild: " + darsteller7bild)

                        darsteller7 = cast[7].get("name")
                        if darsteller7:  # Überprüfen, ob der Wert nicht None ist
                            darsteller7 = darsteller7.split("/")[0].strip()
                            logout(data="Darsteller 7: " + darsteller7)
                        else:
                            darsteller7 = ""
                            logout(data="kein Darsteller 7:" + darsteller7)

                        filmdarsteller7 = cast[7].get("character")
                        if filmdarsteller7:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller7 = filmdarsteller7.split("/")[0].strip()
                            logout(data="FilmDarsteller 7: " + filmdarsteller7)
                        else:
                            darsteller7 = ""
                            logout(data="kein FilmDarsteller 7:" + filmdarsteller7)

                        if darsteller7 and darsteller7bild:
                            # if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller7_ok = True
                            logout(data="Darsteller 7 True")
                            logout(data="Darsteller 7:" + darsteller7)
                            logout(data="FilmDarsteller 7:" + filmdarsteller7)
                            logout(data="Darsteller 7 Bild:" + darsteller7bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 7")

                darsteller8_ok = False
                if len(cast) > 8:
                    darsteller8bild = cast[8].get("profile_path")
                    if darsteller8bild is not None:
                        logout(data="Darsteller 8 Bild: " + darsteller8bild)

                        darsteller8 = cast[8].get("name")
                        if darsteller8:  # Überprüfen, ob der Wert nicht None ist
                            darsteller8 = darsteller8.split("/")[0].strip()
                            logout(data="Darsteller 8: " + darsteller8)
                        else:
                            darsteller8 = ""
                            logout(data="kein Darsteller 8:" + darsteller8)

                        filmdarsteller8 = cast[8].get("character")
                        if filmdarsteller8:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller8 = filmdarsteller8.split("/")[0].strip()
                            logout(data="FilmDarsteller 8: " + filmdarsteller8)
                        else:
                            darsteller8 = ""
                            logout(data="kein FilmDarsteller 8:" + filmdarsteller8)

                        if darsteller8 and darsteller8bild:
                            # if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller8_ok = True
                            logout(data="Darsteller 8 True")
                            logout(data="Darsteller 8:" + darsteller8)
                            logout(data="FilmDarsteller 8:" + filmdarsteller8)
                            logout(data="Darsteller 8 Bild:" + darsteller8bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 8")

                darsteller9_ok = False
                if len(cast) > 9:
                    darsteller9bild = cast[9].get("profile_path")
                    if darsteller9bild is not None:
                        logout(data="Darsteller 9 Bild: " + darsteller9bild)

                        darsteller9 = cast[9].get("name")
                        if darsteller9:  # Überprüfen, ob der Wert nicht None ist
                            darsteller9 = darsteller9.split("/")[0].strip()
                            logout(data="Darsteller 9: " + darsteller9)
                        else:
                            darsteller9 = ""
                            logout(data="kein Darsteller 9:" + darsteller9)

                        filmdarsteller9 = cast[9].get("character")
                        if filmdarsteller9:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller9 = filmdarsteller9.split("/")[0].strip()
                            logout(data="FilmDarsteller 9: " + filmdarsteller9)
                        else:
                            darsteller9 = ""
                            logout(data="kein FilmDarsteller 9:" + filmdarsteller9)

                        if darsteller9 and darsteller9bild:
                            # if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller9_ok = True
                            logout(data="Darsteller 9 True")
                            logout(data="Darsteller 9:" + darsteller9)
                            logout(data="FilmDarsteller 9:" + filmdarsteller9)
                            logout(data="Darsteller 9 Bild:" + darsteller9bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 9")
                        
                darsteller10_ok = False
                if len(cast) > 10:
                    darsteller10bild = cast[10].get("profile_path")
                    if darsteller10bild is not None:
                        logout(data="Darsteller 10 Bild: " + darsteller10bild)

                        darsteller10 = cast[10].get("name")
                        if darsteller10:  # Überprüfen, ob der Wert nicht None ist
                            darsteller10 = darsteller10.split("/")[0].strip()
                            logout(data="Darsteller 10: " + darsteller10)
                        else:
                            darsteller10 = ""
                            logout(data="kein Darsteller 10:" + darsteller10)

                        filmdarsteller10 = cast[10].get("character")
                        if filmdarsteller10:  # Überprüfen, ob der Wert nicht None ist
                            filmdarsteller10 = filmdarsteller10.split("/")[0].strip()
                            logout(data="FilmDarsteller 10: " + filmdarsteller10)
                        else:
                            darsteller10 = ""
                            logout(data="kein FilmDarsteller 10:" + filmdarsteller10)

                        if darsteller10 and darsteller10bild:
                            # if darsteller1 and darsteller1bild and filmdarsteller1:
                            darsteller10_ok = True
                            logout(data="Darsteller 10 True")
                            logout(data="Darsteller 10:" + darsteller10)
                            logout(data="FilmDarsteller 10:" + filmdarsteller10)
                            logout(data="Darsteller 10 Bild:" + darsteller10bild)
                    else:

                        logout(data="Fehler: Fehlende Felder für Darsteller 10")

                logout(data=str(darsteller0_ok))
                logout(data=str(darsteller1_ok))
                logout(data=str(darsteller2_ok))
                logout(data=str(darsteller3_ok))
                logout(data=str(darsteller4_ok))
                logout(data=str(darsteller5_ok))
                logout(data=str(darsteller6_ok))
                logout(data=str(darsteller7_ok))
                logout(data=str(darsteller8_ok))
                logout(data=str(darsteller9_ok))
                logout(data=str(darsteller10_ok))




            except FileNotFoundError:
                logout(data="Die Datei wurde nicht gefunden:".format(name_json))
                return
            except json.JSONDecodeError:
                logout(data="Fehler beim Lesen der JSON-Datei:".format(name_json))
                return

            # jetzt jpg downloaden und saven
            # Basis-URL der TMDb-Images
            base_url = "https://image.tmdb.org/t/p/"

            # Gewünschte Bildgröße (z.B. w500 für mittlere Größe)
            image_size = "w342"
            if darsteller0_ok == True:
                # ---------------------------  Darsteller 0 ----------------------------------------------------------------

                logout(data="Darsteller 0 :")
                if darsteller0bild:
                    image_url = base_url + image_size + darsteller0bild
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings

                    # Zielname und Ort des Bildes
                    output_file = "{}/00_{}({}).jpg".format(name_dir, darsteller0, filmdarsteller0)
                    logout(data="Speichern des Bildes0: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild0: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild0 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 0.")
            else:
                logout(data="Darsteller0 ist nicht vorhanden")

            if darsteller1_ok == True:
                # ---------------------------  Darsteller 1 ----------------------------------------------------------------

                logout(data="Darsteller 1 ist True:")
                if darsteller1bild:
                    image_url = base_url + image_size + darsteller1bild
                    logout(data=str(image_url))
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings
                    logout(data=str(filmdarsteller1))
                    # Zielname und Ort des Bildes
                    output_file = "{}/01_{}({}).jpg".format(name_dir, darsteller1, filmdarsteller1)
                    logout(data="Speichern des Bildes: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild1: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild1 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 1.")
            else:
                logout(data="Darsteller1 ist nicht vorhanden")

            if darsteller2_ok == True:
                # ---------------------------  Darsteller 2 ----------------------------------------------------------------

                logout(data="Darsteller 2:")
                if darsteller2bild:
                    image_url = base_url + image_size + darsteller2bild
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings

                    # Zielname und Ort des Bildes
                    output_file = "{}/02_{}({}).jpg".format(name_dir, darsteller2, filmdarsteller2)
                    logout(data="Speichern des Bildes: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild2: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild2 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 2.")
            else:
                logout(data="Darsteller2 ist nicht vorhanden")

            if darsteller3_ok == True:
                # ---------------------------  Darsteller 3 ----------------------------------------------------------------

                logout(data="Darsteller 3 :")
                if darsteller3bild:
                    image_url = base_url + image_size + darsteller3bild
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings

                    # Zielname und Ort des Bildes
                    output_file = "{}/03_{}({}).jpg".format(name_dir, darsteller3, filmdarsteller3)
                    logout(data="Speichern des Bildes: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild3: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild3 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 3.")
            else:
                logout(data="Darsteller3 ist nicht vorhanden")

            if darsteller4_ok == True:
            # ---------------------------  Darsteller 4 ----------------------------------------------------------------

                logout(data="Darsteller 4 ist True:")
                if darsteller1bild:
                    image_url = base_url + image_size + darsteller4bild
                    logout(data=str(image_url))
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings
                    logout(data=str(filmdarsteller4))
                    # Zielname und Ort des Bildes
                    output_file = "{}/04_{}({}).jpg".format(name_dir, darsteller4, filmdarsteller4)
                    logout(data="Speichern des Bildes 4: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild4: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild4 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 4.")
            else:
                logout(data="Darsteller4 ist nicht vorhanden")

            if darsteller5_ok == True:
        # ---------------------------  Darsteller 5 ----------------------------------------------------------------

                logout(data="Darsteller 5:")
                if darsteller5bild:
                    image_url = base_url + image_size + darsteller5bild
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings

                    # Zielname und Ort des Bildes
                    output_file = "{}/05_{}({}).jpg".format(name_dir, darsteller5, filmdarsteller5)
                    logout(data="Speichern des Bildes5: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild5: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild5 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 5.")

            else:
                logout(data="Darsteller5 ist nicht vorhanden")

            if darsteller6_ok == True:
# ---------------------------  Darsteller 6 ----------------------------------------------------------------

                logout(data="Darsteller 6:")
                if darsteller6bild:
                    image_url = base_url + image_size + darsteller6bild
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings

                    # Zielname und Ort des Bildes
                    output_file = "{}/06_{}({}).jpg".format(name_dir, darsteller6, filmdarsteller6)
                    logout(data="Speichern des Bildes: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild6: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild6 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 6.")
            else:
                logout(data="Darsteller6 ist nicht vorhanden")

            if darsteller7_ok == True:
# ---------------------------  Darsteller 7 ----------------------------------------------------------------

                logout(data="Darsteller 7:")
                if darsteller7bild:
                    image_url = base_url + image_size + darsteller7bild
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings

                    # Zielname und Ort des Bildes
                    output_file = "{}/07_{}({}).jpg".format(name_dir, darsteller7, filmdarsteller7)
                    logout(data="Speichern des Bildes: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild7: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild7 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 7.")
            else:
                logout(data="Darsteller7 ist nicht vorhanden")

            if darsteller8_ok == True:
# ---------------------------  Darsteller 8 ----------------------------------------------------------------

                logout(data="Darsteller 8:")
                if darsteller8bild:
                    image_url = base_url + image_size + darsteller8bild
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings

                    # Zielname und Ort des Bildes
                    output_file = "{}/08_{}({}).jpg".format(name_dir, darsteller8, filmdarsteller8)
                    logout(data="Speichern des Bildes: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild8: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild8 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 8.")
            else:
                logout(data="Darsteller8 ist nicht vorhanden")

            if darsteller9_ok == True:
            # ---------------------------  Darsteller 9 ----------------------------------------------------------------

                logout(data="Darsteller 9:")
                if darsteller9bild:
                    image_url = base_url + image_size + darsteller9bild
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings

                    # Zielname und Ort des Bildes
                    output_file = "{}/09_{}({}).jpg".format(name_dir, darsteller9, filmdarsteller9)
                    logout(data="Speichern des Bildes: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild9: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild9 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 9.")
            else:
                logout(data="Darsteller9 ist nicht vorhanden")

            if darsteller10_ok == True:
            
                # ---------------------------  Darsteller 10 ----------------------------------------------------------------

                logout(data="Darsteller 10 :")
                if darsteller10bild:
                    image_url = base_url + image_size + darsteller10bild
                    logout(data="Bild-URL: {}".format(image_url))  # `format()`-Methode statt f-Strings

                    # Zielname und Ort des Bildes
                    output_file = "{}/10_{}({}).jpg".format(name_dir, darsteller10, filmdarsteller10)
                    logout(data="Speichern des Bildes: {}".format(output_file))

                    # Bild herunterladen und speichern
                    try:
                        logout(data="timeout start")
                        response = requests.get(image_url, timeout=20)
                        logout(data="timeout ende")
                        if response.status_code == 200:
                            logout(data="response ok")
                            with open(output_file, "wb") as file:
                                logout(data="Starte Download für Bild10: {}".format(image_url))
                                file.write(response.content)
                            logout(data="Bild10 erfolgreich heruntergeladen und gespeichert: {}".format(output_file))
                        else:
                            logout(data="Fehler beim Herunterladen des Bildes: {}".format(response.status_code))
                    except requests.exceptions.RequestException as e:
                        logout(data="Netzwerkfehler beim Herunterladen des Bildes: {}".format(e))
                else:
                    logout(data="Kein gültiger Bildpfad für Darsteller 10.")
            else:
                logout(data="Darsteller10 ist nicht vorhanden")


            logout(data="****************************** Casts Download Ende **************************************************")
            return
                # *********************************************************************************************************************
    # in dwn_poster muss der path sein und in url wo man es downloadet
   
  

    def savePoster(self, dwn_path, url):
        start_time5 = time.time()
        logout(data="")
        logout(data="")
        logout(data="++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ def saver start")
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        #log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
        log_message = "Die Funktion getText() wurde von %s aufgerufen." % caller_name
        logout(data=log_message)
        logout(data="save poster - open file")
        logout(data=str(dwn_path))
        logout(data=str(url))
        try:
            with open(dwn_path, 'wb') as f:
                logout(data="with open")
                f.write(urlopen(url).read())
                logout(data="write ")
                # Überprüfe, ob das Schreiben abgeschlossen ist
                f.flush()
                f.close()
                # Überprüfe die Dateigröße
                file_size = os.path.getsize(dwn_path)
                if file_size == 0:
                    # Lösche die Datei, wenn sie 0 Byte groß ist
                    os.remove(dwn_path)
                    logout(data="wurde geloescht, da sie 0 Byte war.")
                else:
                    logout(data="Datei wurde erfolgreich gespeichert ")
            save_time = time.time() - start_time5
            #log_time = f" zeit save  :{save_time} sekunden."
            log_time = " zeit save  %s sekunden." % save_time
            logout(data=log_time)
            logout(data="+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  def save ende")
            logout(data="")
            return url
        except OSError as e:
            logout(data="OS error")
            logout(data=str(e))

        #except URLError as e:
        #    print("URL error")
        #    logout(data=f"Fehler beim Herunterladen der Datei: {e}")

        #except HTTPError as e:
        #    print("HTTP error")
        #    logout(data=f"HTTP-Fehler beim Herunterladen der Datei: {e}")
        except Exception as e:
            logout(data="Exception")
            #print(f"Unerwarteter Fehler beim Herunterladen der Datei: {e}")
            logout(data=str(e))


    def eventname(self, Name):
        logout(data="")
        logout(
            data=">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>     name aus der json in eventname start umwandelen")
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        #log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
        log_message = "Die Funktion getText() wurde von %s aufgerufen." % caller_name
        logout(data=log_message)

        logout(data=Name)
        # hier live: entfernen
        Name = Name.replace('\xc2\x86', '').replace('\xc2\x87', '').replace("live: ", "").replace("LIVE ", "")
        Name = Name.replace("live: ", "").replace("LIVE ", "").replace("LIVE: ", "").replace("live ", "")
        logout(data="name live rausnehmen")
        logout(data=Name)


        # achtung namen muessen gleich bleiben erst mal versuche
        Name = Name.split(":")[0].strip()  # Teilt den String und entfernt fuehrende/trailing Leerzeichen
        # hier versuch name nur vor dem :
        #name1 = Name.split(": ", 1)
        #Name = name1[0]
        #Namezusatz = name1[1]
        #logout(data="name   : abtrennen ")
        #logout(data=Name)
        #logout(data=Namezusatz)

        Name = REGEX.sub('', Name).strip()
        logout(data=Name)

        #Name = Name.replace("&", "und")
        Name = Name.replace("ß", "ss")
        Name = Name.lower()
        logout(data=Name)
        logout(
            data=">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    name aus der json in eventname ende umgewandelt")
        logout(data="")
        return Name  # liefert dem aufruf das zurueck
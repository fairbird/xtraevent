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
import requests
from requests.utils import quote
import os
import re
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

import inspect
# --------------------------- Logfile -------------------------------


from datetime import datetime, timedelta
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraevent-Download.log"

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
logout(data="start-6.75")

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
    else:
        from ConfigParser import ConfigParser
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

logout(data="---------------------- language is -------------------------------------------")
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
logout(data="pathLoc")
logout(data=str(pathLoc))
desktop_size = getDesktop(0).size().width()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
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

class downloads(Screen):
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
        self['info'] = Label()
        self['infoposter'] = Label()
        self['infobackdrop'] = Label()
        self['infobanner'] = Label()
        self['infoinfos'] = Label()
        self['info2'] = Label()
        self['Picture'] = Pixmap()
        self['Picture2'] = Pixmap()
        self['int_statu'] = Label()
        self['key_red'] = Label(_('Back'))
        self['key_green'] = Label(_('Download'))
        # self['key_yellow'] = Label(_('Show'))
        self['key_yellow'] = Label(_('Delete All'))
        self['key_1'] = Label(_('Delete Poster            :1'))
        self['key_2'] = Label(_('Delete Backdrop        :2'))
        self['key_3'] = Label(_('Delete Banner           :3'))
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
        # -----------------------------------------------------------------------------------------------
        self['progress'] = ProgressBar()
        self['progress'].setRange((0, 100))
        self['progress'].setValue(0)
        self.setTitle(_("░ {}".format(lng.get(lang, '45'))))
        self.screen_hide = False
        # -------------------------------------------------------------------------------------------------
        self.anzahlfiles_in_poster()
        self['infoposter'].setText(str(self.countposter))
        self.anzahlfiles_in_backdrop()
        self['infobackdrop'].setText(str(self.countbackdrop))
        self.anzahlfiles_in_banner()
        self['infobanner'].setText(str(self.countbanner))
        self.anzahlfiles_in_infos()
        self['infoinfos'].setText(str(self.countinfos))
        # --------------------------------------------------------------------------------------------------
        testver = version
        self.testver = testver
        self["testver"] = Label()
        self["testver"].setText("%s " % (self.testver))
        self.onLayoutFinish.append(self.showFilm)
        self.onLayoutFinish.append(self.intCheck)


    def anzahlfiles_in_poster(self):
        logout(data="anzahl poster 233")
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
        logout(data="anzahl backdrop 248")
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
        logout(data="anzahl banner 260")
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
        logout(data="anzahl infos 271")
        directory = "{}infos".format(pathLoc)
        count = 0
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                count += 1
        self.countinfos = count
        logout(data=str(self.countinfos))
        self['infoinfos'].setText(str(self.countinfos))

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
        logout(data="save")
        if config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '14'):
            self.currentChEpgs()
        if config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '13'):
            self.selBouquets()

    def deletfilesall(self):
        self.deletfilesposter()
        self.deletfilesbackdrop()
        self.deletfilesbanner()
        self.deletfilesinfos()
        self.deletfilesnoinfos()

    def deletfilesposter(self):
        logout(data="deletfilesposter")
        directoryposter = "{}poster".format(pathLoc)
        files = os.listdir(directoryposter)
        for file in files:
            file_path = os.path.join(directoryposter, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.anzahlfiles_in_poster()

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
        self.anzahlfiles_in_poster()
        self.anzahlfiles_in_backdrop()
        self.anzahlfiles_in_banner()
        self.anzahlfiles_in_infos()
        logout(data="------------------ def delet")


    def currentChEpgs(self):
        logout(data="currentChEpgs")
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
        logout(data="selBouquets")
        if os.path.exists("{}bqts".format(pathLoc)):
            logout(data="-----------------------------------------------    selBouquets file exits")
            with open("{}bqts".format(pathLoc), "r") as f:
                logout(data="selBouquets open file")
                refs = f.readlines()
            nl = len(refs)
            eventlist=[]
            for i in range(nl):
                ref = refs[i]
                try:
                    events = epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
                    n = config.plugins.xtraEvent.searchNUMBER.value
                    for i in range(int(n)):
                        title = events[i][4]
                        title = REGEX.sub('', title).strip()
                        eventlist.append(title)
                except:
                    pass
            self.titles = list(dict.fromkeys(eventlist))
            start_new_thread(self.downloadEvents, ())
        else:
            logout(data="-----------------------------------------------    selBouquets file not exits")

####################################################
    def downloadEvents(self):
        logout(data="downloadEvents")
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
        extra3_poster_downloaded = 0
        extra3_info_downloaded = 0
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
        logout(data="332 ausgeschaltet zu delete files 1355 ")
        self.delete_oldfilesposter()
        self.delete_oldfilesbackdrop()
        self.delete_oldfilesbanner()
        self.delete_oldfilesinfos()
        self.delete_oldfilesnoinfos()
        logout(data="zurueck von delete files")
        #---------------------------------
        logout(data="Extra 3 on-off abfrage")
        if config.plugins.xtraEvent.onoff.value:
            logout(data="--------------------------------------------------- Extra 3 ist an ")
# elcinema(en) #################################################################
            if config.plugins.xtraEvent.extra3.value == True:
                logout(data="extra3 true")
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
                            extra3_poster_downloaded += 1
                            downloaded = extra3_poster_downloaded
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
                                extra3_info_downloaded += 1
                                downloaded = extra3_info_downloaded
                                self.prgrs(downloaded, n)
                                self['info'].setText("► {}, EXTRA3, INFO".format(title.upper()))
                            if os.path.exists(dwnldFile):
                                self.showPoster(dwnldFile)

                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("elcinema ej, %s, %s\n"%(title, err))
                    logout(data=" hier timeout von 1 sec ")
                    time.sleep(1)  # war 5 sec mal neuer versuch
            logout(data=" liste der titel zum downloaden 541")
            n = len(self.titles)
            self.anzahldownloads = n
            logout(data=str(n))
            for i in range(n):
                title = self.titles[i]
                title = title.strip()
                self.setTitle(_("{}".format(title)))

    # tmdb_Poster() #################################################################
                # download



                logout(data=" Poster abfrage vom tmdb holen 744")

                if config.plugins.xtraEvent.poster.value == True:           # abfrage poster ja/nein
                    logout(data=str(config.plugins.xtraEvent.poster.value))
                    dwnldFile = "{}poster/{}.jpg".format(pathLoc, title)
                    logout(data=" Poster download auf JA 744")
                    logout(data=str(dwnldFile))



                    if config.plugins.xtraEvent.tmdb.value == True:         # abfrage soll von tmdb geholt werden
                        logout(data=" Poster von Tmdb holen auf JA 750")
                        if not os.path.exists(dwnldFile):                   # ist das poster schon vorhanden
                            logout(data=" Poster file ist nicht vorhanden 752")



# --------------------------------------  suchen json info ---------------------------------------------------------------------------------------------------
                            try:                                            # das poster ist nicht vorhanden
                                srch = "multi"                              # wie gesucht wird , es gibt auch tv und movie
                                #srch = config.plugins.xtraEvent.searchType.value
                                logout(data=str(srch))
                                logout(data=" URL ")                     # erste anfrage
                                url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
                                logout(data=" URL ")
                                logout(data=str(url_tmdb))

                                # abfrage ist total result 0 keine json vorhanden dann nochmal anfragen ohne titel
                                response = requests.get(url_tmdb)
                                data = response.json()
                                total_results = data.get("total_results", 0)
                                if total_results == 0:
                                    logout(data=" json  total results ist 0 keine daten im tv json")
                                    url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote)
                                    logout(data=" URL 748")
                                    logout(data=str(url_tmdb))

                                # hier
                                #  languag anfrage geht nicht immer wenn dann vorher abfrage ist result >0 bei hier

                                #if config.plugins.xtraEvent.searchLang.value == True:
                                #    logout(data=" URL 566")
                                #    url_tmdb += "&language={}".format(self.searchLanguage())          # nochmal anfragen mir language
                                #    logout(data=" URL 566")
                                #    logout(data=str(url_tmdb))

                                # ------------------------  check od daten ok sind total resulst muss groesser 0 sein

                                response = requests.get(url_tmdb)
                                data = response.json()

                                total_results = data.get("total_results", 0)
                                logout(data=" json total results vom json")
                                logout(data=str(total_results))
                                if total_results == 0:
                                    logout(data=" json total results ist 0 keine daten im json")

# ------------------------------------------------- wenn mit multi nichts gefunden dann nochmal mit tv suchen -----------------------------------------------
                                    if srch == "multi":
                                        logout(data=" nochmal anfragen mit multi")
                                        srch = "tv"
                                        url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
                                        response = requests.get(url_tmdb)
                                        data = response.json()
                                        total_results = data.get("total_results", 0)
                                        logout(data=" json 590  total results vom multi json")
                                        logout(data=str(total_results))

                                        #if total_results == 0:
                                        #    logout(data=" json 594  total results ist 0 keine daten im tv json")

                                        # hier kann man noch abfrage movie machen
                                            #logout(data=" json 600 json info nicht gefunden schreiben titel und path")
                                            # Dateipfad im temporären Verzeichnis erstellen
                                            # file_path = os.path.join('/tmp', 'poster.json')
                                            #logout(data=str(title))
                                            #logout(data=str(pathLoc))

                                            #file_path_no = "{}noinfos/{}.json".format(pathLoc, title)
                                            #logout(data=" json path kpl zum schreiben no json 606")
                                            #logout(data=str(file_path_no))
                                            # NO JSON-Title speichern
                                            #with open(file_path_no, 'w') as file:
                                            #    json.dump(response.json(), file)
                                            #    logout(data=" nojson geschrieben 612")

                                        #else:
                                            # Weiterer Code für den Fall, dass es Ergebnisse im multi-JSON gibt
                                        #    pass

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
                                    logout(data=" poster url aus json holen ")
                                    logout(data=str(poster))
                                    original_title = requests.get(url_tmdb).json()['results'][0]['poster_path']
                                    logout(data=str(original_title))
                                    p_size = config.plugins.xtraEvent.TMDBpostersize.value
                                    logout(data=str(p_size))
                                    logout(data=" URL start download ")
                                    url = "https://image.tmdb.org/t/p/{}{}".format(p_size, poster)
                                    logout(data=" URL ende download von dieser url  ")
                                    logout(data=str(url))

                                    if poster != "":
                                        logout(data=" poster vorhanden ")
                                        open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                                    if os.path.exists(dwnldFile):
                                        logout(data=" if os.path exist")
                                        self['info'].setText("►  {}, TMDB, POSTER".format(title.upper()))
                                        tmdb_poster_downloaded += 1
                                        downloaded = tmdb_poster_downloaded
                                        self.prgrs(downloaded, n)

# ------------------------------------------ versuch logo ----------------------------------------------------------------
                                    if id_nummer is not None:
                                        logout(data="")
                                        logout(data="----------------------------------------------------------------------------------- Gefundene id nummer:")
                                        logout(data=str(id_nummer))
                                        lng = self.searchLanguage()
                                        logout(data=str(lng))
                                        url_tmdb = "https://api.themoviedb.org/3/movie/{}/images?api_key={}".format(id_nummer, tmdb_api)
                                        logout(data=(url_tmdb))
                                        # so url - http://api.themoviedb.org/3/movie/672/images?api_key=3c3efcf47c3577558812bb9d64019d65
                                        # json laden in data
                                        response = requests.get(url_tmdb)
                                        data = response.json()
                                        logout(data="check json daten")

                                        if "id" in data and data["id"] == id_nummer:
                                            logout(data="json hat eine id")
                                            logout(data=str(lng))
                                            if not data["logos"]:
                                                logout(data="json hat keine logo daten")
                                            else:
                                                logout(data="json hat infos daten")
                                                for file_path in data["logos"]:

                                                    if file_path["iso_639_1"] == lng:
                                                        url_logo = file_path["file_path"]
                                                        logout(data="logo")
                                                        logout(data=url_logo)
                                                        break
                                                else:
                                                    # Wenn kein deutsches logo gefunden wurde, nach einem ohne Sprachcode suchen
                                                    for file_path in data["logos"]:
                                                        if file_path["iso_639_1"] == "en":
                                                            url_logo = file_path["file_path"]
                                                            # Weitere Verarbeitung des Datei-Pfads
                                                            logout(data="url Logo ohne sprache gefunden")
                                                            logout(data=url_logo)
                                                            break
                                                    else:
                                                        url_logo = None
                                                        logout(
                                                            data="Kein deutsches oder sprachunabhaengiges logo gefunden.")
                                                logosize = "300"
                                                if not url_logo == None:
                                                    pathLogo = "{}logo/".format(pathLoc)
                                                    url_logo_down = "https://image.tmdb.org/t/p/w{}{}".format(logosize, url_logo)
                                                    logout(data=str(url_logo_down))
                                                    logout(data="logo - open file")
                                                    dwn_logo = pathLogo + "{}.png".format(title)
                                                    logout(data=str(dwn_logo))
                                                    logout(data="----------------------------------------------------------- logo - zu save")
                                                    self.savePoster(dwn_logo, url_logo_down)
                                                    logout(data="----------------------------------------------------------- logo - von save zurueck ende logo_path")
                                                    dwnldFile = dwn_logo
                                                    self.showLogo(dwnldFile)
                                                    logout(data="----------------------------------------------------------------------------------- logo ende")
                                                    logout(data="")
                                                else:
                                                    logout(data="")
# ----------------------------------------------------------------------------------------------------------------------
                                        self.showPoster(dwnldFile)
                                        #continue
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

                        logout(data=" Poster file ist schon vorhanden fertig 646")
        # ---------------------- abfrage if file schon vorhanden ein download reicht ja ---------------------------------------------
        # tvdb_Poster() ######################## wenn file vorhanden hier nicht mehr noetig #########################################

                    logout(data=" Poster abfrage vom tvdb holen 650")
                    if config.plugins.xtraEvent.tvdb.value == True:
                        logout(data=" Poster download tvdb 652")
                        try:
                            img = Image.open(dwnldFile)
                            logout(data=" Poster img tvdb 655")
                            img.verify()
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                logout(data=" Poster tvdb deleted 659")
                                f.write("deleted : %s.jpg\n"%title)
                            try:
                                logout(data=" Poster tvdb remove 660")
                                os.remove(dwnldFile)
                            except:
                                pass
                        if not os.path.exists(dwnldFile):
                            logout(data=" Poster dwnldfile ist nicht vorhanden 662")
                            try:
                                logout(data="url 596")
                                url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(title))
                                logout(data=str(url_tvdb))
                                logout(data="url 596")
                                url_read = requests.get(url_tvdb).text
                                series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
                                if series_id:
                                    logout(data="url 603")
                                    url_tvdb = "https://thetvdb.com/api/{}/series/{}/{}".format(tvdb_api, series_id, self.searchLanguage())
                                    logout(data=str(url_tvdb))
                                    logout(data="url 603")
                                    url_read = requests.get(url_tvdb).text




                                    poster = ""
                                    poster = re.findall('<poster>(.*?)</poster>', url_read)[0]

                                    if poster != '':
                                        logout(data="url artworks 705")
                                        url = "https://artworks.thetvdb.com/banners/{}".format(poster)
                                        logout(data=str(url))
                                        logout(data="url 708")
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
        # maze_Poster() #################################################################
                    if config.plugins.xtraEvent.maze.value == True:

                        logout(data="maze 755")
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
        # fanart_Poster() #################################################################
                    if config.plugins.xtraEvent.fanart.value == True:
                        logout(data="maze 794")
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
                logout(data="backdrop abfrage ob downloaden 830")
                logout(data=str(config.plugins.xtraEvent.backdrop.value))


    #                                       backdrop() #################################################################


                if config.plugins.xtraEvent.backdrop.value == True:
                    logout(data="backdrop ja downloaden 833")
                    dwnldFile = "{}backdrop/{}.jpg".format(pathLoc, title)
                    if config.plugins.xtraEvent.extra.value == True:
                        logout(data="extra ja downloaden 836")
                        if not os.path.exists(dwnldFile):
                            try:
                                logout(data="backdrop extra url 839")
                                url = "http://capi.tvmovie.de/v1/broadcasts/search?q={}&page=1&rows=1".format(title.replace(" ", "+"))
                                logout(data=str(url))
                                logout(data="backdrop extra url 842")
                                try:
                                    logout(data="url 844")
                                    url = requests.get(url).json()['results'][0]['images'][0]['filepath']['android-image-320-180']
                                    logout(data=str(url))
                                    logout(data="url 847")
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


                    if config.plugins.xtraEvent.tmdb_backdrop.value == True:
                        logout(data="backdrop tmdb ja 868")
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
                            #srch = "multi"
                            srch = config.plugins.xtraEvent.searchType.value
                            logout(data="url 882")
                            url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
                            logout(data="url 884")
                            logout(data=str(url_tmdb))
                            if config.plugins.xtraEvent.searchLang.value:
                                logout(data="url 887")
                                url_tmdb += "&language={}".format(self.searchLanguage())
                                logout(data="url 889")
                                logout(data=str(url_tmdb))
                            try:
                                backdrop = requests.get(url_tmdb).json()['results'][0]['backdrop_path']
                                if backdrop:
                                    backdrop_size = config.plugins.xtraEvent.TMDBbackdropsize.value
                                    # backdrop_size = "w300"
                                    logout(data="url 801")
                                    url = "https://image.tmdb.org/t/p/{}{}".format(backdrop_size, backdrop)
                                    logout(data="url 801")
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


                    if config.plugins.xtraEvent.tvdb_backdrop.value == True:
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
                                logout(data="url 838")
                                url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(title))
                                logout(data="url 838")
                                logout(data=str(url_tvdb))
                                url_read = requests.get(url_tvdb).text
                                series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
                                if series_id:
                                    logout(data="url 845")
                                    url_tvdb = "https://thetvdb.com/api/{}/series/{}/{}.xml".format(tvdb_api, series_id, self.searchLanguage())
                                    logout(data="url 845")
                                    logout(data=str(url_tvdb))
                                    url_read = requests.get(url_tvdb).text
                                    backdrop = re.findall('<fanart>(.*?)</fanart>', url_read)[0]
                                    if backdrop:
                                        logout(data="url 852")
                                        url = "https://artworks.thetvdb.com/banners/{}".format(backdrop)
                                        logout(data="url 852")
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


                    if config.plugins.xtraEvent.extra2.value == True:
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
                                logout(data="url 991")
                                url = "https://www.bing.com/images/search?q={}".format(title.replace(" ", "+"))
                                logout(data="url 991")
                                logout(data=str(url))
                                if config.plugins.xtraEvent.PB.value == "posters":
                                    logout(data="url 995")
                                    url += "+poster"
                                else:
                                    logout(data="url 998")
                                    url += "+backdrop"
                                logout(data="url hier ca 500 ms 1000")
                                ff = requests.get(url, stream=True, headers=headers).text
                                logout(data="url 1002")
                                p = ',&quot;murl&quot;:&quot;(.*?)&'
                                logout(data="url 1004")
                                url = re.findall(p, ff)[0]
                                logout(data="url 1006")
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    logout(data="url 1009")
                                    f.write("bing-backdrop, %s, %s\n"%(title, err))
                                try:
                                    logout(data="url 1012")
                                    url = "https://www.google.com/search?q={}&tbm=isch&tbs=sbd:0".format(title.replace(" ", "+"))
                                    logout(data="url 1014")
                                    logout(data=str(url))
                                    if config.plugins.xtraEvent.PB.value == "posters":
                                        logout(data="url 1017")
                                        url += "+poster"
                                    else:
                                        logout(data="url 1020")
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
                                        logout(data="google open 1032")
                                        f.write("google-backdrop, %s, %s\n"%(title, err))
                            try:
                                logout(data="try extra2 1034")
                                with open(dwnldFile, 'wb') as f:
                                    f.write(requests.get(url, stream=True, allow_redirects=True).content)
                                if os.path.exists(dwnldFile):
                                    logout(data="try extra2 1037")
                                    self['info'].setText("►  {}, EXTRA2, BACKDROP".format(title.upper()))
                                    logout(data="try extra2 1039")
                                    extra2_downloaded += 1
                                    downloaded = extra2_downloaded
                                    self.prgrs(downloaded, n)
                                    logout(data="try extra2 1043")
                                    self.showBackdrop(dwnldFile)
                                    logout(data="try extra2 1045")
                                    try:
                                        img = Image.open(dwnldFile)
                                        logout(data="verivy extra2 1048")
                                        img.verify()
                                    except Exception as err:
                                        with open("/tmp/xtraEvent.log", "a+") as f:
                                            logout(data="deleted extra2 1052")
                                            f.write("deleted extra2 backdrop: %s.jpg\n"%title)
                                        try:
                                            logout(data="remove extra2 1055")
                                            #os.remove(dwnldFile)
                                        except:
                                            pass
                            except Exception as err:
                                with open("/tmp/xtraEvent.log", "a+") as f:
                                    f.write("extra2 backdrop, %s, %s\n"%(title, err))

    # banner() #################################################################
                if config.plugins.xtraEvent.banner.value == True:
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
# infos #################################################################
                if config.plugins.xtraEvent.info.value == True:
                    logout(data=" -----------------  info 1149 -----------------------------------")
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



                    info_files = "{}infos/{}.json".format(pathLoc, title)
                    if config.plugins.xtraEvent.omdbAPI.value:
                        omdb_apis = config.plugins.xtraEvent.omdbAPI.value
                    else:
                        omdb_apis = ["6a4c9432", "a8834925", "550a7c40", "8ec53e6b"]
                    if not os.path.exists(info_files):
                        logout(data=" -----------------  info no json 1179 -----------------------------------")
                        try:
                            try:
                                #srch = "multi"
                                srch = config.plugins.xtraEvent.searchType.value
                                logout(data="url 1120")
                                url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
                                logout(data="url 1120")
                                logout(data=str(url_tmdb))
                                title = requests.get(url_tmdb).json()['results'][0]['original_title']
                            except:
                                pass
                            for omdb_api in omdb_apis:
                                try:
                                    logout(data="url 1129")
                                    url = "http://www.omdbapi.com/?apikey={}&t={}".format(omdb_api, title)
                                    logout(data="url ombd1129")
                                    logout(data=str(url))
                                    info_omdb = requests.get(url, timeout=5)
                                    if info_omdb.status_code == 200:
                                        Title = info_omdb.json()["Title"]
                                        Year = info_omdb.json()["Year"]
                                        Rated = info_omdb.json()["Rated"]
                                        Duration = info_omdb.json()["Runtime"]
                                        Released = info_omdb.json()["Released"]
                                        Genre = info_omdb.json()["Genre"]
                                        Director = info_omdb.json()["Director"]
                                        Writer = info_omdb.json()["Writer"]
                                        Actors = info_omdb.json()["Actors"]
                                        if not config.plugins.xtraEvent.searchLang.value:
                                            Plot = info_omdb.json()["Plot"]
                                        Country = info_omdb.json()["Country"]
                                        Awards = info_omdb.json()["Awards"]
                                        imdbRating = info_omdb.json()["imdbRating"]
                                        imdbID = info_omdb.json()["imdbID"]
                                        Type = info_omdb.json()["Type"]
                                except:
                                    pass
                            logout(data="url imbd 1153")
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
                            continue
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("infos, %s, %s\n"%(title, err))
# --------------------------------  report nach dem download ---------------------------------------------------------
            logout(data="-------------  report ausgabe ------------")
            logout(data=str(tmdb_poster_downloaded))
            posterdownloads = tmdb_poster_downloaded + tvdb_poster_downloaded + maze_poster_downloaded + fanart_poster_downloaded
            backdropdownloads = tmdb_backdrop_downloaded + tvdb_backdrop_downloaded + fanart_backdrop_downloaded + extra_downloaded + extra2_downloaded
            self.anzahlfiles_in_poster()
            self.anzahlfiles_in_backdrop()
            self.anzahlfiles_in_banner()
            self.anzahlfiles_in_infos()
            now = datetime.now()
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
            try:
                if os.path.exists("/tmp/urlo.html"):
                    os.remove("/tmp/urlo.html")
            except:
                pass
            with open("/tmp/xtra_report", "a+") as f:
                f.write("%s"%report)
            Screen.show(self)
            self.brokenImageRemove()
            self.brokenInfoRemove()
            self.cleanRam()
            return
# ---------------------------------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------------------------------
    def delete_oldfilesposter(self):
        # --------  hier alte files loeschen poster -------------------------
        logout(data="delete files start poster")
        logout(data=str(config.plugins.xtraEvent.deletFiles.value))
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
        logout(data="delete files start backdrop")
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
                # Überprüfen, ob es sich um eine Datei handelt
                if os.path.isfile(filepath):
                    # Das Änderungsdatum der Datei abrufen
                    mtime = os.path.getmtime(filepath)
                    modified_date = datetime.fromtimestamp(mtime).date()
                    # Überprüfen, ob das Änderungsdatum älter als das aktuelle Datum ist

                    if modified_date < zwei_tage_ago:
                        # Datei löschen
                        os.remove(filepath)
                        logout(data="delete files ende backdrop")
        else:
            logout(data="delete files off")

    def delete_oldfilesbanner(self):
        # --------  hier alte files loeschen backdrop -------------------------
        logout(data="delete files start backdrop")
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
                # Überprüfen, ob es sich um eine Datei handelt
                if os.path.isfile(filepath):
                    # Das Änderungsdatum der Datei abrufen
                    mtime = os.path.getmtime(filepath)
                    modified_date = datetime.fromtimestamp(mtime).date()
                    # Überprüfen, ob das Änderungsdatum älter als das aktuelle Datum ist

                    if modified_date < zwei_tage_ago:
                        # Datei löschen
                        os.remove(filepath)
                        logout(data="delete files ende backdrop")

        else:
            logout(data="delete files off")

    def delete_oldfilesinfos(self):
        # --------  hier alte files loeschen infos json -------------------------
        logout(data="delete files start infos")
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

    def delete_oldfilesnoinfos(self):
            # --------  hier alte files loeschen infos json -------------------------
            logout(data="delete files start infos")
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


    ####################################################################################################################################




    def prgrs(self, downloaded, n):
        self['status'].setText("Download : {} / {}".format(downloaded, n))
        self['progress'].setValue(int(100*downloaded//n))

    def showPoster(self, dwnldFile):
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
        self["Picture2"].instance.setPixmapFromFile("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film2.png")
        self["Picture2"].instance.setScale(1)
        self["Picture2"].show()

    def brokenImageRemove(self):
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
        os.system("echo 1 > /proc/sys/vm/drop_caches")
        os.system("echo 2 > /proc/sys/vm/drop_caches")
        os.system("echo 3 > /proc/sys/vm/drop_caches")


    def savePoster(self, dwn_path, url):
        from urllib.request import urlopen
        logout(data="")
        logout(data="")
        logout(data="------------------------------------------------------------------------------------------------------- def saveposter start")
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
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
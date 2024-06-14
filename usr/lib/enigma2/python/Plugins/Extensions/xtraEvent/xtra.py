#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by digiteng...06.2020, 11.2020, 11.2021, 12.2021, 01.2022
from __future__ import absolute_import
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
import Tools.Notifications
import os
import re
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, \
getConfigListEntry, ConfigSelection, ConfigText, ConfigInteger, ConfigSelectionNumber, \
ConfigDirectory, ConfigClock, NoSave
from Components.ConfigList import ConfigListScreen
from enigma import eTimer, eLabel, ePixmap, eSize, ePoint, loadJPG, eEPGCache, \
getDesktop, addFont, eServiceReference, eServiceCenter
from Components.Sources.StaticText import StaticText
from Screens.VirtualKeyBoard import VirtualKeyBoard
from PIL import Image
from Screens.LocationBox import LocationBox
import socket
import requests

from Components.ProgressBar import ProgressBar
from Screens.ChoiceBox import ChoiceBox
import shutil
from .xtraSelectionList import xtraSelectionList, xtraSelectionEntryComponent
from Plugins.Extensions.xtraEvent.skins.xtraSkins import *
from threading import Timer
from datetime import datetime
import time
# --------------------------- Logfile -------------------------------

from datetime import datetime, timedelta
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraevent-Xtra.log"

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
logout(data="start 6.75")

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


# =================================================================================================================
version = "v6.75"
# ==================================================================================================================


try:
    logout(data="xtra 2")
    import sys
    infoPY = sys.version_info[0]
    if infoPY == 3:
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
    logout(data="xtra 3")
    if config.plugins.xtraEvent.tmdbAPI.value != "":
        tmdb_api = config.plugins.xtraEvent.tmdbAPI.value
    else:
        logout(data="xtra 4")
        tmdb_api = "3c3efcf47c3577558812bb9d64019d65"
    if config.plugins.xtraEvent.tvdbAPI.value != "":
        logout(data="xtra 5")
        tvdb_api = config.plugins.xtraEvent.tvdbAPI.value
    else:
        logout(data="xtra 6")
        tvdb_api = "a99d487bb3426e5f3a60dea6d3d3c7ef"
    if config.plugins.xtraEvent.fanartAPI.value != "":
        logout(data="xtra 7")
        fanart_api = config.plugins.xtraEvent.fanartAPI.value
    else:
        logout(data="xtra 8")
        fanart_api = "6d231536dea4318a88cb2520ce89473b"
except:
    pass

try:
    logout(data="xtra 9")
    from Components.Language import language
    lang = language.getLanguage()
    lang = lang[:2]
except:
    logout(data="xtra 10")
    try:
        logout(data="xtra 11")
        lang = config.osd.language.value[:-3]
    except:
        logout(data="xtra 12")
        lang = "en"

lang_path = r"/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/languages"
try:
    logout(data="xtra 13")
    lng = ConfigParser()
    if infoPY == 3:
        lng.read(lang_path,	 encoding='utf8')
    else:
        lng.read(lang_path)
    lng.get(lang, "0")
except:
    try:
        lang="en"
        lng = ConfigParser()
        if infoPY == 3:
            lng.read(lang_path,	 encoding='utf8')
        else:
            lng.read(lang_path)
    except:
        pass

desktop_size = getDesktop(0).size().width()
epgcache = eEPGCache.getInstance()
logout(data="xtra 14")
#config.plugins.xtraEvent.searchType.value(default ='multi')
config.plugins.xtraEvent = ConfigSubsection()
config.plugins.xtraEvent.onoff = ConfigYesNo(default = True)
config.plugins.xtraEvent.skinSelect = ConfigSelection(default = "skin_1", choices = [("skin_1"), ("skin_2")])
config.plugins.xtraEvent.skinSelectColor = ConfigSelection(default = "#3478c1", choices = [
    ("#3478c1", "Blue"),
    ("#4682B4","Steel Blue"),
    ("#ea5b5b","Red"),
    ("#8B0000","Dark Red"),
    ("#8B4513","Saddle Brown"),
    ("#008080","Teal"),
    ("#4F4F4F","Gray31"),
    ("#4f5b66","Space Gray"),
    ("#008B8B","Dark Cyan"),
    ("#2E8B57","SeaGreen"),
    ])
config.plugins.xtraEvent.loc = ConfigDirectory(default='/tmp/')
config.plugins.xtraEvent.searchMOD = ConfigSelection(default = lng.get(lang, '13'), choices = [(lng.get(lang, '13')), (lng.get(lang, '14')), (lng.get(lang, '14a'))])
config.plugins.xtraEvent.searchNUMBER = ConfigSelectionNumber(0, 999, 1, default=50)
# ------------------------------------------------- hier 50 next events downloaden , ca fuer 1 Tag
# config.plugins.xtraEvent.timerMod = ConfigYesNo(default = False)
config.plugins.xtraEvent.timerMod = ConfigSelection(default="Clock", choices=[
    ("-1", _("Disable")),
    ("Period"),
    ("Clock"),
    ])

logout(data="xtra 16")
config.plugins.xtraEvent.timerHour = ConfigSelectionNumber(1, 168, 1, default=1)
config.plugins.xtraEvent.timerClock = ConfigClock(default=0)
config.plugins.xtraEvent.deletFiles = ConfigYesNo(default = True)

config.plugins.xtraEvent.searchMANUELnmbr = ConfigSelectionNumber(0, 999, 1, default=1)
config.plugins.xtraEvent.searchMANUELyear = ConfigInteger(default = 0, limits=(0, 9999))
config.plugins.xtraEvent.imgNmbr = ConfigSelectionNumber(0, 999, 1, default=1)
config.plugins.xtraEvent.searchModManuel = ConfigSelection(default = lng.get(lang, '16'), choices = [(lng.get(lang, '16')), (lng.get(lang, '17'))])
config.plugins.xtraEvent.EMCloc = ConfigDirectory(default='/media/hdd/movie/')
config.plugins.xtraEvent.apis = ConfigYesNo(default = False)
config.plugins.xtraEvent.tmdbAPI = ConfigText(default="", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.tvdbAPI = ConfigText(default="", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.omdbAPI = ConfigText(default="", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.fanartAPI = ConfigText(default="", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.searchMANUEL_EMC = ConfigText(default="movies name", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.searchMANUEL = ConfigText(default="event name", visible_width=100, fixed_size=False)
# config.plugins.xtraEvent.searchLang = ConfigText(default="", visible_width=100, fixed_size=False)

config.plugins.xtraEvent.searchLang = ConfigYesNo(default = True)
config.plugins.xtraEvent.tmdb = ConfigYesNo(default = True)
config.plugins.xtraEvent.tmdb_backdrop = ConfigYesNo(default = True)
config.plugins.xtraEvent.tvdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.tvdb_backdrop = ConfigYesNo(default = True)
config.plugins.xtraEvent.tvdb_banner = ConfigYesNo(default = True)
config.plugins.xtraEvent.maze = ConfigYesNo(default = False)
config.plugins.xtraEvent.fanart = ConfigYesNo(default = False)
config.plugins.xtraEvent.fanart_backdrop = ConfigYesNo(default = False)
config.plugins.xtraEvent.fanart_banner = ConfigYesNo(default = False)
config.plugins.xtraEvent.bing = ConfigYesNo(default = True)
config.plugins.xtraEvent.extra = ConfigYesNo(default = True)
config.plugins.xtraEvent.extra2 = ConfigYesNo(default = True)
config.plugins.xtraEvent.extra3 = ConfigYesNo(default = False)
config.plugins.xtraEvent.poster = ConfigYesNo(default = True)
config.plugins.xtraEvent.banner = ConfigYesNo(default = False)
config.plugins.xtraEvent.backdrop = ConfigYesNo(default = True)
config.plugins.xtraEvent.info = ConfigYesNo(default = True)
config.plugins.xtraEvent.infoOmdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.infoImdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.opt_Images = ConfigYesNo(default = False)
config.plugins.xtraEvent.cnfg = ConfigYesNo(default = True)
config.plugins.xtraEvent.cnfgSel = ConfigSelection(default = "poster", choices = [("poster"), ("banner"), ("backdrop"), ("EMC")])
config.plugins.xtraEvent.TMDBpostersize = ConfigSelection(default="w185", choices = [
    ("w92", "92x138"),
    ("w154", "154x231"),
    ("w185", "185x278"),
    ("w342", "342x513"),
    ("w500", "500x750"),
    ("w780", "780x1170"),
    ("original", "ORIGINAL")])
config.plugins.xtraEvent.TVDBpostersize = ConfigSelection(default="thumbnail", choices = [
    ("thumbnail", "340x500"),
    ("fileName", "original(680x1000)")])
config.plugins.xtraEvent.TMDBbackdropsize = ConfigSelection(default="w300", choices = [
    ("w300", "300x170"),
    ("w780", "780x440"),
    ("w1280", "1280x720"),
    ("original", "ORIGINAL")])
config.plugins.xtraEvent.TVDBbackdropsize = ConfigSelection(default="thumbnail", choices = [
    ("thumbnail", "640x360"),
    ("fileName", "original(1920x1080)")])
config.plugins.xtraEvent.FANART_Poster_Resize = ConfigSelection(default="10", choices = [
    ("10", "100x142"),
    ("5", "200x285"),
    ("3", "333x475"),
    ("2", "500x713"),
    ("1", "1000x1426")])
config.plugins.xtraEvent.FANART_Backdrop_Resize = ConfigSelection(default="2", choices = [
    ("2", "original/2"),
    ("1", "original")])
config.plugins.xtraEvent.imdb_Poster_size = ConfigSelection(default="185", choices = [
    ("185", "185x278"),
    ("344", "344x510"),
    ("500", "500x750")])
config.plugins.xtraEvent.PB = ConfigSelection(default="posters", choices = [
    ("posters", "Poster"),
    ("backdrops", "Backdrop")])
config.plugins.xtraEvent.srcs = ConfigSelection(default="TMDB", choices = [
    ('TMDB', 'TMDB'),
    ('TVDB', 'TVDB'),
    ('FANART', 'FANART'),
    ('IMDB(poster)', 'IMDB(poster)'),
    ('Bing', 'Bing'),
    ('Google', 'Google')])
config.plugins.xtraEvent.searchType = ConfigSelection(default="tv", choices = [
    ('tv', 'TV'),
    ('movie', 'MOVIE'),
    ('multi', 'MULTI')])
config.plugins.xtraEvent.FanartSearchType = ConfigSelection(default="tv", choices = [
    ('tv', 'TV'),
    ('movies', 'MOVIE')])
config.plugins.xtraEvent.TVDB_Banner_Size = ConfigSelection(default="1", choices = [
    ("1", "758x140"),
    ("2", "379x70"),
    ("4", "190x35")])
config.plugins.xtraEvent.FANART_Banner_Size = ConfigSelection(default="1", choices = [
    ("1", "1000x185"),
    ("2", "500x92"),
    ("4", "250x46"),
    ("8", "125x23")
    ])
logout(data="xtra configs ende")
# --------------------------------------------- check direktories -----------------------------------------------------
pathLoc = ""
logout(data="location")
logout(data=str(config.plugins.xtraEvent.loc.value))
pathLoc = "{}xtraEvent/".format(config.plugins.xtraEvent.loc.value)
logout(data="path location")
logout(data=str(pathLoc))





if not os.path.exists("{}poster".format(pathLoc)):
    os.makedirs("{}poster".format(pathLoc))

if not os.path.exists("{}poster/dummy".format(pathLoc)):
    os.makedirs("{}poster/dummy".format(pathLoc))

if not os.path.exists("{}banner".format(pathLoc)):
    os.makedirs("{}banner".format(pathLoc))

if not os.path.exists("{}banner/dummy".format(pathLoc)):
    os.makedirs("{}banner/dummy".format(pathLoc))

if not os.path.exists("{}backdrop".format(pathLoc)):
    os.makedirs("{}backdrop".format(pathLoc))

if not os.path.exists("{}backdrop/dummy".format(pathLoc)):
    os.makedirs("{}backdrop/dummy".format(pathLoc))

if not os.path.exists("{}infos".format(pathLoc)):
    os.makedirs("{}infos".format(pathLoc))

if not os.path.exists("{}logo/dummy".format(pathLoc)):
    os.makedirs("{}logo/dummy".format(pathLoc))

if not os.path.exists("{}logo".format(pathLoc)):
    os.makedirs("{}logo".format(pathLoc))

if not os.path.exists("{}infosomdb".format(pathLoc)):
    os.makedirs("{}infosomdb".format(pathLoc))

if not os.path.exists("{}noinfos".format(pathLoc)):
    os.makedirs("{}noinfos".format(pathLoc))

if not os.path.exists("{}mSearch".format(pathLoc)):
    os.makedirs("{}mSearch".format(pathLoc))

if not os.path.exists("{}EMC".format(pathLoc)):
    os.makedirs("{}EMC".format(pathLoc))

# ------------------------------- check angelegt vorhanden -----------------------------------------------------------

if os.path.exists("{}poster".format(pathLoc)):
    logout(data="poster vorhanden")

if os.path.exists("{}poster/dummy".format(pathLoc)):
    logout(data="poster/dummy vorhanden")

if os.path.exists("{}backdrop".format(pathLoc)):
    logout(data="backdrop vorhanden")

if os.path.exists("{}backdrop/dummy".format(pathLoc)):
    logout(data="backdrop/dummy vorhanden")

if os.path.exists("{}logo".format(pathLoc)):
    logout(data="logo vorhanden")

if os.path.exists("{}logo/dummy".format(pathLoc)):
    logout(data="logo/dummy vorhanden")

if os.path.exists("{}banner".format(pathLoc)):
    logout(data="banner vorhanden")

if os.path.exists("{}banner/dummy".format(pathLoc)):
    logout(data="banner/dummy vorhanden")

if os.path.exists("{}infos".format(pathLoc)):
    logout(data="infos vorhanden")

if os.path.exists("{}infosomdb".format(pathLoc)):
    logout(data="infosomdb vorhanden")

if os.path.exists("{}noinfos".format(pathLoc)):
    logout(data="noinfos vorhanden")

if os.path.exists("{}mSearch".format(pathLoc)):
    logout(data="mSearch vorhanden")

if os.path.exists("{}EMC".format(pathLoc)):
    logout(data="EMC vorhanden")



# ---------------------------------------------------------------------------------------------------------------------
logout(data="------------------ def check_movieList")
pathMovie = config.plugins.xtraEvent.EMCloc.value
pathXtra = os.path.join(config.plugins.xtraEvent.loc.value, "xtraEvent")
try:
    mlst = os.listdir(pathMovie)
    logout(data=str(mlst))
    if mlst:
        logout(data="movielist mlst")
        movieList = [x for x in mlst if x.endswith(".mvi") or x.endswith(".ts") or x.endswith(".mp4") or x.endswith(
                ".avi") or x.endswith(".mkv") or x.endswith(".divx")]
        logout(data=str(movieList))
        # name bearbeiten und als file rausschreiben
        file_path = os.path.join(pathMovie, "movielist.txt")
        if isfile(file_path):
            remove(file_path)
        with open(file_path, 'a') as file:
            for movie in movieList:
                # movie_name = movie.split('-')[-1].strip().rstrip('.ts')
                movie_name = movie.split('-')[-1].strip()
                #movie_name = re.search(r'\d{8} \d{4} - [^-]* - (.*?)(?:\.ts)?$', movie).group(1).strip()
                logout(data=str(movie_name))
                #movie_name = REGEX.sub('', movie_name).strip()
                movie_name = REGEX.sub('', movie_name).strip().rsplit(".", 1)[0].strip()
                logout(data=str(movie_name))

                poster_path = os.path.join(pathXtra, "EMC", f"{movie_name}-poster.jpg")
                backdrop_path = os.path.join(pathXtra, "EMC", f"{movie_name}-backdrop.jpg")
                info_path = os.path.join(pathXtra, "EMC", f"{movie_name}-info.json")
                logout(data=str(poster_path))
                poster_filename = f"{movie_name}.jpg"
                info_filename = f"{movie_name}.json"
                logout(data=str(poster_filename))
                poster_src_path = os.path.join(pathXtra, "poster", poster_filename)
                logout(data=str(poster_src_path))
                backdrop_src_path = os.path.join(pathXtra, "backdrop", poster_filename)
                logout(data=str(backdrop_src_path))
                info_src_path = os.path.join(pathXtra, "infos", info_filename)
                logout(data=str(info_src_path))
                EMCposter_dest_path = poster_path
                EMCbackdrop_dest_path = backdrop_path
                EMCinfo_dest_path = info_path
                logout(data=str(EMCposter_dest_path))
                logout(data="movie check in EMC")
                if not os.path.exists(poster_path):
                    logout(data="movie nicht in EMC vorhanden check in poster")
                    if os.path.exists(poster_src_path):
                        logout(data="movie in poster vorhanden copiert")
                        shutil.copy(poster_src_path, EMCposter_dest_path)
                        shutil.copy(backdrop_src_path, EMCbackdrop_dest_path)
                        shutil.copy(info_src_path, EMCinfo_dest_path)
                    else:
                        logout(data="movie nicht vorhanden schreibe in file")
                        file.write(movie_name + '\n')

except:
    pass





class xtra(Screen, ConfigListScreen):
    logout(data="xtra class screen")
    def __init__(self, session):
        logout(data="init")
        self.session = session
        Screen.__init__(self, session)

        if desktop_size <= 1280:
            if config.plugins.xtraEvent.skinSelect.value == 'skin_1':
                self.skin = xtra_720
            if config.plugins.xtraEvent.skinSelect.value == 'skin_2':
                self.skin = xtra_720_2
        else:
            if config.plugins.xtraEvent.skinSelect.value == 'skin_1':
                self.skin = xtra_1080
            if config.plugins.xtraEvent.skinSelect.value == 'skin_2':
                self.skin = xtra_1080_2

        list = []
        ConfigListScreen.__init__(self, list, session=session)

        self['key_red'] = Label(_('Close'))
        self['key_green'] = Label(_(lng.get(lang, '40')))
        self['key_yellow'] = Label(_(lng.get(lang, '75')))
        self['key_blue'] = Label(_(lng.get(lang, '18')))
        self["actions"] = ActionMap(["xtraEventAction"],
        {
            "left": self.keyLeft,
            "down": self.keyDown,
            "up": self.keyUp,
            "right": self.keyRight,
            "red": self.exit,
            "green": self.search,
            "yellow": self.update,
            "blue": self.ms,
            "cancel": self.exit,
            "ok": self.keyOK,
            "info": self.strg,
            "menu": self.menuS
        },-1)

        self.setTitle(_("xtraEvent {}".format(version)))
        self['status'] = Label()
        self['info'] = Label()
        self['int_statu'] = Label()
        self['help'] = StaticText()

        self.timer = eTimer()
        self.timer.callback.append(self.xtraList)
        self.onLayoutFinish.append(self.xtraList)
        self.intCheck()





    def intCheck(self):
        try:
            socket.setdefaulttimeout(2)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            self['int_statu'].setText("☻")
            return True
        except:
            self['int_statu'].hide()
            self['status'].setText(lng.get(lang, '68'))
            return False

    def strg(self):
        if config.plugins.xtraEvent.onoff.value:
            try:
                path_poster = "{}poster/".format(pathLoc)
                path_banner = "{}banner/".format(pathLoc)
                path_backdrop = "{}backdrop/".format(pathLoc)
                path_info = "{}infos/".format(pathLoc)
                folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(path_poster, fname)), files)) for path_poster, folders, files in os.walk(path_poster)])
                posters_sz = "%0.1f" % (folder_size//(1024*1024.0))
                poster_nmbr = len(os.listdir(path_poster))
                folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(path_banner, fname)), files)) for path_banner, folders, files in os.walk(path_banner)])
                banners_sz = "%0.1f" % (folder_size//(1024*1024.0))
                banner_nmbr = len(os.listdir(path_banner))
                folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(path_backdrop, fname)), files)) for path_backdrop, folders, files in os.walk(path_backdrop)])
                backdrops_sz = "%0.1f" % (folder_size//(1024*1024.0))
                backdrop_nmbr = len(os.listdir(path_backdrop))
                folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(path_info, fname)), files)) for path_info, folders, files in os.walk(path_info)])
                infos_sz = "%0.1f" % (folder_size//(1024*1024.0))
                info_nmbr = len(os.listdir(path_info))
                self['status'].setText(_(lng.get(lang, '48')))
                pstr = "Poster : {} poster {} MB".format(poster_nmbr, posters_sz)
                bnnr = "Banner : {} banner {} MB".format(banner_nmbr, banners_sz)
                bckdrp = "Backdrop : {} backdrop {} MB".format(backdrop_nmbr, backdrops_sz)
                inf = "Info : {} info {} MB".format(info_nmbr, infos_sz)
                pbbi = "\n".join([pstr, bnnr, bckdrp, inf])
                self['info'].setText(str(pbbi))
            except Exception as err:
                with open("/tmp/xtraEvent.log", "a+") as f:
                    f.write("xtra-info-strg, %s\n"%(err))
        else:
            self.exit()

    def keyOK(self):
        logout(data="key ok")
        if self['config'].getCurrent()[1] is config.plugins.xtraEvent.loc:

            self.session.openWithCallback(self.pathSelected, LocationBox, text=_('Default Folder'), currDir=config.plugins.xtraEvent.loc.getValue(), minFree=100)
        if self['config'].getCurrent()[1] is config.plugins.xtraEvent.cnfgSel:
            self.compressImg()

    def pathSelected(self, res):

        logout(data="path selected 509 ")
        logout(data=str(res))
        import shutil
        if res is not None:
            config.plugins.xtraEvent.loc.value = res
            pathLoc = "{}xtraEvent/".format(config.plugins.xtraEvent.loc.value)
            logout(data="path selected pathLoc ")
            logout(data=str(pathLoc))
            os.makedirs(pathLoc)
            if not os.path.isdir(pathLoc):
                pathLoc = "/tmp/"

            if not os.path.isdir(pathLoc):
                os.makedirs("{}poster".format(pathLoc))
                os.makedirs("{}poster/dummy".format(pathLoc))
                os.makedirs("{}banner".format(pathLoc))
                os.makedirs("{}banner/dummy".format(pathLoc))
                os.makedirs("{}backdrop".format(pathLoc))
                os.makedirs("{}backdrop/dummy".format(pathLoc))
                os.makedirs("{}infos".format(pathLoc))
                os.makedirs("{}logo".format(pathLoc))
                os.makedirs("{}logo/dummy".format(pathLoc))
                os.makedirs("{}infosomdb".format(pathLoc))
                os.makedirs("{}noinfos".format(pathLoc))
                os.makedirs("{}mSearch".format(pathLoc))
                os.makedirs("{}EMC".format(pathLoc))
                logout(data="path download copy bqts")

            self.updateFinish()
        logout(data="path selected nichts gemacht")
    # ------------------------------------------------ neue ordner checken ------------------------
    def pathCheck(self):

        if not os.path.isdir(pathLoc):

            logout(data="check neue ordner 523")
            logout(data=str(pathLoc))
            os.makedirs("{}poster".format(pathLoc))
            os.makedirs("{}banner".format(pathLoc))
            os.makedirs("{}backdrop".format(pathLoc))
            os.makedirs("{}infos".format(pathLoc))
            os.makedirs("{}logo".format(pathLoc))
            os.makedirs("{}logo/dummy".format(pathLoc))
            os.makedirs("{}noinfos".format(pathLoc))
            os.makedirs("{}mSearch".format(pathLoc))
            os.makedirs("{}EMC".format(pathLoc))
            os.makedirs("{}poster/dummy".format(pathLoc))
            os.makedirs("{}banner/dummy".format(pathLoc))
            os.makedirs("{}backdrop/dummy".format(pathLoc))

            logout(data="check neue ordner neu angelegt 536")
        else:
            logout(data="check neue ordner vorhanden 538")


    def delay(self):
        logout(data="delay")
        self.timer.start(100, True)

    def xtraList(self):
        logout(data="xtraList")
        for x in self["config"].list:
            if len(x) > 1:
                x[1].save()
        on_color = "\\c0000??00"
        off_color = "\\c00??0000"
        list = []
# CONFIG_________________________________________________________________________________________________________________

        if config.plugins.xtraEvent.onoff.value:
            list.append(getConfigListEntry("{}◙ \\c00?????? {}".format(on_color, lng.get(lang, '0')), config.plugins.xtraEvent.onoff, _(lng.get(lang, '0'))))
            list.append(getConfigListEntry("♥  {}".format(lng.get(lang, '1')), config.plugins.xtraEvent.cnfg, _(lng.get(lang, '2'))))
            list.append(getConfigListEntry("Delete Files 3 Day old on", config.plugins.xtraEvent.deletFiles, _(lng.get(lang, '4'))))

            list.append(getConfigListEntry("—"*100))
            if config.plugins.xtraEvent.cnfg.value:
                if config.plugins.xtraEvent.loc.value:
                    list.append(getConfigListEntry("{}".format(lng.get(lang, '3')), config.plugins.xtraEvent.loc, _(lng.get(lang, '4'))))
                else:
                    list.append(getConfigListEntry("{}{}".format(off_color, lng.get(lang, '3')), config.plugins.xtraEvent.loc, _(lng.get(lang, '4'))))
                list.append(getConfigListEntry(lng.get(lang, '5'), config.plugins.xtraEvent.skinSelect, _(lng.get(lang, '19'))))
                if config.plugins.xtraEvent.skinSelect.value == 'skin_1':
                    list.append(getConfigListEntry("   {}".format(lng.get(lang, '69')), config.plugins.xtraEvent.skinSelectColor, _(lng.get(lang, '19'))))
                list.append(getConfigListEntry(lng.get(lang, '6'), config.plugins.xtraEvent.opt_Images, _(lng.get(lang, '7'))))
                if config.plugins.xtraEvent.opt_Images.value:
                    list.append(getConfigListEntry("\t{}".format(lng.get(lang, '7')), config.plugins.xtraEvent.cnfgSel, _(lng.get(lang, '21'))))
                list.append(getConfigListEntry(lng.get(lang, '22'), config.plugins.xtraEvent.apis, _("...")))
                if config.plugins.xtraEvent.apis.value:
                    list.append(getConfigListEntry("	TMDB API", config.plugins.xtraEvent.tmdbAPI, _(lng.get(lang, '23'))))
                    list.append(getConfigListEntry("	TVDB API", config.plugins.xtraEvent.tvdbAPI, _(lng.get(lang, '23'))))
                    list.append(getConfigListEntry("	OMDB API", config.plugins.xtraEvent.omdbAPI, _(lng.get(lang, '23'))))
                    list.append(getConfigListEntry("	FANART API", config.plugins.xtraEvent.fanartAPI, _(lng.get(lang, '23'))))
                list.append(getConfigListEntry("—"*100))
                list.append(getConfigListEntry(lng.get(lang, '8'), config.plugins.xtraEvent.searchMOD, _(lng.get(lang, '24'))))
                list.append(getConfigListEntry(lng.get(lang, '9'), config.plugins.xtraEvent.searchNUMBER, _(lng.get(lang, '25'))))
                list.append(getConfigListEntry(lng.get(lang, '10'), config.plugins.xtraEvent.searchLang, _(lng.get(lang, '26'))))

                list.append(getConfigListEntry(lng.get(lang, '11'), config.plugins.xtraEvent.timerMod, _(lng.get(lang, '27'))))
                if config.plugins.xtraEvent.timerMod.value:
                    if config.plugins.xtraEvent.timerMod.value == "Period":
                        list.append(getConfigListEntry(lng.get(lang, '46'), config.plugins.xtraEvent.timerHour, _(lng.get(lang, '67'))))
                    elif config.plugins.xtraEvent.timerMod.value == "Clock":
                        list.append(getConfigListEntry(lng.get(lang, '46'), config.plugins.xtraEvent.timerClock, _(lng.get(lang, '67'))))


                list.append(getConfigListEntry("—"*100))
            list.append(getConfigListEntry(" ▀ {}".format(lng.get(lang, '28'))))
            list.append(getConfigListEntry("_"*100))
    # poster__________________________________________________________________________________________________________________
            list.append(getConfigListEntry("POSTER", config.plugins.xtraEvent.poster, _("...")))
            if config.plugins.xtraEvent.poster.value == True:
                list.append(getConfigListEntry("\tTMDB", config.plugins.xtraEvent.tmdb, _(" "),))
                if config.plugins.xtraEvent.tmdb.value :
                    list.append(getConfigListEntry("\t	Tmdb Poster {}".format(lng.get(lang, '49')), config.plugins.xtraEvent.TMDBpostersize, _(" ")))
                    list.append(getConfigListEntry("\t	  {}".format(lng.get(lang, '63')), config.plugins.xtraEvent.searchType, _(" ")))
                list.append(getConfigListEntry("\tTVDB", config.plugins.xtraEvent.tvdb, _(lng.get(lang, '29'))))
                if config.plugins.xtraEvent.tvdb.value :
                    list.append(getConfigListEntry("\t	Tvdb Poster {}".format(lng.get(lang, '49')), config.plugins.xtraEvent.TVDBpostersize, _(" ")))
                list.append(getConfigListEntry("\tFANART", config.plugins.xtraEvent.fanart, _(lng.get(lang, '29'))))
                if config.plugins.xtraEvent.fanart.value:
                    list.append(getConfigListEntry("\t	Fanart Poster {}".format(lng.get(lang, '49')), config.plugins.xtraEvent.FANART_Poster_Resize, _(" ")))
                list.append(getConfigListEntry("\tMAZE(TV SHOWS)", config.plugins.xtraEvent.maze, _(" ")))
                list.append(getConfigListEntry("_"*100))
    # banner__________________________________________________________________________________________________________________
            list.append(getConfigListEntry("BANNER", config.plugins.xtraEvent.banner, _(" ")))
            if config.plugins.xtraEvent.banner.value == True:
                list.append(getConfigListEntry("\tTVDB", config.plugins.xtraEvent.tvdb_banner, _(" ")))
                if config.plugins.xtraEvent.tvdb_banner.value :
                    list.append(getConfigListEntry("\t	Tvdb Banner {}".format(lng.get(lang, '49')), config.plugins.xtraEvent.TVDB_Banner_Size, _(" ")))
                list.append(getConfigListEntry("\tFANART", config.plugins.xtraEvent.fanart_banner, _(" ")))
                if config.plugins.xtraEvent.fanart_banner.value :
                    list.append(getConfigListEntry("\t	Fanart Banner {}".format(lng.get(lang, '49')), config.plugins.xtraEvent.FANART_Banner_Size, _(" ")))
                list.append(getConfigListEntry("_"*100))
    # backdrop_______________________________________________________________________________________________________________
            list.append(getConfigListEntry("BACKDROP", config.plugins.xtraEvent.backdrop, _(" ")))
            if config.plugins.xtraEvent.backdrop.value == True:
                list.append(getConfigListEntry("\tTMDB", config.plugins.xtraEvent.tmdb_backdrop, _(" ")))
                if config.plugins.xtraEvent.tmdb_backdrop.value :
                    list.append(getConfigListEntry("\t	Tmdb Backdrop {}".format(lng.get(lang, '49')), config.plugins.xtraEvent.TMDBbackdropsize, _(" ")))
                    list.append(getConfigListEntry("\t	  {}".format(lng.get(lang, '63')), config.plugins.xtraEvent.searchType, _(" ")))
                list.append(getConfigListEntry("\tTVDB", config.plugins.xtraEvent.tvdb_backdrop, _(" ")))
                if config.plugins.xtraEvent.tvdb_backdrop.value :
                    list.append(getConfigListEntry("\t	Tvdb Backdrop {}".format(lng.get(lang, '49')), config.plugins.xtraEvent.TVDBbackdropsize, _(" ")))
                list.append(getConfigListEntry("\tFANART", config.plugins.xtraEvent.fanart_backdrop, _(" ")))
                if config.plugins.xtraEvent.fanart_backdrop.value:
                    list.append(getConfigListEntry("\t	Fanart Backdrop {}".format(lng.get(lang, '49')), config.plugins.xtraEvent.FANART_Backdrop_Resize, _(" ")))
                list.append(getConfigListEntry("\tEXTRA", config.plugins.xtraEvent.extra, _(lng.get(lang, '30'))))
                list.append(getConfigListEntry("\tEXTRA-2", config.plugins.xtraEvent.extra2, _(lng.get(lang, '31'))))
                list.append(getConfigListEntry("_"*100))
    # info___________________________________________________________________________________________________________________
            list.append(getConfigListEntry("INFO", config.plugins.xtraEvent.info, _(lng.get(lang, '32'))))
            # if config.plugins.xtraEvent.info.value == True:
                # list.append(getConfigListEntry("\tOMDB", config.plugins.xtraEvent.infoOmdb, _(" ")))
                # list.append(getConfigListEntry("\tIMDB", config.plugins.xtraEvent.infoImdb, _(" ")))
            list.append(getConfigListEntry("EXTRA-3", config.plugins.xtraEvent.extra3, _(lng.get(lang, '64'))))
            list.append(getConfigListEntry("_"*100))
        else:
            list.append(getConfigListEntry("{}◙ \\c00?????? {}".format(off_color, lng.get(lang, '0')), config.plugins.xtraEvent.onoff, _(lng.get(lang, '0'))))



        # self["config"].l.setItemHeight(50)
        self["config"].list = list
        self["config"].l.setList(list)
        self.help()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.delay()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.delay()

    def keyDown(self):
        self["config"].instance.moveSelection(self["config"].instance.moveDown)
        self.delay()

    def keyUp(self):
        self["config"].instance.moveSelection(self["config"].instance.moveUp)
        self.delay()

    def pageUp(self):
        self["config"].instance.moveSelection(self["config"].instance.pageDown)
        self.delay()

    def pageDown(self):
        self["config"].instance.moveSelection(self["config"].instance.pageUp)
        self.delay()

    def help(self):
        cur = self["config"].getCurrent()
        if cur:
            self["help"].text = cur[2]

    def menuS(self):
        logout(data="------------------ def menuS")
        if config.plugins.xtraEvent.onoff.value:
            list = [(_(lng.get(lang, '50')), self.brokenImageRemove), (_(lng.get(lang, '73')), self.removeImagesAll),\
            (_(lng.get(lang, "75")), self.update), (_(lng.get(lang, '35')), self.exit)]
            self.session.openWithCallback(self.menuCallback, ChoiceBox, title=_('xtraEvent...'), list=list)
        else:
            self.exit()

    def update(self):
        logout(data="------------------ def update")
        try:
            url = requests.get("https://api.github.com/repos/digiteng/xtra/releases/latest")
            new_version = url.json()["name"]
            if version != new_version:
                msg = url.json()["body"]
                up_msg = "Current version : {}\n\\c00bb?fbbNew version : {} \n\n\\c00bb?fee{}\n\n\\c00??????Do you want UPDATE PLUGIN ?..".format(version, new_version, msg)
                self.session.openWithCallback(self.instalUpdate, MessageBox, _(up_msg), MessageBox.TYPE_YESNO)
            else:
                self['info'].setText(lng.get(lang, '71'))
        except Exception as err:
            self['info'].setText(str(err))
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("update %s\n\n"%err)

    def instalUpdate(self, answer):
        logout(data="------------------ def installUpdate")
        try:
            if answer is True:
                url = requests.get("https://api.github.com/repos/digiteng/xtra/releases/latest")
                update_url = url.json()["assets"][1]["browser_download_url"]
                up_name	 = url.json()["assets"][1]["name"]
                up_tmp = "/tmp/{}".format(up_name)
                if not os.path.exists(up_tmp):
                    open(up_tmp, 'wb').write(requests.get(update_url, stream=True, allow_redirects=True).content)
                if os.path.exists(up_tmp):
                    from enigma import eConsoleAppContainer
                    cmd = ("rm -rf /usr/lib/enigma2/python/Components/Converter/xtra* \
                    | rm -rf /usr/lib/enigma2/python/Components/Renderer/xtra* \
                    | rm -rf /usr/lib/enigma2/python/Plugins/Extensions/xtraEvent \
                    | rm -rf /usr/share/enigma2/xtra \
                    ")
                    os.system(cmd)
                    container = eConsoleAppContainer()
                    container.execute("tar xf /tmp/xtraEvent.tar.gz -C /")
                    self.updateFinish()
            else:
                self.close()
        except Exception as err:
            self['info'].setText(str(err))
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("instalUpdate %s\n\n"%err)

    def updateFinish(self):
        logout(data="------------------ def updateFinish")
        for x in self["config"].list:
            if len(x) > 1:
                x[1].save()
        logout(data="------------------ def updateFinish configfile save")
        configfile.save()
        logout(data="------------------ def updateFinish configfile save ende")
        self.session.openWithCallback(self.restarte2, MessageBox, _(lng.get(lang, '70')), MessageBox.TYPE_YESNO)

    def restarte2(self, answer):
        logout(data="------------------ def restart2")
        if answer:
            self.session.open(TryQuitMainloop, 3)

    def removeImagesAll(self):
        logout(data="------------------ def removeImagesAll")
        self.session.openWithCallback(self.removeImagesAllYes, MessageBox, _(lng.get(lang, '73')), MessageBox.TYPE_YESNO)

    def removeImagesAllYes(self, answer):
        logout(data="------------------ def removeImagesAllYes")
        if answer:
            import shutil
            pathLoc = "{}xtraEvent/".format(config.plugins.xtraEvent.loc.value)
            logout(data="path download")
            if os.path.isdir(pathLoc):
                shutil.rmtree(pathLoc)
            if not os.path.isdir(pathLoc):
                logout(data="path download anlegen")
                os.makedirs("{}poster".format(pathLoc))
                os.makedirs("{}banner".format(pathLoc))
                os.makedirs("{}backdrop".format(pathLoc))
                os.makedirs("{}infos".format(pathLoc))
                os.makedirs("{}mSearch".format(pathLoc))
                os.makedirs("{}EMC".format(pathLoc))


            self.updateFinish()

    def compressImg(self):
        logout(data="------------------ def compressImg")
        try:
            filepath = "{}{}".format(pathLoc, config.plugins.xtraEvent.cnfgSel.value)
            folder_size = sum([sum([os.path.getsize(os.path.join(filepath, fname)) for fname in files]) for filepath, folders, files in os.walk(filepath)])
            old_size = "%0.1f" % (folder_size//1024)
            if os.path.exists(filepath):
                lstdr = os.listdir(filepath)
                for j in lstdr:
                    try:
                        filepath = "".join([filepath, "/", j])
                        if os.path.isfile(filepath):
                            im = Image.open(filepath)
                            im.save(filepath, optimize=True, quality=80)
                    except:
                        pass
                folder_size = sum([sum([os.path.getsize(os.path.join(filepath, fname)) for fname in files]) for filepath, folders, files in os.walk(filepath)])
                new_size = "%0.1f" % (folder_size//1024)
                self['info'].setText(_("{} images optimization end...\nGain : {}KB to {}KB".format(len(lstdr), old_size, new_size)))
        except Exception as err:
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("compressImg, %s\n"%(err))
            self['info'].setText(str(err))


    def brokenImageRemove(self):
        logout(data="------------------ def brokenImageRemove")
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
        self['info'].setText(_("Removed Broken Images : {}".format(str(rmvd))))

    def menuCallback(self, ret = None):
        logout(data="------------------ def menuCallback")
        ret and ret[1]()

    def search(self):
        logout(data="------------------ def search")
        if config.plugins.xtraEvent.onoff.value:
            if pathLoc != "":
                from . import download
                if config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '14'):
                    self.session.open(download.downloads)
                if config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '13'):
                    self.session.open(selBouquets)
                elif config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '14a'):
                    self.session.open(selBouquets)
            else:
                self.session.open(MessageBox, _(lng.get(lang, '4')), MessageBox.TYPE_INFO, timeout = 10)
                self.session.open(selBouquets)
        else:
            self.exit()

    def ms(self):
        if config.plugins.xtraEvent.onoff.value:
            if pathLoc != "":
                self.session.open(manuelSearch)
            else:
                self.session.open(MessageBox, _(lng.get(lang, '4')), MessageBox.TYPE_INFO, timeout = 10)
        else:
            self.exit()

    def exit(self):
        logout(data="-------------------  def exit")
        if self['config'].getCurrent()[1] is config.plugins.xtraEvent.skinSelectColor or self['config'].getCurrent()[1] is config.plugins.xtraEvent.skinSelect:
            from Plugins.Extensions.xtraEvent.skins import xtraSkins
            from six.moves import reload_module
            reload_module(xtraSkins)
            for x in self["config"].list:
                if len(x)>1:
                    x[1].save()
                configfile.save()
            self.close()
        for x in self["config"].list:
            if len(x) > 1:
                x[1].save()
        configfile.save()
        try:
            logout(data="def exit clock")
            if config.plugins.xtraEvent.timerMod.value == "Clock":
                logout(data="def exit ist clock")
                tc = config.plugins.xtraEvent.timerClock.value
                logout(data=str(tc))

                dt = datetime.today()
                logout(data="date time")
                logout(data=str(dt))

                #setclk = dt.replace(day=dt.day+1, hour=tc[0], minute=tc[1], second=0, microsecond=0)
                offset = tc[0] * 60 + tc[1]  # Offset in Minuten umrechnen
                setclk = datetime.today() + timedelta(minutes=offset)
                logout(data="set clock")
                logout(data=str(setclk))

                ds = setclk - dt
                logout(data="clock - dt")
                logout(data=str(ds))

                secs = ds.seconds + 1
                logout(data="seconds")
                logout(data=str(secs))

                def startDownload():
                    logout(data="start download")
                    from . import download
                    download.downloads("").save()
                    logout(data="ende download")

                logout(data="timer")
                t = Timer(secs, startDownload)
                logout(data="timer start")
                logout(data=str(t))
                t.start()

            self.close()
        except Exception as err:
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("timer clock, %s\n"%(err))

class manuelSearch(Screen, ConfigListScreen):
    logout(data="---------------- def manuelSearchScreen")
    logout(data=str(version))
    def __init__(self, session):
        logout(data="init")
        Screen.__init__(self, session)
        if desktop_size <= 1280:
            if config.plugins.xtraEvent.skinSelect.value == 'skin_1':
                self.skin = manuel_720
            if config.plugins.xtraEvent.skinSelect.value == 'skin_2':
                self.skin = manuel_720_2
        else:
            if config.plugins.xtraEvent.skinSelect.value == 'skin_1':
                self.skin = manuel_1080
            if config.plugins.xtraEvent.skinSelect.value == 'skin_2':
                self.skin = manuel_1080_2
        self.title = ""
        self.year = ""
        self.evnt = ""

        list = []
        ConfigListScreen.__init__(self, list, session=session)
        self.setTitle(_(lng.get(lang, '18')))

        self["key_red"] = StaticText(_(lng.get(lang, '35')))
        self["key_green"] = StaticText(_(lng.get(lang, '40')))
        self["key_yellow"] = StaticText(_(lng.get(lang, '65')))
        self["key_blue"] = StaticText(_("Keyboard"))
        self["actions"] = ActionMap(["xtraEventAction"],
            {
                "left": self.keyLeft,
                "right": self.keyRight,
                "cancel": self.stop,
                "red": self.stop,
                "ok": self.keyOK,
                "green": self.mnlSrch,
                "yellow": self.append,
                "blue": self.vk
            }, -2)
        self['status'] = Label()
        self['info'] = Label()
        self['Picture'] = Pixmap()
        self['Picture2'] = Pixmap()
        self['int_statu'] = Label()
        self['progress'] = ProgressBar()
        self['progress'].setRange((0, 100))
        self['progress'].setValue(0)

        #testver = (_("Neu"))
        testver = version
        self.testver = testver
        self["testver"] = Label()

        self.timer = eTimer()
        self.timer.callback.append(self.msList)
        self.timer.callback.append(self.picShow)
        self.onLayoutFinish.append(self.msList)
        self.onLayoutFinish.append(self.intCheck)




    def stop(self):
        logout(data="------------------ def stop")
        time.sleep(1)
        #f.close()
        logout(data="warten file closed sonst wie schreibgeschuetzt ")
        self.close()

    def intCheck(self):
        logout(data="------------------ def intCheck")
        self["testver"].setText("%s " % (self.testver))
        try:
            socket.setdefaulttimeout(2)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            self['int_statu'].setText("☻")
            return True
        except:
            self['int_statu'].hide()
            self['status'].setText(lng.get(lang, '68'))
            return False

    def keyOK(self):
        logout(data="------------------ def keyOK")
        if self['config'].getCurrent()[1] is config.plugins.xtraEvent.EMCloc:
            self.session.openWithCallback(self.pathSelected, LocationBox, text=_('Default Folder'), currDir=config.plugins.xtraEvent.EMCloc.getValue(), minFree=100)

    def pathSelected(self, res):
        logout(data="------------------ def pathSelected")
        if res is not None:
            config.plugins.xtraEvent.EMCloc.value = res
            pathLoc = config.plugins.xtraEvent.EMCloc.value
        return

    def delay(self):
        logout(data="------------------ def delay")
        self.timer.start(100, True)

    def msList(self):
        logout(data="------------------ def msList")
        self["Picture2"].instance.setPixmapFromFile("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film2.png")
        self["Picture2"].instance.setScale(1)
        self["Picture2"].show()
        for x in self["config"].list:
            if len(x) > 1:
                x[1].save()
        list = []
        list.append(getConfigListEntry(_(lng.get(lang, '59')), config.plugins.xtraEvent.searchModManuel))
        list.append(getConfigListEntry(_(lng.get(lang, '57')), config.plugins.xtraEvent.searchMANUELnmbr))
        if config.plugins.xtraEvent.searchModManuel.value == lng.get(lang, '17'):
            list.append(getConfigListEntry(_(lng.get(lang, '60')), config.plugins.xtraEvent.EMCloc))
        list.append(getConfigListEntry(_("Year"), config.plugins.xtraEvent.searchMANUELyear))
        list.append(getConfigListEntry(_(lng.get(lang, '10')), config.plugins.xtraEvent.searchLang))
        list.append(getConfigListEntry(_(lng.get(lang, '61')), config.plugins.xtraEvent.PB))
        list.append(getConfigListEntry(_(lng.get(lang, '62')), config.plugins.xtraEvent.srcs))
        if config.plugins.xtraEvent.srcs.value == "TMDB":
            list.append(getConfigListEntry(_(lng.get(lang, '63')), config.plugins.xtraEvent.searchType))
            if config.plugins.xtraEvent.PB.value == "posters":
                list.append(getConfigListEntry(_("\t{}".format(lng.get(lang, '49'))), config.plugins.xtraEvent.TMDBpostersize))
            else:
                list.append(getConfigListEntry(_("\t{}".format(lng.get(lang, '49'))), config.plugins.xtraEvent.TMDBbackdropsize))
        if config.plugins.xtraEvent.srcs.value == "TVDB":
            if config.plugins.xtraEvent.PB.value == "posters":
                list.append(getConfigListEntry(_("\t{}".format(lng.get(lang, '49'))), config.plugins.xtraEvent.TVDBpostersize))
            else:
                list.append(getConfigListEntry(_("\t{}".format(lng.get(lang, '49'))), config.plugins.xtraEvent.TVDBbackdropsize))
        if config.plugins.xtraEvent.srcs.value == "FANART":
            list.append(getConfigListEntry(_("\tSearch Type"), config.plugins.xtraEvent.FanartSearchType))
            if config.plugins.xtraEvent.PB.value == "posters":
                list.append(getConfigListEntry(_("\t{}".format(lng.get(lang, '49'))), config.plugins.xtraEvent.FANART_Poster_Resize))
            else:
                list.append(getConfigListEntry(_("\t{}".format(lng.get(lang, '49'))), config.plugins.xtraEvent.FANART_Backdrop_Resize))
        if config.plugins.xtraEvent.srcs.value == "IMDB(poster)":
            list.append(getConfigListEntry(_("\t{}".format(lng.get(lang, '49'))), config.plugins.xtraEvent.imdb_Poster_size))
        list.append(getConfigListEntry("—"*50))
        list.append(getConfigListEntry(_(lng.get(lang, '58')), config.plugins.xtraEvent.imgNmbr))
        list.append(getConfigListEntry("—"*50))
        self["config"].list = list
        self["config"].l.setList(list)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        if self['config'].getCurrent()[0] == lng.get(lang, '57'):
            self.curEpg()
        self.delay()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        if self['config'].getCurrent()[0] == lng.get(lang, '57'):
            self.curEpg()
        self.delay()

    def curEpg(self):
        logout(data="------------------ def curEpg")
        if config.plugins.xtraEvent.searchModManuel.value == lng.get(lang, '16'):
            try:
                events = ""
                ref = self.session.nav.getCurrentlyPlayingServiceReference().toString()
                events = epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
                if events:
                    n = config.plugins.xtraEvent.searchMANUELnmbr.value
                    self.evnt = events[int(n)][4]
                    self.vkEdit("")
            except:
                pass
        if config.plugins.xtraEvent.searchModManuel.value == lng.get(lang, '17'):
            self.movieList()

    def movieList(self):
        logout(data="------------------ def movieList")

        pathLoc = "/media/hdd/movie/movielist.txt"
        try:
            with open(pathLoc, "r") as file:
                movieList = file.readlines()
                logout(data=str(movieList))


                if movieList:
                    logout(data="movielist if")
                    n = config.plugins.xtraEvent.searchMANUELnmbr.value
                    self.evnt = movieList[int(n)]
                    self.vkEdit("")
        except:
            pass


    def movieList2(self):
        logout(data="------------------ def movieList")
        pathLoc = config.plugins.xtraEvent.EMCloc.value


        try:
            mlst = os.listdir(pathLoc)
            logout(data=str(mlst))
            if mlst:
                logout(data="movielist mlst")
                movieList = [x for x in mlst if x.endswith(".mvi") or x.endswith(".ts") or x.endswith(".mp4") or x.endswith(".avi") or x.endswith(".mkv") or x.endswith(".divx")]
                logout(data=str(movieList))

                if movieList:
                    logout(data="movielist if")
                    n = config.plugins.xtraEvent.searchMANUELnmbr.value
                    self.evnt = movieList[int(n)]

                    self.vkEdit("")
        except:
            pass

    def vk(self):
        logout(data="------------------ def vk")
        self.session.openWithCallback(self.vkEdit, VirtualKeyBoard, title=lng.get(lang, '39'), text = self.evnt)

    def vkEdit(self, text=None):
        logout(data="------------------ def vkEdit")
        if text:
            config.plugins.xtraEvent.searchMANUEL = ConfigText(default="{}".format(text), visible_width=100, fixed_size=False)
            config.plugins.xtraEvent.searchMANUEL_EMC = ConfigText(default="{}".format(text), visible_width=100, fixed_size=False)
            if config.plugins.xtraEvent.searchModManuel.value == lng.get(lang, '16'):
                self.title = config.plugins.xtraEvent.searchMANUEL.value
            if config.plugins.xtraEvent.searchModManuel.value == lng.get(lang, '17'):
                self.title = config.plugins.xtraEvent.searchMANUEL_EMC.value
                self.title = self.title.split('-')[-1].split(".")[0].strip()
            self['status'].setText(_("Search : {}".format(str(self.title))))
        else:
            config.plugins.xtraEvent.searchMANUEL = ConfigText(default="{}".format(self.evnt), visible_width=100, fixed_size=False)
            config.plugins.xtraEvent.searchMANUEL_EMC = ConfigText(default="{}".format(self.evnt), visible_width=100, fixed_size=False)
            if config.plugins.xtraEvent.searchModManuel.value == lng.get(lang, '16'):
                self.title = config.plugins.xtraEvent.searchMANUEL.value
            if config.plugins.xtraEvent.searchModManuel.value == lng.get(lang, '17'):
                self.title = config.plugins.xtraEvent.searchMANUEL_EMC.value
                self.title = self.title.split('-')[-1].split(".")[0].strip()
            self['status'].setText(_("Search : {}".format(str(self.title))))

    def mnlSrch(self):
        logout(data="------------------ def mnlSrch")
        try:
            fs = os.listdir("{}mSearch/".format(pathLoc))
            logout(data="def mnlSrch fs")
            logout(data=str(fs))

            for f in fs:
                os.remove("{}mSearch/{}".format(pathLoc, f))
        except:
            logout(data="def mnlSrch return")
            return
        if config.plugins.xtraEvent.PB.value == "posters":
            logout(data="def mnlSrch poster")
            if config.plugins.xtraEvent.srcs.value == "TMDB":
                start_new_thread(self.tmdb, ())
            if config.plugins.xtraEvent.srcs.value == "TVDB":
                start_new_thread(self.tvdb, ())
            if config.plugins.xtraEvent.srcs.value == "FANART":
                start_new_thread(self.fanart, ())
            if config.plugins.xtraEvent.srcs.value == "IMDB(poster)":
                start_new_thread(self.imdb, ())
            if config.plugins.xtraEvent.srcs.value == "Bing":
                start_new_thread(self.bing, ())
            if config.plugins.xtraEvent.srcs.value == "Google":
                start_new_thread(self.google, ())
        if config.plugins.xtraEvent.PB.value == "backdrops":
            if config.plugins.xtraEvent.srcs.value == "TMDB":
                start_new_thread(self.tmdb, ())
            if config.plugins.xtraEvent.srcs.value == "TVDB":
                start_new_thread(self.tvdb, ())
            if config.plugins.xtraEvent.srcs.value == "FANART":
                start_new_thread(self.fanart, ())
            if config.plugins.xtraEvent.srcs.value == "Bing":
                start_new_thread(self.bing, ())
            if config.plugins.xtraEvent.srcs.value == "Google":
                start_new_thread(self.google, ())

    def picShow(self):
        logout(data="------------------ def pecShow")
        self["Picture2"].hide()
        try:
            self.iNmbr = config.plugins.xtraEvent.imgNmbr.value

            self.path = "{}mSearch/{}-{}-{}.jpg".format(pathLoc, self.title, config.plugins.xtraEvent.PB.value, self.iNmbr)
            if config.plugins.xtraEvent.srcs.value == "IMDB(poster)":
                self.path = "{}mSearch/{}-poster-1.jpg".format(pathLoc, self.title)
            self["Picture"].instance.setPixmap(loadJPG(self.path))
            self["Picture"].instance.setScale(1)
            self["Picture"].show()
            if desktop_size <= 1280:
                if config.plugins.xtraEvent.PB.value == "posters":
                    self["Picture"].instance.setScale(1)
                    self["Picture"].instance.resize(eSize(185,278))
                    self["Picture"].instance.move(ePoint(930,325))
                else:
                    self["Picture"].instance.setScale(1)
                    self["Picture"].instance.resize(eSize(300,170))
                    self["Picture"].instance.move(ePoint(890,375))
            else:
                if config.plugins.xtraEvent.PB.value == "posters":
                    self["Picture"].instance.setScale(1)
                    self["Picture"].instance.resize(eSize(185,278))
                    self["Picture"].instance.move(ePoint(1450,550))
                else:
                    self["Picture"].instance.setScale(1)
                    self["Picture"].instance.resize(eSize(300,170))
                    self["Picture"].instance.move(ePoint(1400,600))
            self['Picture'].show()
            self.inf()
        except:
            pass

    def inf(self):
        logout(data="------------------ def inf")
        pb_path = ""
        pb_sz = ""
        tot = ""
        cur = ""
        try:
            msLoc = "{}mSearch/".format(pathLoc)
            n = 0
            for file in os.listdir(msLoc):
                if file.startswith("{}-{}".format(self.title, config.plugins.xtraEvent.PB.value)) == True:
                    e = os.path.join(msLoc, file)
                    n += 1
            tot = n
            cur = config.plugins.xtraEvent.imgNmbr.value
            pb_path = "{}mSearch/{}-{}-{}.jpg".format(pathLoc , self.title, config.plugins.xtraEvent.PB.value, self.iNmbr)
            pb_sz = "{} KB".format(os.path.getsize(pb_path)//1024)
            im = Image.open(pb_path)
            pb_res = im.size
            self['info'].setText(_("{}/{} - {} - {}".format(cur, tot, pb_sz, pb_res)))
        except:
            pass
# ----------------------------- hinzufuegen vom poster backdrop in emc ---------------------------------------------------
    def append(self):
        logout(data="------------------ def append")
        try:
            logout(data="------------------ def append 1")
            self.title = self.title
            logout(data=str(self.title))

            self.title = REGEX.sub('', self.title).strip()
            logout(data=str(self.title))

            if config.plugins.xtraEvent.PB.value == "posters":
                logout(data="------------------ def append 2")
                if config.plugins.xtraEvent.srcs.value == "bing":
                    logout(data="------------------ def append 3")
                    target = "{}poster/{}.jpg".format(pathLoc, self.title)
                if config.plugins.xtraEvent.searchModManuel.value == lng.get(lang, '16'):
                    logout(data="------------------ def append 4")
                    target = "{}poster/{}.jpg".format(pathLoc, self.title)

                else:
                    logout(data="------------------ def append 5")
                    target = "{}EMC/{}-poster.jpg".format(pathLoc, self.title)
            else:
                logout(data="------------------ def append 6")
                if config.plugins.xtraEvent.searchModManuel.value == lng.get(lang, '16'):
                    logout(data="------------------ def append 7")
                    target = "{}backdrop/{}.jpg".format(pathLoc, self.title)
                    if config.plugins.xtraEvent.srcs.value == "bing":
                        logout(data="------------------ def append 8")
                        evntNm = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!|\*", "", self.title).rstrip()
                        target = "{}backdrop/{}.jpg".format(pathLoc, evntNm)
                else:
                    logout(data="------------------ def append 9")
                    target = "{}EMC/{}-backdrop.jpg".format(pathLoc, self.title)
            import shutil
            logout(data="------------------ def append 10")
            if os.path.exists(self.path):
                logout(data="------------------ def append 11")
                shutil.copyfile(self.path, target)
                logout(data=str(self.path))
                logout(data=str(target))
                if os.path.exists(target):
                    logout(data="------------------ def append 12")
                    if config.plugins.xtraEvent.PB.value == "backdrops":
                        logout(data="------------------ def append 13")
                        if not config.plugins.xtraEvent.searchModManuel.value == lng.get(lang, '16'):
                            logout(data="------------------ def append 14 bild auf 1280x720")
                            im1 = Image.open(target)
                            #im1 = im1.resize((1280,720))
                            im1 = im1.resize((640, 360))
                            im1 = im1.save(target)
                            #im1.save("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/im1.jpg")
                            if os.path.exists(target):
                                logout(data="------------------ def append 15 bild wird dunkler")
                                im1 = Image.open(target)
                                im2 = Image.open("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/emc_background.jpg")
                                mask = Image.new("L", im1.size, 80)
                                im = Image.composite(im1, im2, mask)
                                #im.save(target)
                    logout(data="------------------ def append 16")
                    im1 = Image.open(target)
                    # im1 = im1.resize((1280,720))
                    im1 = im1.resize((185, 272))
                    im1 = im1.save(target)

        except:
            return
# --------------------------------------- hier downloads -------------------------------------------------------
    def tmdb(self):
        logout(data="------------------ def tmdb")
        self['status'].setText("Download Start")
        self['progress'].setValue(0)
        try:
            self.srch = config.plugins.xtraEvent.searchType.value
            self.year = config.plugins.xtraEvent.searchMANUELyear.value

            #self.srch = "multi"
            from requests.utils import quote
            url = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(self.srch, tmdb_api, quote(self.title))
            logout(data="------------------ def tmdb url 1")
            logout(data=str(url))

            import json
            response = requests.get(url)
            file_path = "{}EMC/{}-info.json".format(pathLoc, self.title)
            with open(file_path, 'w') as file:
                json.dump(response.json(), file)
                logout(data=" json geschrieben ")


            if self.year != "0":
                logout(data="------------------ def tmdb 1")
                if config.plugins.xtraEvent.searchType.value == "tv":
                    logout(data="------------------ def tmdb 2")
                #if config.plugins.xtraEvent.searchType.value == "multi":
                    url += "&first_air_date_year={}".format(self.year)
                    logout(data=str(url))
                elif config.plugins.xtraEvent.searchType.value == "movie":
                    logout(data="------------------ def tmdb 2a")
                    url += "&year={}".format(self.year)
                    logout(data=str(url))
            id = requests.get(url).json()['results'][0]['id']      # check daten vorhanden
            logout(data="------------------ def tmdb url 2")

            #self.srch = "tv"  # in den anderen findet er nichts
            url = "https://api.themoviedb.org/3/{}/{}?api_key={}&append_to_response=images".format(self.srch, int(id), tmdb_api)
            logout(data="------------------ def tmdb url ist")
            logout(data=str(url))
            if config.plugins.xtraEvent.searchLang.value:
                logout(data="------------------ def tmdb 3")
                url += "&language={}".format(lang)
            logout(data="------------------ def tmdb url 3")
            logout(data=str(url))

            if config.plugins.xtraEvent.PB.value == "posters":
                logout(data="------------------ def tmdb 4")
                sz = config.plugins.xtraEvent.TMDBpostersize.value
                logout(data=str(sz))
            else:
                logout(data="------------------ def tmdb 5")
                sz = config.plugins.xtraEvent.TMDBbackdropsize.value
                logout(data=str(sz))

            logout(data="------------------ def tmdb 6")
            p1 = requests.get(url).json()
            logout(data="------------------ def tmdb 6 p1")
            logout(data=str(p1))
            pb_no = p1['images'][config.plugins.xtraEvent.PB.value]  # hier werden dann die intraege gesucht mit der sprache 'de'
            logout(data="------------------ def tmdb 6 pb_no")
            logout(data=str(pb_no))
            n = len(pb_no)
            logout(data="------------------ def tmdb 6 n")
            logout(data=str(n))

            if n > 0:
                logout(data="------------------ def tmdb 7")
                downloaded = 0
                for i in range(int(n)):
                    poster = p1['images'][config.plugins.xtraEvent.PB.value][i]['file_path']
                    if poster:
                        url_poster = "https://image.tmdb.org/t/p/{}{}".format(sz, poster)
                        dwnldFile = "{}mSearch/{}-{}-{}.jpg".format(pathLoc, self.title, config.plugins.xtraEvent.PB.value, i+1)
                        open(dwnldFile, 'wb').write(requests.get(url_poster, stream=True, allow_redirects=True).content)
                        downloaded += 1
                        self.prgrs(downloaded, n)
            else:
                logout(data="------------------ def tmdb else")
                self['status'].setText(_("Download :  Poster not found - Language off ?"))
            config.plugins.xtraEvent.imgNmbr.value = 0

        except Exception as err:
            logout(data="------------------ def tmdb except")
            self['status'].setText("Download Ende : no files found")
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("Manuel Search tmdb , %s, %s\n"%(self.title, err))

    def tvdb(self):
        logout(data="--------------------------- def tvdb")
        self['status'].setText("Download Start")
        self['progress'].setValue(0)
        try:
            logout(data="--------------------------- def tvdb 1")
            self.srch = config.plugins.xtraEvent.searchType.value
            self.year = config.plugins.xtraEvent.searchMANUELyear.value
            from requests.utils import quote
            url = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(self.title))
            logout(data="------------------ def tvdb url 1 ist")
            logout(data=str(url))
            if self.year != 0:
                logout(data="--------------------------- def tvdb 2")
                url += "%20{}".format(self.year)
            url_read = requests.get(url).text
            series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
            if config.plugins.xtraEvent.PB.value == "posters":
                logout(data="--------------------------- def tvdb 3")
                keyType = "poster"
            else:
                logout(data="--------------------------- def tvdb 4")
                keyType = "fanart"
            url = 'https://api.thetvdb.com/series/{}/images/query?keyType={}'.format(series_id, keyType)
            logout(data="------------------ def tvdb url 2 ist")
            logout(data=str(url))
            if config.plugins.xtraEvent.searchLang.value:
                logout(data="--------------------------- def tvdb 5")
                u = requests.get(url, headers={"Accept-Language":"{}".format(lang)})
            try:
                logout(data="--------------------------- def tvdb 6")
                pb_no = u.json()["data"]
                n = len(pb_no)
            except:
                logout(data="--------------------------- def tvdb 7")
                self['status'].setText(_("Download : No"))
                return
            if n > 0:
                logout(data="--------------------------- def tvdb 8")
                downloaded = 0
                for i in range(int(n)):
                    if config.plugins.xtraEvent.PB.value == "posters":
                        img_pb = u.json()["data"][i]['{}'.format(config.plugins.xtraEvent.TVDBpostersize.value)]
                    else:
                        img_pb = u.json()["data"][i]['{}'.format(config.plugins.xtraEvent.TVDBbackdropsize.value)]
                    url = "https://artworks.thetvdb.com/banners/{}".format(img_pb)
                    logout(data="------------------ def tvdb url 3 ist")
                    logout(data=str(url))
                    dwnldFile = "{}mSearch/{}-{}-{}.jpg".format(pathLoc, self.title, config.plugins.xtraEvent.PB.value, i+1)
                    open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                    downloaded += 1
                    self.prgrs(downloaded, n)
            else:
                logout(data="--------------------------- def tvdb 9")
                self['status'].setText(_("Download : No"))
            config.plugins.xtraEvent.imgNmbr.value = 0
        except Exception as err:
            logout(data="--------------------------- def tvdb 10")
            self['status'].setText("Download Ende : no files found")
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("Manuel Search tvdb , %s, %s\n"%(self.title, err))
            return

    def fanart(self):
        logout(data=" -----------------  def fanart")
        self['status'].setText("Download Start")
        self['progress'].setValue(0)
        id = "-"
        from requests.utils import quote
        if config.plugins.xtraEvent.FanartSearchType.value == "tv":
            try:
                url_maze = "http://api.tvmaze.com/singlesearch/shows?q={}".format(quote(self.title))
                logout(data="------------------ def fanart url maze")
                logout(data=str(url_maze))
                mj = requests.get(url_maze).json()
                id = (mj['externals']['thetvdb'])
            except Exception as err:
                with open("/tmp/xtraEvent.log", "a+") as f:
                    f.write("fanart maze man.search, %s, %s\n"%(self.title, err))
        else:
            try:
                self.year = config.plugins.xtraEvent.searchMANUELyear.value
                url = "https://api.themoviedb.org/3/search/movie?api_key={}&query={}".format(tmdb_api, quote(self.title))
                logout(data="------------------ def fanart url 1449")
                logout(data=str(url))
                if self.year != 0:
                    url += "&primary_release_year={}&year={}".format(self.year, self.year)
                    logout(data="------------------ def fanart url 1453")
                    logout(data=str(url))
                id = requests.get(url).json()['results'][0]['id']
            except Exception as err:
                self['status'].setText("Download Ende : no json info found")
                with open("/tmp/xtraEvent.log", "a+") as f:
                    f.write("fanart tvdb id man.search, %s, %s\n"%(self.title, err))
        try:
            m_type = config.plugins.xtraEvent.FanartSearchType.value
            url_fanart = "https://webservice.fanart.tv/v3/{}/{}?api_key={}".format(m_type, id, fanart_api)
            logout(data="------------------ def fanart url fanart")
            logout(data=str(url_fanart))
            fjs = requests.get(url_fanart, verify=False, timeout=5).json()
            if config.plugins.xtraEvent.PB.value == "posters":
                if config.plugins.xtraEvent.FanartSearchType.value == "tv":
                    pb_no = fjs['tvposter']
                    n = len(pb_no)
                else:
                    pb_no = fjs['movieposter']
                    n = len(pb_no)
            elif config.plugins.xtraEvent.PB.value == "backdrops":
                if config.plugins.xtraEvent.FanartSearchType.value == "tv":
                    pb_no = fjs['showbackground']
                    n = len(pb_no)
                else:
                    pb_no = fjs['moviebackground']
                    n = len(pb_no)
            if n > 0:
                downloaded = 0
                for i in range(int(n)):
                    try:
                        if config.plugins.xtraEvent.PB.value == "posters":
                            if config.plugins.xtraEvent.FanartSearchType.value == "tv":
                                url = (fjs['tvposter'][i]['url'])
                                logout(data="------------------ def fanart url poster")
                                logout(data=str(url))
                            else:
                                url = (fjs['movieposter'][i]['url'])
                                logout(data="------------------ def fanart url movieposter")
                                logout(data=str(url))
                        if config.plugins.xtraEvent.PB.value == "backdrops":
                            if config.plugins.xtraEvent.FanartSearchType.value == "tv":
                                url = (fjs['showbackground'][i]['url'])
                                logout(data="------------------ def fanart url backdrops")
                                logout(data=str(url))
                            else:
                                url = (fjs['moviebackground'][i]['url'])
                                logout(data="------------------ def fanart url moviebackground")
                                logout(data=str(url))
                        open("/tmp/url","a+").write("%s\n"%url)
                        dwnldFile = "{}mSearch/{}-{}-{}.jpg".format(pathLoc, self.title, config.plugins.xtraEvent.PB.value, i+1)
                        open(dwnldFile, 'wb').write(requests.get(url, verify=False).content)
                        downloaded += 1
                        self.prgrs(downloaded, n)
                        scl = 1
                        im = Image.open(dwnldFile)
                        if config.plugins.xtraEvent.PB.value == "posters":
                            scl = config.plugins.xtraEvent.FANART_Poster_Resize.value
                        if config.plugins.xtraEvent.PB.value == "backdrops":
                            scl = config.plugins.xtraEvent.FANART_Backdrop_Resize.value
                        im1 = im.resize((im.size[0] // int(scl), im.size[1] // int(scl)), Image.ANTIALIAS)
                        im1.save(dwnldFile)
                    except Exception as err:
                        logout(data=" -----------------  def fanart 1479")
                        with open("/tmp/xtraEvent.log", "a+") as f:
                            f.write("fanart man.search save, %s, %s\n"%(self.title, err))
            else:
                self['status'].setText(_(lng.get(lang, '56')))
            config.plugins.xtraEvent.imgNmbr.value = 0
        except Exception as err:
            logout(data=" -----------------  def fanart 1487")
            self['status'].setText("Download Ende : no files found")
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("fanart man.search2, %s, %s\n"%(self.title, err))

    def imdb(self):
        logout(data="-------------------- def imdb")
        self['status'].setText("Download Start")
        self['progress'].setValue(0)
        downloaded = 0
        try:
            from requests.utils import quote
            url_find = 'https://m.imdb.com/find?q={}'.format(quote(self.title))
            ff = requests.get(url_find).text
            p = 'src=\"https://(.*?)._V1_UX75_CR0,0,75,109_AL_.jpg'
            pstr = re.findall(p, ff)[0]
            if config.plugins.xtraEvent.PB.value == "posters":
                logout(data="-------------------- def imdb url")
                url = "https://{}._V1_UX{}_AL_.jpg".format(pstr, config.plugins.xtraEvent.imdb_Poster_size.value)
                logout(data=str(downloaded))
                if url:
                    logout(data="-------------------- def imdb if url ")
                    dwnldFile = "{}mSearch/{}-poster-1.jpg".format(pathLoc, self.title)
                    open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                    downloaded += 1
                    n = 1
                    self.prgrs(downloaded, n)
                    logout(data=str(downloaded))
                else:
                    logout(data="-------------------- def imdb no")
                    self['status'].setText(_("Download : No"))
                config.plugins.xtraEvent.imgNmbr.value = 0

        except Exception as err:
            self['status'].setText("Download Ende: ")
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("imdb man.search2, %s, %s\n"%(self.title, err))
            return

    def bing(self):
        logout(data=" -----------------  def bing")
        self['status'].setText("Download Start")
        self['progress'].setValue(0)
        try:
            url = "https://www.bing.com/images/search?q={}".format(self.title.replace(" ", "+"))
            if config.plugins.xtraEvent.PB.value == "posters":
                url += "+poster"
            else:
                url += "+backdrop"
            headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
            try:
                ff = requests.get(url, stream=True, headers=headers).text
                p = re.findall('ihk=\"\/th\?id=(.*?)&', ff)
            except:
                pass
            n = 9
            downloaded = 0
            for i in range(n):
                try:
                    url = re.findall(',&quot;murl&quot;:&quot;(.*?)&', ff)[i]
                    dwnldFile = "{}mSearch/{}-{}-{}.jpg".format(pathLoc, self.title, config.plugins.xtraEvent.PB.value, i+1)
                    open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                    downloaded += 1
                    self.prgrs(downloaded, n)   # hier wird download und progress ausgegeben
                except:
                    self['status'].setText("Download Ende")
                    pass
            config.plugins.xtraEvent.imgNmbr.value = 0
        except Exception as err:
            self['status'].setText(_(str(err)))
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("bing man.search2, %s, %s\n"%(self.title, err))
# -------------------------------  die dateien sind dann in mSerach ordner drin ------------------------------------
    def google(self):
        logout(data="------------------ def google")
        self['status'].setText("Download Start")
        self['progress'].setValue(0)

        try:
            url = "https://www.google.com/search?q={}&tbm=isch&tbs=sbd:0".format(self.title.replace(" ", "+"))
            #url = "https://www.google.com/search?q=%22{}%22&tbm=isch&tbs=sbd:0".format(self.title.replace(" ", "+"))
            #size = 185  # gewünschte Bildgröße
            #url = "https://www.google.com/search?q={}&tbm=isch&tbs=sbd:0&tbm=isch&tbs=isz:{}".format(self.title.replace(" ", "+"), size)
            logout(data=str(url))
            if config.plugins.xtraEvent.PB.value == "posters":
                url += "+poster"
            else:
                url += "+backdrop"
            headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
            try:
                ff = requests.get(url, stream=True, headers=headers).text
                p = re.findall('\],\["https://(.*?)",\d+,\d+]', ff)
            except:
                pass
            n = 9
            downloaded = 0
            for i in range(n):
                try:
                    url = "https://{}".format(p[i+1])
                    logout(data="------------------ def google try")
                    logout(data=str(url))
                    dwnldFile = "{}mSearch/{}-{}-{}.jpg".format(pathLoc, self.title, config.plugins.xtraEvent.PB.value, i+1)
                    open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                    downloaded += 1
                    self.prgrs(downloaded, n)
                except:
                    pass
            config.plugins.xtraEvent.imgNmbr.value = 0
        except Exception as err:
            self['status'].setText(_(str(err)))
            return

    def prgrs(self, downloaded, n):
        self['status'].setText("Download : {} / {}".format(downloaded, n))
        self['progress'].setValue(int(100*downloaded//n))



class selBouquets(Screen):
    logout(data="selBouquets")
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)

        if desktop_size <= 1280:
            if config.plugins.xtraEvent.skinSelect.value == 'skin_1':
                self.skin = selbuq_720
            if config.plugins.xtraEvent.skinSelect.value == 'skin_2':
                self.skin = selbuq_720_2
        else:
            if config.plugins.xtraEvent.skinSelect.value == 'skin_1':
                self.skin = selbuq_1080
            if config.plugins.xtraEvent.skinSelect.value == 'skin_2':
                self.skin = selbuq_1080_2

        try:
            if config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '13'):
                sl = self.getBouquetList()
            elif config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '14a'):
                sl = self.getProviderList()
            else:
                pass
            list = []
            for i in sl:
                list.append(xtraSelectionEntryComponent(i[0], 1, 0, 0))
            self["list"] = xtraSelectionList(list)
        except:
            return

        self["list"].l.setItemHeight(70)
        self["actions"] = ActionMap(["xtraEventAction"],
            {
                "cancel": self.cancel,
                "red": self.bqtinchannelsold,
                "green": self.bqtinchannels,
                "yellow": self["list"].toggleSelection,
                "blue": self["list"].toggleAllSelection,
                "ok": self["list"].toggleSelection
            }, -1)
        self["key_red"] = Label(_("Search"))
        self["key_green"] = Label(_("Save"))
        self["key_yellow"] = Label(_(lng.get(lang, '43')))
        self["key_blue"] = Label(_(lng.get(lang, '44')))
        self.setTitle(_(lng.get(lang, '55')))
        self['status'] = Label()
        self['info'] = Label()

        testver = version
        self.testver = testver
        self["testver"] = Label()
        self["testver"].setText("%s " % (self.testver))
# mit rot die alte liste nehmen und suchen

    def getBouquetList(self):
        logout(data="getBouquetList")

        self.statussearchold = "No Bouquet File make New"
        logout(data="statussearchold text ")
        self["statussearchold"] = Label()
        self['statussearchold'].setText(self.statussearchold)
        self['statussearchold'].show()

        logout(data="statussearchold")
        logout(data=str(self.statussearchold))
        if os.path.exists("{}bqts".format(pathLoc)):
            logout(data="statussearchold new")
            self.statussearchold = (_("Press Red for the Old Bouquets search "))
            self['statussearchold'].setText(self.statussearchold)
            self['statussearchold'].show()
            logout(data=str(self.statussearchold))
            logout(data="statussearchold ende")




        try:
            bouquets = []
            service_types_tv = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 31) || (type == 134) || (type == 195)'
            serviceHandler = eServiceCenter.getInstance()
            if config.usage.multibouquet.value:
                bouquet_root = eServiceReference('1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "bouquets.tv" ORDER BY bouquet')
                list = serviceHandler.list(bouquet_root)
                if list:
                    while True:
                        s = list.getNext()
                        if not s.valid():
                            break
                        if s.flags & eServiceReference.isDirectory and not s.flags & eServiceReference.isInvisible:
                            info = serviceHandler.info(s)
                            if info:
                                bouquets.append((info.getName(s), s))
                    return bouquets
            else:
                bouquet_root = '%s FROM BOUQUET "userbouquet.favourites.tv" ORDER BY bouquet'%(service_types_tv)
                info = serviceHandler.info(bouquet_root)
                if info:
                    bouquets.append((info.getName(bouquet_root), bouquet_root))
                return bouquets
            return None
        except Exception as err:
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("getBouquetList, %s\n"%(err))

    def getProviderList(self):
        logout(data="getProviderList")
        try:
            service_types_tv = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 31) || (type == 134) || (type == 195)'
            self.root = eServiceReference('%s FROM PROVIDERS ORDER BY name' % (service_types_tv))
            serviceHandler = eServiceCenter.getInstance()
            services = serviceHandler.list(eServiceReference(self.root))
            providers = services and services.getContent("NS", True)

            plists = []
            for provider in providers:
                plists.append(provider)
            return plists

        except Exception as err:
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("getProviderList, %s\n"%(err))

    def buqChList(self, bqtNm):
        logout(data="buqChList")
        try:
            channels = []
            serviceHandler = eServiceCenter.getInstance()
            chlist = serviceHandler.list(eServiceReference('1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "bouquets.tv" ORDER BY bouquet'))
            if chlist :
                while True:
                    chh = chlist.getNext()
                    if not chh.valid(): break
                    info = serviceHandler.info(chh)
                    if chh.flags & eServiceReference.isDirectory:
                        info = serviceHandler.info(chh)
                    if info.getName(chh) in bqtNm:
                        chlist = serviceHandler.list(chh)
                        while True:
                            chhh = chlist.getNext()
                            if not chhh.valid(): break
                            channels.append((chhh.toString()))
                # open("/tmp/chList", "w").write(str(channels))
                return channels
            return
        except Exception as err:
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("chList Bouquet, %s\n"%(err))

    def provChList(self, prvNm):
        logout(data="provChList")
        try:
            service_types_tv = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 31) || (type == 134) || (type == 195)'
            channels = []
            serviceHandler = eServiceCenter.getInstance()
            chlist = serviceHandler.list(eServiceReference('%s FROM PROVIDERS ORDER BY name' % (service_types_tv)))
            if chlist :
                while True:
                    chh = chlist.getNext()
                    if not chh.valid(): break
                    info = serviceHandler.info(chh)
                    if chh.flags & eServiceReference.isDirectory:
                        info = serviceHandler.info(chh)
                    if info.getName(chh) in prvNm:
                        chlist = serviceHandler.list(chh)
                        while True:
                            chhh = chlist.getNext()
                            if not chhh.valid(): break
                            channels.append((chhh.toString()))
                # open("/tmp/chList", "w").write(str(channels))
                return channels
            return
        except Exception as err:
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("chList Bouquet, %s\n"%(err))

    def bqtinchannelsold(self):
        logout(data="bqtinchannelsold")

        try:
            if os.path.exists("{}bqts".format(pathLoc)):
            #    os.remove("{}bqts".format(pathLoc))

            #bE = "{}bqts".format(pathLoc)
            #blist = []
            #for idx, item in enumerate(self["list"].list):
            #    item = self["list"].list[idx][0]
            #    if item[3]:
            #        blist.append(item[0])
            #for p in blist:

            #    if config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '13'):
            #        refs = self.buqChList(p)
            #        for ref in refs:
            #            open(bE, "a+").write("{}\n".format(ref))

            #    elif config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '14a'):
            #        refs = self.provChList(p)
            #        for ref in refs:
            #            open(bE, "a+").write("{}\n".format(ref))

            #else:
                    list = [(_(lng.get(lang, '53')), self.withPluginDownload), (_(lng.get(lang, '54')), self.withTimerDownload), (_(lng.get(lang, '35')), self.cancel)]
                    self.session.openWithCallback(self.menuCallback, ChoiceBox, title=_('Download ?'), list=list)
            else:
                return
        except Exception as err:
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("bqtinchannels, %s\n" % (err))

    def bqtinchannels(self):
        logout(data="bqtinchannels")
        try:
            if os.path.exists("{}bqts".format(pathLoc)):
                logout(data="bqtinchannels1")
                logout(data=str(pathLoc))
                import stat
                #os.chmod(pathLoc, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                # achtung wenn die dateien rechte 777 haben geht das loeschen nicht
                os.remove("{}bqts".format(pathLoc))

            bE = "{}bqts".format(pathLoc)
            blist = []
            logout(data="bqtinchannels2")
            for idx,item in enumerate(self["list"].list):
                logout(data="bqtinchannels3")
                item = self["list"].list[idx][0]
                if item[3]:
                    blist.append(item[0])
            for p in blist:

                if config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '13'):
                    logout(data="bqtinchannels3")
                    refs = self.buqChList(p)
                    for ref in refs:
                        open(bE, "a+").write("{}\n".format(ref))

                elif config.plugins.xtraEvent.searchMOD.value == lng.get(lang, '14a'):
                    logout(data="bqtinchannels4")
                    refs = self.provChList(p)
                    for ref in refs:
                        open(bE, "a+").write("{}\n".format(ref))

            else:
                logout(data="bqtinchannels ende")
                list = [(_(lng.get(lang, '53')), self.withPluginDownload), (_(lng.get(lang, '54')), self.withTimerDownload), (_(lng.get(lang, '35')), self.cancel)]
                self.session.openWithCallback(self.menuCallback, ChoiceBox, title=_('Download ?'), list=list)
        except Exception as err:
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("bqtinchannels, %s\n"%(err))

    def withPluginDownload(self):
        logout(data="withPluginDownload")
        from . import download
        self.session.open(download.downloads)

    def withTimerDownload(self):
        logout(data="withTimerDownload")
        if config.plugins.xtraEvent.timerMod.value == False:
            self.session.open(MessageBox, _(lng.get(lang, '52')), MessageBox.TYPE_INFO, timeout = 10)
        else:
            self.session.openWithCallback(self.restart, MessageBox, _(lng.get(lang, '47')), MessageBox.TYPE_YESNO, timeout = 20)

    def menuCallback(self, ret = None):
        logout(data="menuCallback")
        ret and ret[1]()

    def restart(self, answer):
        logout(data="restart")
        if answer is True:
            configfile.save()
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def cancel(self):
        logout(data="cancel")
        self.close(self.session, False)

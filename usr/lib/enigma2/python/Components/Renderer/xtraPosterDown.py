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

myfile="/tmp/xtraPosterDown.log"

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
            logout(data="changed zum download")

            logout(data="changed ende download ")
            if what[0] != self.CHANGED_CLEAR:
                evnt = ''
                pstrNm = ''
                evntNm = ''
                try:
                    event = self.source.event
                    if event:
                        evnt = event.getEventName()
                        evntNm = REGEX.sub('', evnt).strip()
                        pstrNm = "{}xtraEvent/poster/{}.jpg".format(pathLoc, evntNm)
                        if os.path.exists(pstrNm):
                            self.instance.setPixmap(loadJPG(pstrNm))
                            self.instance.setScale(1)
                            self.instance.show()
                        else:
                            self.instance.hide()
                    else:
                        self.instance.hide()
                    return
                except:
                    self.instance.hide()
                    return
            else:
                self.instance.hide()
                return
# -------------------------------- download -----------------------------------------
def
if config.plugins.xtraEvent.poster.value == True:
    dwnldFile = "{}poster/{}.jpg".format(pathLoc, title)

    if config.plugins.xtraEvent.tmdb.value == True:
        if not os.path.exists(dwnldFile):
            try:
                srch = config.plugins.xtraEvent.searchType.value
                logout(data=" URL 544")
                url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
                logout(data=" URL 544")
                logout(data=str(url_tmdb))
                if config.plugins.xtraEvent.searchLang.value == True:
                    logout(data=" URL 548")
                    url_tmdb += "&language={}".format(self.searchLanguage())
                    logout(data=" URL 548")
                    logout(data=str(url_tmdb))

                    # als json datei speichern
                    response = requests.get(url_tmdb)
                if response.status_code == 200:
                    logout(data=" json 557")
                    # Dateipfad im temporären Verzeichnis erstellen
                    #file_path = os.path.join('/tmp', 'poster.json')
                    logout(data=str(title))
                    logout(data=str(pathLoc))
                    file_path = "{}infos/{}.json".format(pathLoc, title)
                    logout(data=" json path 561")
                    logout(data=str(file_path))
                    # JSON-Daten speichern
                    with open(file_path, 'w') as file:
                        json.dump(response.json(), file)
                        logout(data=" json geschrieben 566")
                # ---------------------------------------------------------

                poster = ""
                poster = requests.get(url_tmdb).json()['results'][0]['poster_path']
                original_title = requests.get(url_tmdb).json()['results'][0]['poster_path']
                logout(data=str(original_title))
                p_size = config.plugins.xtraEvent.TMDBpostersize.value
                logout(data=" URL 556")
                url = "https://image.tmdb.org/t/p/{}{}".format(p_size, poster)
                logout(data=" URL 556")
                logout(data=str(url))
                if poster != "":
                    open(dwnldFile, 'wb').write(requests.get(url, stream=True, allow_redirects=True).content)
                if os.path.exists(dwnldFile):
                    self['info'].setText("►  {}, TMDB, POSTER".format(title.upper()))
                    tmdb_poster_downloaded += 1
                    downloaded = tmdb_poster_downloaded
                    self.prgrs(downloaded, n)
                    self.showPoster(dwnldFile)
                    #continue
                    try:
                        img = Image.open(dwnldFile)
                        img.verify()
                    except Exception as err:
                        with open("/tmp/xtraEvent.log", "a+") as f:
                            f.write("deleted tmdb poster: %s.jpg\n"%title)
                        try:
                            os.remove(dwnldFile)
                        except:
                            pass
            except Exception as err:
                with open("/tmp/xtraEvent.log", "a+") as f:
                    f.write("tmdb poster, %s, %s\n"%(title, err))

if config.plugins.xtraEvent.tvdb.value == True:
    try:
        img = Image.open(dwnldFile)
        img.verify()
    except Exception as err:
        with open("/tmp/xtraEvent.log", "a+") as f:
            f.write("deleted : %s.jpg\n" % title)
        try:
            os.remove(dwnldFile)
        except:
            pass
    if not os.path.exists(dwnldFile):
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

                # als json datei speichern
                response = requests.get(url_tvdb)
                if response.status_code == 200:
                    logout(data=" json 632")
                    # Dateipfad im temporären Verzeichnis erstellen
                    # file_path = os.path.join('/tmp', 'poster.json')
                    logout(data=str(title))
                    logout(data=str(pathLoc))
                    file_path = "{}infos/{}.json".format(pathLoc, title)
                    logout(data=" json path 638")
                    logout(data=str(file_path))
                    # JSON-Daten speichern
                    with open(file_path, 'w') as file:
                        json.dump(response.json(), file)
                        logout(data=" json geschrieben 643")
                # ---------------------------------------------------------

                poster = ""
                poster = re.findall('<poster>(.*?)</poster>', url_read)[0]
                if poster != '':
                    logout(data="url 611")
                    url = "https://artworks.thetvdb.com/banners/{}".format(poster)
                    logout(data=str(url))
                    logout(data="url 596")
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
                        # continue
                        try:
                            img = Image.open(dwnldFile)
                            img.verify()
                        except Exception as err:
                            with open("/tmp/xtraEvent.log", "a+") as f:
                                f.write("deleted tvdb poster: %s.jpg\n" % title)
                            try:
                                os.remove(dwnldFile)
                            except:
                                pass
        except Exception as err:
            with open("/tmp/xtraEvent.log", "a+") as f:
                f.write("tvdb poster, %s, %s\n" % (title, err))

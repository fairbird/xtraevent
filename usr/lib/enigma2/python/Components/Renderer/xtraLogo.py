# -*- coding: utf-8 -*-
# by digiteng...08.2020 - 11.2021
# <widget source="session.Event_Now" render="xtraLogo" position="59,148" size="278,185" zPosition="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eEPGCache, loadJPG, loadPNG
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

import inspect
from Plugins.Extensions.xtraEvent.skins.xtraSkins import *
from Plugins.Extensions.xtraEvent.xtraTitleHelper import *
########################### log file loeschen ##################################
dir_path = "/tmp/xtraevent"

try:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print("Directory has been created:", dir_path)
    else:
        print("Directory already exists:", dir_path)
except Exception as e:
    print("Error creating directory:", e)




myfile=dir_path + "/logo.log"
## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)

logstatus = "on"
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


# ----------------------------- so muss das commando aussehen , um in den file zu schreiben  ------------------------------
logout(data="start 6.76")
logout(data=str(config.plugins.xtraEvent.logFiles.value))
logout(data=str(logstatus))


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

class xtraLogo(Renderer):
    GUI_WIDGET = ePixmap

    def __init__(self):
        Renderer.__init__(self)
        self.download_starts = {}

    def can_start_download(self, key):
        try:
            now = time.time()
            last_time = self.download_starts.get(key, 0)
            if now - last_time < 20:
                logout(data="skip duplicate logo download for key={}".format(key))
                return False
            self.download_starts[key] = now
            return True
        except Exception as e:
            logout(data="can_start_download error: {}".format(str(e)))
            return True

    def download_logo_now(self, evntNm):
        try:
            if not config.plugins.xtraEvent.logoFiles.value:
                logout(data="logoFiles is OFF")
                return

            from requests.utils import quote

            srch = config.plugins.xtraEvent.searchType.value
            if not srch:
                srch = "multi"

            url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(
                srch, tmdb_api, quote(evntNm)
            )
            logout(data="xtraLogo search url={}".format(url_tmdb))
            data = requests.get(url_tmdb).json()
            results = data.get("results", [])
            if not results:
                logout(data="xtraLogo no TMDB search results")
                return

            item = results[0]
            tmdb_id = item.get("id")
            media_type = item.get("media_type", srch)

            if srch in ("movie", "tv"):
                media_type = srch
            elif media_type not in ("movie", "tv"):
                if item.get("title", "") or item.get("release_date", ""):
                    media_type = "movie"
                else:
                    media_type = "tv"

            if not tmdb_id:
                logout(data="xtraLogo no tmdb id")
                return

            url_images = "https://api.themoviedb.org/3/{}/{}/images?api_key={}".format(
                media_type, tmdb_id, tmdb_api
            )
            logout(data="xtraLogo images url={}".format(url_images))
            img_json = requests.get(url_images).json()
            logos = img_json.get("logos", [])
            if not logos:
                logout(data="xtraLogo no logos found")
                return

            # Prefer current GUI language, then English, then first available
            selected_logo = None
            for item in logos:
                if item.get("iso_639_1") == lang:
                    selected_logo = item
                    break
            if selected_logo is None:
                for item in logos:
                    if item.get("iso_639_1") == "en":
                        selected_logo = item
                        break
            if selected_logo is None:
                selected_logo = logos[0]

            file_path = selected_logo.get("file_path")
            if not file_path:
                logout(data="xtraLogo selected logo missing file_path")
                return

            logo_size = "w300"
            try:
                logo_size = config.plugins.xtraEvent.TMDBlogosize.value
            except:
                pass

            url_logo = "https://image.tmdb.org/t/p/{}{}".format(logo_size, file_path)
            dwn_logo = "{}xtraEvent/logo/{}.png".format(pathLoc, evntNm)
            logout(data="xtraLogo save path={}".format(dwn_logo))

            open(dwn_logo, 'wb').write(requests.get(url_logo, stream=True, allow_redirects=True).content)

        except Exception as e:
            logout(data="xtraLogo download error={}".format(str(e)))

    def changed(self, what):
        logout(data="xtraLogo changed")
        if not self.instance:
            return

        if what[0] == self.CHANGED_CLEAR:
            self.instance.hide()
            return

        try:
            event = self.source.event
            if not event:
                self.instance.hide()
                return

            evnt = event.getEventName()
            logout(data="xtraLogo raw event={}".format(str(evnt)))

            evntNm = clean_search_title(evnt)
            logout(data="xtraLogo clean event={}".format(str(evntNm)))

            if not evntNm:
                self.instance.hide()
                return

            pstrNm = "{}xtraEvent/logo/{}.png".format(pathLoc, evntNm)
            logout(data="xtraLogo expected path={}".format(pstrNm))

            if os.path.exists(pstrNm):
                self.instance.setPixmap(loadPNG(pstrNm))
                self.instance.setScale(1)
                self.instance.show()
                return

            # Current event has priority
            key = "logo::{}".format(evntNm)
            if self.can_start_download(key):
                try:
                    from _thread import start_new_thread
                except:
                    from thread import start_new_thread
                start_new_thread(self.download_logo_now, (evntNm,))

            self.instance.hide()

        except Exception as e:
            logout(data="xtraLogo changed error={}".format(str(e)))
            self.instance.hide()

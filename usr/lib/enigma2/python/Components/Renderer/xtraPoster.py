# -*- coding: utf-8 -*-
# by digiteng...08.2020 - 11.2021
# patched with auto-download + logging
# <widget source="session.Event_Now" render="xtraPoster" position="0,0" size="185,278" zPosition="1" />

from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eEPGCache, loadJPG
from Components.config import config

import os
import re
import json
import time

from Plugins.Extensions.xtraEvent.skins.xtraSkins import *
from Plugins.Extensions.xtraEvent.xtraTitleHelper import *

# --------------------------- Logfile -------------------------------
from datetime import datetime
from os import remove
from os.path import isfile

dir_path = "/tmp/xtraevent"

try:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
except Exception as e:
    print("xtraPoster: error creating log dir:", e)

myfile = dir_path + "/poster.log"
if isfile(myfile):
    remove(myfile)

logstatus = "off"
if config.plugins.xtraEvent.logFiles.value == True:
    logstatus = "on"
else:
    logstatus = "off"


def write_log(msg):
    if logstatus == 'on':
        try:
            with open(myfile, "a") as log:
                log.write(datetime.now().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + str(msg) + "\n")
        except:
            pass


def logout(data):
    if logstatus == 'on':
        write_log(data)


logout(data="xtraPoster start")

# --------------------------- APIs -------------------------------
if config.plugins.xtraEvent.tmdbAPI.value != "":
    tmdb_api = config.plugins.xtraEvent.tmdbAPI.value
else:
    tmdb_api = "3c3efcf47c3577558812bb9d64019d65"

if config.plugins.xtraEvent.tvdbAPI.value != "":
    tvdb_api = config.plugins.xtraEvent.tvdbAPI.value
else:
    tvdb_api = "a99d487bb3426e5f3a60dea6d3d3c7ef"

try:
    if config.plugins.xtraEvent.fanartAPI.value != "":
        fanart_api = config.plugins.xtraEvent.fanartAPI.value
    else:
        fanart_api = "6d231536dea4318a88cb2520ce89473b"
except:
    fanart_api = "6d231536dea4318a88cb2520ce89473b"

# --------------------------- Py2 / Py3 -------------------------------
try:
    import sys
    PY3 = sys.version_info[0]
    if PY3 == 3:
        from builtins import str
        from builtins import range
        from builtins import object
        from configparser import ConfigParser
        from _thread import start_new_thread
        from urllib.parse import quote
    else:
        from ConfigParser import ConfigParser
        from thread import start_new_thread
        from urllib import quote
except:
    pass

try:
    import requests
except Exception as err:
    logout(data="requests import error: {}".format(err))

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}

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
        lng.read(lang_path, encoding='utf8')
    else:
        lng.read(lang_path)
    lng.get(lang, "0")
except:
    try:
        lang = "en"
        lng = ConfigParser()
        if PY3 == 3:
            lng.read(lang_path, encoding='utf8')
        else:
            lng.read(lang_path)
    except:
        pass

epgcache = eEPGCache.getInstance()

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
    r'\sح\s*\d+|'
    r'\sج\s*\d+|'
    r'\sم\s*\d+|'
    r'\d+$',
    re.DOTALL
)


class xtraPoster(Renderer):
    GUI_WIDGET = ePixmap

    def __init__(self):
        Renderer.__init__(self)
        self.last_name = ""
        self.download_starts = {}

    # --------------------------- helpers -------------------------------

    def _search_language(self):
        try:
            from Components.Language import language
            lng_code = language.getLanguage()
            return lng_code[:2]
        except:
            try:
                return config.osd.language.value[:-3]
            except:
                return "en"

    def _clean_title(self, evnt):
        try:
            name = evnt.replace('\xc2\x86', '').replace('\xc2\x87', '')
        except:
            name = evnt

        return clean_search_title(name)

    def _poster_dir(self):
        return "{}xtraEvent/poster".format(pathLoc)

    def _dummy_dir(self):
        return "{}xtraEvent/poster/dummy".format(pathLoc)

    def _poster_path(self, title):
        return "{}/{}.jpg".format(self._poster_dir(), title)

    def _dummy_path(self, title):
        return "{}/{}.jpg".format(self._dummy_dir(), title)

    def _ensure_dirs(self):
        try:
            if not os.path.exists(self._poster_dir()):
                os.makedirs(self._poster_dir())
        except Exception as err:
            logout(data="mkdir poster dir error: {}".format(err))

    def _show_poster(self, poster_path):
        try:
            if self.instance and os.path.exists(poster_path):
                self.instance.setPixmap(loadJPG(poster_path))
                self.instance.setScale(1)
                self.instance.show()
                logout(data="poster shown: {}".format(poster_path))
                return True
        except Exception as err:
            logout(data="show poster error: {}".format(err))
        return False

    def _show_dummy(self, title):
        try:
            dummy = self._dummy_path(title)
            if os.path.exists(dummy):
                self.instance.setPixmap(loadJPG(dummy))
                self.instance.setScale(1)
                self.instance.show()
                logout(data="dummy shown: {}".format(dummy))
                return True
        except Exception as err:
            logout(data="show dummy error: {}".format(err))
        return False


    def _info_candidates(self, title):
        try:
            prefer_tmdb = bool(config.plugins.xtraEvent.tmdb.value)
        except:
            prefer_tmdb = True
        candidates = get_info_json_candidates(pathLoc, title, prefer_tmdb=prefer_tmdb)
        logout(data="poster info candidates title={} candidates={}".format(title, candidates))
        return candidates

    def _elcinema_json_poster_download(self, title, dest):
        try:
            for json_path in self._info_candidates(title):
                if not os.path.exists(json_path):
                    continue
                with open(json_path, "r") as handle:
                    data = json.load(handle)
                provider = safe_str(data.get("provider", "")).lower()
                poster_url = safe_str(data.get("poster", "")) or safe_str(data.get("poster_path", ""))
                if provider == "elcinema" and poster_url:
                    logout(data="[ELCINEMA] poster json={}".format(json_path))
                    logout(data="[ELCINEMA] poster url={}".format(poster_url))
                    return self._download_file(poster_url, dest)
        except Exception as err:
            logout(data="[ELCINEMA] poster json error: {}".format(err))
        return False

    def _download_file(self, url, dest):
        try:
            logout(data="download file url={}".format(url))
            r = requests.get(url, stream=True, allow_redirects=True, timeout=10, headers=headers)
            if r.status_code != 200:
                logout(data="download file bad status={}".format(r.status_code))
                return False
            with open(dest, 'wb') as f:
                f.write(r.content)
            if os.path.exists(dest) and os.path.getsize(dest) > 0:
                logout(data="download file saved={}".format(dest))
                return True
            logout(data="download file saved empty")
            try:
                os.remove(dest)
            except:
                pass
            return False
        except Exception as err:
            logout(data="download file error: {}".format(err))
            try:
                if os.path.exists(dest):
                    os.remove(dest)
            except:
                pass
            return False

    def _tmdb_download(self, title, dest):
        if not config.plugins.xtraEvent.tmdb.value:
            logout(data="tmdb disabled")
            return False

        try:
            srch = config.plugins.xtraEvent.searchType.value
        except:
            srch = "multi"

        if not srch:
            srch = "multi"

        search_lang = self._search_language()
        queries = []

        try:
            if config.plugins.xtraEvent.searchLang.value:
                queries.append("https://api.themoviedb.org/3/search/{}?api_key={}&query={}&language={}".format(srch, tmdb_api, quote(title), search_lang))
        except:
            pass

        queries.append("https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title)))

        if srch != "multi":
            queries.append("https://api.themoviedb.org/3/search/multi?api_key={}&query={}".format(tmdb_api, quote(title)))
        if srch != "movie":
            queries.append("https://api.themoviedb.org/3/search/movie?api_key={}&query={}".format(tmdb_api, quote(title)))
        if srch != "tv":
            queries.append("https://api.themoviedb.org/3/search/tv?api_key={}&query={}".format(tmdb_api, quote(title)))

        seen = set()
        for url_tmdb in queries:
            if url_tmdb in seen:
                continue
            seen.add(url_tmdb)
            try:
                logout(data="[TMDB] query={}".format(url_tmdb))
                data = requests.get(url_tmdb, timeout=10, headers=headers).json()
                results = data.get("results", [])
                if not results:
                    logout(data="[TMDB] no results")
                    continue

                poster = results[0].get("poster_path")
                logout(data="[TMDB] poster={}".format(poster))
                if poster:
                    p_size = config.plugins.xtraEvent.TMDBpostersize.value
                    img_url = "https://image.tmdb.org/t/p/{}{}".format(p_size, poster)
                    if self._download_file(img_url, dest):
                        logout(data="[TMDB] success")
                        return True
            except Exception as err:
                logout(data="[TMDB] error: {}".format(err))

        return False

    def _tvdb_download(self, title, dest):
        if not config.plugins.xtraEvent.tvdb.value:
            logout(data="tvdb disabled")
            return False

        try:
            url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(title))
            logout(data="[TVDB] search={}".format(url_tvdb))
            url_read = requests.get(url_tvdb, timeout=10, headers=headers).text
            ids = re.findall('<seriesid>(.*?)</seriesid>', url_read)
            if not ids:
                logout(data="[TVDB] no series id")
                return False

            series_id = ids[0]
            search_lang = self._search_language()
            url_tvdb = "https://thetvdb.com/api/{}/series/{}/{}".format(tvdb_api, series_id, search_lang)
            logout(data="[TVDB] data={}".format(url_tvdb))
            url_read = requests.get(url_tvdb, timeout=10, headers=headers).text
            posters = re.findall('<poster>(.*?)</poster>', url_read)
            if not posters:
                logout(data="[TVDB] no poster field")
                return False

            poster = posters[0]
            if not poster:
                logout(data="[TVDB] empty poster field")
                return False

            img_url = "https://artworks.thetvdb.com/banners/{}".format(poster)
            try:
                if config.plugins.xtraEvent.TVDBpostersize.value == "thumbnail":
                    img_url = img_url.replace(".jpg", "_t.jpg")
            except:
                pass

            if self._download_file(img_url, dest):
                logout(data="[TVDB] success")
                return True

        except Exception as err:
            logout(data="[TVDB] error: {}".format(err))

        return False

    def _maze_download(self, title, dest):
        if not config.plugins.xtraEvent.maze.value:
            logout(data="maze disabled")
            return False

        try:
            url_maze = "http://api.tvmaze.com/search/shows?q={}".format(quote(title))
            logout(data="[MAZE] query={}".format(url_maze))
            data = requests.get(url_maze, timeout=10, headers=headers).json()
            if not data:
                logout(data="[MAZE] no results")
                return False

            img_url = data[0].get('show', {}).get('image', {}).get('medium')
            logout(data="[MAZE] img={}".format(img_url))
            if img_url and self._download_file(img_url, dest):
                logout(data="[MAZE] success")
                return True

        except Exception as err:
            logout(data="[MAZE] error: {}".format(err))

        return False

    def _download_poster(self, title, dest):
        logout(data="auto download start title={}".format(title))
        logout(data="auto download dest={}".format(dest))

        self._ensure_dirs()

        # stop duplicate parallel downloads for same title
        now = time.time()
        last = self.download_starts.get(title, 0)
        if now - last < 20:
            logout(data="skip duplicate download for {}".format(title))
            return
        self.download_starts[title] = now

        # provider order similar to plugin logic
        ok = False
        is_arabic = contains_arabic_text(title)

        if is_arabic:
            logout(data="poster arabic title -> elcinema first")
            try:
                ok = self._elcinema_json_poster_download(title, dest)
            except Exception as err:
                logout(data="elcinema outer error: {}".format(err))

        if not ok:
            try:
                ok = self._tmdb_download(title, dest)
            except Exception as err:
                logout(data="tmdb outer error: {}".format(err))

        if not ok and not is_arabic:
            try:
                ok = self._elcinema_json_poster_download(title, dest)
            except Exception as err:
                logout(data="elcinema outer error: {}".format(err))

        if not ok:
            try:
                ok = self._tvdb_download(title, dest)
            except Exception as err:
                logout(data="tvdb outer error: {}".format(err))

        if not ok:
            try:
                ok = self._maze_download(title, dest)
            except Exception as err:
                logout(data="maze outer error: {}".format(err))

        if ok:
            logout(data="auto download success for {}".format(title))
        else:
            logout(data="auto download failed for {}".format(title))

    # --------------------------- renderer -------------------------------

    def changed(self, what):
        logout(data="changed called")
        try:
            logout(data="changed what={}".format(what))
        except:
            pass

        if not self.instance:
            logout(data="no instance")
            return

        if what[0] == self.CHANGED_CLEAR:
            logout(data="changed clear")
            self.instance.hide()
            return

        evnt = ''
        pstrNm = ''
        evntNm = ''

        try:
            event = self.source.event
            logout(data="event={}".format(event))

            if not event:
                logout(data="no event")
                self.instance.hide()
                return

            evnt = event.getEventName()
            logout(data="event raw={}".format(evnt))

            if not evnt:
                logout(data="empty event name")
                self.instance.hide()
                return

            evntNm = self._clean_title(evnt)
            logout(data="event cleaned={}".format(evntNm))

            if not evntNm:
                logout(data="clean title empty")
                self.instance.hide()
                return

            pstrNm = self._poster_path(evntNm)
            logout(data="poster expected path={}".format(pstrNm))
            logout(data="poster exists={}".format(os.path.exists(pstrNm)))

            if os.path.exists(pstrNm):
                self.last_name = evntNm
                self._show_poster(pstrNm)
                return

            logout(data="poster missing -> try auto download")

            # show dummy first if available
            if self._show_dummy(evntNm):
                logout(data="dummy displayed while downloading")
            else:
                self.instance.hide()
                logout(data="no dummy available")

            # start background download
            start_new_thread(self._download_poster, (evntNm, pstrNm))

            # next zap / refresh / service event will show the file automatically
            # if you want forced repaint, zapping away/back or reopening the screen will show it

        except Exception as err:
            logout(data="changed error={}".format(err))
            self.instance.hide()
            return
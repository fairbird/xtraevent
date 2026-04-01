# -*- coding: utf-8 -*-
# by digiteng...
# 07.2020 - 11.2020 - 11.2021
# <widget render="xtraParental" source="session.Event_Now" position="0,0" size="60,60" alphatest="blend" zPosition="2" transparent="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, loadPNG
from Components.config import config
import re
import json
import os
from Plugins.Extensions.xtraEvent.skins.xtraSkins import *
from Plugins.Extensions.xtraEvent.xtraTitleHelper import *
# --------------------------- Logfile -------------------------------

from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile

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




myfile=dir_path + "/parental.log"
## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)


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


# ----------------------------- so muss das commando aussehen , um in den file zu schreiben  ------------------------------
logout(data="start xtraParental")


try:
    import sys
    if sys.version_info[0] == 3:
        from builtins import str
except:
    pass

pratePath = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/parental/"
try:
    pathLoc = config.plugins.xtraEvent.loc.value
    logout(data="start pathloc")
    logout(data=str(pathLoc))
except:
    pathLoc = ""

REGEX = re.compile(
    r'([\(\[]).*?([\)\]])|'
    r'(: odc\.\d+)|'
    r'(\d+: odc\.\d+)|'
    r'(\d+ odc\.\d+)|'
    r'!|'
    r'/.*|'
    r'\|\s[0-9]+\+|'
    r'[0-9]+\+|'
    r'([\(\[\|].*?[\)\]\|])|'
    r'(\"|\"\.|\"\,|\.)\s.+|'
    r'\"|'
    r'\*|'
    r'Премьера\.\s|'
    r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
    r'(х|Х|м|М|т|Т|д|Д)/с\s',
    re.DOTALL
)


def safe_str(value):
    try:
        if value is None:
            return ""
        return str(value).strip()
    except:
        return ""


def smart_capitalize_title(title):
    """
    Normalize title case without destroying sequel numbers or dotted decimals.
    Examples:
        THE MATRIX -> The Matrix
        the matrix -> The Matrix
        M3GAN 2.0 -> M3GAN 2.0
        F1 THE MOVIE -> F1 The Movie
    """
    try:
        title = safe_str(title)
        if not title:
            return ""

        small_words = {
            "a", "an", "and", "as", "at", "but", "by", "for", "from",
            "in", "into", "nor", "of", "on", "or", "over", "the", "to", "with"
        }

        words = title.split()
        result = []

        for i, word in enumerate(words):
            original = word

            # Keep pure numbers as they are
            if re.match(r'^\d+([.,]\d+)?$', original):
                result.append(original)
                continue

            # Keep words with digits inside as uppercase-ish originals
            # Examples: M3GAN, F1
            if re.search(r'\d', original):
                result.append(original.upper() if original.isupper() else original)
                continue

            lower_word = original.lower()

            if i > 0 and lower_word in small_words:
                result.append(lower_word)
            else:
                result.append(lower_word[:1].upper() + lower_word[1:])

        return " ".join(result)

    except Exception:
        return safe_str(title)


def clean_search_title(title):
    """
    Shared title cleaner for xtraInfo / xtraParental / xtraStar / xtraLogo.

    Goals:
    - remove EPG junk
    - remove explicit episode/season suffixes
    - normalize separators
    - remove ':' so saved filenames stay consistent
    - normalize title case so duplicates do not happen because of letter case
    """
    try:
        if not title:
            return ""

        original_title = safe_str(title)
        title = original_title

        # Remove service control chars
        title = title.replace('\xc2\x86', '').replace('\xc2\x87', '')

        # Normalize common live prefixes
        title = re.sub(r'^(live:\s*|LIVE:\s*|LIVE\s+|live\s+)', '', title).strip()

        # First run generic cleanup regex
        title = REGEX.sub('', title).strip()

        # Normalize separators early
        title = title.replace(":", " ")
        title = re.sub(r'[_]+', ' _ ', title)
        title = re.sub(r'[-]+', ' - ', title)
        title = re.sub(r'\s{2,}', ' ', title).strip()

        # Arabic season / episode patterns
        arabic_patterns = [
            r'\s*[_\-]+\s*ج\s*\d+\s*[_\-]+\s*ح\s*\d+.*$',
            r'\s*[_\-]+\s*ح\s*\d+\s*[_\-]+\s*ج\s*\d+.*$',

            r'\s*[_\-]+\s*جزء\s*\d+\s*[_\-]+\s*حلقة\s*\d+.*$',
            r'\s*[_\-]+\s*حلقة\s*\d+\s*[_\-]+\s*جزء\s*\d+.*$',
            r'\s*[_\-]+\s*الموسم\s*\d+\s*[_\-]+\s*الحلقة\s*\d+.*$',
            r'\s*[_\-]+\s*الحلقة\s*\d+\s*[_\-]+\s*الموسم\s*\d+.*$',

            r'\s+ج\s*\d+\s+ح\s*\d+.*$',
            r'\s+ح\s*\d+\s+ج\s*\d+.*$',
            r'\s+جزء\s*\d+\s+حلقة\s*\d+.*$',
            r'\s+حلقة\s*\d+\s+جزء\s*\d+.*$',
            r'\s+الموسم\s*\d+\s+الحلقة\s*\d+.*$',
            r'\s+الحلقة\s*\d+\s+الموسم\s*\d+.*$',

            r'\s*[_\-]+\s*ج\s*\d+.*$',
            r'\s*[_\-]+\s*ح\s*\d+.*$',
            r'\s*[_\-]+\s*جزء\s*\d+.*$',
            r'\s*[_\-]+\s*حلقة\s*\d+.*$',
            r'\s*[_\-]+\s*الموسم\s*\d+.*$',
            r'\s*[_\-]+\s*الحلقة\s*\d+.*$',

            r'\s+ج\s*\d+.*$',
            r'\s+ح\s*\d+.*$',
            r'\s+جزء\s*\d+.*$',
            r'\s+حلقة\s*\d+.*$',
            r'\s+الموسم\s*\d+.*$',
            r'\s+الحلقة\s*\d+.*$',
        ]

        for pattern in arabic_patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE).strip()

        # English TV episode patterns
        english_patterns = [
            r'\s*[_\-]+\s*S\d+\s*E\d+.*$',
            r'\s+S\d+\s*E\d+.*$',
            r'\s*[_\-]+\s*Season\s*\d+\s*Episode\s*\d+.*$',
            r'\s+Season\s*\d+\s*Episode\s*\d+.*$',
            r'\s*[_\-]+\s*Episode\s*\d+.*$',
            r'\s+Episode\s*\d+.*$',
            r'\s*[_\-]+\s*Ep\.?\s*\d+.*$',
            r'\s+Ep\.?\s*\d+.*$',
        ]

        for pattern in english_patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE).strip()

        # Final normalization
        title = re.sub(r'\s*[_\-:|]+\s*$', '', title).strip()
        title = re.sub(r'\s{2,}', ' ', title).strip()

        # Normalize case so same title from different channels becomes one filename
        title = smart_capitalize_title(title)

        logout(data="clean_search_title original={}".format(original_title))
        logout(data="clean_search_title result={}".format(title))

        return title

    except Exception as e:
        logout(data="clean_search_title error: {}".format(str(e)))
        return smart_capitalize_title(safe_str(title))

class xtraParental(Renderer):

    def __init__(self):
        logout(data="init")

        Renderer.__init__(self)
        self.rateNm = ''

    GUI_WIDGET = ePixmap
    def changed(self, what):
        logout(data="changed")
        if not self.instance:
            return
        else:
            logout(data="rate-prate-parentname")
            rate = ""
            prate = ""
            parentName = ""
            event = self.source.event
            if event:
                logout(data="event")
                fd = "{}{}{}".format(event.getEventName(), event.getShortDescription(), event.getExtendedDescription())
                ppr = [r"[aA]b ((\d+))", r"[+]((\d+))", r"Od lat: ((\d+))"]
                #ppr = ["[aA]b ((\d+))", "[+]((\d+))", "Od lat: ((\d+))"]
                for i in ppr:
                    logout(data="for i")
                    prr = re.search(i, fd)
                    if prr:
                        logout(data="prr")
                        logout(data=str(prr))
                        try:
                            logout(data="prr1")
                            parentName = prr.group(1)
                            parentName = parentName.replace("7", "6")
                            break
                        except:
                            logout(data="prr2")
                            pass
                else:
                    logout(data="event 2")
                    evnt = event.getEventName()
                    logout(data="event")
                    logout(data=str(evnt))
                    evntNm = clean_search_title(evnt)
                    logout(data="evntNm")
                    logout(data=str(evntNm))
                    def map_rating_to_fsk(value):
                        value = str(value or "").strip().upper()
                        if not value:
                            return ""

                        rating_map = {
                            "TV-Y7": "6",
                            "TV-Y": "6",
                            "TV-14": "12",
                            "TV-PG": "16",
                            "TV-G": "0",
                            "TV-MA": "18",
                            "PG-13": "16",
                            "PG": "12",
                            "R": "18",
                            "NC-17": "18",
                            "G": "0",
                            "0": "0",
                            "6": "6",
                            "7": "6",
                            "9": "6",
                            "10": "12",
                            "11": "12",
                            "12": "12",
                            "13": "12",
                            "14": "16",
                            "15": "16",
                            "16": "16",
                            "17": "18",
                            "18": "18",
                        }

                        if value in rating_map:
                            return rating_map[value]

                        match = re.search(r"(\d{1,2})", value)
                        if match:
                            num = int(match.group(1))
                            if num <= 6:
                                return "6" if num else "0"
                            elif num <= 13:
                                return "12"
                            elif num <= 16:
                                return "16"
                            else:
                                return "18"
                        return ""

                    def get_tmdb_rating(data):
                        # TV result: {"results": [{"iso_3166_1": "DE", "rating": "16"}, ...]}
                        if isinstance(data, dict) and isinstance(data.get("results"), list):
                            preferred_countries = ["DE", "US", "GB"]
                            results = data.get("results", [])
                            for country in preferred_countries:
                                for item in results:
                                    if item.get("iso_3166_1") == country and item.get("rating"):
                                        return item.get("rating")
                            for item in results:
                                if item.get("rating"):
                                    return item.get("rating")

                        # Movie result: {"results": [{"iso_3166_1": "DE", "release_dates": [{"certification": "16"}, ...]}]}
                        if isinstance(data, dict) and isinstance(data.get("results"), list):
                            preferred_countries = ["DE", "US", "GB"]
                            results = data.get("results", [])
                            for country in preferred_countries:
                                for item in results:
                                    if item.get("iso_3166_1") == country:
                                        for rel in item.get("release_dates", []):
                                            cert = rel.get("certification")
                                            if cert:
                                                return cert
                            for item in results:
                                for rel in item.get("release_dates", []):
                                    cert = rel.get("certification")
                                    if cert:
                                        return cert

                        return ""

                    try:
                        prefer_tmdb = bool(config.plugins.xtraEvent.tmdb.value)
                    except:
                        prefer_tmdb = True

                    rating_files = get_rated_json_candidates(pathLoc, evntNm, prefer_tmdb=prefer_tmdb)

                    for rating_json in rating_files:
                        logout(data="rating json")
                        logout(data=str(rating_json))
                        if os.path.exists(rating_json):
                            logout(data="json path check")
                            try:
                                with open(rating_json) as f:
                                    data = json.load(f)

                                # New TMDB dedicated parental json
                                if isinstance(data, dict) and data.get("parental"):
                                    prate = data.get("parental")

                                # OMDB rated json or OMDB info json
                                elif isinstance(data, dict) and data.get("Rated"):
                                    prate = data.get("Rated")

                                else:
                                    prate = ""

                                if prate:
                                    break

                            except Exception as e:
                                logout(data="rating read error: {}".format(str(e)))

                    logout(data="prate")
                    logout(data=str(prate))
                    rate = map_rating_to_fsk(prate)
                    if rate:
                        logout(data="rate leer schreibe parentName")
                        parentName = str(rate)

                if parentName:
                    logout(data="parentName")
                    logout(data=str(parentName))
                    rateNm = "{}FSK_{}.png".format(pratePath, parentName)
                    logout(data="rateNm")
                    logout(data=str(rateNm))
                    self.instance.setPixmap(loadPNG(rateNm))
                    self.instance.setScale(1)
                    self.instance.show()
                else:
                    logout(data="parentName-NA")
                    self.instance.setPixmap(loadPNG("{}FSK_NA.png".format(pratePath)))
                    self.instance.setScale(1)
                    self.instance.show()
            else:
                logout(data="parentName-NA-2")
                self.instance.setPixmap(loadPNG("FSK_NA.png".format(pratePath)))
                self.instance.setScale(1)
                self.instance.show()
            return

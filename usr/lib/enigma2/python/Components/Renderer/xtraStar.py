# -*- coding: utf-8 -*-
# by digiteng
# patched for TMDB star support + stronger title cleaning
# <widget source="ServiceEvent" render="xtraStar" position="750,390" size="200,20" alphatest="blend" transparent="1" zPosition="3" />
# or
# <widget source="ServiceEvent" render="xtraStar" pixmap="xtra/star.png" position="750,390" size="200,20" alphatest="blend" transparent="1" zPosition="3" />

from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from Components.VariableValue import VariableValue
from Components.config import config
from enigma import ePoint, eWidget, eSize, eSlider, loadPNG
from Plugins.Extensions.xtraEvent.xtraTitleHelper import *

import re
import json
import os
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




myfile=dir_path + "/star.log"
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
logout(data="start xtraStar")
try:
    pathLoc = config.plugins.xtraEvent.loc.value
except:
    pathLoc = ""

star = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/star/star.png"
starBackgrund = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/star/star_back.png"

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


def get_star_rating_from_json(data):
    """
    Priority:
    1) dedicated TMDB star json -> {"star": "..."}
    2) OMDB info json -> {"imdbRating": "..."}
    3) TMDB details json -> {"vote_average": ...}
    """
    try:
        if not isinstance(data, dict):
            return None

        if data.get("star") not in (None, ""):
            return float(data.get("star"))

        if data.get("imdbRating") not in (None, "", "N/A"):
            return float(data.get("imdbRating"))

        if data.get("vote_average") not in (None, ""):
            return float(data.get("vote_average"))

    except:
        pass

    return None


class xtraStar(VariableValue, Renderer):
    GUI_WIDGET = eWidget

    def __init__(self):
        Renderer.__init__(self)
        VariableValue.__init__(self)
        self.star = None
        self.pxmp = None
        self.szX = 200
        self.szY = 20

    def applySkin(self, desktop, screen):
        attribs = self.skinAttributes[:]
        for attrib, value in self.skinAttributes:
            if attrib == 'size':
                self.szX = int(value.split(',')[0])
                self.szY = int(value.split(',')[1])
            elif attrib == 'pixmap':
                self.pxmp = value

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, screen)

    def changed(self, what):
        if not self.instance:
            return

        if what[0] == self.CHANGED_CLEAR:
            if self.star:
                self.star.hide()
            return

        event = self.source.event
        if not event:
            if self.star:
                self.star.hide()
            return

        try:
            evnt = event.getEventName()
            evntNm = clean_search_title(evnt)

            if not evntNm:
                self.star.hide()
                return

            try:
                prefer_tmdb = bool(config.plugins.xtraEvent.tmdb.value)
            except:
                prefer_tmdb = True

            rating_files = get_star_json_candidates(pathLoc, evntNm, prefer_tmdb=prefer_tmdb)

            rating_value = None

            for rating_json in rating_files:
                if os.path.exists(rating_json):
                    try:
                        with open(rating_json) as f:
                            data = json.load(f)

                        rating_value = get_star_rating_from_json(data)
                        if rating_value is not None:
                            break
                    except:
                        pass

            if rating_value is None:
                self.star.hide()
                return

            rtng = int(10 * float(rating_value))
            if rtng < 0:
                rtng = 0
            if rtng > 100:
                rtng = 100

            self.star.setValue(rtng)

            if self.pxmp is None or self.pxmp == "":
                self.star.setPixmap(loadPNG(star))
                self.star.setBackgroundPixmap(loadPNG(starBackgrund))
            else:
                self.star.setPixmap(loadPNG(self.pxmp))
                self.star.setBackgroundPixmap(loadPNG(starBackgrund))

            self.star.move(ePoint(0, 0))
            self.star.resize(eSize(self.szX, self.szY))
            self.star.setAlphatest(2)
            self.star.setRange(0, 100)
            self.star.show()

        except:
            self.star.hide()
            return

    def GUIcreate(self, parent):
        self.instance = eWidget(parent)
        self.star = eSlider(self.instance)
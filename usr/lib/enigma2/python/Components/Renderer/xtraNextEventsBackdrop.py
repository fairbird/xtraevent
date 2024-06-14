# -*- coding: utf-8 -*-
# by digiteng...05.2020, 08.2020, 11.2021, 12.2021
# for channellist,
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="1" usedImage="backdrop" delayPic="200" position="840,420" size="100,60" zPosition="5" />
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="2" usedImage="backdrop" delayPic="200" position="940,420" size="100,60" zPosition="5" />
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="3" usedImage="backdrop" delayPic="200" position="1040,420" size="100,60" zPosition="5" />
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="4" usedImage="backdrop" delayPic="200" position="1140,420" size="100,60" zPosition="5" />
# ...
# usedImage="backdrop", usedImage="poster", usedImage="banner"
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, loadJPG, eTimer, eEPGCache
from Components.config import config
import os
import re

# --------------------------- Logfile -------------------------------

from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraNextEventsBackdrop.log"

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


NoImage = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film.jpg"
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

class xtraNextEventsBackdrop(Renderer):

    def __init__(self):
        Renderer.__init__(self)

        self.nxEvnt = 0
        self.nxEvntUsed = ""
        self.delayPicTime = 100
        self.epgcache = eEPGCache.getInstance()
        self.timer = eTimer()
        self.timer.callback.append(self.showPicture)

    def applySkin(self, desktop, parent):
        attribs = self.skinAttributes[:]
        for attrib, value in self.skinAttributes:
            if attrib == "size":
                self.piconsize = value
            elif attrib == 'nextEvent':          # 0(current), 1, 2, 3.........
                self.nxEvnt = int(value)
                logout(data="nextEvent")
                logout(data=str(self.nxEvnt))
            elif attrib == 'usedImage':          # poster, banner, backdrop
                self.nxEvntUsed = value
            elif attrib == 'delayPic':          # delay time(ms) for poster-banner-backdrop showing...
                self.delayPicTime = int(value)

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap
    def changed(self, what):
        logout(data="changed")
        if not self.instance:
            return
        else:
            if what[0] != self.CHANGED_CLEAR:
                self.instance.hide()
                self.timer.start(self.delayPicTime, True)
            else:
                self.instance.hide()

    def showPicture(self):
        evnt = ''
        pstrNm = ''
        evntNm = ''
        events = ''
        try:
            ref = self.source.service
            if ref:
                events = self.epgcache.lookupEvent(['T', (ref.toString(), 0, -1, 1200)])
                if events:
                    logout(data="showPicture")
                    evnt = events[self.nxEvnt][0]
                    logout(data=str(evnt))
                    evntNm = REGEX.sub('', evnt).strip()
                    logout(data=str(evntNm))
                    pstrNm = "{}xtraEvent/backdrop/{}/{}.jpg".format(pathLoc, self.nxEvntUsed, evntNm)
                    #pstrNm = "{}xtraEvent/{}/{}.jpg".format(pathLoc, self.nxEvntUsed, evntNm)
                    logout(data=str(pstrNm))
                    if os.path.exists(pstrNm):
                        self.instance.setPixmap(loadJPG(pstrNm))
                        self.instance.setScale(1)
                        self.instance.show()
                    else:
                        self.instance.hide()
                else:
                    self.instance.hide()
            else:
                self.instance.hide()
                return
        except:
            return

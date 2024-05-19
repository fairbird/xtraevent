# -*- coding: utf-8 -*-
# by digiteng...04.2020 - 11.2020 - 11.2021
# <widget source="ServiceEvent" render="xtraBackdrop" position="785,75" size="300,170" zPosition="2" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, loadJPG, eServiceCenter
from Components.config import config
import re
import os

# --------------------------- Logfile -------------------------------

from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraBackdrop.log"

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

piconPath = ""
paths = ('/media/hdd/picon/', '/media/usb/picon/', '/media/mmc/picon/', 
'/usr/share/enigma2/picon/', '/picon/', '/media/sda1/picon/', 
'/media/sda2/picon/', '/media/sda3/picon/')
for path in paths:
    if os.path.isdir(path):
        piconPath = path
        break

try:
    import sys
    if sys.version_info[0] == 3:
        from builtins import str
except:
    pass

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

class xtraBackdrop(Renderer):
    def __init__(self):
        Renderer.__init__(self)

    GUI_WIDGET = ePixmap
    def changed(self, what):
        logout(data="changed")
        if not self.instance:
            return
        else:
            logout(data="changed ist jpg vorhanden")
            if what[0] != self.CHANGED_CLEAR:
                evnt = ''
                pstrNm = ''
                evntNm = ''
                try:
                    event = self.source.event
                    logout(data=str(event))
                    if event:
                        logout(data="if event")
                        evnt = event.getEventName()
                        logout(data=str(evnt))
                        evntNm = REGEX.sub('', evnt).strip()
                        logout(data=str(evntNm))
                        pstrNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
                        logout(data=str(pstrNm))
                        if os.path.exists(pstrNm):
                            logout(data="jpg vorhanden")
                            self.instance.setPixmap(loadJPG(pstrNm))
                            self.instance.setScale(1)
                            self.instance.show()
                        else:
                            logout(data="jpg nicht vorhanden")
                            pstrNmno = "{}xtraEvent/backdrop/dummy/{}.jpg".format(pathLoc, evntNm)
                            logout(data=str(pstrNmno))
                            if os.path.exists(pstrNmno):
                                logout(data="jpg dummy vorhanden")
                                self.instance.setPixmap(loadJPG(pstrNmno))
                                self.instance.setScale(1)
                                self.instance.show()
                                logout(data="changed ende jpg dummy vorhanden ")
                            else:
                                logout(data="changed ende jpg dummy nicht vorhanden ")
                                self.showPicon()
                    else:
                        logout(data="no event")
                        self.showPicon()
                except Exception as err:
                    logout(data="no ")
                    with open("/tmp/xtra_error.log", "a+") as f:
                        f.write("xtraBackdrop(Renderer), %s, %s\n"%(evntNm, err))
            else:
                logout(data="nichts changed")
                self.instance.hide()
                return

    def showPicon(self):
        logout(data="show Picon")
        ref = ""
        info = None
        ChNm=""
        try:
            import NavigationInstance
            ref = NavigationInstance.instance.getCurrentlyPlayingServiceReference()
            ChNm = eServiceCenter.getInstance().info(ref).getName(ref)
            ChNm = ChNm.replace('\xc2\x86', '').replace('\xc2\x87', '')
            ChNm = ChNm.lower().replace('&', 'and').replace('+', 'plus').replace('*', 'star').replace(' ', '').replace('.', '')

            picName = "{}{}.png".format(piconPath, ChNm)
            picName = picName.strip()
            if os.path.exists(picName):
                self.instance.setScale(2)
                self.instance.setPixmapFromFile(picName)
                self.instance.setAlphatest(2)
                self.instance.show()

            elif not os.path.exists(picName):
                picName = "{}{}.png".format(piconPath, str(ref).replace(':', '_'))
                picName = picName.replace('_.png', '.png')
                if os.path.exists(picName):
                    self.instance.setScale(2)
                    self.instance.setPixmapFromFile(picName)
                    self.instance.setAlphatest(2)
                    self.instance.show()

                else:
                    picName = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/picon_default.png"
                    self.instance.setScale(2)
                    self.instance.setPixmapFromFile(picName)
                    self.instance.setAlphatest(2)
                    self.instance.show()
        except Exception as err:
            with open("/tmp/xtra_error.log", "a+") as f:
                f.write("xtraBackdrop(Renderer) /picon, %s\n\n"%err)

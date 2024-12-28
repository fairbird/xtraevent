# -*- coding: utf-8 -*-
# by digiteng...05.2024, 10.2024  , danke , habe es etwas umgearbeitet
# <widget source="session.CurrentService" render="xtraCast" noWrap="1" 
# castNum="0" castNameColor="#ffffff" castCaracterColor="#999999" castNameFont="Console; 14" castCaracterFont="Regular; 12" 
# position="80,455" size="154,462" zPosition="1" backgroundColor="background" transparent="1" />

from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePoint, eWidget, eSize, eLabel, gFont, ePixmap, eEPGCache, loadJPG
from skin import parseColor
from Components.config import config
from Tools.xtraTool import REGEX, pathLoc
from Plugins.Extensions.xtraEvent.download import REGEX, pathLoc

import re
import os
# --------------------------- Logfile -------------------------------


from datetime import datetime, timedelta
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraevent-cast.log"

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
    r'[\u0600-\u06FF]+'  # Arabische Schrift
    , re.DOTALL)

class xtraCast(Renderer):
    def __init__(self):
        logout(data="init")
        Renderer.__init__(self)
        # self.epgcache = eEPGCache.getInstance()
        self.castNamefontType = "Regular"
        self.castNamefontSize = 25
        self.castCaracterfontType = "Regular"
        self.castCaracterfontSize = 25
        self.csx, self.csy = 205,470
        self.cpx, self.cpy = 0,0
        self.foregroundColor = "#ffffff"
        self.backgroundColor = "#000000"
        self.castNameColor = "#0099ccff"
        self.castCaracterColor = "#001edb76"
        self.castNamenumber = 0
        space=20
        self.namesize = 80
        self.pigsize = 277
        self.charactersize = 80
        self.chacterpos = 0
        self.pigpos = self.chacterpos + self.namesize
        self.namepos = self.chacterpos + self.namesize + self.pigsize + space
        # jpg ist 185x277  , size 185 , 80 + 277 + 20 + 80 = 457
        logout(data="positionen")
        logout(data=str(self.chacterpos))
        logout(data=str(self.pigpos))
        logout(data=str(self.namepos))

        # Übergabe einer Variable
        from Plugins.Extensions.xtraEvent.xtra_event_name import eventname
        Name = "Max Mustermann"
        result = eventname(Name)
        logout(data=str(result))

    def applySkin(self, desktop, screen):
        logout(data="applySkin     hier vom skin die daten holen")
        attribs = self.skinAttributes[:]
        for attrib, value in self.skinAttributes:
            if attrib == 'backgroundColor':
                self.backgroundColor = value
            if attrib == 'castNameColor':
                self.castNameColor = value
            if attrib == 'castCaracterColor':
                self.castCaracterColor = value
            if attrib == 'castNum':
                self.castNamenumber = int(value)
            if attrib == 'castNameFont':
                self.castNamefontType = value.split(";")[0]
                self.castNamefontSize = value.split(";")[1]
            if attrib == 'castCaracterFont':
                self.castCaracterfontType = value.split(";")[0]
                self.castCaracterfontSize = value.split(";")[1]
            if attrib == 'size':
                self.csx = int(value.split(",")[0])
                self.csy = int(value.split(",")[1])
                logout(data="csx")
                logout(data=str(self.csx))
                logout(data="csy")
                logout(data=str(self.csy))
            if attrib == 'position':
                self.cpx = int(value.split(",")[0])
                self.cpy = int(value.split(",")[1])
                logout(data="cpx")
                logout(data=str(self.cpx))
                logout(data="cpy")
                logout(data=str(self.cpy))


        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, screen)

    GUI_WIDGET = eWidget
    def changed(self, what):
        logout(data="changed start mit Nummer")

        if not self.instance:
            return
        if what[0] == self.CHANGED_CLEAR:
            return
        self.castName.hide()
        self.castNamePic.hide()
        self.castCaracter.hide()
        ref=""
        evnt=""
        events=None
        event = self.source.event
        logout(data="nummer anfrage")

        # <widget source="session.Event_Now" render="xtraCast" noWrap="1"
        # castNum="0"
        # castNameColor="#ffffff"
        # castCaracterColor="#999999"
        # castNameFont="Console; 24"
        # castCaracterFont="Regular; 25"
        # position="190,110"
        # size="154,462"
        # zPosition="3" backgroundColor="background" transparent="1" />
        if event:
            try:
                logout(data="#############################################")
                logout(data="Sendungs name")
                evnt = event.getEventName()
                logout(data=str(evnt))
                # so vorher aber da passen die namen nicht zum download
                #evntNm = REGEX.sub('', evnt).strip()
                #logout(data="nach Regex Tools name")
                #logout(data=str(evntNm))

                #logout(data="nach Regex meiner name")
                #title = REGEX.sub('', evnt).strip()
                #logout(data=str(title))
                #evntNm=title
                #logout(data="#################### muss in evnNm stehen #########################")

                # hier live: entfernen
                Name = evnt.replace('\xc2\x86', '').replace('\xc2\x87', '').replace("live: ", "").replace("LIVE ", "")
                evnt = Name.replace("live: ", "").replace("LIVE ", "").replace("LIVE: ", "").replace("live ", "")
                logout(data="name live rausnehmen")
                logout(data=evnt)

                # hier versuch name nur vor dem :
                #name1 = evnt.split(": ", 1)
                #Name = name1[0]
                #logout(data="name   : abtrennen ")
                #logout(data=Name)

                evnt = Name
                # -------------------------------

                evntNm = REGEX.sub('', evnt).strip()
                logout(data=str(evntNm))
                # ------------------------------ name setht in evntNm drin ---------------------------------------------
                cf=""
                cNm=""
                logout(data="name")
                logout(data=str(evnt))
                castsFolder = "{}/casts/{}".format(pathLoc, evntNm)

                logout(data="name")
                logout(data=str(evntNm))
                logout(data="pathLoc")
                logout(data=str(pathLoc))
                logout(data="castsFolder")
                logout(data=str(castsFolder))

                if os.path.isdir(castsFolder):
                    logout(data="file vorhanden")
                    #castFiles = sorted(os.listdir(castsFolder))
                    castFiles = sorted([f for f in os.listdir(castsFolder) if f.lower().endswith('.jpg')])
                    logout(data="list files")
                    logout(data=str(castFiles))
                    if castFiles:
                        try:
                            cf = castFiles[self.castNamenumber]
                            logout(data="cf")
                            logout(data=str(cf))
                        except:
                            return


                        logout(data="------------------------------ Orginal csx: {}, csy: {}".format(self.csx, self.csy))

                        # --------------------------------- hier Pig ---------------------------------------------------
                        # Das Bild wird mit setPixmapFromFile geladen
                        self.castNamePic.setPixmapFromFile("{}/{}".format(castsFolder, cf))
                        logout(data="namePic")
                        logout(data=str(self.castNamePic.setPixmapFromFile))

                        # Die Größe wird durch resize festgelegt
                        # self.csx: Breite des Bildes.
                        # self.csy // 2: Höhe des Bildes (hälfte der gesamten Bildschirmhöhe).
                        self.castNamePic.resize(eSize(self.csx, self.pigsize))
                        # Das Bild wird oben positioniert
                        logout(data="----------------------------- csx: {}, pigsize: {}".format(self.csx, self.pigsize))
                        self.castNamePic.move(ePoint(0, self.pigpos))
                        logout(data="----------------------------- pigpos Y: {}".format(self.pigpos))

                        self.castNamePic.setTransparent(1)
                        self.castNamePic.setZPosition(3)
                        self.castNamePic.setScale(1)
                        self.castNamePic.setAlphatest(2)
                        self.castNamePic.show()

                        # ---------------------------- hier der Name --------------------------------------------------
                        # so ist der Filename , 00_Archie Madekwe(Jann Mardenborough).jpg
                        # Der Name und CaracterName wird aus dem Dateinamen extrahiert
                        # Entfernt die Dateiendung .jpg mit [:-4].
                        # Schneidet die ersten 3 Zeichen ab mit [3:].
                        # Trennt den Hauptnamen vor dem ersten (.
                        # Trennt den Text in der Klammer () und entfernt die Klammern.
                        cCrctr = cf[:-4][3:].split("(")[1].replace(")", "")
                        logout(data="charcter")
                        logout(data=str(cCrctr))
                        cName = " ".join(cf[:-4][3:].split("(")[0].split())
                        logout(data="name")
                        logout(data=str(cName))
                        self.castName.setText(cName)
                        # ------------------------------- name aufsetzen -----------------------------------------------
                        self.castName.setBackgroundColor(parseColor(self.backgroundColor))
                        self.castName.setForegroundColor(parseColor(self.castNameColor))
                        logout(data="----------------------------- csx: {}, namesize: {}".format(self.csx, self.namesize))
                        self.castName.resize(eSize(self.csx, self.namesize))
                        logout(data="----------------------------- name position Y: {}".format(self.namepos))
                        # Position unter dem Bild: Höhe: self.csy // 2 (hälfte der Bildschirmhöhe).
                        self.castName.move(ePoint(0, self.namepos))

                        self.castName.setFont(gFont(self.castNamefontType, int(self.castNamefontSize)))
                        self.castName.setHAlign(eLabel.alignLeft)
                        self.castName.setTransparent(1)
                        self.castName.setZPosition(99)
                        self.castName.show()

                        # ------------------------------------ hier charter --------------------------------------------

                        self.castCaracter.setText(cCrctr)
                        self.castCaracter.setBackgroundColor(parseColor(self.backgroundColor))
                        self.castCaracter.setForegroundColor(parseColor(self.castCaracterColor))
                        logout(data="-------------------- csx: {}, charctersize: {}".format(self.csx, self.charactersize))
                        self.castCaracter.resize(eSize(self.csx, self.charactersize))
                        logout(data="------------------------- charter position Y: {}".format(self.chacterpos))
                        # # Position unter dem Bild: Höhe: self.csy // 2 (hälfte der Bildschirmhöhe) + platz + schrifthoehe.
                        self.castCaracter.move(ePoint(0, self.chacterpos))


                        self.castCaracter.setFont(gFont(self.castCaracterfontType, int(self.castCaracterfontSize)))
                        self.castCaracter.setHAlign(eLabel.alignLeft)
                        self.castCaracter.setTransparent(1)
                        self.castCaracter.setZPosition(99)
                        self.castCaracter.show()

                    else:
                        logout(data="file nicht vorhanden 1")
                        self.castName.hide()
                        self.castNamePic.hide()
                        self.castCaracter.hide()
                else:
                    logout(data="folder nicht vorhanden 2")
                    self.castName.hide()
                    self.castNamePic.hide()
                    self.castCaracter.hide()

            except Exception as err:
                logout(data="exeption error ")

        else:
            logout(data="file nicht vorhanden 3")
            self.castName.hide()
            self.castNamePic.hide()
            self.castCaracter.hide()
            return

    def GUIcreate(self, parent):
        logout(data="GUIcreate")
        self.instance = eWidget(parent)
        self.castName = eLabel(self.instance)
        self.castCaracter = eLabel(self.instance)
        self.castNamePic = ePixmap(self.instance)

    def GUIdelete(self):
        logout(data="GUIdelete")
        self.castName = None
        self.castCaracter = None
        self.castNamePic = None

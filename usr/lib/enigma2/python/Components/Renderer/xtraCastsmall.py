# -*- coding: utf-8 -*-
# by digiteng...05.2024, 10.2024
# <widget source="session.CurrentService" render="xtraCastsmall" noWrap="1" 
# castNum="0" castNameColor="#ffffff" castCaracterColor="#999999" castNameFont="Console; 14" castCaracterFont="Regular; 12" 
# position="80,455" size="154,462" zPosition="1" backgroundColor="background" transparent="1" />

from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePoint, eWidget, eSize, eLabel, gFont, ePixmap, eEPGCache, loadJPG
from skin import parseColor
from Components.config import config
from Tools.xtraTool import REGEX, pathLoc
import re
import os

from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile

import inspect
from Plugins.Extensions.xtraEvent.skins.xtraSkins import *
########################### log file loeschen ##################################

import os
########################### log file loeschen ##################################
dir_path = "/tmp/xtraevent"

try:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print("Verzeichnis wurde erstellt:", dir_path)
    else:
        print("Verzeichnis existiert bereits:", dir_path)
except Exception as e:
    print("Fehler beim Erstellen des Verzeichnisses:", e)




myfile=dir_path + "/castsmall.log"
## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
############################## File copieren ############################################
# fuer py2 die int und str anweisung raus genommen und das Grad zeichen

###########################  log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus



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

class xtraCastsmall(Renderer):
    def __init__(self):
        logout(data="init")
        Renderer.__init__(self)
        # self.epgcache = eEPGCache.getInstance()
        self.castNamefontType = "Regular"
        self.castNamefontSize = 12
        self.castCaracterfontType = "Regular"
        self.castCaracterfontSize = 10
        self.csx, self.csy = 200,30
        self.cpx, self.cpy = 0,0
        self.foregroundColor = "#ffffff"
        self.backgroundColor = "#000000"
        self.castNameColor = "#ffffff"
        self.castCaracterColor = "#cccccc"
        self.castNamenumber = 0

    def applySkin(self, desktop, screen):
        logout(data="applySkin")
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
        logout(data="changed")
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
        if event:
            try:
                evnt = event.getEventName()
                evntNm = REGEX.sub('', evnt).strip()
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
                    castFiles = sorted(os.listdir(castsFolder))
                    logout(data="list files")
                    logout(data=str(castFiles))
                    if castFiles:
                        try:
                            cf = castFiles[self.castNamenumber]
                            logout(data="cf")
                            logout(data=str(cf))
                        except:
                            return
                        self.castNamePic.setPixmapFromFile("{}/{}".format(castsFolder, cf))
                        logout(data="namePic")
                        logout(data=str(self.castNamePic.setPixmapFromFile))
                        self.castNamePic.resize(eSize(self.csx, self.csy // 2))

                        self.castNamePic.move(ePoint(0,0))
                        logout(data="csy")
                        logout(data=str(self.castNamePic))


                        self.castNamePic.setTransparent(1)
                        self.castNamePic.setZPosition(3)
                        self.castNamePic.setScale(1)
                        self.castNamePic.setAlphatest(2)
                        self.castNamePic.show()

                        cName = cf[:-4][3:].split("(")[0]
                        cCrctr = cf[:-4][3:].split("(")[1].replace(")", "")

                        self.castName.setText(cName)
                        self.castName.setBackgroundColor(parseColor(self.backgroundColor))
                        self.castName.setForegroundColor(parseColor(self.castNameColor))
                        self.castName.resize(eSize(self.csx, int(self.castNamefontSize) + 4))

                        self.castName.move(ePoint(0, (self.csy // 2) + 5))
                        logout(data="csy1")
                        logout(data=str(self.castName.move))


                        self.castName.setFont(gFont(self.castNamefontType, int(self.castNamefontSize)))
                        self.castName.setHAlign(eLabel.alignLeft)
                        self.castName.setTransparent(1)
                        self.castName.setZPosition(99)
                        self.castName.show()

                        self.castCaracter.setText(cCrctr)
                        self.castCaracter.setBackgroundColor(parseColor(self.backgroundColor))
                        self.castCaracter.setForegroundColor(parseColor(self.castCaracterColor))
                        self.castCaracter.resize(eSize(self.csx, self.csy // 2))

                        self.castCaracter.move(ePoint(0, (self.csy // 2) + 10 + int(self.castNamefontSize)))
                        logout(data="csy2")
                        logout(data=str(self.castCaracter.move))

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
                    logout(data="file nicht vorhanden 2")
                    self.castName.hide()
                    self.castNamePic.hide()
                    self.castCaracter.hide()

            except Exception as err:
                logout(data="file error ")
               
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

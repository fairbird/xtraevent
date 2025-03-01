# -*- coding: utf-8 -*-
# by digiteng...06.2020 - 08.2020 - 11.2021
# <widget source="session.Event_Now" render="xtraBanner" position="0,0" size="762,141" zPosition="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, ePicLoad, eEPGCache
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap
from Components.config import config
import os
import re

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
        r'\sح\s*\d+|'                # Entfernt Episodennummern in arabischen Serien
        r'\sج\s*\d+|'                # Entfernt Staffelangaben in arabischen Serien
        r'\sم\s*\d+|'                # Entfernt weitere Staffelangaben in arabischen Serien
        r'\d+$'                     # Entfernt Zahlen am Ende
        , re.DOTALL)

class xtraBanner(Renderer):

    def __init__(self):
        Renderer.__init__(self)

    GUI_WIDGET = ePixmap
    def changed(self, what):
        if not self.instance:
            return
        else:
            if what[0] != self.CHANGED_CLEAR:
                evnt = ''
                pstrNm = ''
                evntNm = ''
                try:
                    event = self.source.event
                    if event:
                        evnt = event.getEventName()

                        # hier live: entfernen
                        Name = evnt.replace('\xc2\x86', '').replace('\xc2\x87', '').replace("live: ", "").replace("LIVE ", "")
                        evnt = Name.replace("live: ", "").replace("LIVE ", "").replace("LIVE: ", "").replace("live ",
                                                                                                             "")
                        #logout(data="name live rausnehmen")
                        #logout(data=Name)

                        # hier versuch name nur vor dem :
                        #name1 = evnt.split(": ", 1)
                        #Name = name1[0]
                        #logout(data="name   : abtrennen ")
                        #logout(data=Name)

                        evnt = Name
                        # -------------------------------

                        evntNm = REGEX.sub('', evnt).strip()
                        pstrNm = "{}xtraEvent/banner/{}.jpg".format(pathLoc, evntNm)
                        if os.path.exists(pstrNm):
                            size = self.instance.size()
                            self.picload = ePicLoad()
                            sc = AVSwitch().getFramebufferScale()
                            if self.picload:
                                self.picload.setPara((size.width(), size.height(),  sc[0], sc[1], False, 1, '#00000000'))
                            result = self.picload.startDecode(pstrNm, 0, 0, False)
                            if result == 0:
                                ptr = self.picload.getData()
                                if ptr != None:
                                    self.instance.setPixmap(ptr)
                                    self.instance.show()
                            del self.picload
                        else:
                            self.instance.hide()
                    else:
                        self.instance.hide()
                except:
                    pass
            else:
                self.instance.hide()
                return

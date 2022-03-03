# -*- coding: utf-8 -*-
# by digiteng
# 11.2021
# for channellist
# <widget source="ServiceEvent" render="xtraStar" position="750,390" size="200,20" alphatest="blend" transparent="1" zPosition="3" />
# or
# <widget source="ServiceEvent" render="xtraStar" pixmap="xtra/star.png" position="750,390" size="200,20" alphatest="blend" transparent="1" zPosition="3" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from Components.VariableValue import VariableValue
from enigma import ePoint, eWidget, eSize, eSlider, loadPNG
from Components.config import config
import re
import json
import os

try:
	pathLoc = config.plugins.xtraEvent.loc.value
except:
	pathLoc = ""

star = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/star/star.png"
starBackgrund = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/star/star_back.png"

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

class xtraStar2(VariableValue, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableValue.__init__(self)
		self.star = None
		self.pxmp = None

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

	GUI_WIDGET = eWidget
	def changed(self, what):
		if not self.instance:
			return
		else:
			if what[0] != self.CHANGED_CLEAR:
				rating = None
				rtng = 0
				event = self.source.event
				if event:
					evnt = event.getEventName()
					try:
						evntNm = REGEX.sub('', evnt).strip()
						rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
						if os.path.exists(rating_json):
							with open(rating_json) as f:
								rating = json.load(f)['imdbRating']
							if rating:
								rtng = int(10*(float(rating)))
								self.star.setValue(rtng)
								if self.pxmp is None or self.pxmp == "":
									self.star.setPixmap(loadPNG(star))
									self.star.setBackgroundPixmap(loadPNG(starBackgrund))
								else:
									self.star.setPixmap(loadPNG(self.pxmp))
								self.star.move(ePoint(0, 0))
								self.star.resize(eSize(self.szX, self.szY))
								self.star.setAlphatest(2)
								self.star.setRange(0, 100)
								self.star.show()
							else:
								self.star.hide()
						else:
							self.star.hide()
					except:
						self.star.hide()
						return
				else:
					self.star.hide()
			else:
				self.star.hide()

	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.star = eSlider(self.instance)


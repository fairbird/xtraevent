# -*- coding: utf-8 -*-
# by digiteng...04.2020 - 11.2020 - 11.2021
# <widget source="ServiceEvent" render="xtraBackdrop" position="785,75" size="300,170" zPosition="2" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, loadJPG
from Components.config import config
import re
import os

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
		r'( -(.*?).*)|(,)|'
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
						evntNm = REGEX.sub('', evnt).strip()
						pstrNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
						if os.path.exists(pstrNm):
							self.instance.setPixmap(loadJPG(pstrNm))
							self.instance.setScale(1)
							self.instance.show()
						else:
							self.showPicon()
					else:
						self.showPicon()
				except Exception as err:
					with open("/tmp/xtra_error.log", "a+") as f:
						f.write("xtraBackdrop(Renderer), %s, %s\n"%(evntNm, err))
			else:
				self.instance.hide()
				return

	def showPicon(self):
		ref = ""
		info = None
		ChNm=""
		try:
			service = self.source.service
			ref = service.toString()
			info = self.source.info
			ChNm = info.getName(service)
			if ChNm is None:
				ChNm = info.getName()
			ChNm = ChNm.replace('\xc2\x86', '').replace('\xc2\x87', '')
			ChNm = ChNm.lower().replace('&', 'and').replace('+', 'plus').replace('*', 'star').replace(' ', '').replace('.', '')
			paths = ('/media/hdd/picon/', '/media/usb/picon/', '/media/mmc/picon/', 
			'/usr/share/enigma2/picon/', '/picon/', '/media/sda1/picon/', 
			'/media/sda2/picon/', '/media/sda3/picon/')
			for path in paths:
				picName = "{}{}.png".format(path, ChNm)
				picName = picName.strip()
				if os.path.exists(picName):
					self.instance.setScale(2)
					self.instance.setPixmapFromFile(picName)
					self.instance.show()
					break
				elif not os.path.exists(picName):
					picName = "{}{}.png".format(path, str(ref).replace(':', '_'))
					picName = picName.replace('_.png', '.png')
					if os.path.exists(picName):
						self.instance.setScale(2)
						self.instance.setPixmapFromFile(picName)
						self.instance.show()
						break
					else:
						picName = "/usr/share/enigma2/skin_default/picon_default.png"
						self.instance.setScale(2)
						self.instance.setPixmapFromFile(picName)
						self.instance.show()
		except Exception as err:
			with open("/tmp/xtra_error.log", "a+") as f:
				f.write("xtraBackdrop(Renderer) /picon, %s\n\n"%err)

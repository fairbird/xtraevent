# -*- coding: utf-8 -*-
# by digiteng...08.2020
# <widget source="session.Event_Now" render="xtraPoster" position="0,0" size="185,278" zPosition="1" />
from Renderer import Renderer
from enigma import ePixmap, loadJPG
from Components.config import config
import re
from Tools.Directories import fileExists

try:
	from Plugins.Extensions.xtraEvent.xtra import xtra
	pathLoc = config.plugins.xtraEvent.loc.value
except:
	pass

class xtraPoster(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.piconsize = (0,0)

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for (attrib, value) in self.skinAttributes:
			if attrib == "size":
				self.piconsize = value
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap
	def changed(self, what):
		if not self.instance:
			return
		else:
			event = ''
			pstrNm = ''
			evntNm = ''
			if what[0] != self.CHANGED_CLEAR:
				event = self.source.event
				if event:
					evnt = event.getEventName()
					evntNm = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", evnt).rstrip().lower()
					pstrNm = "{}xtraEvent/poster/{}.jpg".format(pathLoc, evntNm)
					if fileExists(pstrNm):
						self.instance.setScale(1)
						self.instance.setPixmap(loadJPG(pstrNm))
						self.instance.show()
					else:
						self.instance.hide()
				else:
					self.instance.hide()
			return

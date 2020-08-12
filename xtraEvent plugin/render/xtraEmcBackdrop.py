# -*- coding: utf-8 -*-
# by digiteng...07.2020 - 08.2020
# <widget source="Service" render="xtraEmcBackdrop" position="0,0" size="1280,720" zPosition="0"
from Renderer import Renderer
from enigma import ePixmap, loadJPG
from Components.Sources.ServiceEvent import ServiceEvent
from Components.Sources.CurrentService import CurrentService
from Components.config import config
from Tools.Directories import fileExists
import re

try:
	from Plugins.Extensions.xtraEvent.xtra import xtra
	pathLoc = config.plugins.xtraEvent.loc.value
except:
	pass

class xtraEmcBackdrop(Renderer):

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
			service = ''
			pstrNm = ''
			evntNm = ''
			if what[0] != self.CHANGED_CLEAR:
				service = self.source.getCurrentService()
				if service:
					evnt = service.getPath()
					movieNm = evnt.split('-')[-1].split(".")[0].strip().lower()
					movieNm = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", movieNm)
					pstrNm = "{}xtraEvent/EMC/{}-backdrop.jpg".format(pathLoc, movieNm.strip())
					if fileExists(pstrNm):
						self.instance.setScale(2)
						self.instance.setPixmap(loadJPG(pstrNm))
						self.instance.show()
					else:
						self.instance.setScale(2)
						self.instance.setPixmap(loadJPG("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/noMovie.jpg"))
						self.instance.show()
				else:
					self.instance.hide()
			return

# -*- coding: utf-8 -*-
# by digiteng...05.2020
# for channellist,
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="1" position="840,420" size="100,60" zPosition="5" />
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="2" position="940,420" size="100,60" zPosition="5" />
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="3" position="1040,420" size="100,60" zPosition="5" />
# <widget source="ServiceEvent" render="xtraNextEvents" nextEvent="4" position="1140,420" size="100,60" zPosition="5" />
# ...

from Renderer import Renderer
from enigma import ePixmap, ePicLoad, eTimer, eEPGCache, loadPNG
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap
from ServiceReference import ServiceReference
from Components.config import config
import re
import os

try:
	from Plugins.Extensions.xtraEvent.xtra import xtra
	if config.plugins.xtraEvent.locations.value == "internal":
		pathLoc = "/etc/enigma2/xtraEvent/backdrop/"
	else:
		pathLoc = "/media/{}/xtraEvent/backdrop/".format(config.plugins.xtraEvent.locations.value)
except:
	pathLoc = "/"


class xtraNextEvents(Renderer):

	def __init__(self):
		Renderer.__init__(self)

		self.pstrNm = ''
		self.evntNm = ''
		
		self.nxEvnt = 0
		self.epgcache = eEPGCache.getInstance()

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'nextEvent':
				self.nxEvnt = int(value)

		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap
	def changed(self, what):
		try:
			if not self.instance:
				return
			if what[0] == self.CHANGED_CLEAR:
				self.instance.hide()
			if what[0] != self.CHANGED_CLEAR:
				self.delay()


		except:
			pass

	def showEvents(self):
		cevnt = ''
		try:
			ref = self.source.service
			events = self.epgcache.lookupEvent(['IBDCTM', (ref.toString(), 0, 1, -1)])
			if events:
				cevnt = events[self.nxEvnt][4]
			else:
				pass
		except:
			pass
		try:
			evntN = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", cevnt)
			evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").replace("LOS ", "The ").rstrip()
			pstrNm = pathLoc + evntNm + ".jpg"
			if os.path.exists(pstrNm):
				size = self.instance.size()
				self.picload = ePicLoad()
				sc = AVSwitch().getFramebufferScale()
				if self.picload:
					self.picload.setPara((size.width(),
					size.height(),
					sc[0],
					sc[1],
					False,
					1,
					'#00000000'))
				result = self.picload.startDecode(pstrNm, 0, 0, False)
				if result == 0:
					ptr = self.picload.getData()
					if ptr != None:
						self.instance.setPixmap(ptr)
						self.instance.show()
			else:
				noEvnt = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/plugin2.png"
				self.instance.setPixmap(loadPNG(noEvnt))
				self.instance.show()
		except:
			self.instance.hide()
		
	def delay(self):
		self.timer = eTimer()
		self.timer.callback.append(self.showEvents)
		self.timer.start(500, True)

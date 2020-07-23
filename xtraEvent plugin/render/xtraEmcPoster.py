# -*- coding: utf-8 -*-
# by digiteng...07.2020
# <widget source="Service" render="xtraEmcPoster" position="0,0" size="185,278" zPosition="0"
from Renderer import Renderer
from enigma import ePixmap, eTimer, loadJPG
from Components.Sources.ServiceEvent import ServiceEvent
from Components.Sources.CurrentService import CurrentService
from Components.config import config
import os

try:
	from Plugins.Extensions.xtraEvent.xtra import xtra
	pathLoc = config.plugins.xtraEvent.loc.value
except:
	pass

class xtraEmcPoster(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.pstrNm = ''
		self.evntNm = ''

	GUI_WIDGET = ePixmap
	def changed(self, what):
		if not self.instance:
			return
		if what[0] == self.CHANGED_CLEAR:
			self.instance.hide()
		if what[0] != self.CHANGED_CLEAR:
			self.delay()

	def showPoster(self):
		try:

			service = self.source.getCurrentService()
			if service:
				evnt = service.getPath()
				movieNm = evnt.split('-')[-1].split(".")[0].strip()
				pstrNm = pathLoc + "xtraEvent/EMC/{}-poster.jpg".format(movieNm)
				if os.path.exists(pstrNm):
					self.instance.setPixmap(loadJPG(pstrNm))
					self.instance.show()

				else:
					self.instance.hide()

		except:
			return

	def delay(self):
		self.timer = eTimer()
		self.timer.callback.append(self.showPoster)
		self.timer.start(500, True)

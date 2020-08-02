# -*- coding: utf-8 -*-
# by digiteng...07.2020
# <widget source="Service" render="xtraEmcBackdrop" position="0,0" size="1280,720" zPosition="0"
from Renderer import Renderer
from enigma import ePixmap, eTimer, loadJPG
from Components.Sources.ServiceEvent import ServiceEvent
from Components.Sources.CurrentService import CurrentService
from Components.config import config
from Tools.Directories import fileExists

try:
	from Plugins.Extensions.xtraEvent.xtra import xtra
	pathLoc = config.plugins.xtraEvent.loc.value
except:
	pass

class xtraEmcBackdrop(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.pstrNm = ''

	GUI_WIDGET = ePixmap
	def changed(self, what):
		if not self.instance:
			return
		if what[0] == self.CHANGED_CLEAR:
			self.instance.hide()
		if what[0] != self.CHANGED_CLEAR:
			self.delay()

	def showBackdrop(self):
		try:
			service = self.source.getCurrentService()
			if service:
				evnt = service.getPath()
				movieNm = evnt.split('-')[-1].split(".")[0].strip()
				pstrNm = pathLoc + "xtraEvent/EMC/{}-backdrop.jpg".format(movieNm)
				if fileExists(pstrNm):
					self.instance.setPixmap(loadJPG(pstrNm))
					self.instance.show()
				else:
					self.instance.setPixmap(loadJPG("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/noMovie.jpg"))
					self.instance.show()
		except:
			return

	def delay(self):
		self.timer = eTimer()
		self.timer.callback.append(self.showBackdrop)
		self.timer.start(500, True)

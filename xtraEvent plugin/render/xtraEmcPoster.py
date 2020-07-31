# -*- coding: utf-8 -*-
# by digiteng...07.2020
# <widget source="Service" render="xtraEmcPoster" position="0,0" size="185,278" zPosition="0"
from Renderer import Renderer
from enigma import ePixmap, eTimer, ePicLoad
from Components.AVSwitch import AVSwitch
from Components.Sources.ServiceEvent import ServiceEvent
from Components.Sources.CurrentService import CurrentService
from Components.config import config
from Tools.Directories import fileExists

try:
	from Plugins.Extensions.xtraEvent.xtra import xtra
	pathLoc = config.plugins.xtraEvent.loc.value
except:
	pass

class xtraEmcPoster(Renderer):

	def __init__(self):
		Renderer.__init__(self)


	GUI_WIDGET = ePixmap
	def changed(self, what):
		if not self.instance:
			return
		if what[0] == self.CHANGED_CLEAR:
			self.instance.hide()
		if what[0] != self.CHANGED_CLEAR:
			self.delay()

	def showPoster(self):
		movieNm = ""
		try:
			service = self.source.getCurrentService()
			if service:
				evnt = service.getPath()
				movieNm = evnt.split('-')[-1].split(".")[0].strip()
				pstrNm = "{}xtraEvent/EMC/{}-poster.jpg".format(pathLoc, movieNm)
				if fileExists(pstrNm):
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
					del self.picload
			else:
				self.instance.hide()
				return
		except:
			return

	def delay(self):
		self.timer = eTimer()
		self.timer.callback.append(self.showPoster)
		self.timer.start(500, True)

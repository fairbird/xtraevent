# -*- coding: utf-8 -*-
# by digiteng...04.2020
# <widget source="session.Event_Now" render="xtraBanner" position="0,0" size="762,141" zPosition="1" />
from Renderer import Renderer
from enigma import ePixmap, ePicLoad
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap

import re
import os


if os.path.ismount('/media/hdd'):
	if os.path.isdir("/media/hdd/xtraEvent/"):
		pathLoc = "/media/hdd/xtraEvent/banner/"
elif os.path.ismount('/media/usb'):
	if os.path.isdir("/media/usb/xtraEvent/"):
		pathLoc = "/media/usb/xtraEvent/banner/"
elif os.path.isdir("/media/usb/xtraEvent/"):
	pathLoc = "/etc/enigma2/xtraEvent/banner/"
else:
	pathLoc = "/tmp/"

class xtraBanner(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.bannerName = ''

	GUI_WIDGET = ePixmap
	def changed(self, what):
		try:
			if not self.instance:
				return
			event = self.source.event
			if what[0] == self.CHANGED_CLEAR:
				self.instance.hide()
			if what[0] != self.CHANGED_CLEAR:
				if event:
					evnt = event.getEventName()
					evntN = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", evnt)
					evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").replace("LOS ", "The ").rstrip()
					self.dwn = pathLoc + "%s.jpg" %(evntNm)
					bannerName = pathLoc + evntNm + ".jpg"

					if os.path.exists(bannerName):
						try:
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
							result = self.picload.startDecode(bannerName, 0, 0, False)
							if result == 0:
								ptr = self.picload.getData()
								if ptr != None:
									self.instance.setPixmap(ptr)
									self.instance.show()
						except:
							self.instance.hide()
					else:
						self.instance.hide()
				else:
					self.instance.hide()
		except:
			return



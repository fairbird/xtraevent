# -*- coding: utf-8 -*-
# by digiteng...04.2020

# <widget source="session.Event_Now" render="xtraBackdrop" position="0,0" size="300,169" zPosition="1" />
from Renderer import Renderer
from enigma import ePixmap, ePicLoad, eTimer
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap

import re
import os



if os.path.ismount('/media/hdd'):
	if os.path.isdir("/media/hdd/xtraEvent/"):
		pathLoc = "/media/hdd/xtraEvent/backdrop/"
elif os.path.ismount('/media/usb'):
	if os.path.isdir("/media/usb/xtraEvent/"):
		pathLoc = "/media/usb/xtraEvent/backdrop/"
elif os.path.isdir("/etc/enigma2/xtraEvent/"):
	pathLoc = "/etc/enigma2/xtraEvent/backdrop/"
else:
	pathLoc = "/tmp/"


class xtraBackdrop(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.pstrNm = ''
		self.evntNm = ''



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

	def showBackdrop(self):
		try:
			event = self.source.event
			if event:
				evnt = event.getEventName()
				evntN = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", evnt)
				evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").replace("LOS ", "The ").rstrip()
				self.dwn_backdrop = pathLoc + "{}.jpg".format(evntNm)
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
					self.instance.hide()
			else:
				self.instance.hide()
		except:
			self.instance.hide()
			return



	def delay(self):
		self.timer = eTimer()
		self.timer.callback.append(self.showBackdrop)
		self.timer.start(500, True)

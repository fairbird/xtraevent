# -*- coding: utf-8 -*-
# by digiteng...05.2020
# <widget render="infoEvent" source="session.Event_Now" position="244,360" size="300,130" font="Regular; 14" halign="left" valign="top" zPosition="1" foregroundColor="foreground" backgroundColor="background" transparent="0" />
from Renderer import Renderer
from Components.VariableText import VariableText
from enigma import eLabel, eTimer

import re
import os


if os.path.ismount('/media/hdd'):
	if os.path.isdir("/media/hdd/xtraEvent/"):
		pathLoc = "/media/hdd/xtraEvent/infos/"
elif os.path.ismount('/media/usb'):
	if os.path.isdir("/media/usb/xtraEvent/"):
		pathLoc = "/media/usb/xtraEvent/infos/"
elif os.path.isdir("/etc/enigma2/xtraEvent/"):
	pathLoc = "/etc/enigma2/xtraEvent/infos/"
else:
	pathLoc = "/tmp/"

class xtraInfos(Renderer, VariableText):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)


	GUI_WIDGET = eLabel

	def changed(self, what):
		if what[0] == self.CHANGED_CLEAR:
			self.text = ''
		else:
			self.delay()

	def infos(self):
		event = self.source.event
		if event:
			evnt = event.getEventName()
			try:
				evntN = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)", "", evnt)
				evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").replace("LOS ", "The ").rstrip()
				info_file = pathLoc + "{}".format(evntNm)
				if os.path.exists(info_file):
					with open(info_file, "r") as f:
						info = f.read()
					self.text = "%s"%info
				else:
					self.text = ""
			except:
				return ""
		else:
			return ""

	def delay(self):
		self.timer = eTimer()
		self.timer.callback.append(self.infos)
		self.timer.start(100, True)

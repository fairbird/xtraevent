#!/usr/bin/python
# -*- coding: utf-8 -*-
from Renderer import Renderer
from enigma import ePixmap, eTimer, ePicLoad
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap
from Components.config import config
import re, os, gettext
from Tools.Directories import fileExists
from Components.Console import Console

REDC =  '\033[31m'
ENDC = '\033[m'

def cprint(text):
    print(REDC+"[xtraEvent] "+text+ENDC)

try:
	pathLoc = config.plugins.xtraEvent.loc.value
	PosterPath = "{}xtraEvent/poster".format(pathLoc)
	cprint("PosterPath = %s" % PosterPath)
	foldersize = config.plugins.xtraEvent.rmposter.value
	cprint("foldersize = %s" % foldersize)

	folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(PosterPath, fname)), files)) for PosterPath, folders, files in os.walk(PosterPath)])
	posters_sz = "%0.f" % (folder_size/(1024*1024.0))
	cprint("posters_sz = %s" % posters_sz)
	CMD = "rm -f %s/*" % PosterPath
	if foldersize == "50MB":
		if posters_sz >= "50":  # folder remove size(50MB)...
			Console().ePopen(CMD)
	elif foldersize == "100MB":
		if posters_sz >= "100": # folder remove size(100MB)...
			Console().ePopen(CMD)
	elif foldersize == "200MB":
		if posters_sz >= "200": # folder remove size(200MB)...
			Console().ePopen(CMD)
	elif foldersize == "500MB":
		if posters_sz >= "500": # folder remove size(500MB)...
			Console().ePopen(CMD)
	else:
		cprint('No order to remove poster icons')
except:
	pass


class xtraPoster(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.delayPicTime = 100
		self.timer = eTimer()
		self.timer.callback.append(self.showPicture)

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'delayPic':          # delay time(ms) for poster showing...
				self.delayPicTime = int(value)
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if not self.instance:
			return
		else:
			if what[0] != self.CHANGED_CLEAR:
				self.timer.start(self.delayPicTime, True)

	def showPicture(self):
		evnt = ''
		pstrNm = ''
		evntNm = ''
		try:
			event = self.source.event
			if event:
				evnt = event.getEventName()
				evntNm = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", evnt).rstrip()
				pstrNm = "{}xtraEvent/poster/{}.jpg".format(pathLoc, evntNm)
				if fileExists(pstrNm):
					size = self.instance.size()
					self.picload = ePicLoad()
					sc = AVSwitch().getFramebufferScale()
					if self.picload:
						self.picload.setPara((size.width(), size.height(), sc[0], sc[1], False, 1, '#00000000'))
					result = self.picload.startDecode(pstrNm, 0, 0, False)
					if result == 0:
						ptr = self.picload.getData()
						if ptr != None:
							self.instance.setPixmap(ptr)
							self.instance.show()
					del self.picload
				else:
					self.instance.hide()
			else:
				self.instance.hide()
			return
		except:
			pass

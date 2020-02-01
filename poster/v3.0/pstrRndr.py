# -*- coding: utf-8 -*-
# by digiteng...12-2019
# v3.0 added poster resize...01.2020
from Renderer import Renderer
from enigma import ePixmap, ePicLoad
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
import os
import re


class pstrRndr(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.pstrNm = ''
		self.path = ""

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if attrib == 'path':
				self.path = value
				if value.endswith("/"):
					self.path = value
				else:
					self.path = value + "/"
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap
	def changed(self, what):
		try:
			eventName = self.source.text
			if eventName :
				posterNm = re.sub('\s+', '+', eventName)
				pstrNm = "/media/hdd/" + self.path + posterNm + ".jpg"
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
			pass

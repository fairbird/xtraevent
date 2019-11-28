# -*- coding: utf-8 -*-
# by digiteng...
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Tools import Notifications
from Screens.ChoiceBox import ChoiceBox
from Screens.Standby import TryQuitMainloop
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger,ConfigOnOff, ConfigSlider, ConfigNothing
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from os import environ, listdir, remove, rename, system, popen
import shutil
from distutils.dir_util import copy_tree
from Components.Sources.CanvasSource import CanvasSource
from Components.MenuList import MenuList
from Components.ActionMap import NumberActionMap
from skin import parseColor
import urllib
import urllib2
import os
import time
from Components.Pixmap import Pixmap
from enigma import ePicLoad, eTimer, getDesktop
from Tools.Directories import SCOPE_CURRENT_SKIN, fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Components.Slider import Slider
from Components.Ipkg import IpkgComponent
from Screens.Ipkg import Ipkg
from Components.ProgressBar import ProgressBar
from Tools.Downloader import downloadWithProgress
from zipfile import ZipFile

stylecolor = [
	("0000000", _("Black")),
	("0ffff00", _("Navy")),
	("00000ff", _("Blue")),
	("000ffff", _("Silver")),
	("0ff00ff", _("WhiteSmoke")),
	("0ffffff", _("White"))]
colors = []
colors.append(("def", _("DEFAULT")))
colors.append(("bg", _("BACKGROUND")))
colors.append(("fg", _("FONT COLOR")))

config.skin.clr = ConfigSubsection()
config.skin.clr.colorforeground1 = ConfigSelection(default="000ffff", choices = stylecolor)
config.skin.clr.colorbackground1 = ConfigSelection(default="0000000", choices = stylecolor)
config.skin.clr.Colored = ConfigSelection(default="def", choices=colors)
#BACKGROUND
config.skin.clr.colorR = ConfigSlider(default=0, increment=15, limits=(0,255))
config.skin.clr.colorG = ConfigSlider(default=255, increment=15, limits=(0,255))
config.skin.clr.colorB = ConfigSlider(default=0, increment=15, limits=(0,255))

config.skin.clr.colorR2 = ConfigSlider(default=0, increment=15, limits=(0,255))
config.skin.clr.colorG2 = ConfigSlider(default=0, increment=15, limits=(0,255))
config.skin.clr.colorB2 = ConfigSlider(default=0, increment=15, limits=(0,255))




class tst(ConfigListScreen, Screen):
	skin = """
<screen position="center,center" size="1000,600" flags="wfBorder" title="test color text..." backgroundColor="#485b6d">
	<widget name="config" position="0,0" size="800,400" scrollbarMode="showNever" itemHeight="30" font="Regular; 24" backgroundColor="#485b6d" transparent="1" />
	<widget name="bgcolor1a" position="500,550" size="300,30" backgroundColor="#485b6d" font="Regular; 25" zPosition="1" transparent="0" />
	<widget name="fgcolor1a" position="500,550" size="300,30" font="Regular; 25" halign="left" backgroundColor="#485b6d" zPosition="2" transparent="1" />
	<widget source="preview" render="Canvas" position="0,0" size="10,10" zPosition="5" transparent="0" />
	<widget name="txtcolor" position="15,300" size="300,25" font="Regular; 25" halign="left" backgroundColor="#485b6d" transparent="1" />
	<widget name="bgcolor" position="50,550" size="300,30" backgroundColor="#000000" font="Regular; 30" zPosition="1" transparent="0" />
	<widget name="fgcolor" position="50,550" size="300,30" font="Regular; 25" halign="left" backgroundColor="#485b6d" zPosition="2" transparent="1" />
</screen>"""	

	def __init__(self, session):

		Screen.__init__(self, session)
		self.session = session
		
		self["preview"] = CanvasSource()
		
		#ConfigListScreen.__init__(self, self.list(), session = session)
		list = []
		ConfigListScreen.__init__(self, list)

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "EPGSelectActions"],
		{
			"cancel": self.close,
			"left": self.keyLeft,
			"right": self.keyRight,
			"down": self.keyDown,
			"up": self.keyUp,
			"red": self.close,

		}, -1)

		self["bgcolor"] = Label(_(" "))
		self["fgcolor"] = Label(_(" "))
		self["bgcolor1a"] = Label(_(" "))
		self["fgcolor1a"] = Label(_(" "))
		self["txtcolor"] = Label(_(" "))
		self.timer = eTimer()
		self.timer.callback.append(self.list)
		self.onLayoutFinish.append(self.list)
		self.onLayoutFinish.append(self.previewSkin)

	def delay(self):
		self.timer.start(100, True)
		
	def list(self):

		list = []
		list.append(getConfigListEntry(_("Font color :"), config.skin.clr.colorforeground1))
		list.append(getConfigListEntry(_("Background color:"), config.skin.clr.colorbackground1))
		list.append(getConfigListEntry(_("RGB :"), config.skin.clr.Colored))
		if config.skin.clr.Colored.value == "fg":
			list.append(getConfigListEntry(_("Red"), config.skin.clr.colorR))
			list.append(getConfigListEntry(_("Green"), config.skin.clr.colorG))
			list.append(getConfigListEntry(_("Blue"), config.skin.clr.colorB))
			self.cslider(self.RGB(int(config.skin.clr.colorR.value), int(config.skin.clr.colorG.value), int(config.skin.clr.colorB.value)))
			r = "{:02x}".format(int(config.skin.clr.colorR.value)) + "{:02x}".format(int(config.skin.clr.colorG.value)) + "{:02x}".format(int(config.skin.clr.colorB.value))
			self.rgbclr = "#%s" %r
		
			self["fgcolor"].setText(_("eeeeeeeeeeee"))
			self["fgcolor"].instance.setForegroundColor(parseColor(self.rgbclr))

		if config.skin.clr.Colored.value == "bg":
			list.append(getConfigListEntry(_("Red"), config.skin.clr.colorR2))
			list.append(getConfigListEntry(_("Green"), config.skin.clr.colorG2))
			list.append(getConfigListEntry(_("Blue"), config.skin.clr.colorB2))
			self.cslider(self.RGB(int(config.skin.clr.colorR2.value), int(config.skin.clr.colorG2.value), int(config.skin.clr.colorB2.value)))
			r2 = "{:02x}".format(int(config.skin.clr.colorR2.value)) + "{:02x}".format(int(config.skin.clr.colorG2.value)) + "{:02x}".format(int(config.skin.clr.colorB2.value))
			self.rgbclr2 = "#%s" %r2
			self["bgcolor"].setText(_("."))
			self["bgcolor"].instance.setBackgroundColor(parseColor(self.rgbclr2))
			self["bgcolor"].instance.setForegroundColor(parseColor(self.rgbclr2))




		self.previewSkin()
		self["config"].list = list
		self["config"].l.setList(list)
		#return list

	def RGB(self, r, g, b):
		return r << 16 | g << 8 | b

	def cslider(self, fcolor):
		c = self["preview"]
		c.fill(0, 0, 1920, 1080, fcolor)
		c.flush()

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.previewSkin()
		self.delay()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.previewSkin()
		self.delay()

	def keyDown(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.previewSkin()
		self.delay()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.previewSkin()
		self.delay()


	def previewSkin(self):
		self.bgtext = "background"
		self.fgtext = " foreground"
		self.fgColor1 = "#0%s" % config.skin.clr.colorforeground1.value
		self["fgcolor1a"].setText(_(self.fgtext))
		self["fgcolor1a"].instance.setForegroundColor(parseColor(self.fgColor1))

		self.bgColor1 = "#0%s" % config.skin.clr.colorbackground1.value
		self["bgcolor1a"].setText(_(self.bgtext))
		self["bgcolor1a"].instance.setBackgroundColor(parseColor(self.bgColor1))
		self["bgcolor1a"].instance.setForegroundColor(parseColor(self.bgColor1))



		




































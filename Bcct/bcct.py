# -*- coding: utf-8 -*-
# by digiteng...01.2020

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from enigma import eTimer
from os import path as os_path
import configs

class bcct(ConfigListScreen, Screen):
	skin = """
<screen position="center,550" size="600,150" flags="wfBorder" title="video setup..." backgroundColor="#000000">
	<widget name="config" position="0,0" size="600,120"  itemHeight="30" font="Regular; 24" backgroundColor="#000000" transparent="1" />
	<widget source="key_red" render="Label" position="0,120" zPosition="1" size="150,30" font="Regular;20" foregroundColor="#00ff0000" backgroundColor="#000000" halign="center" valign="center" transparent="1" />
	<widget source="key_green" render="Label" position="150,120" zPosition="1" size="150,30" font="Regular;20" foregroundColor="#606060" backgroundColor="#000000" halign="center" valign="center" transparent="1" />
	<widget source="key_yellow" render="Label" position="300,120" zPosition="1" size="150,30" font="Regular;20" foregroundColor="#ffff00" backgroundColor="#000000" halign="center" valign="center" transparent="1" />
	<widget source="key_blue" render="Label" position="450,120" zPosition="1" size="150,30" font="Regular;20" foregroundColor="#0000ff" backgroundColor="#000000" halign="center" valign="center" transparent="1" />
</screen>"""

	def __init__(self, session):

		Screen.__init__(self, session)
		self.session = session
		
		list = []
		ConfigListScreen.__init__(self, list)
		self['config'].l.setSeperation(200)
		 
		self['key_red'] = Label(_('Close'))
		self['key_green'] = Label(_('Save(Auto)'))
		self['key_yellow'] = Label(_('Restore'))
		self['key_blue'] = Label(_('Default'))  

		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions"],
		{
			"red": self.close,
			"green": self.close,
			"yellow": self.restoreOk,
			"blue": self.default,
			"cancel": self.close
		},-1)

		self.restore()
		self.timer = eTimer()
		self.timer.callback.append(self.vlist)
		self.onLayoutFinish.append(self.vlist)

	def delay(self):
		self.timer.start(100, True)

	def restore(self):
		self.brght = config.vset.bright.value
		self.cntrst = config.vset.contrast.value
		self.clr = config.vset.color.value
		self.tnt = config.vset.tint.value

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.delay()
		self.save()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.delay()
		self.save()

	def vlist(self):
		for x in self["config"].list:
			if len(x) > 1:
				x[1].save()
		list = []
		list.append(getConfigListEntry(_("BRIGHTNESS "), config.vset.bright))
		list.append(getConfigListEntry(_("CONTRAST "), config.vset.contrast))
		list.append(getConfigListEntry(_("COLOR "), config.vset.color))
		list.append(getConfigListEntry(_("HUE "), config.vset.tint))
	
		self["config"].list = list
		self["config"].l.setList(list)

	def save(self):
		if config.vset.bright.value:
			if os_path.exists('/proc/stb/video/plane/psi_brightness'):
				try:
					b = str(config.vset.bright.value)
					f = open('/proc/stb/video/plane/psi_brightness', 'w')
					f.write(b)
					f.close()
				except:
					pass

		if config.vset.contrast.value:
			if os_path.exists('/proc/stb/video/plane/psi_contrast'):
				try:
					b = str(config.vset.contrast.value)
					f = open('/proc/stb/video/plane/psi_contrast', 'w')
					f.write(b)
					f.close()
				except:
					pass

		if config.vset.color.value:
			if os_path.exists('/proc/stb/video/plane/psi_saturation'):
				try:
					b = str(config.vset.color.value)
					f = open('/proc/stb/video/plane/psi_saturation', 'w')
					f.write(b)
					f.close()
				except:
					pass

		if config.vset.tint.value:
			if os_path.exists('/proc/stb/video/plane/psi_tint'):
				try:
					b = str(config.vset.tint.value)
					f = open('/proc/stb/video/plane/psi_tint', 'w')
					f.write(b)
					f.close()
				except:
					pass

	def restoreOk(self):
		if self.brght is not None:
			config.vset.bright.setValue(self.brght)
		if self.cntrst is not None:
			config.vset.contrast.setValue(self.cntrst)
		if self.clr is not None:
			config.vset.color.setValue(self.clr)
		if self.tnt is not None:
			config.vset.tint.setValue(self.tnt)
		self.save()
		self.vlist()

	def default(self):
		config.vset.bright.setValue(128)
		config.vset.contrast.setValue(128)
		config.vset.color.setValue(128)
		config.vset.tint.setValue(128)
		self.save()
		self.vlist()	

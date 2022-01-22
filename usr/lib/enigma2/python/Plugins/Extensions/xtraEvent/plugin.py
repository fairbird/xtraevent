#!/usr/bin/python
# -*- coding: utf-8 -*-

# by digiteng...(digiteng@gmail.com)
# https://github.com/digiteng/
# 06.2020 - 11.2020(v2.0) - 11.2021(v3.x)
from __future__ import absolute_import
from Plugins.Plugin import PluginDescriptor
from Components.config import config
import threading
from datetime import datetime
from six.moves import reload_module
from . import xtra
from . import download

from enigma import addFont
addFont("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/fonts/arial.ttf", "xtraRegular", 100, 1)

try:
	if config.plugins.xtraEvent.timerMod.value == "Clock":
		tc = config.plugins.xtraEvent.timerClock.value
		dt = datetime.today()
		setclk = dt.replace(day=dt.day+1, hour=tc[0], minute=tc[1], second=0, microsecond=0)
		ds = setclk - dt
		secs = ds.seconds + 1
		def startDownload():
			from . import download
			download.downloads("").save()

		t = threading.Timer(secs, startDownload)
		t.start()

except Exception as err:
	with open("/tmp/xtraEvent.log", "a+") as f:
		f.write("plugin timer clock, %s\n"%(err))

def ddwn():
	try:
		if config.plugins.xtraEvent.timerMod.value == "Period":
			download.downloads("").save()
			tmr = config.plugins.xtraEvent.timer.value
			t = threading.Timer(3600*int(tmr), ddwn) # 1h=3600
			t.start()
	except Exception as err:
		with open("/tmp/xtra_error.log", "a+") as f:
			f.write("xtra plugin ddwn, %s\n\n"%err)
		
try:
	if config.plugins.xtraEvent.timerMod.value == "Period":
		threading.Timer(30, ddwn).start()
except Exception as err:
	with open("/tmp/xtra_error.log", "a+") as f:
		f.write("xtra plugin timer start, %s\n\n"%err)	

def main(session, **kwargs):
	try:
		reload_module(xtra)
		reload_module(download)
		session.open(xtra.xtra)
	except:
		import traceback
		traceback.print_exc()

def Plugins(**kwargs):
	return [PluginDescriptor(name="xtraEvent {}".format(xtra.version), description="Poster, Baskdrop, Banner, Info...Etc, Support...", where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)]

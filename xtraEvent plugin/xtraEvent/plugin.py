# -*- coding: utf-8 -*-
# by digiteng...
# digiteng@gmail.com
# https://github.com/digiteng/
# 06.2020, 07.2020,
from Plugins.Plugin import PluginDescriptor
from Components.config import config
import threading
import xtra
import download

def ddwn():
    download.save()
    if config.plugins.xtraEvent.timerMod.value == True:
        tmr = config.plugins.xtraEvent.timer.value
        t = threading.Timer(3600*int(tmr), ddwn) # 1h=3600
        t.start()

threading.Timer(60, ddwn).start()

def main(session, **kwargs):
	reload(xtra)
	reload(download)

	try:
		session.open(xtra.xtra)
	except:
		import traceback
		traceback.print_exc()

def Plugins(**kwargs):
	return [PluginDescriptor(name="xtraEvent", description="extra event material and info...", where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)]

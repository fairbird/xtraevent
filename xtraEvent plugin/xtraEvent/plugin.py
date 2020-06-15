# -*- coding: utf-8 -*-
# by digiteng...06.2020
from Plugins.Plugin import PluginDescriptor
from enigma import eTimer
from Components.config import config
import threading
import xtra
import download

def ddwn():
    download.save()
    if config.plugins.xtraEvent.upMOD.value == True:
        tmr = config.plugins.xtraEvent.timer.value
        t = threading.Timer(60 * int(tmr), ddwn)
        t.start()


threading.Timer(10, ddwn).start()
# t.cancel()
	# timer = eTimer()
	# timer.callback.append(ddwn)
	# timer.start(1000*30, 1)
	# timer2 = eTimer()
	# timer2.callback.append(ddwn)
	# t = config.plugins.xtraEvent.timer.value
	# timer2.start(60000*int(t), False) #1min-60 000msn, 1h-3 600 000 msn

def main(session, **kwargs):
	reload(xtra)
	reload(download)
	try:
		session.open(xtra.xtra)
	except:
		import traceback
		traceback.print_exc()

def Plugins(**kwargs):
	return [PluginDescriptor(name="xtraEvent", description="xtraEvent plugin...", where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)]

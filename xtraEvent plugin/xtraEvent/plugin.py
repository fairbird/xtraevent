# -*- coding: utf-8 -*-
# by digiteng...06.2020
from Plugins.Plugin import PluginDescriptor
from Components.config import config
from urllib2 import urlopen
import threading
import json
import xtra
import download




def upPlgn():

	urls = ["https://api.github.com/repos/digiteng/plugins-test-/commits?path=/xtraEvent%20plugin/xtraEvent/plugin.py",
	"https://api.github.com/repos/digiteng/plugins-test-/commits?path=/xtraEvent%20plugin/xtraEvent/xtra.py",
	"https://api.github.com/repos/digiteng/plugins-test-/commits?path=/xtraEvent%20plugin/xtraEvent/download.py"]

	jsPath = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/update.json"
	nl=len(urls)
	for u in range(nl):
		upUrl = json.load(urlopen(urls[u]))[0]['commit']['tree']['sha']

		with open(jsPath) as f:
			ups = json.load(f)["{}".format(urls[u].split('/')[-1])]

		if str(ups) != str(upUrl):
			fileName = urls[u].split('/')[-1]
			newUpUrl = "https://github.com/digiteng/plugins-test-/raw/master/xtraEvent%20plugin/xtraEvent/{}".format(fileName)
			with open("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/"+fileName,'wb') as f:
				f.write(urlopen(newUpUrl).read())
			
			with open(jsPath) as f:
				data = json.load(f)
				data["{}".format(urls[u].split('/')[-1])] = upUrl
				json.dump(data, open(jsPath, "w"), indent = 4)	



u=threading.Timer(10, upPlgn)
u.start()
u.join()

def ddwn():
    download.save()
    if config.plugins.xtraEvent.upMOD.value == True:
        tmr = config.plugins.xtraEvent.timer.value
        t = threading.Timer(3600*int(tmr), ddwn) # 1h=3600
        t.start()

threading.Timer(10, ddwn).start()


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

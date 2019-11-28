# by digiteng...10.2019
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
from Components.Label import Label
from enigma import getDesktop
import tst

def main(session, **kwargs):
	reload(tst)
	try:
		session.open(tst.tst)
	except:
		import traceback
		traceback.print_exc()

def Plugins(**kwargs):
	return [PluginDescriptor(name="Createtst", description="tst creater plugin...", where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)]

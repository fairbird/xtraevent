# by digiteng...04,2020
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
from Components.Label import Label
from enigma import getDesktop
import xtra


def main(session, **kwargs):
	reload(xtra)
	try:
		session.open(xtra.xtra)
	except:
		import traceback
		traceback.print_exc()

def Plugins(**kwargs):
	return [PluginDescriptor(name="xtraEvent", description="xtraEvent creater plugin...", where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)]

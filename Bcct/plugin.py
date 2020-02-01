# by digiteng...01.2020

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
import bcct


def main(session, **kwargs):
	reload(bcct)
	try:
		session.open(bcct.bcct)
	except:
		import traceback
		traceback.print_exc()

def Plugins(**kwargs):
	return [PluginDescriptor(name="bcct", description="bright-color-contrast-tint setup...", where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)]










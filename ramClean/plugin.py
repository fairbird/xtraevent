# by digiteng...v1.0...10.2019
# v1.1...11.2019
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from os import system
from enigma import eTimer
#from Tools import Notifications
#from Screens.MessageBox import MessageBox

system("echo 1 > /proc/sys/vm/drop_caches")
system("echo 2 > /proc/sys/vm/drop_caches")
system("echo 3 > /proc/sys/vm/drop_caches")

def cleanRam():
	system("echo 1 > /proc/sys/vm/drop_caches")
	system("echo 2 > /proc/sys/vm/drop_caches")
	system("echo 3 > /proc/sys/vm/drop_caches")
	#Notifications.AddPopup("RAM CLEANED", MessageBox.TYPE_INFO, timeout=7)

Timer = eTimer()
Timer.callback.append(cleanRam)
Timer.start(1000*600, False) #10min

def main(session, **kwargs):
	session.open(ramClean)

def Plugins(**kwargs):
	return PluginDescriptor(name=_("Setup ramClean"),
	description=_("Setup ramClean"),
	where = [PluginDescriptor.WHERE_EXTENSIONSMENU],
	icon="plugin.png",
	fnc=main)

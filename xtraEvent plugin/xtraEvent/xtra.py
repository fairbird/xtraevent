# -*- coding: utf-8 -*-
# by digiteng...06.2020
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Screens.MessageBox import MessageBox
import re
import os
import json
import random
from urllib2 import urlopen, quote
from urllib import urlretrieve, quote
import requests
from Components.Sources.Event import Event
from Components.Sources.CurrentService import CurrentService
from Components.MenuList import MenuList
from Components.SelectionList import SelectionList, SelectionEntryComponent

from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger,ConfigOnOff, ConfigSlider, ConfigNothing
from Components.ConfigList import ConfigListScreen
from Screens.ChoiceBox import ChoiceBox
from enigma import eTimer, getDesktop, eLabel, eServiceCenter, eServiceReference, iServiceInformation, eEPGCache, ePixmap, eSize, ePoint, loadJPG, loadPNG
from Components.Sources.List import List
from Components.Sources.ServiceList import ServiceList
from ServiceReference import ServiceReference
from Components.Sources.StaticText import StaticText
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.Pixmap import Pixmap


epgcache = eEPGCache.getInstance()
tmdb_api = "3c3efcf47c3577558812bb9d64019d65"

def bqtList():
	bouquets = []
	serviceHandler = eServiceCenter.getInstance()
	list = serviceHandler.list(eServiceReference('1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "bouquets.tv" ORDER BY bouquet'))
	if list:
		while True:
			bqt = list.getNext()
			if not bqt.valid(): break
			info = serviceHandler.info(bqt)
			if info:
				bouquets.append((info.getName(bqt), bqt))
		return bouquets
	return 

def chList(bqtNm):
	channels = []
	serviceHandler = eServiceCenter.getInstance()
	chlist = serviceHandler.list(eServiceReference('1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "bouquets.tv" ORDER BY bouquet'))
	if chlist :
		while True:
			chh = chlist.getNext()
			if not chh.valid(): break
			info = serviceHandler.info(chh)
			if chh.flags & eServiceReference.isDirectory:
				info = serviceHandler.info(chh)
			if info.getName(chh) in bqtNm:
				chlist = serviceHandler.list(chh)
				while True:
					chhh = chlist.getNext()
					if not chhh.valid(): break
					channels.append((chhh.toString()))
		return channels
	return


config.plugins.xtraEvent = ConfigSubsection()
config.plugins.xtraEvent.locations = ConfigSelection(default = "hdd", choices = [
	("hdd"), 
	("usb"),
	("internal"),
	])

config.plugins.xtraEvent.searchMOD = ConfigSelection(default = "Current Channel", choices = [("Bouquets"), ("Current Channel")])
nmbrlist = []
for i in range(1, 999):
	nmbrlist.append(("%d" % i))
config.plugins.xtraEvent.searchNUMBER = ConfigSelection(default = "1", choices = nmbrlist)

config.plugins.xtraEvent.searchLang = ConfigText(default="en", visible_width=100, fixed_size=False)


config.plugins.xtraEvent.upMOD = ConfigYesNo(default = False)

timelist = []
for i in range(1, 24):
	timelist.append(("%d" % i))
config.plugins.xtraEvent.timer = ConfigSelection(default = "1", choices = timelist)
# config.plugins.xtraEvent.upStndby = ConfigYesNo(default = False)	


config.plugins.xtraEvent.tmdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.tvdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.omdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.maze = ConfigYesNo(default = False)
config.plugins.xtraEvent.fanart = ConfigYesNo(default = False)

config.plugins.xtraEvent.poster = ConfigYesNo(default = False)
config.plugins.xtraEvent.banner = ConfigYesNo(default = False)
config.plugins.xtraEvent.backdrop = ConfigYesNo(default = False)
config.plugins.xtraEvent.info = ConfigYesNo(default = False)

config.plugins.xtraEvent.TMDBpostersize = ConfigSelection(default="w185", choices = [
	("w92", "92x138"), 
	("w154", "154x231"), 
	("w185", "185x278"), 
	("w342", "342x513"), 
	("w500", "500x750"), 
	("w780", "780x1170"), 
	("original", "ORIGINAL")])
config.plugins.xtraEvent.TVDBpostersize = ConfigSelection(default="thumbnail", choices = [
	("thumbnail", "340x500"), 
	("original", "680x1000")])

config.plugins.xtraEvent.TMDBbackdropsize = ConfigSelection(default="w300", choices = [
 	("w300", "300x170"), 
	("w780", "780x440"), 
	("w1280", "1280x720"),
	("original", "ORIGINAL")])

config.plugins.xtraEvent.TVDBbackdropsize = ConfigSelection(default="thumbnail", choices = [
	("thumbnail", "340x500"), 
	("original", "680x1000")])

config.plugins.xtraEvent.FANARTresize = ConfigSelection(default="10", choices = [
	("10", "100x142"), 
	("5", "200x285"), 
	("3", "333x475"), 
	("2", "500x713"), 
	("1", "1000x1426")])

# config.plugins.xtraEvent.FANARTresize = ConfigSelection(default="10", choices = [
	# ("(92,138)", "92x138"), 
	# ("(185,278)", "185x278"), 
	# ("(342,513)", "342x513"), 
	# ("(500,750)", "500x750"), 
	# ("(1000,1426)", "1000,1426")])

config.plugins.xtraEvent.searchMANUEL = ConfigText(default="event name", visible_width=100, fixed_size=False)
choicelist = []
for i in range(0, 999):
	choicelist.append(("%d" % i))
config.plugins.xtraEvent.searchMANUELnmbr = ConfigSelection(default = "0", choices = choicelist)
config.plugins.xtraEvent.searchMANUELyear = ConfigInteger(default = 0, limits=(0, 9999))

config.plugins.xtraEvent.PB = ConfigSelection(default="poster", choices = [
	("posters", "Poster"), 
	("backdrops", "backdrop")])

config.plugins.xtraEvent.imgs = ConfigSelection(default="TMDB", choices = [
	('TMDB', 'TMDB'),
	('TVDB', 'TVDB'),
	('FANART', 'FANART')])

imglist = []
for i in range(1, 999):
	imglist.append(("%d" % i))
config.plugins.xtraEvent.imgNmbr = ConfigSelection(default = "1", choices = imglist)

config.plugins.xtraEvent.searchType = ConfigSelection(default="tv", choices = [

	('tv', 'TV'),
	('movie', 'MOVIE'),
	('multi', 'MULTI')])

class xtra(Screen, ConfigListScreen):
	skin = """
  <screen name="xtra" position="center,center" size="1280,720" title="xtraEvent v1" backgroundColor="#ffffff">
    <ePixmap position="0,0" size="1280,720" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/bckg.png" transparent="1" />
    <widget source="Title" render="Label" position="40,35" size="745,40" font="Console; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
    <widget name="config" position="40,95" size="745,510" itemHeight="30" font="Regular;24" foregroundColor="#c5c5c5" scrollbarMode="showOnDemand" transparent="1" backgroundColor="#23262e" backgroundColorSelected="#565d6d" foregroundColorSelected="#ffffff" />
    <widget source="help" position="40,605" size="745,26" render="Label" font="Regular;22" foregroundColor="#f3fc92" backgroundColor="#23262e" halign="left" valign="center" transparent="1" />
    <widget name="status" position="840,300" size="400,30" transparent="1" font="Regular;22" foregroundColor="#92f1fc" backgroundColor="#23262e" />
    <widget name="info" position="840,330" size="400,270" transparent="1" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" halign="left" valign="top" />
    <widget source="key_red" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="40,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_green" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="230,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_yellow" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="420,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_blue" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="610,640" size="170,30" halign="left" transparent="1" zPosition="1" />

    <eLabel name="" text="v1" position="840, 35" size="400, 40" transparent="1" halign="center" font="Console; 30" backgroundColor="background" />
  </screen>
	"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		
		self.epgcache = eEPGCache.getInstance()

		list = []
		ConfigListScreen.__init__(self, list)

		self['key_red'] = Label(_('Close'))
		self['key_green'] = Label(_('Save'))
		self['key_yellow'] = Label(_('Download'))
		self['key_blue'] = Label(_('Manuel Search'))

		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions", "EventViewActions", "VirtualKeyboardAction"],
		{
			"left": self.keyLeft,
			"down": self.keyDown,
			"up": self.keyUp,
			"right": self.keyRight,
			"red": self.exit,
			"green": self.save,
			"yellow": self.dwnld,
			"blue": self.ms,
			"cancel": self.exit,


			# "info": self.about,
		},-1)
		
		self.setTitle(_("xtraEvent v1"))
		self['status'] = Label()
		self['info'] = Label()
		self["help"] = StaticText()

		self.timer = eTimer()
		self.timer.callback.append(self.xtraList)
		self.onLayoutFinish.append(self.xtraList)

	
		if config.plugins.xtraEvent.locations.value == "hdd":
			if os.path.ismount('/media/hdd'):
				if not os.path.isdir("/media/hdd/xtraEvent/"):
					os.makedirs("/media/hdd/xtraEvent/poster")
					os.makedirs("/media/hdd/xtraEvent/banner")
					os.makedirs("/media/hdd/xtraEvent/backdrop")
					os.makedirs("/media/hdd/xtraEvent/infos")
				self.pathLoc = "/media/hdd/xtraEvent/"

		elif config.plugins.xtraEvent.locations.value == "usb":
			if os.path.ismount('/media/usb'):
				if not os.path.isdir("/media/usb/xtraEvent/"):
					os.makedirs("/media/usb/xtraEvent/poster")
					os.makedirs("/media/usb/xtraEvent/banner")
					os.makedirs("/media/usb/xtraEvent/backdrop")
					os.makedirs("/media/usb/xtraEvent/infos")
				self.pathLoc = "/media/usb/xtraEvent/"

		elif config.plugins.xtraEvent.locations.value == "internal":
			if not os.path.isdir("/etc/enigma2/xtraEvent/"):
				os.makedirs("/etc/enigma2/xtraEvent/poster")
				os.makedirs("/etc/enigma2/xtraEvent/banner")
				os.makedirs("/etc/enigma2/xtraEvent/backdrop")
				os.makedirs("/etc/enigma2/xtraEvent/infos")
			self.pathLoc = "/etc/enigma2/xtraEvent/"


		try:
			path_poster = self.pathLoc+ "poster/"
			path_banner = self.pathLoc+ "banner/"
			path_backdrop = self.pathLoc+ "backdrop/"			
			path_info = self.pathLoc+ "infos/"
			
			folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(path_poster, fname)), files)) for path_poster, folders, files in os.walk(path_poster)])
			posters_sz = "%0.1f" % (folder_size/(1024*1024.0))
			poster_nmbr = len(os.listdir(path_poster))

			folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(path_banner, fname)), files)) for path_banner, folders, files in os.walk(path_banner)])
			banners_sz = "%0.1f" % (folder_size/(1024*1024.0))
			banner_nmbr = len(os.listdir(path_banner))

			folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(path_backdrop, fname)), files)) for path_backdrop, folders, files in os.walk(path_backdrop)])
			backdrops_sz = "%0.1f" % (folder_size/(1024*1024.0))
			backdrop_nmbr = len(os.listdir(path_backdrop))

			folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(path_info, fname)), files)) for path_info, folders, files in os.walk(path_info)])
			infos_sz = "%0.1f" % (folder_size/(1024*1024.0))
			info_nmbr = len(os.listdir(path_info))
			
			self['status'].setText(_("Storage ;"))
			self['info'].setText(_(
				"Total Poster : {} poster {} MB".format(poster_nmbr, posters_sz)+ 
				"\nTotal Banner : {} banner {} MB".format(banner_nmbr, banners_sz)+
				"\nTotal Backdrop : {} backdrop {} MB".format(backdrop_nmbr, backdrops_sz)+
				"\nTotal Info : {} info {} MB".format(info_nmbr, infos_sz)))
		except Exception as e:
			print e
			self['info'].setText(_(str(e)))


		
	def delay(self):
		self.timer.start(100, True)

	def xtraList(self):
		for x in self["config"].list:
			if len(x) > 1:
				x[1].save()
		list = []
		list.append(getConfigListEntry("—"*100))
# path location_________________________________________________________________________________________________________________
		list.append(getConfigListEntry("LOCATION", config.plugins.xtraEvent.locations, _("select locations...")))
		list.append(getConfigListEntry("—"*100))
# config_________________________________________________________________________________________________________________
		list.append(getConfigListEntry("SEARCH MODE", config.plugins.xtraEvent.searchMOD, _("select search mode...")))
		if config.plugins.xtraEvent.searchMOD.value == "Manuel Search":
			list.append(getConfigListEntry("\tTitle", config.plugins.xtraEvent.searchMANUEL, _("enter the event name to search...")))

		else:
			list.append(getConfigListEntry("SEARCH NEXT EVENTS", config.plugins.xtraEvent.searchNUMBER, _("enter the number of next events to be scanned for each channel...")))
		list.append(getConfigListEntry("SEARCH LANGUAGE", config.plugins.xtraEvent.searchLang, _("select search language...")))


		list.append(getConfigListEntry("TIMER", config.plugins.xtraEvent.upMOD, _("select timer update for events..")))
		if config.plugins.xtraEvent.upMOD.value == True:
			list.append(getConfigListEntry("\tTIMER(hours)", config.plugins.xtraEvent.timer, _("..."),))
		list.append(getConfigListEntry("—"*100))

# poster__________________________________________________________________________________________________________________
		list.append(getConfigListEntry("POSTER", config.plugins.xtraEvent.poster, _("...")))
		if config.plugins.xtraEvent.poster.value == True:
			list.append(getConfigListEntry("\tTMDB", config.plugins.xtraEvent.tmdb, _("best source for poster..."),))
			if config.plugins.xtraEvent.tmdb.value :
				list.append(getConfigListEntry("\tTMDB POSTER SIZE", config.plugins.xtraEvent.TMDBpostersize, _("Choose poster sizes for TMDB")))
				list.append(getConfigListEntry("-"*100))
			list.append(getConfigListEntry("\tTVDB", config.plugins.xtraEvent.tvdb, _("best source for banner...")))
			if config.plugins.xtraEvent.tvdb.value :
				list.append(getConfigListEntry("\tTVDB POSTER SIZE", config.plugins.xtraEvent.TVDBpostersize, _("Choose poster sizes for TVDB")))
				list.append(getConfigListEntry("_"*100))
			list.append(getConfigListEntry("\tOMDB", config.plugins.xtraEvent.omdb, _("best source for info...")))
			list.append(getConfigListEntry("\tMAZE(TV SHOWS)", config.plugins.xtraEvent.maze, _("best source for tv shows...")))
			list.append(getConfigListEntry("\tFANART", config.plugins.xtraEvent.fanart, _("alternative source for poster, banner, etc...")))	
			if config.plugins.xtraEvent.fanart.value:
				list.append(getConfigListEntry("\tFANART POSTER SIZE", config.plugins.xtraEvent.FANARTresize, _("Choose poster sizes for FANART")))
				

			list.append(getConfigListEntry("—"*100))
# banner__________________________________________________________________________________________________________________
		list.append(getConfigListEntry("BANNER", config.plugins.xtraEvent.banner, _("tvdb and fanart for banner...")))



# backdrop_______________________________________________________________________________________________________________
		list.append(getConfigListEntry("BACKDROP", config.plugins.xtraEvent.backdrop, _("best source for poster...")))
		if config.plugins.xtraEvent.backdrop.value == True:
			list.append(getConfigListEntry("\tTMDB", config.plugins.xtraEvent.tmdb, _("source for backdrop...")))
			if config.plugins.xtraEvent.tmdb.value :
				list.append(getConfigListEntry("\tTMDB BACKDROP SIZE", config.plugins.xtraEvent.TMDBbackdropsize, _("Choose backdrop sizes for TMDB")))
				list.append(getConfigListEntry("_"*100))
			list.append(getConfigListEntry("\tTVDB", config.plugins.xtraEvent.tvdb, _("source for backdrop...")))
			if config.plugins.xtraEvent.tvdb.value :
				list.append(getConfigListEntry("\tTVDB BACKDROP SIZE", config.plugins.xtraEvent.TVDBbackdropsize, _("Choose backdrop sizes for TVDB")))
				list.append(getConfigListEntry("_"*100))
			list.append(getConfigListEntry("\tFANART", config.plugins.xtraEvent.fanart, _("source for backdrop...")))
			if config.plugins.xtraEvent.fanart.value:
				list.append(getConfigListEntry("\tFANART BACKDROP SIZE", config.plugins.xtraEvent.FANARTresize, _("Choose backdrop sizes for FANART")))
				list.append(getConfigListEntry("_"*100))
# info___________________________________________________________________________________________________________________
		list.append(getConfigListEntry("INFO", config.plugins.xtraEvent.info, _("Program information with omdb...")))
		list.append(getConfigListEntry("—"*100))



		self["config"].list = list
		self["config"].l.setList(list)
		self.help()

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.delay()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.delay()

	def keyDown(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.delay()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.delay()

	def pageUp(self):
		self["config"].instance.moveSelection(self["config"].instance.pageDown)
		self.delay()

	def pageDown(self):
		self["config"].instance.moveSelection(self["config"].instance.pageUp)
		self.delay()

	def help(self):
		cur = self["config"].getCurrent()
		if cur:
			self["help"].text = cur[2]

	def save(self):
		if config.plugins.xtraEvent.searchMOD.value == "Current Channel":
			self.currentChEpgs()
		elif config.plugins.xtraEvent.searchMOD.value == "Bouquets":
			self.session.open(selBouquets)

	def currentChEpgs(self):
		if os.path.exists(self.pathLoc+"events"):
			os.remove(self.pathLoc+"events")
		try:
			events = None
			ref = self.session.nav.getCurrentlyPlayingServiceReference().toString()
			try:
				events = self.epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
				n = config.plugins.xtraEvent.searchNUMBER.value
				for i in xrange(int(n)):
					title = events[i][4]
					evntN = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", title)
					evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").replace("LOS ", "The ").rstrip()
					open(self.pathLoc+"events","a+").write("%s\n" % str(evntNm))
				if os.path.exists(self.pathLoc+"events"):
					with open(self.pathLoc+"events", "r") as f:
						titles = f.readlines()
					titles = list(dict.fromkeys(titles))
					n = len(titles)
					self['info'].setText(_("Event to be Scanned : {}".format(str(n))))
			except:
				pass

		except:
			pass

	
    # from Screens.Standby import inStandby
    # inStandby.onClose.append(onLeaveStandby)


	def ms(self):
		self.session.open(manuelSearch)

	def dwnld(self):
		from download import download
		download()

	def exit(self):
		for x in self["config"].list:
			if len(x) > 1:
				x[1].save()
		configfile.save()
		self.close()

class manuelSearch(Screen, ConfigListScreen):
	skin = """
  <screen name="manuelSearch" position="0,0" size="1280,720" title="Manuel Search..." backgroundColor="#ffffff" flags="wfNoBorder">
	<ePixmap position="0,0" size="1280,720" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/bckg.png" transparent="1" />
    <widget source="Title" render="Label" position="40,40" size="745,40" font="Console; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
	<widget source="session.CurrentService" render="Label" position="40,80" size="638,40" zPosition="2" font="Console; 30" transparent="1" backgroundColor="#23262e" valign="center">
		<convert type="ServiceName">Name</convert>
	</widget>
	<widget name="config" position="40,150" size="745,550" itemHeight="30" font="Regular;24" foregroundColor="#c5c5c5" scrollbarMode="showOnDemand" transparent="1" backgroundColor="#23262e" backgroundColorSelected="#565d6d" foregroundColorSelected="#ffffff" />
    <widget name="status" position="840,300" size="400,30" transparent="1" font="Regular;22" foregroundColor="#92f1fc" backgroundColor="#23262e" />
    <widget name="info" position="840,640" size="400,30" transparent="1" font="Regular;22" halign="center" foregroundColor="#c5c5c5" backgroundColor="#23262e" />
    <widget name="Picture" position="840,320" size="185,278" zPosition="5" transparent="1" />
	
	<widget source="key_red" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="40,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_green" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="230,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_yellow" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="420,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_blue" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="610,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <eLabel name="" position="40,120" size="745, 1" backgroundColor="#898989" />
    <eLabel name="" position="840,675" size="400, 1" backgroundColor="#898989" />
  </screen>
  """

	def __init__(self, session):
		Screen.__init__(self, session)

		self.pathLoc = ""
		self.text = ""
		self.year = ""
		
		list = []
		ConfigListScreen.__init__(self, list)

		self.setTitle(_("Manuel Search Events..."))
		self["key_red"] = StaticText(_("Exit"))
		self["key_green"] = StaticText(_("Search"))
		self["key_yellow"] = StaticText(_("Append"))
		self["key_blue"] = StaticText(_("Keyboard"))
		self["actions"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions", "VirtualKeyboardAction"],
			{
				"left": self.keyLeft,

				"right": self.keyRight,
				"cancel": self.close,
				"red": self.close,
				"ok": self.mnlSrch,
				"green": self.mnlSrch,
				"yellow": self.append,
				"blue": self.vk,
			}, -2)
		
		self['status'] = Label()
		self['info'] = Label()
		self["Picture"] = Pixmap()

		if config.plugins.xtraEvent.locations.value == "hdd":
			self.pathLoc = "/media/hdd/xtraEvent/"
		elif config.plugins.xtraEvent.locations.value == "usb":
			self.pathLoc = "/media/usb/xtraEvent/"
		elif config.plugins.xtraEvent.locations.value == "internal":
			self.pathLoc = "/etc/enigma2/xtraEvent/"
		else:
			self.pathLoc = "/tmp/"

		if not os.path.isdir(self.pathLoc + "mSearch"):
			os.makedirs(self.pathLoc + "mSearch")
		# fs = os.listdir(self.pathLoc + "mSearch/")
		# for f in fs:
			# os.remove(self.pathLoc + "mSearch/" + f)

		self.timer = eTimer()
		self.timer.callback.append(self.msList)
		self.timer.callback.append(self.pc)
		self.onLayoutFinish.append(self.msList)

	def delay(self):
		self.timer.start(100, True)

	def msList(self):
		for x in self["config"].list:
			if len(x) > 1:
				x[1].save()
	
		list = []
		list.append(getConfigListEntry(_("Events Next"), config.plugins.xtraEvent.searchMANUELnmbr))
		list.append(getConfigListEntry(_("Search Event"), config.plugins.xtraEvent.searchMANUEL))
		list.append(getConfigListEntry(_("Year"), config.plugins.xtraEvent.searchMANUELyear))
		list.append(getConfigListEntry(_("Search Language"), config.plugins.xtraEvent.searchLang))
		list.append(getConfigListEntry(_("Search Image"), config.plugins.xtraEvent.PB))
		
		list.append(getConfigListEntry(_("Search Source"), config.plugins.xtraEvent.imgs))
		if config.plugins.xtraEvent.imgs.value == "TMDB":
			list.append(getConfigListEntry(_("\tSearch Type"), config.plugins.xtraEvent.searchType))
			if config.plugins.xtraEvent.PB.value == "posters":
				list.append(getConfigListEntry(_("\tSize"), config.plugins.xtraEvent.TMDBpostersize))
			else:
				list.append(getConfigListEntry(_("\tSize"), config.plugins.xtraEvent.TMDBbackdropsize))
			
		list.append(getConfigListEntry("—"*100))
		list.append(getConfigListEntry(_("Next Images"), config.plugins.xtraEvent.imgNmbr))
		
		
		
		
		
		self["config"].list = list
		self["config"].l.setList(list)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.curEpg()
		self.inf()
		self.delay()
		
	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.curEpg()
		self.inf()
		self.delay()


	def curEpg(self):
		try:
			events = ""
			ref = self.session.nav.getCurrentlyPlayingServiceReference().toString()
			events = epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
			if events:
				n = config.plugins.xtraEvent.searchMANUELnmbr.value
				self.event = events[int(n)][4]
				config.plugins.xtraEvent.searchMANUEL = ConfigText(default="{}".format(self.event), visible_width=100, fixed_size=False)

		except:
			pass

	def mnlSrch(self):
		from download import intCheck
		if intCheck():
			if config.plugins.xtraEvent.PB.value == "posters":
				if config.plugins.xtraEvent.tmdb.value == True:
					self.tmdb()
				# if config.plugins.xtraEvent.tvdb.value == True:
					# tvdb_Poster()

				# if config.plugins.xtraEvent.fanart.value == True:
					# fanart_Poster()
			if config.plugins.xtraEvent.PB.value == "backdrops":
				if config.plugins.xtraEvent.tmdb.value == True:
					self.tmdb()
				# if config.plugins.xtraEvent.tvdb.value == True:
					# tvdb_backdrop()
				# if config.plugins.xtraEvent.fanart.value == True:
					# fanart_backdrop()
					pass

	def vk(self):
		self.session.openWithCallback(self.vkEdit, VirtualKeyBoard, title="edit event name...", text = config.plugins.xtraEvent.searchMANUEL.value)

	def vkEdit(self, text=None):
		if text:
			self.text = text
			self.year = config.plugins.xtraEvent.searchMANUELyear.value
			self.manuelSearchWrite()
		else:
			text = config.plugins.xtraEvent.searchMANUEL.value
			self.year = config.plugins.xtraEvent.searchMANUELyear.value
			self.text = text
			self.manuelSearchWrite()

	def manuelSearchWrite(self):
		if config.plugins.xtraEvent.locations.value == "hdd":
			self.pathLoc = "/media/hdd/xtraEvent/"
		elif config.plugins.xtraEvent.locations.value == "usb":
			self.pathLoc = "/media/usb/xtraEvent/"
		elif config.plugins.xtraEvent.locations.value == "internal":
			self.pathLoc = "/etc/enigma2/xtraEvent/"
		else:
			self.pathLoc = "/tmp/"
		if os.path.exists(self.pathLoc+"events"):
			os.remove(self.pathLoc+"events")
		open(self.pathLoc+"events","w").write(self.text)
		if os.path.exists(self.pathLoc+"events-year"):
			os.remove(self.pathLoc+"events-year")
		open(self.pathLoc+"events-year","w").write(str(self.year))
		# self.close()


	def pc(self):
		self.text = config.plugins.xtraEvent.searchMANUEL.value
		self.year = config.plugins.xtraEvent.searchMANUELyear.value
		try:
			self.iNmbr = config.plugins.xtraEvent.imgNmbr.value
			self.pb = config.plugins.xtraEvent.PB.value
			self.path = self.pathLoc + "mSearch/{}-{}-{}.jpg".format(self.text, self.pb, self.iNmbr)
			self["Picture"].instance.setPixmap(loadJPG(self.path))
			
			if self.pb == "posters":
				self["Picture"].instance.setScale(1)
				self["Picture"].instance.resize(eSize(185,278))
				self["Picture"].instance.move(ePoint(930,325))
			else:
				self["Picture"].instance.setScale(1)
				self["Picture"].instance.resize(eSize(300,170))
				self["Picture"].instance.move(ePoint(890,375))
			self['Picture'].show()
		except:
			return

	def inf(self):
		try:
			dir = self.pathLoc + "mSearch/"
			tot = next(os.walk(dir))[2]
			tot = len(tot)
			# tot = any(x.startswith('{}'.format(self.text)) for x in os.listdir(dir))
			# tot = len(tot)
			cur = config.plugins.xtraEvent.imgNmbr.value
			self['info'].setText(_(str(cur) + "/" + str(tot)))
		except:
			return

	def append(self):
		try:
			if config.plugins.xtraEvent.PB.value == "posters":
				target = self.pathLoc + "poster/{}.jpg".format(self.text)
			else:
				target = self.pathLoc + "backdrop/{}.jpg".format(self.text)

			import shutil
			if os.path.exists(self.path):
				shutil.copyfile(self.path, target)

		except:
			return

	def tmdb(self):
		
		try:
			self.srch = config.plugins.xtraEvent.searchType.value
			url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key=3c3efcf47c3577558812bb9d64019d65&query={}".format(self.srch, quote(self.text))
			if self.year:
				url_tmdb += "&primary_release_year={}&year={}".format(self.year, self.year)
			id = json.load(urlopen(url_tmdb))['results'][0]['id']
			lang = config.plugins.xtraEvent.searchLang.value
			url = "https://api.themoviedb.org/3/{}/{}?api_key=3c3efcf47c3577558812bb9d64019d65&append_to_response=images&language={}".format(self.srch, int(id), lang)
			# pb = config.plugins.xtraEvent.PB.value
			if config.plugins.xtraEvent.PB.value == "posters":
				sz = config.plugins.xtraEvent.TMDBpostersize.value
			else:
				sz = config.plugins.xtraEvent.TMDBbackdropsize.value
			for i in xrange(99):
				poster = json.load(urlopen(url))['images']['{}'.format(self.pb)][i]['file_path']
				if poster:
					url_poster = "https://image.tmdb.org/t/p/{}{}".format(sz, poster)
					dwn = self.pathLoc + "mSearch/{}-{}-{}.jpg".format(self.text, self.pb, i+1)
					open(dwn, 'wb').write(requests.get(url_poster, stream=True, allow_redirects=True).content)

		except:
			return



# self['info'].setText(_(str(e)))


class selBouquets(Screen):
	skin = """
  <screen name="selBouquets" position="center,center" size="1280,720" title="xtraEvent v1" backgroundColor="#ffffff">
    <ePixmap position="0,0" size="1280,720" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/bckg.png" transparent="1" />
    <widget source="Title" render="Label" position="40,35" size="745,40" font="Console; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
    <widget name="list" position="40,95" size="745,510" itemHeight="30" font="Regular;24" foregroundColor="#c5c5c5" scrollbarMode="showOnDemand" transparent="1" backgroundColor="#23262e" backgroundColorSelected="#565d6d" foregroundColorSelected="#ffffff" />

    <widget name="status" position="840,300" size="400,30" transparent="1" font="Regular;22" foregroundColor="#92f1fc" backgroundColor="#23262e" />
    <widget name="info" position="840,330" size="400,270" transparent="1" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" halign="left" valign="top" />
    <widget source="key_red" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="40,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_green" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="230,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_yellow" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="420,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_blue" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="610,640" size="170,30" halign="left" transparent="1" zPosition="1" />

    <eLabel name="" text="v1" position="840, 35" size="400, 40" transparent="1" halign="center" font="Console; 30" backgroundColor="background" />
  </screen>
	"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self.bouquets = bqtList()
		self.epgcache = eEPGCache.getInstance()
		self.setTitle(_("Bouquet Selection"))
		self.sources = [SelectionEntryComponent(s[0], s[1], 0, (s[0] in ["sources"])) for s in self.bouquets]
		self["list"] = SelectionList(self.sources)

		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"red": self.cancel,
				"green": self.bouquetEpgs,
				"yellow": self["list"].toggleSelection,
				"blue": self["list"].toggleAllSelection,

				"ok": self["list"].toggleSelection,
			}, -2)

		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Save"))
		self["key_yellow"] = Label(_("Select"))
		self["key_blue"] = Label(_("All Select"))
		
		self['status'] = Label()
		self['info'] = Label()

	def bouquetEpgs(self):
		try:

			self.sources = []
			for eb,be in enumerate(self["list"].list):
					be = self["list"].list[eb][0]
					if be[3]:
						self.sources.append(be[0])
			serviceHandler = eServiceCenter.getInstance()
			channels = chList(self.sources)
			if config.plugins.xtraEvent.locations.value == "hdd":
				self.pathLoc = "/media/hdd/xtraEvent/"
			elif config.plugins.xtraEvent.locations.value == "usb":
				self.pathLoc = "/media/usb/xtraEvent/"
			elif config.plugins.xtraEvent.locations.value == "internal":
				self.pathLoc = "/etc/enigma2/xtraEvent/"
			else:
				self.pathLoc = "/tmp/"
			if os.path.exists(self.pathLoc+"bqts"):
				os.remove(self.pathLoc+"bqts")
			for r in channels:
				open(self.pathLoc + "bqts", "a+").write("%s\n"% str(r))
		except:
			pass
		try:
			if os.path.exists(self.pathLoc+"events"):
				os.remove(self.pathLoc+"events")
			ref = ""
			refs = channels
			for ref in refs:
				try:
					events = self.epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
					n = config.plugins.xtraEvent.searchNUMBER.value
					for i in xrange(int(n)):
						title = events[i][4]
						evntN = re.sub('([\(\[]).*?([\)\]])|(: odc.\d+)|[?|$|.|!|,|:|/]', '', str(title))
						evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").rstrip()
						open(self.pathLoc+"events","a+").write("%s\n"% str(evntNm))
					
				except:
					pass

			self.close()
		except:
			pass

		
		
	def cancel(self):
		self.close(self.session, False)
		
		
		
		
		
		
		
		
		
# -*- coding: utf-8 -*-
# by digiteng...06.2020, 08.2020
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
import Tools.Notifications
import os, re, random
from Components.SelectionList import SelectionList, SelectionEntryComponent
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigText, ConfigInteger, ConfigSelectionNumber, ConfigDirectory
from Components.ConfigList import ConfigListScreen
from enigma import eTimer, eLabel, eServiceCenter, eServiceReference, ePixmap, eSize, ePoint, loadJPG, iServiceInformation, eEPGCache, getBestPlayableServiceReference, getDesktop
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Screens.VirtualKeyBoard import VirtualKeyBoard
from PIL import Image, ImageDraw, ImageFilter
from Screens.LocationBox import LocationBox
import requests
import thread
from Components.ProgressBar import ProgressBar

desktop_size = getDesktop(0).size().width()
epgcache = eEPGCache.getInstance()

config.plugins.xtraEvent = ConfigSubsection()
config.plugins.xtraEvent.loc = ConfigDirectory(default='')
config.plugins.xtraEvent.searchMOD = ConfigSelection(default = "Current Channel", choices = [("Bouquets"), ("Current Channel")])
# config.plugins.xtraEvent.searchNUMBER = ConfigSelectionNumber(0, 999, 1, default=0)
imglist = []
for i in range(0, 999):
	if i == 0:
		imglist.append(("all epg"))
	else:
		imglist.append(("%d" % i))
config.plugins.xtraEvent.searchNUMBER = ConfigSelection(default = "all epg", choices = imglist)

config.plugins.xtraEvent.timer = ConfigSelectionNumber(1, 168, 1, default=1)
config.plugins.xtraEvent.searchMANUELnmbr = ConfigSelectionNumber(0, 999, 1, default=1)
config.plugins.xtraEvent.searchMANUELyear = ConfigInteger(default = 0, limits=(0, 9999))
config.plugins.xtraEvent.imgNmbr = ConfigSelectionNumber(0, 999, 1, default=1)

config.plugins.xtraEvent.searchModManuel = ConfigSelection(default = "TV List", choices = [("TV List"), ("Movies List")])
config.plugins.xtraEvent.EMCloc = ConfigDirectory(default='')

config.plugins.xtraEvent.tmdbAPI = ConfigText(default="", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.tvdbAPI = ConfigText(default="", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.omdbAPI = ConfigText(default="", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.fanartAPI = ConfigText(default="", visible_width=100, fixed_size=False)

config.plugins.xtraEvent.searchMANUEL_EMC = ConfigText(default="movies name", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.searchMANUEL = ConfigText(default="event name", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.searchLang = ConfigText(default="en", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.timerMod = ConfigYesNo(default = False)

config.plugins.xtraEvent.tmdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.tvdb = ConfigYesNo(default = False)
# config.plugins.xtraEvent.omdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.maze = ConfigYesNo(default = False)
config.plugins.xtraEvent.fanart = ConfigYesNo(default = False)
config.plugins.xtraEvent.bing = ConfigYesNo(default = False)
config.plugins.xtraEvent.extra = ConfigYesNo(default = False)

config.plugins.xtraEvent.poster = ConfigYesNo(default = False)
config.plugins.xtraEvent.banner = ConfigYesNo(default = False)
config.plugins.xtraEvent.backdrop = ConfigYesNo(default = False)
config.plugins.xtraEvent.info = ConfigYesNo(default = False)

config.plugins.xtraEvent.opt_Images = ConfigYesNo(default = False)
config.plugins.xtraEvent.cnfg = ConfigYesNo(default = False)
config.plugins.xtraEvent.cnfgSel = ConfigSelection(default = "poster", choices = [("poster"), ("banner"), ("backdrop"), ("EMC")])

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
	("fileName", "original(680x1000)")])

config.plugins.xtraEvent.TMDBbackdropsize = ConfigSelection(default="w300", choices = [
 	("w300", "300x170"), 
	("w780", "780x440"), 
	("w1280", "1280x720"),
	("original", "ORIGINAL")])

config.plugins.xtraEvent.TVDBbackdropsize = ConfigSelection(default="thumbnail", choices = [
	("thumbnail", "640x360"), 
	("fileName", "original(1920x1080)")])

config.plugins.xtraEvent.FANART_Poster_Resize = ConfigSelection(default="10", choices = [
	("10", "100x142"), 
	("5", "200x285"), 
	("3", "333x475"), 
	("2", "500x713"), 
	("1", "1000x1426")])

config.plugins.xtraEvent.FANART_Backdrop_Resize = ConfigSelection(default="10", choices = [
	("10", "192x108"), 
	("5", "384x216"), 
	("3", "634x357"), 
	("2", "960x540"), 
	("1", "1920x1080")])

config.plugins.xtraEvent.imdb_Poster_size = ConfigSelection(default="10", choices = [
	("185", "185x278"), 
	("344", "344x510"), 
	("500", "500x750")])

config.plugins.xtraEvent.PB = ConfigSelection(default="posters", choices = [
	("posters", "Poster"), 
	("backdrops", "Backdrop")])

config.plugins.xtraEvent.imgs = ConfigSelection(default="TMDB", choices = [
	('TMDB', 'TMDB'), 
	('TVDB', 'TVDB'), 
	('FANART', 'FANART'), 
	('IMDB(poster)', 'IMDB(poster)'), 
	('Bing', 'Bing'), 
	('Google', 'Google')])

config.plugins.xtraEvent.searchType = ConfigSelection(default="tv", choices = [
	('tv', 'TV'), 
	('movie', 'MOVIE'), 
	('multi', 'MULTI')])

config.plugins.xtraEvent.FanartSearchType = ConfigSelection(default="tv", choices = [
	('tv', 'TV'),
	('movies', 'MOVIE')])

class xtra(Screen, ConfigListScreen):
	if desktop_size <= 1280:
		skin = """<screen name="xtra" position="0,0" size="1280,720">
			  <ePixmap position="0,0" size="1280,720" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_hd.png" transparent="1" />
			  <widget source="Title" render="Label" position="40,35" size="745,40" font="Console; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
			  <widget name="config" position="40,95" size="745,510" itemHeight="30" font="Regular;24" foregroundColor="#c5c5c5" scrollbarMode="showOnDemand" transparent="1" backgroundColor="#23262e" backgroundColorSelected="#565d6d" foregroundColorSelected="#ffffff" />
			  <widget source="help" position="840,600" size="400,26" render="Label" font="Regular;22" foregroundColor="#f3fc92" backgroundColor="#23262e" halign="left" valign="center" transparent="1" />
			  <widget name="status" position="840,300" size="400,30" transparent="1" font="Regular;22" foregroundColor="#92f1fc" backgroundColor="#23262e" />
			  <widget name="info" position="840,330" size="400,260" transparent="1" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" halign="left" valign="top" />
			  <widget source="key_red" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="45,640" size="170,30" halign="left" transparent="1" zPosition="1" />
			  <widget source="key_green" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="235,640" size="170,30" halign="left" transparent="1" zPosition="1" />
			  <widget source="key_yellow" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="425,640" size="170,30" halign="left" transparent="1" zPosition="1" />
			  <widget source="key_blue" render="Label" font="Regular; 20" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="615,640" size="170,30" halign="left" transparent="1" zPosition="1" />

			  <eLabel name="" text=" INFO" position="1150,640" size="100,30" transparent="1" halign="center" font="Console; 20" />
			</screen>"""


	else:
		skin = """<screen name="xtra" position="0,0" size="1920,1080">
		  <ePixmap position="0,0" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_fhd.png" transparent="1" />
		  <widget source="Title" render="Label" position="60,53" size="1118,60" font="Console; 45" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
		  <widget name="config" position="60,143" size="1118,765" itemHeight="45" font="Regular;36" foregroundColor="#c5c5c5" scrollbarMode="showOnDemand" transparent="1" backgroundColor="#23262e" backgroundColorSelected="#565d6d" foregroundColorSelected="#ffffff" />
		  <widget source="help" position="1260,850" size="600,60" render="Label" font="Regular;28" foregroundColor="#f3fc92" backgroundColor="#23262e" halign="left" valign="center" transparent="1" />
		  <widget name="status" position="1260,450" size="600,45" transparent="1" font="Regular;33" foregroundColor="#92f1fc" backgroundColor="#23262e" />
		  <widget name="info" position="1260,495" size="600,390" transparent="1" font="Regular;33" foregroundColor="#c5c5c5" backgroundColor="#23262e" halign="left" valign="top" />
		  <widget source="key_red" render="Label" font="Regular;33" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="68,960" size="255,45" halign="left" transparent="1" zPosition="1" />
		  <widget source="key_green" render="Label" font="Regular;33" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="353,960" size="255,45" halign="left" transparent="1" zPosition="1" />
		  <widget source="key_yellow" render="Label" font="Regular;33" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="638,960" size="255,45" halign="left" transparent="1" zPosition="1" />
		  <widget source="key_blue" render="Label" font="Regular; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="923,960" size="255,45" halign="left" transparent="1" zPosition="1" />

		  <eLabel name="" text=" INFO" position="1725,960" size="150,45" transparent="1" halign="center" font="Console; 30" />
		</screen>"""


	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)

		self.epgcache = eEPGCache.getInstance()

		list = []
		ConfigListScreen.__init__(self, list, session=session)

		self['key_red'] = Label(_('Close'))
		self['key_green'] = Label(_('Search'))
		self['key_yellow'] = Label(_('Download'))
		self['key_blue'] = Label(_('Manuel Search'))

		self["actions"] = ActionMap(["OkCancelActions", "SetupActions", "DirectionActions", "ColorActions", "EventViewActions", "VirtualKeyboardAction"],
		{
			"left": self.keyLeft,
			"down": self.keyDown,
			"up": self.keyUp,
			"right": self.keyRight,
			# "red": self.exit,
			# "green": self.search,
			# "yellow": self.dwnldFileld,
			# "blue": self.ms,
			# "cancel": self.exit,
			# "ok": self.keyOK,
			# "info": self.strg,
			# "menu": self.brokenImageRemove,

			# "info": self.about,
			
			"cancel": self.close
		},-1)
		
		self.setTitle(_("xtraEvent v1"))
		self['status'] = Label()
		self['info'] = Label()
		self["help"] = StaticText()

		self.timer = eTimer()
		self.timer.callback.append(self.xtraList)
		self.onLayoutFinish.append(self.xtraList)

	def delay(self):
		self.timer.start(100, True)

	def xtraList(self):
		for x in self["config"].list:
			if len(x) > 1:
				x[1].save()
		list = []
		list.append(getConfigListEntry("—"*100))
# path location_________________________________________________________________________________________________________________
		list.append(getConfigListEntry("CONFIG MENU", config.plugins.xtraEvent.cnfg, _("adjust your settings and close ... your settings are valid ...")))
		list.append(getConfigListEntry("—"*100))
		if config.plugins.xtraEvent.cnfg.value:
			list.append(getConfigListEntry("    LOCATION", config.plugins.xtraEvent.loc, _("'OK' select location downloads...")))
			
			list.append(getConfigListEntry("    OPTIMIZE IMAGES", config.plugins.xtraEvent.opt_Images, _("optimize images...")))
			if config.plugins.xtraEvent.opt_Images.value:
				list.append(getConfigListEntry("\tOPTIMIZE IMAGES SELECT", config.plugins.xtraEvent.cnfgSel, _("'OK' select for optimize images...")))
			list.append(getConfigListEntry("    TMDB API", config.plugins.xtraEvent.tmdbAPI, _("enter your own api key...")))
			list.append(getConfigListEntry("    TVDB API", config.plugins.xtraEvent.tvdbAPI, _("enter your own api key...")))
			list.append(getConfigListEntry("    OMDB API", config.plugins.xtraEvent.omdbAPI, _("enter your own api key...")))
			list.append(getConfigListEntry("    FANART API", config.plugins.xtraEvent.fanartAPI, _("enter your own api key...")))
			list.append(getConfigListEntry("—"*100))
# config_________________________________________________________________________________________________________________
			list.append(getConfigListEntry("    SEARCH MODE", config.plugins.xtraEvent.searchMOD, _("select search mode...")))		
			list.append(getConfigListEntry("    SEARCH NEXT EVENTS", config.plugins.xtraEvent.searchNUMBER, _("enter the number of next events...")))
			# if config.plugins.xtraEvent.searchNUMBER.value == 0:
				# config.plugins.xtraEvent.searchNUMBER.value = "all"
			list.append(getConfigListEntry("    SEARCH LANGUAGE", config.plugins.xtraEvent.searchLang, _("select search language...")))
			list.append(getConfigListEntry("    TIMER", config.plugins.xtraEvent.timerMod, _("select timer update for events..")))
			if config.plugins.xtraEvent.timerMod.value == True:
				list.append(getConfigListEntry("\tTIMER(hours)", config.plugins.xtraEvent.timer, _("..."),))
		list.append(getConfigListEntry("—"*100))
		list.append(getConfigListEntry("IMAGE SOURCES"))
		list.append(getConfigListEntry("—"*100))

# poster__________________________________________________________________________________________________________________
		list.append(getConfigListEntry("POSTER", config.plugins.xtraEvent.poster, _("...")))
		if config.plugins.xtraEvent.poster.value == True:
			list.append(getConfigListEntry("\tTMDB", config.plugins.xtraEvent.tmdb, _("source for poster..."),))
			if config.plugins.xtraEvent.tmdb.value :
				list.append(getConfigListEntry("\tTMDB POSTER SIZE", config.plugins.xtraEvent.TMDBpostersize, _("Choose poster sizes for TMDB")))
				list.append(getConfigListEntry("-"*100))
			list.append(getConfigListEntry("\tTVDB", config.plugins.xtraEvent.tvdb, _("source for poster...")))
			if config.plugins.xtraEvent.tvdb.value :
				list.append(getConfigListEntry("\tTVDB POSTER SIZE", config.plugins.xtraEvent.TVDBpostersize, _("Choose poster sizes for TVDB")))
				list.append(getConfigListEntry("_"*100))
			list.append(getConfigListEntry("\tFANART", config.plugins.xtraEvent.fanart, _("source for poster...")))	
			if config.plugins.xtraEvent.fanart.value:
				list.append(getConfigListEntry("\tFANART POSTER SIZE", config.plugins.xtraEvent.FANART_Poster_Resize, _("Choose poster sizes for FANART")))
				list.append(getConfigListEntry("—"*100))
			list.append(getConfigListEntry("\tMAZE(TV SHOWS)", config.plugins.xtraEvent.maze, _("source for tv shows...")))
# banner__________________________________________________________________________________________________________________
		list.append(getConfigListEntry("BANNER", config.plugins.xtraEvent.banner, _("tvdb and fanart for BANNER...")))

# backdrop_______________________________________________________________________________________________________________
		list.append(getConfigListEntry("BACKDROP", config.plugins.xtraEvent.backdrop, _("source for backdrop...")))
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
				list.append(getConfigListEntry("\tFANART BACKDROP SIZE", config.plugins.xtraEvent.FANART_Backdrop_Resize, _("Choose backdrop sizes for FANART")))
				list.append(getConfigListEntry("_"*100))
			list.append(getConfigListEntry("\tEXTRA", config.plugins.xtraEvent.extra, _("tvmovie.de, bing, google search images...")))
			list.append(getConfigListEntry("—"*100))
# info___________________________________________________________________________________________________________________
		list.append(getConfigListEntry("INFO", config.plugins.xtraEvent.info, _("Program information with OMDB...")))
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




class pathLocation():
	def __init__(self):
		self.location()

	def location(self):
		pathLoc = ""
		if not os.path.isdir(config.plugins.xtraEvent.loc.value):
			pathLoc = "/tmp/xtraEvent/"
			try:
				if not os.path.isdir(pathLoc):
					os.makedirs(pathLoc + "poster")
					os.makedirs(pathLoc + "banner")
					os.makedirs(pathLoc + "backdrop")
					os.makedirs(pathLoc + "infos")
					os.makedirs(pathLoc + "mSearch")
					os.makedirs(pathLoc + "EMC")
			except:
				pass
		else:	
			pathLoc = config.plugins.xtraEvent.loc.value + "xtraEvent/"
			try:
				if not os.path.isdir(pathLoc):
					os.makedirs(pathLoc + "poster")
					os.makedirs(pathLoc + "banner")
					os.makedirs(pathLoc + "backdrop")
					os.makedirs(pathLoc + "infos")
					os.makedirs(pathLoc + "mSearch")
					os.makedirs(pathLoc + "EMC")
			except:
				pass

		return pathLoc
pathLoc = pathLocation().location()

if config.plugins.xtraEvent.tmdbAPI.value != "":
	tmdb_api = config.plugins.xtraEvent.tmdbAPI.value
else:
	tmdb_api = "3c3efcf47c3577558812bb9d64019d65"

if config.plugins.xtraEvent.fanartAPI.value != "":
	fanart_api = config.plugins.xtraEvent.fanartAPI.value
else:
	fanart_api = "6d231536dea4318a88cb2520ce89473b"
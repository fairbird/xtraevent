# -*- coding: utf-8 -*-
# by digiteng...05.2020...
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

from Components.Sources.Event import Event
from Components.Sources.CurrentService import CurrentService
from Components.MenuList import MenuList
from Components.SelectionList import SelectionList, SelectionEntryComponent

from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger,ConfigOnOff, ConfigSlider, ConfigNothing
from Components.ConfigList import ConfigListScreen
from Screens.ChoiceBox import ChoiceBox
from enigma import eTimer, getDesktop, eLabel, eServiceCenter, eServiceReference, iServiceInformation, eEPGCache
from Components.Sources.List import List
from Components.Sources.ServiceList import ServiceList
from ServiceReference import ServiceReference
from Components.Sources.StaticText import StaticText
from Screens.VirtualKeyBoard import VirtualKeyBoard 
from Screens.NumericalTextInputHelpDialog import NumericalTextInputHelpDialog

from PIL import Image





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
config.plugins.xtraEvent.tmdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.tvdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.omdb = ConfigYesNo(default = False)
config.plugins.xtraEvent.maze = ConfigYesNo(default = False)
config.plugins.xtraEvent.fanart = ConfigYesNo(default = False)

config.plugins.xtraEvent.poster = ConfigYesNo(default = False)
config.plugins.xtraEvent.banner = ConfigYesNo(default = False)
config.plugins.xtraEvent.backdrop = ConfigYesNo(default = False)
config.plugins.xtraEvent.info = ConfigYesNo(default = False)

config.plugins.xtraEvent.searchMOD = ConfigSelection(default = "Current Channel", choices = [("Bouquets"), ("Current Channel")])

config.plugins.xtraEvent.searchNUMBER = ConfigInteger(default = 5, limits=(0, 999))
config.plugins.xtraEvent.searchMANUEL = ConfigText(default="event name", visible_width=100, fixed_size=False)
config.plugins.xtraEvent.searchMANUELyear = ConfigInteger(default = 2020, limits=(0, 9999))

config.plugins.xtraEvent.locations = ConfigSelection(default = "hdd", choices = [
	("hdd"), 
	("usb"),
	("internal"),
	])

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

		list = []
		ConfigListScreen.__init__(self, list)

		self.epgcache = eEPGCache.getInstance()
		
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
			"yellow": self.download,
			"blue": self.currentEvent,
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
		else:
			self.pathLoc = "/tmp/"

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
		list.append(getConfigListEntry("Location", config.plugins.xtraEvent.locations, _("select locations...")))
		list.append(getConfigListEntry("—"*100))
# config_________________________________________________________________________________________________________________
		list.append(getConfigListEntry("SEARCH MODE", config.plugins.xtraEvent.searchMOD, _("select search mode...")))
		if config.plugins.xtraEvent.searchMOD.value == "Manuel Search":
			self.timer.start(100, True)
			list.append(getConfigListEntry("  Title", config.plugins.xtraEvent.searchMANUEL, _("enter the event name to search...")))
			# self.ms()
			
		else:
			list.append(getConfigListEntry("SEARCH NEXT EVENTS", config.plugins.xtraEvent.searchNUMBER, _("enter the number of next events to be scanned for each channel...")))
		list.append(getConfigListEntry("—"*100))

# poster__________________________________________________________________________________________________________________
		list.append(getConfigListEntry("POSTER", config.plugins.xtraEvent.poster, _("...")))
		if config.plugins.xtraEvent.poster.value == True:
			list.append(getConfigListEntry("  TMDB", config.plugins.xtraEvent.tmdb, _("best source for poster..."),))
			if config.plugins.xtraEvent.tmdb.value :
				list.append(getConfigListEntry("    TMDB POSTER SIZE", config.plugins.xtraEvent.TMDBpostersize, _("Choose poster sizes for TMDB")))
				list.append(getConfigListEntry("_"*100))
			list.append(getConfigListEntry("  TVDB", config.plugins.xtraEvent.tvdb, _("best source for banner...")))
			if config.plugins.xtraEvent.tvdb.value :
				list.append(getConfigListEntry("    TVDB POSTER SIZE", config.plugins.xtraEvent.TVDBpostersize, _("Choose poster sizes for TVDB")))
				list.append(getConfigListEntry("_"*100))
			list.append(getConfigListEntry("  OMDB", config.plugins.xtraEvent.omdb, _("best source for info...")))
			list.append(getConfigListEntry("  MAZE(TV SHOWS)", config.plugins.xtraEvent.maze, _("best source for tv shows...")))
			list.append(getConfigListEntry("  FANART", config.plugins.xtraEvent.fanart, _("alternative source for poster, banner, etc...")))	
			if config.plugins.xtraEvent.fanart.value:
				list.append(getConfigListEntry("    FANART POSTER SIZE", config.plugins.xtraEvent.FANARTresize, _("Choose poster sizes for FANART")))
				

			list.append(getConfigListEntry("—"*100))
# banner__________________________________________________________________________________________________________________
		list.append(getConfigListEntry("BANNER", config.plugins.xtraEvent.banner, _("tvdb and fanart for banner...")))



# backdrop_______________________________________________________________________________________________________________
		list.append(getConfigListEntry("BACKDROP", config.plugins.xtraEvent.backdrop, _("best source for poster...")))
		if config.plugins.xtraEvent.backdrop.value == True:
			list.append(getConfigListEntry("  TMDB", config.plugins.xtraEvent.tmdb, _("source for backdrop...")))
			if config.plugins.xtraEvent.tmdb.value :
				list.append(getConfigListEntry("    TMDB BACKDROP SIZE", config.plugins.xtraEvent.TMDBbackdropsize, _("Choose backdrop sizes for TMDB")))
				list.append(getConfigListEntry("_"*100))
			list.append(getConfigListEntry("  TVDB", config.plugins.xtraEvent.tvdb, _("source for backdrop...")))
			if config.plugins.xtraEvent.tvdb.value :
				list.append(getConfigListEntry("    TVDB BACKDROP SIZE", config.plugins.xtraEvent.TVDBbackdropsize, _("Choose backdrop sizes for TVDB")))
				list.append(getConfigListEntry("_"*100))
			list.append(getConfigListEntry("  FANART", config.plugins.xtraEvent.fanart, _("source for backdrop...")))
			if config.plugins.xtraEvent.fanart.value:
				list.append(getConfigListEntry("    FANART BACKDROP SIZE", config.plugins.xtraEvent.FANARTresize, _("Choose backdrop sizes for FANART")))
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
		for x in self["config"].list:
			if len(x) > 1:
				x[1].save()
		if config.plugins.xtraEvent.searchMOD.value == "Current Channel":
			self.currentChEpgs()
		elif config.plugins.xtraEvent.searchMOD.value == "Bouquets":
			self.session.open(selBouquets)

	def download(self):
		if config.plugins.xtraEvent.poster.value == True:
			if config.plugins.xtraEvent.tmdb.value == True:
				self.tmdb_Poster()
			if config.plugins.xtraEvent.tvdb.value == True:
				self.tvdb_Poster()	
			if config.plugins.xtraEvent.omdb.value == True:
				self.omdb_Poster()
			if config.plugins.xtraEvent.maze.value == True:
				self.maze_Poster()
			if config.plugins.xtraEvent.fanart.value == True:
				self.fanart_Poster()

		if config.plugins.xtraEvent.banner.value == True:
			self.Banner()

		if config.plugins.xtraEvent.backdrop.value == True:
			if config.plugins.xtraEvent.tmdb.value == True:
				self.tmdb_backdrop()
			if config.plugins.xtraEvent.tvdb.value == True:
				self.tvdb_backdrop()
			if config.plugins.xtraEvent.fanart.value == True:
				self.fanart_backdrop()

		if config.plugins.xtraEvent.info.value == True:
			self.infos()

	def currentChEpgs(self):
		if os.path.exists("/tmp/events"):
			os.remove("/tmp/events")
		try:
			event = None
			serviceref = self.session.nav.getCurrentlyPlayingServiceReference()
			ref = serviceref.toString()
			try:
				events = self.epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
				n = config.plugins.xtraEvent.searchNUMBER.value

				for i in xrange(n):
					title = events[i][4]
					evntN = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", title)
					evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").replace("LOS ", "The ").rstrip()
					# evntNm = evntNm.replace(" ","_")
					# Year ######################################################
					# epgcache = eEPGCache.getInstance()
					# event = epgcache.lookupEvent(['ESX', (ref, 1, -1, -1)])

					# short_description = event[i][1]
					# ext_description = event[i][0]
					# full_description = short_description + "\n" + ext_description

					# year=""
					# pattern = ["(20[0-9][0-9])", "(19[0-9][0-9])"]
				
					# for ii in pattern:
						# yr = re.search(ii, short_description[i])
						# if yr:
							# year = yr.group(1)
					# open("/tmp/events","a+").write("year: %s" % str(year) + " title: %s\n" % str(evntNm))
					# ##################################################

					open("/tmp/events","a+").write("%s\n" % str(evntNm))

					if os.path.exists("/tmp/events"):
						with open("/tmp/events", "r") as f:
							titleNm = f.readlines()
						titleNm = list(dict.fromkeys(titleNm))
						titleNm = len(titleNm)
						self['status'].setText(_("number of events to be scanned : {}".format(titleNm)))
			except:
				pass

		except Exception as e: 
			print(e)
			self['info'].setText(_(str(e)))

	def currentEvent(self):
		event = None
		info = ""
		import NavigationInstance
		# ref = self.session.nav.getCurrentlyPlayingServiceReference().toString()
		# ref = NavigationInstance.instance.getCurrentlyPlayingServiceReference().toString()
		ref = self.source.service
		info = ref and self.source.info
		if info is None:
			return
		# playingref = eServiceCenter.getInstance()
		# playingref = eServiceReference().toString()
		# service = self.session.nav.getCurrentService()
		if ref:
			# events = self.epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
			events = self.epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1)])
			cevnt = events[1][4]
			# open("/tmp/cevnt","w").write(cevnt)
			self['info'].setText(_(str(cevnt)))



# DOWNLOAD POSTERS ######################################################################################################

	def tmdb_Poster(self):
		self.year = ""
		try:
			if os.path.exists("/tmp/event-year"):
				with open("/tmp/event-year", "r") as f:
					self.year = f.read()
					
			if os.path.exists("/tmp/events"):
				with open("/tmp/events", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
				# open("/tmp/prgrs-poster", "w").write(str(n))
				for i in xrange(n):
					# self.i = i
					title = titles[i]
					title = title.strip()
					
					srch = "multi"
					url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
					if self.year != "":
						url_tmdb += "&primary_release_year={}&year={}".format(self.year, self.year)

					try:
						poster = json.load(urlopen(url_tmdb))['results'][0]['poster_path']
						p_size = config.plugins.xtraEvent.TMDBpostersize.value
						url_poster = "https://image.tmdb.org/t/p/{}{}".format(p_size, poster)
						# open("/tmp/url_poster", "a+").write("%s\n"% str(url_poster))
						dwn_poster = self.pathLoc + "poster/{}.jpg".format(title)
						urlretrieve(url_poster, dwn_poster)

					except:
						pass

				self['status'].setText(_("downloaded posters : {}".format(n)))

		except Exception as e:
			print e
			self['info'].setText(_(str(e)))

	def tvdb_Poster(self):
		try:
			if os.path.exists("/tmp/events"):
				with open("/tmp/events", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
				for i in xrange(n):
					title = titles[i]
					title = title.strip()
					try:
						url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(title))
						url_read = urlopen(url_tvdb).read()
						series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
						if series_id:
							url_tvdb = "https://thetvdb.com/api/a99d487bb3426e5f3a60dea6d3d3c7ef/series/{}/en".format(series_id)
							url_read = urlopen(url_tvdb).read()
							poster = re.findall('<poster>(.*?)</poster>', url_read)[0]
							if poster:
								url_poster = "https://artworks.thetvdb.com/banners/{}".format(poster)
								if config.plugins.xtraEvent.TVDBpostersize.value == "thumbnail":
									url_poster = url_poster.replace(".jpg", "_t.jpg")
								dwn_poster = self.pathLoc + "poster/{}.jpg".format(title)
								urlretrieve(url_poster, dwn_poster)

					except:
						pass
		except:
			pass

	def omdb_Poster(self):
		try:
			if os.path.exists("/tmp/events"):
				with open("/tmp/events", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
				for i in xrange(n):
					title = titles[i]
					title = title.strip()
					
					omdb_apis = ["6a4c9432", "a8834925", "550a7c40", "8ec53e6b"]
					omdb_api = random.sample(omdb_apis, 1)[0]
					url_omdb = 'https://www.omdbapi.com/?apikey=%s&t=%s' %(omdb_api, quote(title))
					try:
						url_poster = json.load(urlopen(url_omdb))['Poster']

						dwn_poster = self.pathLoc + "poster/{}.jpg".format(title)
						urlretrieve(url_poster, dwn_poster)
					except:
						pass
					continue
		except:
			pass
	
	def maze_Poster(self):
		try:
			if os.path.exists("/tmp/events"):
				with open("/tmp/events", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
				for i in xrange(n):
					title = titles[i]
					title = title.strip()
			
					url_maze = "http://api.tvmaze.com/search/shows?q={}".format(quote(title))
					try:
						url_poster = json.load(urlopen(url_maze))[0]['show']['image']['medium']
						dwn_poster = self.pathLoc + "poster/{}.jpg".format(title)
						urlretrieve(url_poster, dwn_poster)
					except:
						pass
					continue
		except:
			return

	def fanart_Poster(self):
		try:
			if os.path.exists("/tmp/events"):
				with open("/tmp/events", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
				for i in xrange(n):
					title = titles[i]
					title = title.strip()
					self.title=title
					try:
						srch = "multi"
						url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
						bnnr = json.load(urlopen(url_tmdb))
						tmdb_id = (bnnr['results'][0]['id'])
						if tmdb_id:
							m_type = (bnnr['results'][0]['media_type'])
							if m_type == "movie":
								m_type = (bnnr['results'][0]['media_type']) + "s"
							else:
								mm_type = m_type
							

							dwn_poster = self.pathLoc + "poster/{}.jpg".format(title)
							if not os.path.exists(dwn_poster):
								url_maze = "http://api.tvmaze.com/singlesearch/shows?q=%s" %quote(title)
								
								mj = json.load(urlopen(url_maze))
								tvdb_id = (mj['externals']['thetvdb'])
								if tvdb_id:
									try:
										
										url_fanart = "https://webservice.fanart.tv/v3/%s/%s?api_key=6d231536dea4318a88cb2520ce89473b" %(m_type, tvdb_id)
										fjs = json.load(urlopen(url_fanart))
										
										if fjs:
											if m_type == "movies":
												mm_type = (bnnr['results'][0]['media_type'])
											else:
												mm_type = m_type
											url_poster = (fjs['tvposter'][0]['url'])
											# open("/tmp/mm_type","w").write("%s" % str(mm_type))
											if url_poster:
												dwn_poster = self.pathLoc + "poster/{}.jpg".format(title)
												self.dwn_poster=dwn_poster
												urlretrieve(url_poster, dwn_poster)
												self.Fnrtresz()

									except:
										pass
				
					except:
						pass
				
		except:
			pass

	def Fnrtresz(self):
		scl = 1
		im = Image.open(self.dwn_poster)
		scl = config.plugins.xtraEvent.FANARTresize.value
		im1 = im.resize((im.size[0] // int(scl), im.size[1] // int(scl)), Image.ANTIALIAS)
		im1.save(self.dwn_poster)
		
		# image = Image.open(self.dwn_poster)
		# maxsize = config.plugins.xtraEvent.FANARTresize.value
		# image.thumbnail(maxsize, Image.ANTIALIAS)
 		# image.save(self.dwn_poster)
		
# DOWNLOAD BANNERS ######################################################################################################

	def Banner(self):
		if os.path.exists("/tmp/events"):
			with open("/tmp/events", "r") as f:
				titles = f.readlines()

			titles = list(dict.fromkeys(titles))
			n = len(titles)
			for i in xrange(n):
				title = titles[i]
				title = title.strip()
				
				try:
					url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname=%s" %quote(title)
					url_read = urlopen(url_tvdb).read()			
					series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read, re.I)[0]
					if series_id:
						url_banner = "https://artworks.thetvdb.com/banners/graphical/%s-g_t.jpg" %(series_id)
						if url_banner:
							dwn_banner = self.pathLoc + "banner/{}.jpg".format(title)
							urlretrieve(url_banner, dwn_banner)
				except:
					try:
						srch = "multi"
						url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
						bnnr = json.load(urlopen(url_tmdb))
						tmdb_id = (bnnr['results'][0]['id'])
						if tmdb_id:
							m_type = (bnnr['results'][0]['media_type'])
							if m_type == "movie":
								m_type = (bnnr['results'][0]['media_type']) + "s"
							else:
								mm_type = m_type
							url_fanart = "https://webservice.fanart.tv/v3/%s/%s?api_key=6d231536dea4318a88cb2520ce89473b" %(m_type, tmdb_id)
							fjs = json.load(urlopen(url_fanart))
							if fjs:
								if m_type == "movies":
									mm_type = (bnnr['results'][0]['media_type'])
								url_banner = (fjs[mm_type+'banner'][0]['url'])
								if url_banner:
									dwn_banner = self.pathLoc + "banner/{}.jpg".format(title)
									urlretrieve(url_banner, dwn_banner)
					except:
						try:
							url_maze = "http://api.tvmaze.com/singlesearch/shows?q=%s" %(title)
							mj = json.load(urlopen(url_maze))
							poster = (mj['externals']['thetvdb'])
							if poster:
								url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname=%s" %quote(title)
								url_read = urlopen(url_tvdb).read()
								series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read, re.I)[0]
								banner_img = re.findall('<banner>(.*?)</banner>', url_read, re.I)[0]
								if banner_img:
									url_banner = "https://artworks.thetvdb.com%s" %(banner_img)
									dwn_banner = self.pathLoc + "banner/{}.jpg".format(title)
									urlretrieve(url_banner, dwn_banner)
								if series_id:
									try:
										url_fanart = "https://webservice.fanart.tv/v3/%s/%s?api_key=6d231536dea4318a88cb2520ce89473b" %(m_type, series_id)
										fjs = json.load(urlopen(url_fanart))
										if fjs:
											if m_type == "movies":
												mm_type = (bnnr['results'][0]['media_type'])
											else:
												mm_type = m_type
											url_banner = (fjs[mm_type+'banner'][0]['url'])

											if url_banner:
												dwn_banner = self.pathLoc + "banner/{}.jpg".format(title)
												urlretrieve(url_banner, dwn_banner)
									except:
										pass
						except:
							pass

# DOWNLOAD BACKDROP ######################################################################################################

	def tmdb_backdrop(self):
		try:
			if os.path.exists("/tmp/events"):
				with open("/tmp/events", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
				for i in xrange(n):
					title = titles[i]
					title = title.strip()
					srch = "multi"
					# tmdb_api = "3c3efcf47c3577558812bb9d64019d65" 
					url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
					try:
						backdrop = json.load(urlopen(url_tmdb))['results'][0]['backdrop_path']
						backdrop_size = config.plugins.xtraEvent.TMDBbackdropsize.value
						url_backdrop = "https://image.tmdb.org/t/p/{}{}".format(backdrop_size, backdrop)
						dwn_backdrop = self.pathLoc + "backdrop/{}.jpg".format(title)
						urlretrieve(url_backdrop, dwn_backdrop)
					except:
						pass
					self['status'].setText(_("downloaded backdrop : {}".format(n)))
		except:
			pass

	def tvdb_backdrop(self):
		try:
			if os.path.exists("/tmp/events"):
				with open("/tmp/events", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
				for i in xrange(n):
					title = titles[i]
					title = title.strip()

					try:
						url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(title))
						url_read = urlopen(url_tvdb).read()
						series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
						if series_id:
							url_tvdb = "https://thetvdb.com/api/a99d487bb3426e5f3a60dea6d3d3c7ef/series/{}/en".format(series_id)
							url_read = urlopen(url_tvdb).read()
							backdrop = re.findall('<fanart>(.*?)</fanart>', url_read)[0]
							if backdrop:
								url_backdrop = "https://artworks.thetvdb.com/banners/{}".format(backdrop)
								if config.plugins.xtraEvent.TVDBbackdropsize.value == "thumbnail":
									url_backdrop = url_backdrop.replace(".jpg", "_t.jpg")
								# open("/tmp/url_backdrop","a+").write("%s\n" % str(url_backdrop))
								dwn_backdrop = self.pathLoc + "backdrop/{}.jpg".format(title)
								urlretrieve(url_backdrop, dwn_backdrop)

					except:
						pass

		except:
			pass

	def fanart_backdrop(self):
		try:
			if os.path.exists("/tmp/events"):
				with open("/tmp/events", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
				for i in xrange(n):
					title = titles[i]
					title = title.strip()
					
					try:
						srch = "multi"
						url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
						bnnr = json.load(urlopen(url_tmdb))
						tmdb_id = (bnnr['results'][0]['id'])
						if tmdb_id:
							m_type = (bnnr['results'][0]['media_type'])
							if m_type == "movie":
								m_type = (bnnr['results'][0]['media_type']) + "s"
							else:
								mm_type = m_type
							

							dwn_backdrop = self.pathLoc + "backdrop/{}.jpg".format(title)
							if not os.path.exists(dwn_backdrop):
								url_maze = "http://api.tvmaze.com/singlesearch/shows?q=%s" %quote(title)
								
								mj = json.load(urlopen(url_maze))
								tvdb_id = (mj['externals']['thetvdb'])
								if tvdb_id:
									try:
										
										url_fanart = "https://webservice.fanart.tv/v3/%s/%s?api_key=6d231536dea4318a88cb2520ce89473b" %(m_type, tvdb_id)
										fjs = json.load(urlopen(url_fanart))
										
										if fjs:
											if m_type == "movies":
												mm_type = (bnnr['results'][0]['media_type'])
											else:
												mm_type = m_type
											url_backdrop = (fjs['tvthumb'][0]['url'])
											# open("/tmp/mm_type","w").write("%s" % str(mm_type))
											if url_backdrop:
												dwn_backdrop = self.pathLoc + "backdrop/{}.jpg".format(title)
												urlretrieve(url_backdrop, dwn_backdrop)
									except:
										pass
					except:
						pass

		except:
			pass

# DOWNLOAD INFOS ######################################################################################################

	def infos(self):
		try:
			if os.path.exists("/tmp/events"):
				with open("/tmp/events", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
				for i in xrange(n):
					title = titles[i]
					title = title.strip()

					omdb_apis = ["6a4c9432", "a8834925", "550a7c40", "8ec53e6b"]
					omdb_api = random.sample(omdb_apis, 1)[0]
					url_omdb = 'https://www.omdbapi.com/?apikey=%s&t=%s' %(omdb_api, quote(title))

					try:
						data = json.load(urlopen(url_omdb))

						name = data['Title']
						rtng = data['imdbRating']
						country = data['Country']
						year = data['Year']
						rate = data['Rated']
						genre = data['Genre']
						award = data['Awards']

						info = "Title: %s"%str(name) + "\nImdb: %s"%str(rtng) + "\nYear: %s, %s"%(str(country), str(year.encode('utf-8'))) + "\nRate: %s"%str(rate) + "\nGenre: %s"%str(genre) + "\nAwards: %s" %str(award)
						info_files = self.pathLoc + "infos/{}".format(title)
						if not os.path.exists(info_files):
							open(info_files, "w").write(str(info))
						self['info'].setText(_("info     {}/{}".format(i, n-1)))
					except:
						pass

					
				if os.path.exists("/tmp/events"):
					with open("/tmp/events", "r") as f:
						titles = f.readlines()

					titles = list(dict.fromkeys(titles))
					n = len(titles)
				
					for i in xrange(n):
						title = titles[i]
						title = title.strip()
						srch = "multi"
						url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key=3c3efcf47c3577558812bb9d64019d65&query={}".format(srch, quote(title))
						try:
							org_title = json.load(urlopen(url_tmdb))['results'][0]['original_title']
						except:
							pass
						info_files = self.pathLoc + "infos/{}".format(title)
						if not os.path.exists(info_files):
							open("/tmp/org_title", "a+").write("%s\n"% str(org_title))


				if os.path.exists("/tmp/org_title"):
					with open("/tmp/org_title", "r") as f:
						titles = f.readlines()

					titles = list(dict.fromkeys(titles))
					n = len(titles)
					for i in xrange(n):
						title = titles[i]
						title = title.strip()

						omdb_apis = ["6a4c9432", "a8834925", "550a7c40", "8ec53e6b"]
						omdb_api = random.sample(omdb_apis, 1)[0]
						url_omdb = 'https://www.omdbapi.com/?apikey=%s&t=%s' %(omdb_api, quote(title))

						try:
							data = json.load(urlopen(url_omdb))

							name = data['Title']
							rtng = data['imdbRating']
							country = data['Country']
							year = data['Year']
							rate = data['Rated']
							genre = data['Genre']
							award = data['Awards']

							info = "Title: %s"%str(name) + "\nImdb: %s"%str(rtng) + "\nYear: %s, %s"%(str(country), str(year.encode('utf-8'))) + "\nRate: %s"%str(rate) + "\nGenre: %s"%str(genre) + "\nAwards: %s" %str(award)
							info_files = self.pathLoc + "infos/{}".format(title)
							if not os.path.exists(info_files):
								open(info_files, "w").write(str(info))
							self['info'].setText(_("info+    {}/{}".format(i, n-1)))
						except:
							pass



		except Exception as e:
			print e
			self['info'].setText(_(str(e)))
			
	def ms(self):
		self.session.open(manuelSearch)
		self.timer.start(1000, True)

	def exit(self):
		configfile.save()
		self.close()

class manuelSearch(Screen, ConfigListScreen):
	skin = """
  <screen name="manuelSearch" position="0,0" size="1280,720" title="Manuel Search..." backgroundColor="#ffffff" flags="wfNoBorder">
	<ePixmap position="0,0" size="1280,720" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/bckg.png" transparent="1" />

    <widget source="Title" render="Label" position="40,40" size="745,40" font="Console; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
    <widget name="config" position="40,80" size="745,510" itemHeight="30" font="Regular;24" foregroundColor="#c5c5c5" scrollbarMode="showOnDemand" transparent="1" backgroundColor="#23262e" backgroundColorSelected="#565d6d" foregroundColorSelected="#ffffff" />

    <widget source="key_red" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="40,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_green" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="230,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_yellow" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="420,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <widget source="key_blue" render="Label" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="610,640" size="170,30" halign="left" transparent="1" zPosition="1" />
    <eLabel name="" position="840,575" size="400, 1" backgroundColor="#898989" />
    <eLabel name="" position="840,675" size="400, 1" backgroundColor="#898989" />
  </screen>
  """

	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("SoftCam path configuration"))
		self["key_red"] = StaticText(_("Exit"))
		self["key_green"] = StaticText(_("Ok"))
		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.close,
				"red": self.close,
				"ok": self.manuelSearchWrite,
				"green": self.manuelSearchWrite,
			}, -2)
		configlist = []
		ConfigListScreen.__init__(self, configlist, session=session)
		configlist.append(getConfigListEntry(_("Search Event"), config.plugins.xtraEvent.searchMANUEL))
		configlist.append(getConfigListEntry(_("Year"), config.plugins.xtraEvent.searchMANUELyear))
		self["config"].setList(configlist)


	def manuelSearchWrite(self):
		if os.path.exists("/tmp/events"):
			os.remove("/tmp/events")
		open("/tmp/events","w").write(config.plugins.xtraEvent.searchMANUEL.value)
		if os.path.exists("/tmp/events-year"):
			os.remove("/tmp/events-year")
		open("/tmp/events-year","w").write(str(config.plugins.xtraEvent.searchMANUELyear.value))
		self.close()

class selBouquets(Screen):
	skin = """
	<screen position="center,center" size="1200,600" title="Bouquets..." backgroundColor="#23262e">
		<widget name="list" position="25,25" size="600,500"  scrollbarMode="showOnDemand" backgroundColor="#23262e" />
		<widget name="status" position="750,25" size="500,30" transparent="1" font="Regular;22" foregroundColor="#92f1fc" backgroundColor="#23262e" halign="left" valign="center" />
		<widget name="info" position="750,100" size="500,400" transparent="1" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" halign="left" valign="top" />
		
		<widget name="key_red" position="25,550" zPosition="2" size="150,30" valign="center" halign="left" font="Regular;22" transparent="1" foregroundColor="#c5c5c5" />
		<widget name="key_green" position="250,550" zPosition="2" size="150,30" valign="center" halign="left" font="Regular;22" transparent="1" foregroundColor="#c5c5c5" />
		<eLabel name="new eLabel" position="25,585" size="200,5" backgroundColor="red" zPosition="2" />
		<eLabel name="new eLabel" position="250,585" size="200,5" backgroundColor="green" zPosition="2" />
		<eLabel name="new eLabel" position="700,0" size="2,500" backgroundColor="#898989" zPosition="2" />
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		
		self.bouquets = bqtList()
		self.epgcache = eEPGCache.getInstance()
		#self.setTitle(_("Channel Selection"))
		self.sources = [SelectionEntryComponent(s[0], s[1], 0, (s[0] in ["sources"])) for s in self.bouquets]
		self["list"] = SelectionList(self.sources)

		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"red": self.cancel,
				"green": self.bouquetEpgs,

				"ok": self["list"].toggleSelection,
			}, -2)

		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Save"))
		
		self['status'] = Label()
		self['info'] = Label()

	def bouquetEpgs(self):
		try:
			self.sources = []
			for idx,item in enumerate(self["list"].list):
					item = self["list"].list[idx][0]
					if item[3]:
						self.sources.append(item[0])
			serviceHandler = eServiceCenter.getInstance()
			self.channels = chList(self.sources)

		except Exception as e: 
			print(e)
			self['info'].setText(_(str(e)))
		try:
			if os.path.exists("/tmp/events"):
				os.remove("/tmp/events")
			ref = ""
			refs = self.channels
			for ref in refs:
				try:
					events = self.epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
					n = config.plugins.xtraEvent.searchNUMBER.value
					for i in xrange(n):
						title = events[i][4]
						evntN = re.sub('([\(\[]).*?([\)\]])|(: odc.\d+)|[?|$|.|!|,|:|/]', '', str(title))
						evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").rstrip()
						open("/tmp/events","a+").write("%s\n"% str(evntNm))
						if os.path.exists("/tmp/events"):
							with open("/tmp/events", "r") as f:
								titleNm = f.readlines()
							titleNm = list(dict.fromkeys(titleNm))
							titleNm = len(titleNm)
							self['status'].setText(_("number of events to be scanned : {}".format(titleNm)))
				except:
					pass


		except Exception as e: 
			print(e)
			self['info'].setText(_(str(e)))
		
		
	def cancel(self):
		self.close(self.session, False)
		
		
		
		
		
		
		
		
		
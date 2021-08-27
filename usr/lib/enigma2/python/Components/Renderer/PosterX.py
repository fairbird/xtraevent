# -*- coding: utf-8 -*-
# by digiteng...07.2021, 08.2021(stb lang support)
# © Provided that digiteng rights are protected, all or part of the code can be used, modified...
# russian and py3 support by sunriser...
# downloading in the background while zaping...
#
# for infobar,
# <widget source="session.Event_Now" render="PosterX" position="0,125" size="185,278" path="/media/hdd/poster/" nexts="10" language="en" zPosition="9" />
# for ch,
# <widget source="ServiceEvent" render="PosterX" position="820,100" size="100,150" path="/media/hdd/poster/" zPosition="9" />
# for secondInfobar,
# <widget source="session.Event_Now" render="PosterX" position="20,155" size="100,150" path="/media/hdd/poster/" zPosition="9" />
# <widget source="session.Event_Next" render="PosterX" position="1080,155" size="100,150" path="/media/hdd/poster/" zPosition="9" />
# for epg, event
# <widget source="Event" render="PosterX" position="931,184" size="185,278" path="/media/hdd/poster/" zPosition="9" />

from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eTimer, loadJPG, eEPGCache, getBestPlayableServiceReference
import json, re, os, socket, sys

try:
	from Components.config import config
	lng = config.osd.language.value
except:
	lng = None
	pass

tmdb_api = "3c3efcf47c3577558812bb9d64019d65"
epgcache = eEPGCache.getInstance()

PY3 = (sys.version_info[0] == 3)
try:
	if PY3:
		from urllib.parse import quote, urlencode
		from urllib.request import urlopen, Request
		from _thread import start_new_thread
	else:
		from urllib2 import urlopen, quote
		from thread import start_new_thread
except:
	pass

REGEX = re.compile(
		r'([\(\[]).*?([\)\]])|'
		r'(: odc.\d+)|'
		r'(\d+: odc.\d+)|'
		r'(\d+ odc.\d+)|(:)|'
		r'( -(.*?).*)|(,)|'
		r'!|'
		r'/.*|'
		r'\|\s[0-9]+\+|'
		r'[0-9]+\+|'
		r'\s\d{4}\Z|'
		r'([\(\[\|].*?[\)\]\|])|'
		r'(\"|\"\.|\"\,|\.)\s.+|'
		r'\"|:|'
		r'Премьера\.\s|'
		r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
		r'(х|Х|м|М|т|Т|д|Д)/с\s|'
		r'\s(с|С)(езон|ерия|-н|-я)\s.+|'
		r'\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
		r'\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
		r'\s(ч|ч\.|с\.|с)\s\d{1,3}.+|'
		r'\d{1,3}(-я|-й|\sс-н).+|', re.DOTALL)
		
class PosterX(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.pth = "/tmp/poster/"
		self.lngg = None
		self.sz = "185,278"
		self.nxts = 1
		self.intCheck()
		self.timer = eTimer()
		self.timer.callback.append(self.showPoster)

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if attrib == "path":
				self.pth = value
			if attrib == "language":
				self.lngg = value
			if attrib == "nexts":
				self.nxts = int(value)
			if attrib == "size":
				self.sz = value.split(",")[0]
			attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
		
	def intCheck(self):
		try:
			socket.setdefaulttimeout(1)
			socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
			return True
		except:
			return
			
	GUI_WIDGET = ePixmap
	def changed(self, what):
		if not self.instance:
			return
		if what[0] == self.CHANGED_CLEAR:
			self.instance.hide()
		if what[0] != self.CHANGED_CLEAR:
			self.timer.start(100, True)
			
	def showPoster(self):
		self.instance.hide()
		self.event = self.source.event
		if self.event is None:
			self.instance.hide()
			return
		if self.event:
			evntNm = REGEX.sub('', self.event.getEventName()).strip()
			evntNm = evntNm.replace('\xc2\x86', '').replace('\xc2\x87', '')
			if not os.path.isdir(self.pth):
				os.makedirs(self.pth)
			pstrNm = self.pth + evntNm + ".jpg"
			if os.path.exists(pstrNm):
				self.instance.setPixmap(loadJPG(pstrNm))
				self.instance.setScale(2)
				self.instance.show()
			else:
				start_new_thread(self.downloadPoster, ())
		else:
			self.instance.hide()
			return

	def downloadPoster(self):
		
		events = None
		evntNm = ""
		try:
			import NavigationInstance
			ref = NavigationInstance.instance.getCurrentlyPlayingServiceReference().toString()
			events = epgcache.lookupEvent(['IBDCTESX', (ref, 0, -1, -1)])
		except:
			pass
		try:
			for i in range(self.nxts):
				title = events[i][4]
				evntNm = REGEX.sub('', title).rstrip()
				sd = events[i][6]
				ed = events[i][5]
				fd = "{}\n{}\n{}".format(title, sd, ed)
				srch=None
				year=None
				checkTV = [ "serial", "series", "serie", "serien", "série", "séries", "serious",
				"folge", "episodio", "episode", "épisode", "l'épisode", "ep.", 
				"staffel", "soap", "doku", "tv", "talk", "show", "news", "factual", "entertainment", "telenovela", 
				"dokumentation", "dokutainment", "documentary", "informercial", "information", "sitcom", "reality", 
				"program", "magazine", "mittagsmagazin", "т/с", "м/с", "сезон", "с-н", "эпизод", "сериал", "серия"  ]
				checkMovie = ["film", "movie", "фильм", "кино", "ταινία", "película", "cinéma", "cine", "cinema", "filma"]
				for i in checkMovie:
					if i in fd.lower():
						srch = "movie"
						try:
							if srch == "movie":
								pattern = re.findall('[A-Z].+ 19\d{2}|[A-Z].+ 20\d{2}', fd)
								pattern = re.findall('\d{4}', pattern[0])
								year = pattern[0]
							break
						except:
							pass
				if srch != "movie":
					for i in checkTV:
						if i in fd.lower():
							srch = "tv"
							break
					if srch != "tv":
						srch = "multi"
				evntNm = evntNm.replace('\xc2\x86', '').replace('\xc2\x87', '')
				pstrNm = self.pth + evntNm + ".jpg"
				if not os.path.exists(pstrNm):
					try:
						url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(evntNm))
						if year != None:
							url_tmdb += "&year={}".format(year)
						if self.lngg != None:
							url_tmdb += "&language={}".format(self.lngg)
						elif lng != None:
							url_tmdb += "&language={}".format(lng[:-3])
						else:
							pass
						poster = json.load(urlopen(url_tmdb))['results'][0]['poster_path']
						url_poster = "https://image.tmdb.org/t/p/w{}{}".format(self.sz, poster)
						dwn_poster = self.pth + "{}.jpg".format(evntNm)
						with open(dwn_poster,'wb') as f:
							f.write(urlopen(url_poster).read())
							self.timer.start(10, True)
					except:
						pass
		except:
			pass

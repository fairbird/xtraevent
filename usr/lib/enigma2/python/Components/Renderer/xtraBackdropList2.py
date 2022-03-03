# -*- coding: utf-8 -*-
# by digiteng...11.2021
# for channellist, fhd skin, 300x170 backdrops
# <widget source="ServiceEvent" render="xtraBackdropList2" position="980,113" size="920,863" backgroundColor="background" zPosition="99" transparent="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePoint, eWidget, eLabel, eSize, gFont, ePixmap, loadJPG, eEPGCache
from Components.Converter.xtraEventGenre import getGenreStringSub
from Components.config import config
from skin import parseColor
from time import localtime
import re
import os
import json

try:
	import sys
	if sys.version_info[0] == 3:
		from builtins import str
except:
	pass

NoImage = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film.jpg"
pratePath = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/parental/"

try:
	pathLoc = config.plugins.xtraEvent.loc.value
except:
	pathLoc = ""
	
REGEX = re.compile(
		r'([\(\[]).*?([\)\]])|'
		r'(: odc.\d+)|'
		r'(\d+: odc.\d+)|'
		r'(\d+ odc.\d+)|(:)|'
		
		r'!|'
		r'/.*|'
		r'\|\s[0-9]+\+|'
		r'[0-9]+\+|'
		r'\s\d{4}\Z|'
		r'([\(\[\|].*?[\)\]\|])|'
		r'(\"|\"\.|\"\,|\.)\s.+|'
		r'\"|:|'
		r'\*|'
		r'Премьера\.\s|'
		r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
		r'(х|Х|м|М|т|Т|д|Д)/с\s|'
		r'\s(с|С)(езон|ерия|-н|-я)\s.+|'
		r'\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
		r'\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
		r'\s(ч|ч\.|с\.|с)\s\d{1,3}.+|'
		r'\d{1,3}(-я|-й|\sс-н).+|', re.DOTALL)

class xtraBackdropList2(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.epgcache = eEPGCache.getInstance()
		self.fontSizeNow = 24
		self.fontSizeNexts = 20
		
	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'position':
				self.px = int(value.split(',')[0])
				self.py = int(value.split(',')[1])
			elif attrib == 'size':
				self.szX = int(value.split(',')[0])
				self.szY = int(value.split(',')[1])
			elif attrib == 'backgroundColor':
				self.backgroundColor = value
			elif attrib == 'fontSizeNow':
				self.fontSizeNow = int(value)
			elif attrib == 'fontSizeNexts':
				self.fontSizeNexts = int(value)
				
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, screen)

	GUI_WIDGET = eWidget
	def changed(self, what):
		if not self.instance:
			return
		else:
			if what[0] != self.CHANGED_CLEAR:
				
				evnt = ''
				pstrNm = ''
				evntNm = ''
				service = ''
				event = None
				fd = ''
				ed = ''
				desc = ''
				rtd = ''
				imdbRtng = ''
				imdbRating = ''
				events = None
				rate = ''
				prate = ''
				service = self.source.service
				event = self.source.event
				if event:
					self.instance.show()
					evnt = event.getEventName()
					evntNm = REGEX.sub('', evnt).strip()
					rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
					if os.path.exists(rating_json):
						with open(rating_json) as f:
							read_json = json.load(f)
					fd = "{}\n{}\n{}".format(event.getEventName(), event.getShortDescription(), event.getExtendedDescription())
					ed = event.getExtendedDescription()

					try:
						prate = read_json["Rated"]
						if prate != "Not Rated":
							rtd = prate
						elif prate == "Not Rated":
							parentName = ''
							prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
							for i in prs:
								prr = re.search(i, fd)
								if prr:
									parentName = prr.group(1)
									parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
									rtd = parentName
									break
						else:
							try:
								age = ''
								rating = event.getParentalData()
								if rating:
									age = rating.getRating()
									rtd = age
							except:
								pass
					except:
						parentName = ''
						prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
						for i in prs:
							prr = re.search(i, fd)
							if prr:
								parentName = prr.group(1)
								parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
								rtd = parentName
								break
					if prate == "TV-Y7":
						rate = "6"
					elif prate == "TV-Y":
						rate = "6"
					elif prate == "TV-14":
						rate = "12"
					elif prate == "TV-PG":
						rate = "16"
					elif prate == "TV-G":
						rate = "0"
					elif prate == "TV-MA":
						rate = "18"
					elif prate == "PG-13":
						rate = "16"
					elif prate == "R":
						rate = "18"
					elif prate == "G":
						rate = "0"
					else:
						pass
					if rate:	
						rtd = str(rate)
					if rtd:
						rateNm = "{}FSK_{}.png".format(pratePath, rtd)
						self.parentPxmp.setPixmapFromFile(rateNm)
						self.parentPxmp.resize(eSize(60, 60))
						self.parentPxmp.move(ePoint(240, 110))
						self.parentPxmp.setZPosition(10)
						self.parentPxmp.setAlphatest(2)
						self.parentPxmp.setScale(1)
						self.parentPxmp.show()
					else:
						self.parentPxmp.hide()
					try:
						Plot = read_json["Plot"]
						if Plot:
							desc = str(Plot)
						else:
							desc = str(fd)
					except:
						desc = str(fd)
					description =	'\\c0000????Description : \\c00??????{}\n\n'.format((desc))
					description = "\n".join(["-"*100, description, "-"*100])
					events = self.epgcache.lookupEvent(['IBDCT', (service.toString(), 0, -1, 480)])
					if self.epgcache is not None and events:
						try:
							# event 0
							evnt = events[0][4]
							evntNm = REGEX.sub('', evnt).strip()
							bt = localtime(events[0][1])
							evntNm0 = "%02d:%02d - %s\n%s"%(bt[3], bt[4], evnt, self.info())
							pstrNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
							if os.path.exists(pstrNm):
								self.eventPxmp0.setPixmap(loadJPG(pstrNm))
								self.eventPxmp0.resize(eSize(300, 170))
								self.eventPxmp0.move(ePoint(0,0))
								self.eventPxmp0.setTransparent(0)
								self.eventPxmp0.setZPosition(9)
								self.eventPxmp0.setScale(1)
								self.eventPxmp0.show()
							else:
								self.eventPxmp0.setPixmap(loadJPG(NoImage))
								self.eventName0.hide()
							self.eventName0.setText(str(evntNm0))
							self.eventName0.setBackgroundColor(parseColor(self.backgroundColor))
							self.eventName0.resize(eSize(600,170))
							self.eventName0.move(ePoint(310,0))
							self.eventName0.setFont(gFont("Regular", self.fontSizeNow))
							self.eventName0.setHAlign(eLabel.alignLeft)
							self.eventName0.show()
						except:
							self.eventPxmp0.hide()
							self.eventName0.hide()
						try:
							self.eventDesc.setText(description)
							self.eventDesc.setBackgroundColor(parseColor(self.backgroundColor))
							self.eventDesc.resize(eSize(900, 400))
							self.eventDesc.move(ePoint(0, 180))
							self.eventDesc.setFont(gFont("Regular", self.fontSizeNow))
							self.eventDesc.setHAlign(eLabel.alignLeft)
							self.eventDesc.setVAlign(eLabel.alignCenter)
							self.eventDesc.show()
						except:
							self.eventPxmp0.hide()
							self.eventName0.hide()
						try:
							# event 1
							evnt = events[1][4]
							evntNm = REGEX.sub('', evnt).strip()
							bt = localtime(events[1][1])
							evntNm1 = "%02d:%02d - %s\n"%(bt[3], bt[4], evnt)
							pstrNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
							if os.path.exists(pstrNm):
								self.eventPxmp1.setPixmap(loadJPG(pstrNm))
								self.eventPxmp1.resize(eSize(300, 170))
								self.eventPxmp1.move(ePoint(0, 630))
								self.eventPxmp1.setTransparent(0)
								self.eventPxmp1.setZPosition(9)
								self.eventPxmp1.setScale(1)
								self.eventPxmp1.show()
							else:
								self.eventPxmp1.setPixmap(loadJPG(NoImage))
								self.eventName1.hide()
							self.eventName1.setText(str(evntNm1))
							self.eventName1.setBackgroundColor(parseColor(self.backgroundColor))
							self.eventName1.resize(eSize(300, 60))
							self.eventName1.move(ePoint(0, 810))
							self.eventName1.setFont(gFont("Regular", self.fontSizeNexts))
							self.eventName1.setHAlign(eLabel.alignLeft)
							self.eventName1.show()
						except:
							self.eventPxmp1.hide()
							self.eventName1.hide()
						try:
							# event 2
							evnt = events[2][4]
							evntNm = REGEX.sub('', evnt).strip()
							bt = localtime(events[2][1])
							evntNm2 = "%02d:%02d - %s\n"%(bt[3], bt[4], evnt)
							pstrNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
							if os.path.exists(pstrNm):
								self.eventPxmp2.setPixmap(loadJPG(pstrNm))
								self.eventPxmp2.resize(eSize(300, 170))
								self.eventPxmp2.move(ePoint(310, 630))
								self.eventPxmp2.setTransparent(0)
								self.eventPxmp2.setZPosition(3)
								self.eventPxmp2.setScale(1)
								self.eventPxmp2.show()
							else:
								self.eventPxmp2.setPixmap(loadJPG(NoImage))
								self.eventName2.hide()
							self.eventName2.setText(str(evntNm2))
							self.eventName2.setBackgroundColor(parseColor(self.backgroundColor))
							self.eventName2.resize(eSize(300, 60))
							self.eventName2.move(ePoint(310, 810))
							self.eventName2.setFont(gFont("Regular", self.fontSizeNexts))
							self.eventName2.setHAlign(eLabel.alignLeft)
							self.eventName2.show()
						except:
							self.eventPxmp2.hide()
							self.eventName2.hide()
						try:
							# event 3
							evnt = events[3][4]
							evntNm = REGEX.sub('', evnt).strip()
							bt = localtime(events[3][1])
							evntNm3 = "%02d:%02d - %s\n"%(bt[3], bt[4], evnt)
							pstrNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
							if os.path.exists(pstrNm):
								self.eventPxmp3.setPixmap(loadJPG(pstrNm))
								self.eventPxmp3.resize(eSize(300, 170))
								self.eventPxmp3.move(ePoint(620, 630))
								self.eventPxmp3.setTransparent(0)
								self.eventPxmp3.setZPosition(3)
								self.eventPxmp3.setScale(1)
								self.eventPxmp3.show()
							else:
								self.eventPxmp3.setPixmap(loadJPG(NoImage))
								self.eventName3.hide()
							self.eventName3.setText(str(evntNm3))
							self.eventName3.setBackgroundColor(parseColor(self.backgroundColor))
							self.eventName3.resize(eSize(300, 60))
							self.eventName3.move(ePoint(620, 810))
							self.eventName3.setFont(gFont("Regular", self.fontSizeNexts))
							self.eventName3.setHAlign(eLabel.alignLeft)
							self.eventName3.show()
						except:
							self.eventPxmp3.hide()
							self.eventName3.hide()
					else:
						self.eventPxmp1.hide()
						self.eventPxmp2.hide()
						self.eventPxmp3.hide()
						self.eventName1.hide()
						self.eventName2.hide()
						self.eventName3.hide()
						self.eventDesc.hide()
				else:
					self.instance.hide()
			else:
				self.instance.hide()

	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.eventDesc = eLabel(self.instance)
		self.eventName0 = eLabel(self.instance)
		self.eventName1 = eLabel(self.instance)
		self.eventName2 = eLabel(self.instance)
		self.eventName3 = eLabel(self.instance)
		self.eventPxmp0 = ePixmap(self.instance)
		self.eventPxmp1 = ePixmap(self.instance)
		self.eventPxmp2 = ePixmap(self.instance)
		self.eventPxmp3 = ePixmap(self.instance)
		self.parentPxmp = ePixmap(self.instance)

	def info(self):
		event = ""
		tc = ""
		try:
			event = self.source.event
			if event:
				evnt = event.getEventName()
				evntNm = REGEX.sub('', evnt).strip()
				rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
				fd = "{}\n{}\n{}".format(event.getEventName(), event.getShortDescription(), event.getExtendedDescription())
				if os.path.exists(rating_json):
					with open(rating_json) as f:
						read_json = json.load(f)
				evnt = []
				try:
					year = ''
					fd = fd.replace(',', '').replace('(', '').replace(')', '')
					fdl = ['\d{4} [A-Z]+', '[A-Z]+ \d{4}', '[A-Z][a-z]+\s\d{4}', '\+\d+\s\d{4}']
					for i in fdl:
						year = re.findall(i, fd)
						if year:
							year = re.sub(r'\(.*?\)|\.|\+\d+', ' ', year[0]).strip()
							evnt.append("Year : {}".format(year))
							break
				except:
					year = read_json["Year"]
					if year:
						evnt.append("Year : {}".format(year))
				try:
					imdbRating = read_json["imdbRating"]
					if imdbRating:
						evnt.append("IMDB : {}".format(imdbRating))
				except:
					pass
				try:
					Rated = read_json["Rated"]
					if Rated != "Not Rated":
						evnt.append("Rated : {}+".format(Rated))
					elif Rated == "Not Rated":
						parentName = ''
						prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
						for i in prs:
							prr = re.search(i, fd)
							if prr:
								parentName = prr.group(1)
								parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
								evnt.append("Rated : {}+".format(parentName))
								break
					else:
						try:
							age = ''
							rating = event.getParentalData()
							if rating:
								age = rating.getRating()
								evnt.append("Rated : {}+".format(age))
						except:
							pass
				except:
					parentName = ''
					prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
					for i in prs:
						prr = re.search(i, fd)
						if prr:
							parentName = prr.group(1)
							parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
							evnt.append("Rated : {}+".format(parentName))
							break
				try:
					Genre = read_json["Genre"]
					if Genre:
						evnt.append("Genre : {}".format(Genre))
				except:
					genres = event.getGenreDataList()
					if genres:
						genre = genres[0]
						evnt.append("Genre : {}".format(getGenreStringSub(genre[0], genre[1])))
				tc = "\n".join(evnt)
				return tc
			else:
				return tc
		except:
			pass

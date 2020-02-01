# -*- coding: utf-8 -*-
# by digiteng...01.2020

from Converter import Converter
from Components.Element import cached
import json
import re
import os
import urllib2

api = 'b1538d0b'

class Rtng(Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getValue(self):
		event = self.source.event
		if event:
			evnt = event.getEventName()
			if self.type == 'STARS':
				try:
					p = ['((.*?)).\(.*?(.*?)\)', '((.*?))[:-].*?(.*?)']
					for i in p:
						e1 = re.search(i, evnt)
						if e1:
							jr = e1.group(1)
							ffilm = re.sub('\s+', '+', jr)
						else:
							ffilm = re.sub('\s+', '+', evnt)
					year = self.yearPr(event)
					if year != "":
						yr = self.yearPr(event)

					url = 'http://www.omdbapi.com/?apikey=%s&t=%s&y=%s&' %(api, ffilm, yr)
					js = json.load(urllib2.urlopen(url))
					rtng = (js['imdbRating'])
					if rtng:
						return int(10*(float(rtng)))
					else:
						pass
				except:
					pass
		else:
			pass

	value = property(getValue)
	range = 100

	@cached
	def getText(self):
		event = self.source.event
		if event:
			evnt = event.getEventName()
			if self.type == 'RATING':
				try:
					p = ['((.*?)).\(.*?(.*?)\)', '((.*?))[:-].*?(.*?)']
					for i in p:
						e1 = re.search(i, evnt)
						if e1:
							jr = e1.group(1)
							ffilm = re.sub('\s+', '+', jr)
						else:
							ffilm = re.sub('\s+', '+', evnt)
					year = self.yearPr(event)
					if year != "":
						yr = self.yearPr(event)

					url = 'http://www.omdbapi.com/?apikey=%s&t=%s&y=%s&' %(api, ffilm, yr)
					open("/tmp/url.txt", "w").write(url)
					js = json.load(urllib2.urlopen(url))
					rtng = (js['imdbRating'])
					if rtng:
						return "imdb : %s" %(str(rtng))
					else:
						pass
				except:
					pass
		else:
			pass
	text = property(getText)

	def yearPr(self, event):
		fd = event.getShortDescription() + "\n" + event.getExtendedDescription()
		#open("/tmp/evnt.txt", "w").write(fd)
		pattern = [".*[A-Z][A-Z]*\s(\d+)+", "\([+][0-9]+\)\s((\d+)(\d+)+)"]
		for i in pattern:
			yr = re.search(i, fd)
			if yr:
				jr = yr.group(1)
				return "%s"%jr
		return ""

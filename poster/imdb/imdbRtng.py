# -*- coding: utf-8 -*-
# by digiteng...01.2020

from Components.Converter.Converter import Converter
from Components.Element import cached
import json
import re
import os
import urllib2

api = 'b1538d0b'

class imdbRtng(Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getValue(self):
		try:
			event = self.source.event
			if event:
				evnt = event.getEventName()
				if self.type == 'STARS':
					try:
						try:
							p = '((.*?))[;=:-].*?(.*?)'
							e1 = re.search(p, evnt)
							ffilm = e1.group(1)
						except:
							w = re.sub("([\(\[]).*?([\)\]])", " ", evnt)
							ffilm = re.sub('\W+','+', w)

						year = self.yearPr(event)
						if year != "":
							yr = self.yearPr(event)

						url = 'https://www.omdbapi.com/?apikey=%s&t=%s&y=%s&' %(api, ffilm, yr)
						js = json.load(urllib2.urlopen(url))
						open("/tmp/url.txt", "w").write(url)
						rtng = (js['imdbRating'])
						if rtng:
							return int(10*(float(rtng)))

					except:
						try:
							url = 'https://www.omdbapi.com/?apikey=%s&t=%s&' %(api, ffilm)
							print url
							js = json.load(urllib2.urlopen(url))
							rtng = (js['imdbRating'])
							if rtng:
								return int(10*(float(rtng)))
						except:
							pass
			else:
				pass

		except:
			pass

	value = property(getValue)
	range = 100

	@cached
	def getText(self):
		try:
			event = self.source.event
			if event is None:
				return ""
			if not event is None:
				if self.type == "RATING":
					evnt = event.getEventName()
					try:
						try:
							p = '((.*?))[;=:-].*?(.*?)'
							e1 = re.search(p, evnt)
							ffilm = e1.group(1)
						except:
							w = re.sub("([\(\[]).*?([\)\]])", " ", evnt)
							ffilm = re.sub('\W+','+', w)

						year = self.yearPr(event)
						if year != "":
							yr = self.yearPr(event)

						url = 'https://www.omdbapi.com/?apikey=%s&t=%s&y=%s&' %(api, ffilm, yr)
						js = json.load(urllib2.urlopen(url))
						
						rtng = (js['imdbRating'])
						if rtng:
							return "imdb : %s" %(str(rtng))
						else:
							return "imdb : N/A"

					except:
						try:
							url = 'https://www.omdbapi.com/?apikey=%s&t=%s&' %(api, ffilm)
							print url
							js = json.load(urllib2.urlopen(url))
							#open("/tmp/url.txt", "w").write(str(js)+"\n\n"+url)
							rtng = (js['imdbRating'])
							if rtng:
								return "imdb : %s" %(str(rtng))
						except:
							pass
			else:
				return ""
		except:
			pass

	text = property(getText)

	def yearPr(self, event):
		fd = event.getShortDescription() + "\n" + event.getExtendedDescription()
		pattern = [".*[A-Z][A-Z]*\s(\d+)+", "\([+][0-9]+\)\s((\d+)(\d+)+)"]
		for i in pattern:
			yr = re.search(i, fd)
			if yr:
				jr = yr.group(1)
				return "%s"%jr
		return ""

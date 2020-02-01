# -*- coding: utf-8 -*-
# by digiteng...01.2020

from Components.Converter.Converter import Converter
from Components.Element import cached
import json
import re
import os
import urllib2

api = 'your api key'

class omdbImdbRtng(Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getText(self):
		event = self.source.event
		if event is None:
			return ""
		if not event is None:
			if self.type == "RATING":
				evnt = event.getEventName()
				try:
					p = '((.*?)).\(.*?(.*?)\)'
					e1 = re.search(p, evnt)
					if e1:
						jr = e1.group(1)
						ffilm = re.sub('\s+', '+', jr)
					else:
						ffilm = re.sub('\s+', '+', evnt)
					url = 'https://www.omdbapi.com/?t=%s&apikey=%s' %(ffilm, api)
					jjj = json.load(urllib2.urlopen(url))
					rtng = (jjj['imdbRating'])
					if rtng:
						return "imdb : %s" %(str(rtng))
				except:
					pass
		else:
			return ""

	text = property(getText)

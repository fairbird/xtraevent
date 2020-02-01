# -*- coding: utf-8 -*-
# by digiteng...01.2020

from Converter import Converter
from Components.Element import cached
import json
import re
import os
import urllib2

api = 'b1538d0b'

class ImdbRtngStar(Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getValue(self):
		event = self.source.event
		if event:
			evnt = event.getEventName()
			if self.type == 'Progress':
				try:
					p = '((.*?)).\(.*?(.*?)\)'
					e1 = re.search(p, evnt)
					if e1:
						jr = e1.group(1)
						ffilm = re.sub('\s+', '+', jr)
					else:
						ffilm = re.sub('\s+', '+', evnt)
					url = 'https://www.omdbapi.com/?t=%s&apikey=%s' %(ffilm, api)
					js = json.load(urllib2.urlopen(url))
					rtng = (js['imdbRating'])
					if rtng:
						return int(10*(float(rtng)))

				except:
					pass

		else:
			return ""

	value = property(getValue)
	range = 100

# -*- coding: utf-8 -*-
# by digiteng...01.2020

from Components.Converter.Converter import Converter
from Components.Element import cached
import re
import urllib2

class oscoboImdbRating(Converter, object):

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
					url = 'https://www.oscobo.com/search.php?q=%s+imdb+rating' % ffilm
					req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
					resp = urllib2.urlopen(req).read(15000)
					p = '(</b> (.*?)) ((\d+)\.(\d+))'
					parse = re.search(p,str(resp))
					return "IMDB : %s" %(parse.group(3))
				except:
					pass
		else:
			return ""

	text = property(getText)

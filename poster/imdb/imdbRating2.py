# -*- coding: utf-8 -*-
# by digiteng...01-2020

from Components.Converter.Converter import Converter
from Components.Element import cached
import urllib2
import re
from urllib import quote

class imdbRating2(Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getText(self):
		event = self.source.event
		if event is None:
			return ''

		if not event is None:
			if self.type == 'RATING':
				evnt = event.getEventName()
				try:
					#find
					url_find = 'https://m.imdb.com/find?q=%s'% quote(evnt)
					ff = urllib2.urlopen(urllib2.Request(url_find)).read(100000)
					fe = str(ff[80000:100000])
					rc = re.compile('<a href="/title/(.*?)/"', re.DOTALL)
					rs = rc.search(fe)
					id = rs.group(1)
					#title
					url_title = 'https://m.imdb.com/title/%s'%id
					tt = urllib2.urlopen(urllib2.Request(url_title)).read(10000)
					#we = str(tt[4000:10000])
					#rating
					rct = re.compile('"ratingValue": "(.*?)"', re.DOTALL)
					rst = rct.search(str(tt))
					return "imdb : %s" %(rst.group(1))
				except:
					pass
		else:
			pass
	text = property(getText)

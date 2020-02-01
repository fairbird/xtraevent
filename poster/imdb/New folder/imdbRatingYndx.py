# -*- coding: utf-8 -*-
# by digiteng...01-2020

from Components.Converter.Converter import Converter
from Components.Element import cached
import urllib2
import re
from urllib import pathname2url

class imdbRatingYndx(Converter, object):

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
				#ff = re.sub('\s+', '+', evnt)
				film = pathname2url(evnt)
				try:
					url = 'https://m.yandex.com/search/?lr=11511&text=%s+imdb+rating' % film
					req = urllib2.Request(url)
					resp = urllib2.urlopen(req).read()
					p = 'class="rating__value rating__value_bold_yes">(.*?)</span>'
					parse = re.search(p, resp)
					return "IMDB : " + parse.group(1)
				except:
					url = 'https://m.yandex.com/search/?lr=11511&text=%s+imdb+bewertung' % film
					req = urllib2.Request(url)
					resp = urllib2.urlopen(req).read()
					p = 'class="rating__value rating__value_bold_yes">(.*?)</span>'
					parse = re.search(p, resp)
					return "IMDB : " + parse.group(1)
				else:
					pass
		else:
			pass
	text = property(getText)
	
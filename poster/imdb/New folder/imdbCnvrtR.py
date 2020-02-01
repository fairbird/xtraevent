# -*- coding: utf-8 -*-
# by digiteng...12-2019

from Components.Converter.Converter import Converter
from Components.Element import cached
import urllib2
import re

class imdbCnvrtR(Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getText(self):
		event = self.source.event
		if event is None:
			return ""

		if not event is None:
			if self.type == "imdbRating":
				evnt = event.getEventName()
				film = re.sub('\s+', '+', evnt)
				try:
					url = 'https://www.oscobo.com/search.php?q=%s+imdb' % film
					req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
					resp = urllib2.urlopen(req)
					respData = resp.read()
					p = 'https://www.imdb.com/title/(.*?)</div>'
					parse = re.search(p,str(respData))
					id = parse.group(1)
					
					f = open("/media/hdd/data.tsv", "r")
					m = f.readlines()
					f.close()
					for i in m:
						m = i.split()
						if m[0] == id:
							mtotal = str(m[1])
							mtotal = ("%s") % mtotal 
							
							return mtotal
				except:
					pass
		else:
			pass
	text = property(getText)
	

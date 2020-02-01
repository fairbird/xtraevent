# -*- coding: utf-8 -*-
# by digiteng...01.2020

from Components.Converter.Converter import Converter
from Components.Element import cached
import json
import re
import os
import urllib2

api = 'your api key'

class omdbImdbRtngPlus(Converter, object):

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
					#open("/tmp/url.txt","w").write(url)
					jjj = json.load(urllib2.urlopen(url))
					rtng = (jjj['imdbRating'])
					#open("/tmp/rtng.txt","w").write(rtng)
					if rtng:
						return "imdb : %s" %(str(rtng))
						os.system("echo 1 > /proc/sys/vm/drop_caches")
				except:
					try:
						url = 'https://www.oscobo.com/search.php?q=%s+imdb' % ffilm
						req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
						resp = urllib2.urlopen(req).read(5000)
						p = 'https://www.imdb.com/title/(.*?)</div>'
						parse = re.search(p,str(resp))
						id = parse.group(1)
						url = 'https://www.omdbapi.com/?i=%s&apikey=%s' %(id, api)
						jjj = json.load(urllib2.urlopen(url))
						jj = (jjj['imdbRating'])
						if jj:
							return "imdb : %s" %(str(jj))
							os.system("echo 1 > /proc/sys/vm/drop_caches")
					except:
						pass
				finally:
					os.system("echo 1 > /proc/sys/vm/drop_caches")
					pass
		else:
			return ""

	text = property(getText)

# -*- coding: utf-8 -*-
# by digiteng...01.2020

from Components.Converter.Converter import Converter
from Components.Element import cached
import json
import re
import os
import urllib2
from urllib import quote

class tmdbRtng(Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	def sessionEpisode(self, event):
		fd = event.getShortDescription() + "\n" + event.getExtendedDescription()
		pattern = ["(\d+). Staffel, Folge (\d+)", "T(\d+) Ep.(\d+)", "'Episodio (\d+)' T(\d+)"]
		for i in pattern:
			seg = re.search(i, fd)
			if seg:
				if re.search("Episodio",i):
					return "S"+seg.group(2).zfill(2)+"E"+seg.group(1).zfill(2)
				else :
					return "S"+seg.group(1).zfill(2)+"E"+seg.group(2).zfill(2)
		return ""

	@cached
	def getText(self):
		event = self.source.event
		if event is None:
			return ""
		
		if not event is None:
			if self.type == "RATING":
				self.evnt = event.getEventName()
				try:
					p = '((.*?)).\(.*?(.*?)\)'
					e1 = re.search(p,self.evnt)
					if e1:
						jr = e1.group(1)
						self.evntNm = quote(jr)
					else:
						self.evntNm = quote(self.evnt)
					ses_ep = self.sessionEpisode(event)
					if ses_ep != "" and len(ses_ep) > 0:
						self.srch = "tv"
					else:
						self.srch = "multi"

					url_json = "https://api.themoviedb.org/3/search/%s?api_key=3c3efcf47c3577558812bb9d64019d65&query=%s"%(self.srch, self.evntNm)
					jp = json.load(urllib2.urlopen(url_json))
					rtng = (jp['results'][0]['vote_average'])
					if rtng:
						return "tmdb : %s" %(str(rtng))
				except:
					pass
		else:
			return ""
	
	text = property(getText)


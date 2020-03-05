# -*- coding: utf-8 -*-
# by digiteng...03.2020
# <widget source="session.Event_Now" render="banner" position="0,0" size="762,141" zPosition="1" />
from Renderer import Renderer
from enigma import ePixmap, ePicLoad
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap
import json
import re
import os
import urllib2

if os.path.isdir("/media/hdd"):
	path_folder = "/media/hdd/banner/"
else:
	path_folder = "/media/usb/banner/"

try:
	folder_size=sum([sum(map(lambda fname: os.path.getsize(os.path.join(path_folder, fname)), files)) for path_folder, folders, files in os.walk(path_folder)])
	banners_sz = "%0.f" % (folder_size/(1024*1024.0))
	if banners_sz >= "10":    # folder remove size(10MB)...
		import shutil
		shutil.rmtree(path_folder)
except:
	pass

class banner(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.bannerName = ''

	GUI_WIDGET = ePixmap
	def changed(self, what):
		try:
			if not self.instance:
				return
			event = self.source.event
			if what[0] == self.CHANGED_CLEAR:
				self.instance.hide()
			if what[0] != self.CHANGED_CLEAR:
				if event:
					evnt = event.getEventName()
					try:
						e1 = re.search('((.*?))[;=!/(:-].*?(.*?)', evnt)
						jr = e1.group(1)
						evntNm = jr
					except:
						evntNm = evnt
					self.dwn_banner = path_folder + "%s_banner.jpg" %(evntNm)
					bannerName = path_folder + evntNm + "_banner.jpg"
					self.evntNm = urllib2.quote(evntNm)
					if os.path.exists(bannerName):
						try:
							size = self.instance.size()
							self.picload = ePicLoad()
							sc = AVSwitch().getFramebufferScale()
							if self.picload:
								self.picload.setPara((size.width(),
								size.height(),
								sc[0],
								sc[1],
								False,
								1,
								'#00000000'))
							result = self.picload.startDecode(bannerName, 0, 0, False)
							if result == 0:
								ptr = self.picload.getData()
								if ptr != None:
									self.instance.setPixmap(ptr)
									self.instance.show()
						except:
							self.instance.hide()
					else:
						self.downloadBanner()
						self.instance.hide()
				else:
					self.instance.hide()
		except:
			pass

	def downloadBanner(self):
		if not os.path.isdir(path_folder):
			os.makedirs(path_folder)
		try:
			url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname=%s" %(self.evntNm)
			url_read = urllib2.urlopen(url_tvdb).read()			
			series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read, re.I)[0]
			if series_id:
				self.url_banner = "https://artworks.thetvdb.com/banners/graphical/%s-g_t.jpg" %(series_id)
				if self.url_banner:
					self.saveBanner()
		except:
			try:
				url_series = "https://thetvdb.com/api/API/series/%s" %(series_id)
				url_read = urllib2.urlopen(url_series).read()
				banner_img = re.findall('<banner>(.*?)</banner>', url_read, re.I)[0]
				if banner_img:
					self.url_banner = "https://www.thetvdb.com/banners/%s" %(banner_img)
					self.saveBanner()
				else:
					try:
						url_json = "https://api.themoviedb.org/3/search/multi?api_key=3c3efcf47c3577558812bb9d64019d65&query=%s" %(self.evntNm)
						jp = json.load(urllib2.urlopen(url_json))
						tmdb_id = (jp['results'][0]['id'])
						if tmdb_id:
							m_type = (jp['results'][0]['media_type'])
							if m_type == "movie":
								m_type = (jp['results'][0]['media_type']) + "s"
							else:
								mm_type = m_type
							url_fanart = "https://webservice.fanart.tv/v3/%s/%s?api_key=6d231536dea4318a88cb2520ce89473b" %(m_type, tmdb_id)
							fjs = json.load(urllib2.urlopen(url_fanart))
							if fjs:
								if m_type == "movies":
									mm_type = (jp['results'][0]['media_type'])
								self.url_banner = (fjs[mm_type+'banner'][0]['url'])
								if self.url_banner:
									self.saveBanner()
					except:
						try:
							url_maze = "http://api.tvmaze.com/singlesearch/shows?q=%s" %(self.evntNm)
							mj = json.load(urllib2.urlopen(url_maze))
							poster = (mj['externals']['thetvdb'])
							if poster:
								url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname=%s" %(poster)
								url_read = urllib2.urlopen(url_tvdb).read()
								series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read, re.I)[0]
								banner_img = re.findall('<banner>(.*?)</banner>', url_read, re.I)[0]
								if banner_img:
									self.url_banner = "https://artworks.thetvdb.com%s" %(banner_img)
									self.saveBanner()
								if series_id:
									try:
										url_fanart = "https://webservice.fanart.tv/v3/%s/%s?api_key=6d231536dea4318a88cb2520ce89473b" %(m_type, series_id)
										fjs = json.load(urllib2.urlopen(url_fanart))
										if fjs:
											if m_type == "movies":
												mm_type = (jp['results'][0]['media_type'])
											else:
												mm_type = m_type
											self.url_banner = (fjs[mm_type+'banner'][0]['url'])

											if self.url_banner:
												self.saveBanner()
									except:
										pass
						except:
							pass
			except:
				pass

	def saveBanner(self):
		with open(self.dwn_banner,'wb') as f:
			f.write(urllib2.urlopen(self.url_banner).read())
			f.close()

# -*- coding: utf-8 -*-
# by digiteng...06.2020
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from urllib import urlretrieve
from urllib2 import urlopen, quote
import requests
from twisted.web.client import downloadPage
from enigma import eTimer, getDesktop, eLabel, eServiceCenter, eServiceReference, iServiceInformation, eEPGCache
from Components.config import config
from Components.ConfigList import ConfigListScreen
from ServiceReference import ServiceReference
from Components.Sources.CurrentService import CurrentService
from Components.Sources.ServiceList import ServiceList
from PIL import Image
# from Tools.Downloader import downloadWithProgress
from Screens.MessageBox import MessageBox
from Tools import Notifications
import socket
import os
import re
import json
import random
import xtra

tmdb_api = "3c3efcf47c3577558812bb9d64019d65"
epgcache = eEPGCache.getInstance()


if config.plugins.xtraEvent.locations.value == "hdd":
	pathLoc = "/media/hdd/xtraEvent/"
elif config.plugins.xtraEvent.locations.value == "usb":
	pathLoc = "/media/usb/xtraEvent/"
elif config.plugins.xtraEvent.locations.value == "internal":
	pathLoc = "/etc/enigma2/xtraEvent/"
else:
	pathLoc = "/tmp/"

# pathLoc = "/etc/enigma2/xtraEvent/"
# open("/tmp/path","w").write(pathLoc)

def save():
	if config.plugins.xtraEvent.searchMOD.value == "Current Channel":
		currentChEpgs()
	if config.plugins.xtraEvent.searchMOD.value == "Bouquets":
		selBouquets()

def currentChEpgs():
	if os.path.exists(pathLoc + "events"):
		os.remove(pathLoc + "events")
	try:
		events = None
		import NavigationInstance
		ref = NavigationInstance.instance.getCurrentlyPlayingServiceReference().toString()
		try:
			
			events = epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
			n = config.plugins.xtraEvent.searchNUMBER.value

			for i in xrange(int(n)):
				title = events[i][4]
				evntN = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", title)
				evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").replace("LOS ", "The ").rstrip()
				open(pathLoc + "events", "a+").write("%s\n" %str(evntNm))

			intCheck()
			download()
		except:
			pass

	except:
		pass

def selBouquets():
	if os.path.exists(pathLoc + "events"):
		os.remove(pathLoc + "events")
		
	if os.path.exists(pathLoc + "bqts"):
		with open(pathLoc + "bqts", "r") as f:
			refs = f.readlines()
		
		nl=len(refs)
		for i in xrange(nl):
			ref = refs[i]
			try:
				events = epgcache.lookupEvent(['IBDCTSERNX', (ref, 1, -1, -1)])
				n = config.plugins.xtraEvent.searchNUMBER.value
				for ii in xrange(int(n)):
					title = events[ii][4]
					evntN = re.sub('([\(\[]).*?([\)\]])|(: odc.\d+)|[?|$|.|!|,|:|/]', '', str(title))
					evntNm = evntN.replace("Die ", "The ").replace("Das ", "The ").replace("und ", "and ").rstrip()
					open(pathLoc + "events", "a+").write("%s\n" %str(evntNm))
				
			except:
				pass		
		intCheck()
		download()


def intCheck():
	try:
		socket.setdefaulttimeout(0.5)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
		return True
	except:
		return False

def download():
	try:
		if intCheck():
			if config.plugins.xtraEvent.poster.value == True:
				if config.plugins.xtraEvent.tmdb.value == True:
					tmdb_Poster()
				if config.plugins.xtraEvent.tvdb.value == True:
					tvdb_Poster()
				if config.plugins.xtraEvent.omdb.value == True:
					omdb_Poster()
				if config.plugins.xtraEvent.maze.value == True:
					maze_Poster()
				if config.plugins.xtraEvent.fanart.value == True:
					fanart_Poster()

			if config.plugins.xtraEvent.banner.value == True:
				Banner()

			if config.plugins.xtraEvent.backdrop.value == True:
				if config.plugins.xtraEvent.tmdb.value == True:
					tmdb_backdrop()
				if config.plugins.xtraEvent.tvdb.value == True:
					tvdb_backdrop()
				if config.plugins.xtraEvent.fanart.value == True:
					fanart_backdrop()

			if config.plugins.xtraEvent.info.value == True:
				infos()
		else:
			Notifications.AddNotification(MessageBox, _("NO INTERNET CONNECTION !.."), MessageBox.TYPE_INFO, timeout = 5)
			return
	except:
		return
# DOWNLOAD POSTERS ######################################################################################################


def tmdb_Poster():
	year = ""
	try:
		if os.path.exists(pathLoc+"event-year"):
			with open(pathLoc+"event-year", "r") as f:
				year = f.read()
				
		if os.path.exists(pathLoc+"events"):
			with open(pathLoc+"events", "r") as f:
				titles = f.readlines()
			titles = list(dict.fromkeys(titles))
			n = len(titles)
			for i in xrange(n):
				title = titles[i]
				title = title.strip()
				
				srch = "multi"
				lang = config.plugins.xtraEvent.searchLang.value
				url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}&language={}".format(srch, tmdb_api, quote(title), lang)
				if year != "0":
					url_tmdb += "&primary_release_year={}&year={}".format(year, year)
				try:
					poster = ""
					poster = json.load(urlopen(url_tmdb))['results'][0]['poster_path']
					p_size = config.plugins.xtraEvent.TMDBpostersize.value
					url_poster = "https://image.tmdb.org/t/p/{}{}".format(p_size, poster)
					if url_poster:
						dwn_poster = pathLoc + "poster/{}.jpg".format(title)
						if not os.path.isfile(dwn_poster):
							# open(dwn_poster, 'wb').write(requests.get(url_poster, stream=True, allow_redirects=True).content)
							downloadPage(str(url_poster), dwn_poster)
				except:
					pass


	except:
		pass

def tvdb_Poster():
	try:
		if os.path.exists(pathLoc+"events"):
			with open(pathLoc+"events", "r") as f:
				titles = f.readlines()

			titles = list(dict.fromkeys(titles))
			n = len(titles)
			for i in xrange(n):
				title = titles[i]
				title = title.strip()
				try:
					url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(title))
					url_read = urlopen(url_tvdb).read()
					series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
					if series_id:
						url_tvdb = "https://thetvdb.com/api/a99d487bb3426e5f3a60dea6d3d3c7ef/series/{}/en".format(series_id)
						url_read = urlopen(url_tvdb).read()
						poster = re.findall('<poster>(.*?)</poster>', url_read)[0]

						url_poster = "https://artworks.thetvdb.com/banners/{}".format(poster)
						if config.plugins.xtraEvent.TVDBpostersize.value == "thumbnail":
							url_poster = url_poster.replace(".jpg", "_t.jpg")
						dwn_poster = pathLoc + "poster/{}.jpg".format(title)
						if not os.path.isfile(dwn_poster):
							# open(dwn_poster, 'wb').write(requests.get(url_poster, allow_redirects=True).content)
							downloadPage(str(url_poster), dwn_poster)
				except:
					pass
	except:
		pass

def omdb_Poster():
	try:
		if os.path.exists(pathLoc+"events"):
			with open(pathLoc+"events", "r") as f:
				titles = f.readlines()

			titles = list(dict.fromkeys(titles))
			n = len(titles)
			for i in xrange(n):
				title = titles[i]
				title = title.strip()
				try:
					omdb_apis = ["6a4c9432", "a8834925", "550a7c40", "8ec53e6b"]
					omdb_api = random.sample(omdb_apis, 1)[0]
					url_omdb = 'https://www.omdbapi.com/?apikey=%s&t=%s' %(omdb_api, quote(title))
					url_poster = json.load(urlopen(url_omdb))['Poster']
					dwn_poster = pathLoc + "poster/{}.jpg".format(title)
					if not os.path.isfile(dwn_poster):
						# open(dwn_poster, 'wb').write(requests.get(url_poster, allow_redirects=True).content)
						downloadPage(str(url_poster), dwn_poster)
				except:
					pass
				continue
	except:
		pass

def maze_Poster():
	try:
		if os.path.exists(pathLoc+"events"):
			with open(pathLoc+"events", "r") as f:
				titles = f.readlines()

			titles = list(dict.fromkeys(titles))
			n = len(titles)
			for i in xrange(n):
				title = titles[i]
				title = title.strip()
		
				url_maze = "http://api.tvmaze.com/search/shows?q={}".format(quote(title))
				try:
					url_poster = json.load(urlopen(url_maze))[0]['show']['image']['medium']
					dwn_poster = pathLoc + "poster/{}.jpg".format(title)
					if not os.path.isfile(dwn_poster):
						# open(dwn_poster, 'wb').write(requests.get(url_poster, allow_redirects=True).content)
						downloadPage(str(url_poster), dwn_poster)
				except:
					pass
				continue
	except:
		return

def fanart_Poster():
	try:
		if os.path.exists(pathLoc+"events"):
			with open(pathLoc+"events", "r") as f:
				titles = f.readlines()

			titles = list(dict.fromkeys(titles))
			n = len(titles)
			for i in xrange(n):
				title = titles[i]
				title = title.strip()
				title=title
				try:
					srch = "multi"
					url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
					bnnr = json.load(urlopen(url_tmdb))
					tmdb_id = (bnnr['results'][0]['id'])
					if tmdb_id:
						m_type = (bnnr['results'][0]['media_type'])
						if m_type == "movie":
							m_type = (bnnr['results'][0]['media_type']) + "s"
						else:
							mm_type = m_type
						

						dwn_poster = pathLoc + "poster/{}.jpg".format(title)
						if not os.path.exists(dwn_poster):
							url_maze = "http://api.tvmaze.com/singlesearch/shows?q=%s" %quote(title)
							mj = json.load(urlopen(url_maze))
							tvdb_id = (mj['externals']['thetvdb'])
							if tvdb_id:
								try:
									url_fanart = "https://webservice.fanart.tv/v3/%s/%s?api_key=6d231536dea4318a88cb2520ce89473b" %(m_type, tvdb_id)
									fjs = json.load(urlopen(url_fanart))
									if fjs:
										if m_type == "movies":
											mm_type = (bnnr['results'][0]['media_type'])
										else:
											mm_type = m_type
										url_poster = (fjs['tvposter'][0]['url'])
										if url_poster:
											dwn_poster = pathLoc + "poster/{}.jpg".format(title)
											dwn_poster=dwn_poster
											if not os.path.isfile(dwn_poster):
												# open(dwn_poster, 'wb').write(requests.get(url_poster, allow_redirects=True).content)
												downloadPage(str(url_poster), dwn_poster)

												scl = 1
												im = Image.open(dwn_poster)
												scl = config.plugins.xtraEvent.FANARTresize.value
												im1 = im.resize((im.size[0] // int(scl), im.size[1] // int(scl)), Image.ANTIALIAS)
												im1.save(dwn_poster)

								except:
									pass
			
				except:
					pass
			
	except:
		pass

# def Fnrtresz():
	# scl = 1
	# im = Image.open(dwn_poster)
	# scl = config.plugins.xtraEvent.FANARTresize.value
	# im1 = im.resize((im.size[0] // int(scl), im.size[1] // int(scl)), Image.ANTIALIAS)
	# im1.save(dwn_poster)
	
	# image = Image.open(dwn_poster)
	# maxsize = config.plugins.xtraEvent.FANARTresize.value
	# image.thumbnail(maxsize, Image.ANTIALIAS)
	# image.save(dwn_poster)
	
# DOWNLOAD BANNERS ######################################################################################################

def Banner():
	if os.path.exists(pathLoc+"events"):
		with open(pathLoc+"events", "r") as f:
			titles = f.readlines()

		titles = list(dict.fromkeys(titles))
		n = len(titles)
		for i in xrange(n):
			title = titles[i]
			title = title.strip()
			
			try:
				url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname=%s" %quote(title)
				url_read = urlopen(url_tvdb).read()			
				series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read, re.I)[0]
				if series_id:
					url_banner = "https://artworks.thetvdb.com/banners/graphical/%s-g_t.jpg" %(series_id)
					if url_banner:
						dwn_banner = pathLoc + "banner/{}.jpg".format(title)
						if not os.path.isfile(dwn_banner):
							# open(dwn_banner, 'wb').write(requests.get(url_banner, allow_redirects=True).content)
							downloadPage(str(url_banner), dwn_banner)

			except:
				try:
					srch = "multi"
					url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
					bnnr = json.load(urlopen(url_tmdb))
					tmdb_id = (bnnr['results'][0]['id'])
					if tmdb_id:
						m_type = (bnnr['results'][0]['media_type'])
						if m_type == "movie":
							m_type = (bnnr['results'][0]['media_type']) + "s"
						else:
							mm_type = m_type
						url_fanart = "https://webservice.fanart.tv/v3/%s/%s?api_key=6d231536dea4318a88cb2520ce89473b" %(m_type, tmdb_id)
						fjs = json.load(urlopen(url_fanart))
						if fjs:
							if m_type == "movies":
								mm_type = (bnnr['results'][0]['media_type'])
							url_banner = (fjs[mm_type+'banner'][0]['url'])
							if url_banner:
								dwn_banner = pathLoc + "banner/{}.jpg".format(title)
								if not os.path.isfile(dwn_banner):
									# open(dwn_banner, 'wb').write(requests.get(url_banner, allow_redirects=True).content)
									downloadPage(str(url_banner), dwn_banner)

				except:
					try:
						url_maze = "http://api.tvmaze.com/singlesearch/shows?q=%s" %(title)
						mj = json.load(urlopen(url_maze))
						poster = (mj['externals']['thetvdb'])
						if poster:
							url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname=%s" %quote(title)
							url_read = urlopen(url_tvdb).read()
							series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read, re.I)[0]
							banner_img = re.findall('<banner>(.*?)</banner>', url_read, re.I)[0]
							if banner_img:
								url_banner = "https://artworks.thetvdb.com%s" %(banner_img)
								dwn_banner = pathLoc + "banner/{}.jpg".format(title)
								if not os.path.isfile(dwn_banner):
									# open(dwn_banner, 'wb').write(requests.get(url_banner, allow_redirects=True).content)
									downloadPage(str(url_banner), dwn_banner)

							if series_id:
								try:
									url_fanart = "https://webservice.fanart.tv/v3/%s/%s?api_key=6d231536dea4318a88cb2520ce89473b" %(m_type, series_id)
									fjs = json.load(urlopen(url_fanart))
									if fjs:
										if m_type == "movies":
											mm_type = (bnnr['results'][0]['media_type'])
										else:
											mm_type = m_type
										url_banner = (fjs[mm_type+'banner'][0]['url'])

										if url_banner:
											dwn_banner = pathLoc + "banner/{}.jpg".format(title)
											if not os.path.isfile(dwn_banner):
												# open(dwn_banner, 'wb').write(requests.get(url_banner, allow_redirects=True).content)
												downloadPage(str(url_banner), dwn_banner)

								except:
									pass
					except:
						pass

# DOWNLOAD BACKDROP ######################################################################################################

def tmdb_backdrop():
	try:
		if os.path.exists(pathLoc+"events"):
			with open(pathLoc+"events", "r") as f:
				titles = f.readlines()

			titles = list(dict.fromkeys(titles))
			n = len(titles)
			for i in xrange(n):
				title = titles[i]
				title = title.strip()
				srch = "multi"
				lang = config.plugins.xtraEvent.searchLang.value
				url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}&language={}".format(srch, tmdb_api, quote(title), lang)
				try:
					backdrop = json.load(urlopen(url_tmdb))['results'][0]['backdrop_path']
					if backdrop:
						backdrop_size = config.plugins.xtraEvent.TMDBbackdropsize.value
						url_backdrop = "https://image.tmdb.org/t/p/{}{}".format(backdrop_size, backdrop)
						dwn_backdrop = pathLoc + "backdrop/{}.jpg".format(title)
						if not os.path.isfile(dwn_backdrop):
							# open(dwn_backdrop, 'wb').write(requests.get(url_backdrop, allow_redirects=True).content)
							downloadPage(str(url_backdrop), dwn_backdrop)
				except:
					pass
				
	except:
		pass

def tvdb_backdrop():
	try:
		if os.path.exists(pathLoc+"events"):
			with open(pathLoc+"events", "r") as f:
				titles = f.readlines()

			titles = list(dict.fromkeys(titles))
			n = len(titles)
			for i in xrange(n):
				title = titles[i]
				title = title.strip()

				try:
					url_tvdb = "https://thetvdb.com/api/GetSeries.php?seriesname={}".format(quote(title))
					url_read = urlopen(url_tvdb).read()
					series_id = re.findall('<seriesid>(.*?)</seriesid>', url_read)[0]
					if series_id:
						url_tvdb = "https://thetvdb.com/api/a99d487bb3426e5f3a60dea6d3d3c7ef/series/{}/en".format(series_id)
						url_read = urlopen(url_tvdb).read()
						backdrop = re.findall('<fanart>(.*?)</fanart>', url_read)[0]
						if backdrop:
							url_backdrop = "https://artworks.thetvdb.com/banners/{}".format(backdrop)
							if config.plugins.xtraEvent.TVDBbackdropsize.value == "thumbnail":
								url_backdrop = url_backdrop.replace(".jpg", "_t.jpg")

							dwn_backdrop = pathLoc + "backdrop/{}.jpg".format(title)
							if not os.path.isfile(dwn_backdrop):
								# open(dwn_backdrop, 'wb').write(requests.get(url_backdrop, allow_redirects=True).content)
								downloadPage(str(url_backdrop), dwn_backdrop)

				except:
					pass

	except:
		pass

def fanart_backdrop():
	try:
		if os.path.exists(pathLoc+"events"):
			with open(pathLoc+"events", "r") as f:
				titles = f.readlines()

			titles = list(dict.fromkeys(titles))
			n = len(titles)
			for i in xrange(n):
				title = titles[i]
				title = title.strip()
				
				try:
					srch = "multi"
					url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(srch, tmdb_api, quote(title))
					bnnr = json.load(urlopen(url_tmdb))
					tmdb_id = (bnnr['results'][0]['id'])
					if tmdb_id:
						m_type = (bnnr['results'][0]['media_type'])
						if m_type == "movie":
							m_type = (bnnr['results'][0]['media_type']) + "s"
						else:
							mm_type = m_type
						

						dwn_backdrop = pathLoc + "backdrop/{}.jpg".format(title)
						if not os.path.exists(dwn_backdrop):
							url_maze = "http://api.tvmaze.com/singlesearch/shows?q=%s" %quote(title)
							
							mj = json.load(urlopen(url_maze))
							tvdb_id = (mj['externals']['thetvdb'])
							if tvdb_id:
								try:
									
									url_fanart = "https://webservice.fanart.tv/v3/%s/%s?api_key=6d231536dea4318a88cb2520ce89473b" %(m_type, tvdb_id)
									fjs = json.load(urlopen(url_fanart))
									
									if fjs:
										if m_type == "movies":
											mm_type = (bnnr['results'][0]['media_type'])
										else:
											mm_type = m_type
										url_backdrop = (fjs['tvthumb'][0]['url'])

										if url_backdrop:
											dwn_backdrop = pathLoc + "backdrop/{}.jpg".format(title)
											if not os.path.isfile(dwn_backdrop):
												# open(dwn_backdrop, 'wb').write(requests.get(url_backdrop, allow_redirects=True).content)
												downloadPage(str(url_backdrop), dwn_backdrop)

								except:
									pass
				except:
					pass

	except:
		pass

# DOWNLOAD INFOS ######################################################################################################

def infos():
	try:
		if os.path.exists(pathLoc+"events"):
			with open(pathLoc+"events", "r") as f:
				titles = f.readlines()

			titles = list(dict.fromkeys(titles))
			n = len(titles)
			for i in xrange(n):
				title = titles[i]
				title = title.strip()

				omdb_apis = ["6a4c9432", "a8834925", "550a7c40", "8ec53e6b"]
				omdb_api = random.sample(omdb_apis, 1)[0]
				url_omdb = 'https://www.omdbapi.com/?apikey=%s&t=%s' %(omdb_api, quote(title))

				try:
					data = json.load(urlopen(url_omdb))

					name = data['Title']
					rtng = data['imdbRating']
					country = data['Country']
					year = data['Year']
					rate = data['Rated']
					genre = data['Genre']
					award = data['Awards']

					info = "Title: %s"%str(name) + "\nImdb: %s"%str(rtng) + "\nYear: %s, %s"%(str(country), str(year.encode('utf-8'))) + "\nRate: %s"%str(rate) + "\nGenre: %s"%str(genre) + "\nAwards: %s" %str(award)
					info_files = pathLoc + "infos/{}".format(title)
					if not os.path.exists(info_files):
						open(info_files, "w").write(str(info))
					
				except:
					pass

				
			if os.path.exists(pathLoc+"events"):
				with open(pathLoc+"events", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
			
				for i in xrange(n):
					title = titles[i]
					title = title.strip()
					srch = "multi"
					url_tmdb = "https://api.themoviedb.org/3/search/{}?api_key=3c3efcf47c3577558812bb9d64019d65&query={}".format(srch, quote(title))
					try:
						org_title = json.load(urlopen(url_tmdb))['results'][0]['original_title']
					except:
						pass
					info_files = pathLoc + "infos/{}".format(title)
					if not os.path.exists(info_files):
						open("/tmp/org_title", "a+").write("%s\n"% str(org_title))


			if os.path.exists("/tmp/org_title"):
				with open("/tmp/org_title", "r") as f:
					titles = f.readlines()

				titles = list(dict.fromkeys(titles))
				n = len(titles)
				for i in xrange(n):
					title = titles[i]
					title = title.strip()

					omdb_apis = ["6a4c9432", "a8834925", "550a7c40", "8ec53e6b"]
					omdb_api = random.sample(omdb_apis, 1)[0]
					url_omdb = 'https://www.omdbapi.com/?apikey=%s&t=%s' %(omdb_api, quote(title))

					try:
						data = json.load(urlopen(url_omdb))

						name = data['Title']
						rtng = data['imdbRating']
						country = data['Country']
						year = data['Year']
						rate = data['Rated']
						genre = data['Genre']
						award = data['Awards']

						info = "Title: %s"%str(name) + "\nImdb: %s"%str(rtng) + "\nYear: %s, %s"%(str(country), str(year.encode('utf-8'))) + "\nRate: %s"%str(rate) + "\nGenre: %s"%str(genre) + "\nAwards: %s" %str(award)
						info_files = pathLoc + "infos/{}".format(title)
						if not os.path.exists(info_files):
							open(info_files, "w").write(str(info))
						
					except:
						pass



	except:
		pass

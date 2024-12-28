# -*- coding: utf-8 -*-
# by digiteng...03.2024

from __future__ import absolute_import
from time import time, localtime, strftime
import socket
from Components.config import config
import re
REGEX = re.compile(
		r'([\(\[]).*?([\)\]])|'
		r'(: odc.\d+)|'
		r'(\d+: odc.\d+)|'
		r'(\d+ odc.\d+)|(:)|'
		r'(\d+.* \(odc. \d+.*\))|'
		r'!|'
		r'/.*|'
		r'\|\s[0-9]+\+|'
		r'[0-9]+\+|'
		r'\s\d{4}\Z|'
		r'([\(\[\|].*?[\)\]\|])|'
		# r'(\"|\"\.|\"\,|\.)\s.+|'
		r'\"|:|'
		r'\*|'
		r'Премьера\.\s|'
		r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
		r'(х|Х|м|М|т|Т|д|Д)/с\s|'
		r'\s(с|С)(езон|ерия|-н|-я)\s.+|'
		r'\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
		r'\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
		r'\s(ч|ч\.|с\.|с)\s\d{1,3}.+|'
		r'\d{1,3}(-я|-й|\sс-н).+|', re.DOTALL)

header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
try:
	pathLoc =  "{}xtraEvent/".format(config.plugins.xtraEvent.loc.value)
except:
	pathLoc = "/tmp/"
def pathLocation():
	try:
		return config.plugins.xtrvnt.loc.value
	except:
		return "/"
		
def errorlog(err, filex):
	tm = strftime("%Y-%m-%d %H:%M:%S")
	with open("/tmp/xtraError.log", "a+") as f:
		f.write("File : {}, {}, \nERROR:{}, \nLine:{}\n\n".format(filex, tm, err, err.__traceback__.tb_lineno))

def eventlog(filex):
	tm = strftime("%Y-%m-%d %H:%M:%S")
	with open("/tmp/xtraEvent.log", "a+") as f:
		f.write("[{}], {}\n".format(tm, filex))

def intCheck():
	try:
		socket.setdefaulttimeout(2)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
		return True
	except:
		return False

def getLanguage():
	lang = "en_UK"
	try:
		from Components.Language import language
		lang = language.getLanguage()
	except:
		try:
			lang = config.osd.language.value
		except:
			lang = "en-UK"
	return lang.replace("_", "-")

def version():
	ver="N/A"
	with open("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/version", "r") as f:
		ver = f.read()
	return ver

def pRating(rate):
	if rate in ["G", "TV-G", "PG", "TV-Y", "TV-PG", "E"]:
		rate = "0"
	elif rate in ["4", "6", "6+", "7", "7A", "7+", "9", "9+", "TV-Y7"]:
		rate = "6"
	elif rate in ["TV-14", "PG-13", "E10+", "T", "T+", "12", "12+", "12A", "13", "13+", "13A", "14", "14+", "14A", "10+"]:
		rate = "12"
	elif rate in ["R", "TV-MA", "M", "16", "16+", "15", "15+"]:
		rate = "16"
	elif rate in ["NC-17", "AO", "MAX", "18", "18+"]:
		rate = "18"
	else:
		rate : "NA"
	return rate

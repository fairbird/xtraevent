# -*- coding: utf-8 -*-
# by digiteng...07.2020 - 11.2020 - 11.2021
# FOR INFO
# <widget source="session.Event_Now" render="Label" position="50,545" size="930,400" font="Regular; 32" halign="left" transparent="1" zPosition="2" backgroundColor="background">
    # <convert type="xtraInfo">Title,Year,Description</convert>
# </widget>
# 
# FOR IMDB RATING STAR...
# <ePixmap pixmap="xtra/star_b.png" position="990,278" size="200,20" alphatest="blend" zPosition="2" transparent="1" />
# <widget source="ServiceEvent" render="Progress" pixmap="xtra/star.png" position="990,278" size="200,20" alphatest="blend" transparent="1" zPosition="2" backgroundColor="background">
    # <convert type="xtraInfo">imdbRatingValue</convert>
# </widget>

from __future__ import absolute_import
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from Components.Converter.xtraEventGenre import getGenreStringSub
import re
import json
import os

import sys


api = 'b1538d0b'
import inspect
# --------------------------- Logfile -------------------------------

from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraInfo.log"

## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
############################## File copieren ############################################
# fuer py2 die int und str anweisung raus genommen und das Grad zeichen

###########################  log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus

logstatus = "on"


# ________________________________________________________________________________

def write_log(msg):
    if logstatus == ('on'):
        with open(myfile, "a") as log:

            log.write(datetime.now().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")

            return
    return

# ****************************  test ON/OFF Logfile ************************************************


def logout(data):
    if logstatus == ('on'):
        write_log(data)
        return
    return


# ----------------------------- so muss das commando aussehen , um in den file zu schreiben  ------------------------------
logout(data="start")
if sys.version_info[0] >= 3:
    import requests

else:
    import urllib2

try:
    pathLoc = config.plugins.xtraEvent.loc.value
    logout(data="start pathloc")
    logout(data=str(pathLoc))

except:
    pass

REGEX = re.compile(
        r'([\(\[]).*?([\)\]])|'
        r'(: odc.\d+)|'
        r'(\d+: odc.\d+)|'
        r'(\d+ odc.\d+)|(:)|'
        
        r'!|'
        r'/.*|'
        r'\|\s[0-9]+\+|'
        r'[0-9]+\+|'
        r'\s\d{4}\Z|'
        r'([\(\[\|].*?[\)\]\|])|'
        r'(\"|\"\.|\"\,|\.)\s.+|'
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

class xtraInfo(Converter, object):
    logout(data="----------------------------- class xrtraInfo --------------------------------------------")
    Title = "Title"
    Year = "Year"
    Rated = "Rated"
    Released = "Released"
    Runtime = "Runtime"
    Genre = "Genre"
    Director = "Director"
    Writer = "Writer"
    Actors = "Actors"
    Plot = "Description"
    Language = "Language"
    Country = "Country"
    Awards = "Awards"
    imdbRating = "imdbRating"
    imdbRatingValue = "imdbRatingValue"
    imdbRatingSimple = "imdbRatingSimple"
    imdbVotes = "imdbVotes"
    Type = "Type"
    totalSeasons = "totalSeasons"
    SE = "SE"
    Duration = "Duration"
    Compact = "Compact"

    lastevnt = "none"
    logout(data=str(lastevnt))


    def __init__(self, type):
        logout(data="----------------------------- def init --------------------------------------------")
        Converter.__init__(self, type)
        self.types = str(type).split(",")

        lastevnt = ""
    @cached
    def getText(self):
        logout(data="---------------------------  start def getText ------------------------------------")
        caller_frame = inspect.currentframe().f_back
        caller_name = inspect.getframeinfo(caller_frame).function
        log_message = f"Die Funktion getText() wurde von {caller_name} aufgerufen."
        logout(data=log_message)

        event = self.source.event
        logout(data=str(event))
        logout(data="sendungs name")
        if event:
            logout(data="if event -------------------  name gefunden")
            if self.types:
                evnt = event.getEventName()
                logout(data="getText-evnt ------ sendungsname")
                logout(data=str(evnt))

                logout(data="getText-lastevnt ------ sendungsname")
                logout(data=str(self.lastevnt))

                if self.lastevnt == evnt:
                    logout(data="lastevnt ist wie evnt gleiche anfrage")
                    #return

                self.lastevnt = evnt
                evntNm = REGEX.sub('', evnt).strip()
                logout(data=str(evntNm))


                rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
                rating_jsonomdb = "{}xtraEvent/infosomdb/{}.json".format(pathLoc, evntNm)
                jsonomdb = "{}xtraEvent/infosomdb".format(pathLoc)
                xtrapath = "{}xtraEvent/".format(pathLoc)
                logout(data="path json")
                logout(data=str(rating_json))
                logout(data=str(rating_jsonomdb))
                logout(data=str(jsonomdb))
                if not os.path.exists(jsonomdb):
                    logout(data="make dir anlegen")
                    os.makedirs("{}infosomdb".format(xtrapath))

# ------------------------------  ist json von omdb vorhanden --------------------------------------------------------
                if os.path.exists(rating_jsonomdb):
                    logout(data="path jsonomdb datei ist vorhanden")
                else:
                    logout(data="path jsonmdb datei ist nicht vorhanden")
                    url = 'https://www.omdbapi.com/?apikey=%s&t=%s' % (api, evntNm.lower())
                    logout(data=str(url))
                    logout(data="url")



                    if sys.version_info[0] >= 3:
                        logout(data="ist py3")
                        response = requests.get(url)
                        read_json = response.json()
                        logout(data=str(read_json))
                        logout(data="---------------------------------------------------------------------------")
                        # JSON-Daten speichern
                        logout(data="open file")
                        logout(data=str(rating_jsonomdb))
                        if read_json.get("Response") == "True":
                            logout(data="json hatt info")
                            with open(rating_jsonomdb, 'w') as file:
                                json.dump(response.json(), file)
                        else:
                            logout(data="json hatte keine info")
                        #with open(rating_jsonomdb, "x") as datei:
                        #    json.dump(read_json, datei)
                    else:
                        logout(data="ist py2")
                        data = json.load(urllib2.urlopen(url))





                # hier infos von der box holen aus dem epg
                fd = "{}\n{}\n{}".format(event.getEventName(), event.getShortDescription(), event.getExtendedDescription())
                #logout(data="info in fd")
                #logout(data=str(fd))

                evnt = []
                try:
                    logout(data="getText-try")

                    for type in self.types:
                        logout(data="getText-----------------------------type anfrage")
                        logout(data=str(type))
                        type.strip()

                        if os.path.exists(rating_jsonomdb):
                            logout(data="getText------------------------------json omdb vorhanden")

                            with open(rating_jsonomdb, "r") as datei:
                                logout(data="getText--------------- open json und load")
                                read_json = json.load(datei)
                                #logout(data=str(read_json))


                        else:
                            logout(data="getText-------------------------json omdb  nicht vorhanden")

                            if os.path.exists(rating_json):
                                logout(data="getText------------------------------json tmdb vorhanden")

                                with open(rating_json, "r") as datei:
                                    logout(data="getText--------------- open json und load")
                                    read_json = json.load(datei)
                                    #logout(data=str(read_json))
                            else:
                                logout(data="getText-------------------------json tmdb  nicht vorhanden")

                        #-----------------------------------------------------------------------------------------------------------------------
                        if type == self.Title:
                            logout(data="Title")
                            try:
                                title = read_json['Title']
                                logout(data="Title aus json")
                                logout(data=str(title))
                                if title:
                                    logout(data="title 1")
                                    # hier aus json ins array rein
                                    evnt.append("Title : {}".format(title))
                            except:
                                logout(data="title 2 info ohne json")
                                # hier ins array reinschreiben sind aber infos von der box epg
                                evnt.append("Title - {}".format(event.getEventName()))
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Year:
                            logout(data="Year")
                            try:
                                logout(data="Year 1")
                                year = read_json["Year"]
                                year = year.replace("-", "")
                                logout(data=str(year))
                                if year:
                                    logout(data="Year 2")
                                    evnt.append("Year : {}".format(year))

                            except:
                                logout(data="Year 3")
                                year = ''
                                fd = fd.replace(',', '').replace('(', '').replace(')', '')
                                fdl = ['\d{4} [A-Z]+', '[A-Z]+ \d{4}', '[A-Z][a-z]+\s\d{4}', '\+\d+\s\d{4}']
                                for i in fdl:
                                    logout(data="Year 4")
                                    year = re.findall(i, fd)
                                    if year:
                                        logout(data="Year 5")
                                        year = re.sub(r'\(.*?\)|\.|\+\d+', ' ', year[0]).strip()
                                        evnt.append("Year : {}".format(year))
                                        break
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Rated:
                            logout(data="Rated")
                            try:
                                Rated = read_json["Rated"]
                                if Rated != "Not Rated":
                                    evnt.append("Rated : {}+".format(Rated))
                                elif Rated == "Not Rated":
                                    parentName = ''
                                    prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
                                    for i in prs:
                                        prr = re.search(i, fd)
                                        if prr:
                                            parentName = prr.group(1)
                                            parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
                                            evnt.append("Rated : {}+".format(parentName))
                                            break
                                else:
                                    try:
                                        age = ''
                                        rating = event.getParentalData()
                                        if rating:
                                            age = rating.getRating()
                                            evnt.append("Rated - {}+".format(age))
                                    except:
                                        pass
                            except:
                                parentName = ''
                                prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
                                for i in prs:
                                    prr = re.search(i, fd)
                                    if prr:
                                        parentName = prr.group(1)
                                        parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
                                        evnt.append("Rated : {}+".format(parentName))
                                        break
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Released:
                            logout(data="Released")
                            try:
                                Released = read_json["Released"]
                                if Released:
                                    evnt.append("Released : {}".format(Released))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Runtime:
                            logout(data="Runtime")
                            try:
                                Runtime = read_json["Runtime"]
                                if Runtime:
                                    evnt.append("Runtime : {}".format(Runtime))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Genre:
                            logout(data="Genre")
                            try:
                                Genre = read_json["Genre"]
                                if Genre:
                                    evnt.append("Genre : {}".format(Genre))
                            except:
                                genres = event.getGenreDataList()
                                if genres:
                                    genre = genres[0]
                                    evnt.append("Genre - {}".format(getGenreStringSub(genre[0], genre[1])))
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Director:
                            logout(data="Director")
                            try:
                                Director = read_json["Director"]
                                if Director:
                                    evnt.append("Director : {}".format(Director))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Writer:
                            logout(data="Writer")
                            try:
                                Writer = read_json["Writer"]
                                if Writer:
                                    evnt.append("Writer : {}".format(Writer))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Actors:
                            logout(data="Actors")
                            try:
                                Actors = read_json["Actors"]
                                if Actors:
                                    evnt.append("Actors : {}".format(Actors))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Plot:
                            logout(data="Plot")
                            try:
                                Plot = read_json["Plot"]
                                if Plot:
                                    evnt.append("Description : {}".format(Plot))
                                else:
                                    evnt.append("Description : {}".format(fd))
                            except:
                                evnt.append("Description : {}".format(fd))
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Language:
                            logout(data="Language")
                            try:
                                Language = read_json["Language"]
                                if Language:
                                    evnt.append("Language : {}".format(Language))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Country:
                            logout(data="Country")
                            try:
                                Country = read_json["Country"]
                                if Country:
                                    evnt.append("Country : {}".format(Country))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Awards:
                            logout(data="Awards")
                            try:
                                Awards = read_json["Awards"]
                                if Awards:
                                    evnt.append("Awards : {}".format(Awards))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.imdbRating:
                            logout(data="imdbRating")
                            try:
                                imdbRating = read_json["imdbRating"]
                                if imdbRating:
                                    evnt.append("IMDB : {}".format(imdbRating))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.imdbRatingSimple:
                            logout(data="imdbRatingSimpel")
                            try:
                                imdbRatingSimple = read_json["imdbRating"]
                                if imdbRatingSimple:
                                    evnt.append("{}".format(imdbRatingSimple))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.imdbVotes:
                            logout(data="imdbVotes")
                            try:
                                imdbVotes = read_json["imdbVotes"]
                                if imdbVotes:
                                    evnt.append("imdbVotes : {}".format(imdbVotes))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Type:
                            logout(data="Type")
                            try:
                                Type = read_json["Type"]
                                if Type:
                                    evnt.append("Type : {}".format(Type))
                            except:
                                pass
                        elif type == self.totalSeasons:
                            try:
                                totalSeasons = read_json["totalSeasons"]
                                if totalSeasons:
                                    evnt.append("TotalSeasons : {}".format(totalSeasons))
                            except:
                                pass
#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.Duration:
                            logout(data="Duration")
                            try:
                                Duration = read_json["Duration"]
                                if totalSeasons:
                                    evnt.append("Duration : {}min".format(Duration))
                            except:
                                drtn = round(event.getDuration()// 60)
                                if drtn > 0:
                                    evnt.append("Duration - {}min".format(drtn))
                                else:
                                    prs = re.findall(r' \d+ Min', fd)
                                    if prs:
                                        drtn = round(prs[0])
                                        evnt.append("Duration : {}min".format(drtn))

#-----------------------------------------------------------------------------------------------------------------------
                        elif type == self.SE:
                            logout(data="SE")
                            ""
                            try:
                                prs = ['(\d+). Staffel, Folge (\d+)', 'T(\d+) Ep.(\d+)', '"Episodio (\d+)" T(\d+)']
                                for i in prs:
                                    seg = re.search(i, fd)
                                    if seg:
                                        s = seg.group(1).zfill(2)
                                        e = seg.group(2).zfill(2)
                                        evnt.append("SE : S{}E{}".format(s, e))
                            except:
                                pass
# ----------------------------------------------------------------------------------------------------------------------
                        # Compact
                        elif type == self.Compact:
                            logout(data="Compact")

                            try:
                                Genre = read_json["Genre"]
                                if Genre:
                                    Genre = Genre.split(",")
                                    evnt.append("{}".format(Genre[0]))
                            except:
                                try:
                                    genres = event.getGenreDataList()
                                    if genres:
                                        genre = genres[0]
                                        genre = getGenreStringSub(genre[0], genre[1])
                                        genre = genre.split(",")
                                        genre = genre[0]
                                        evnt.append("{}".format(genre))
                                except:
                                    pass

                            try:
                                Country = read_json["Country"]
                                Country = Country.replace("United States", "USA").replace("United Kingdom", "UK")
                                if Country:
                                    evnt.append("{}".format(Country))
                            except:
                                pass
                            try:
                                imdbRating = read_json["imdbRating"]
                                if imdbRating:
                                    evnt.append("IMDB:{}".format(imdbRating))
                            except:
                                pass

                            try:
                                Rated = read_json["Rated"]
                                if Rated != "Not Rated":
                                    evnt.append("{}+".format(Rated))
                                elif Rated == "Not Rated":
                                    parentName = ''
                                    prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
                                    for i in prs:
                                        prr = re.search(i, fd)
                                        if prr:
                                            parentName = prr.group(1)
                                            parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
                                            evnt.append("{}+".format(parentName))
                                            break
                                else:
                                    try:
                                        age = ''
                                        rating = event.getParentalData()
                                        if rating:
                                            age = rating.getRating()
                                            evnt.append("{}+".format(age))
                                    except:
                                        pass
                            except:
                                parentName = ''
                                prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
                                for i in prs:
                                    prr = re.search(i, fd)
                                    if prr:
                                        parentName = prr.group(1)
                                        parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
                                        evnt.append("{}+".format(parentName))
                                        break

                            try:
                                prs = ['(\d+). Staffel, Folge (\d+)', 'T(\d+) Ep.(\d+)', '"Episodio (\d+)" T(\d+)']
                                for i in prs:
                                    seg = re.search(i, fd)
                                    if seg:
                                        s = seg.group(1).zfill(2)
                                        e = seg.group(2).zfill(2)
                                        evnt.append("S{}E{}".format(s, e))
                            except:
                                pass

                            try:
                                year = ''
                                fd = fd.replace(',', '').replace('(', '').replace(')', '')
                                fdl = ['\d{4} [A-Z]+', '[A-Z]+ \d{4}', '[A-Z][a-z]+\s\d{4}', '\+\d+\s\d{4}']
                                for i in fdl:
                                    year = re.findall(i, fd)
                                    if year:
                                        year = re.sub(r'\(.*?\)|\.|\+\d+', ' ', year[0]).strip()
                                        evnt.append("{}".format(year))
                                        break
                            except:
                                year = read_json["Year"]
                                if year:
                                    evnt.append("{}".format(year))


                        if type != self.Compact:
                            tc = "\n".join(evnt)
                        else:
                            # tc = " | ".join(evnt)

                            tc = '\\c0000??00 • '
                            tc += '\\c00??????'
                            tc = tc.join(evnt)

                    return tc
                except:
                    logout(data="abfragen")
                    return ""
        else:
            logout(data="kein event name")
            return ""

    logout(data="------------------ Ausgabe Text ----------------")
    text = property(getText)
    logout(data=str(text))

    @cached
    def getValue(self):
        logout(data="getValue")
        event = self.source.event
        if event:
            if self.types:
                evnt = event.getEventName()
                evntNm = REGEX.sub('', evnt).strip()
                rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)

                try:
                    for type in self.types:
                        type.strip()
                        if type == self.imdbRatingValue:
                            if os.path.exists(rating_json):
                                with open(rating_json) as f:
                                    read_json = json.load(f)
                                try:
                                    imdbRatingValue = read_json["imdbRating"]
                                    if imdbRatingValue:
                                        return int(10*(float(imdbRatingValue)))
                                    else:
                                        return 0
                                except:
                                    return 0
                except:
                    return 0
        else:
            return 0

    value = property(getValue)
    range = 100


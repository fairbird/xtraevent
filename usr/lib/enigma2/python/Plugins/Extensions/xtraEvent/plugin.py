#!/usr/bin/python
# -*- coding: utf-8 -*-

# by digiteng...(digiteng@gmail.com)
# https://github.com/digiteng/
# 06.2020 - 11.2020(v2.0) - 11.2021(v3.x)
from __future__ import absolute_import
from Plugins.Plugin import PluginDescriptor
from Components.config import config
import threading
from datetime import datetime
from six.moves import reload_module
from . import xtra
from . import download

from enigma import addFont

# --------------------------- Logfile -------------------------------
from datetime import datetime, timedelta
from threading import Timer
#from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/xtraevent-Plugin.log"

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
logout(data="start 6.75")

addFont("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/fonts/arial.ttf", "xtraRegular", 100, 1)

def startTimer():
    logout(data="start timer mit download")
    if config.plugins.xtraEvent.timerMod.value == "Clock":
        logout(data="clock")

        tc = config.plugins.xtraEvent.timerClock.value
        logout(data=str(tc))

        dt = datetime.today()
        logout(data="date time")
        logout(data=str(dt))

        #setclk = dt.replace(day=dt.day+1, hour=tc[0], minute=tc[1], second=0, microsecond=0)
        offset = tc[0] * 60 + tc[1]  # Offset in Minuten umrechnen
        setclk = datetime.today() + timedelta(minutes=offset)
        logout(data="set clock")
        logout(data=str(setclk))

        ds = setclk - dt
        logout(data="clock - dt")
        logout(data=str(ds))

        secs = ds.seconds + 1
        logout(data="seconds")
        logout(data=str(secs))

        def startDownload():
            logout(data="start download")
            from . import download
            download.downloads("").save()
            logout(data="ende download")
            startTimer()
        err = ""
        t = threading.Timer(secs, startDownload)
        t.start()

        with open("/tmp/xtraEvent.log", "a+") as f:
           f.write("plugin timer clock, %s\n"%(err))


try:
    logout(data="clock start")
    if config.plugins.xtraEvent.timerMod.value == "Clock":
        logout(data="clock")

        tc = config.plugins.xtraEvent.timerClock.value
        logout(data=str(tc))

        dt = datetime.today()
        logout(data="date time")
        logout(data=str(dt))

        #setclk = dt.replace(day=dt.day+1, hour=tc[0], minute=tc[1], second=0, microsecond=0)
        offset = tc[0] * 60 + tc[1]  # Offset in Minuten umrechnen
        setclk = datetime.today() + timedelta(minutes=offset)
        logout(data="set clock")
        logout(data=str(setclk))

        ds = setclk - dt
        logout(data="clock - dt")
        logout(data=str(ds))
# ------------------------------------------- nach plugin start wird nach ca 10 sec ein download gemacht
        #secs = ds.seconds + 1
        secs = 10
        logout(data="seconds")
        logout(data=str(secs))

        def startDownload():
            logout(data="start download")
            from . import download
            download.downloads("").save()
            logout(data="ende download")
            startTimer()

        t = threading.Timer(secs, startDownload)
        t.start()

except Exception as err:
    logout(data="---------------------------------------------------------------- timer write und err --------------")
    logout(data=str(err))
    #with open("/tmp/xtraEvent.log", "a+") as f:
    #    f.write("plugin timer clock, %s\n"%(err))
    try:
        with open("/tmp/xtraEvent.log", "a+") as f:
            f.write("plugin timer clock, %s\n" % (err))
    except IOError as e:
        logout(data="Fehler beim Schreiben in die Datei")
        logout(data=str(e))

def ddwn():
    logout(data="def ddwn")
    try:
        logout(data="def ddwn 1")
        if config.plugins.xtraEvent.timerMod.value == "Period":
            logout(data="ddwn period")
            logout(data="start download period")
            download.downloads("").save()
            logout(data="ende download period")
            logout(data=str(config.plugins.xtraEvent.timerHour.value))
            tmr = config.plugins.xtraEvent.timerHour.value
            logout(data="ddwn period tmr zeit stunde")
            logout(data=str(tmr))
            t = threading.Timer(3600*int(tmr), ddwn) # 1h=3600
            logout(data="ddwn period timer in secunde start timer ")
            logout(data=str(t))
            t.start()
    except Exception as err:
        with open("/tmp/xtra_error.log", "a+") as f:
            f.write("xtra plugin ddwn, %s\n\n"%err)

try:
    if config.plugins.xtraEvent.timerMod.value == "Period":
        logout(data="ddwn period download start in 30 sec")
        threading.Timer(30, ddwn).start()
except Exception as err:
    with open("/tmp/xtra_error.log", "a+") as f:
        f.write("xtra plugin timer start, %s\n\n"%err)

def main(session, **kwargs):
    try:
        logout(data="main")
        reload_module(xtra)
        reload_module(download)
        session.open(xtra.xtra)

    except:
        logout(data="main 1")
        import traceback
        traceback.print_exc()

def Plugins(**kwargs):
    return [PluginDescriptor(name="xtraEvent {}".format(xtra.version), description="Poster, Backdrop, Banner, Info...Etc, Support...", where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)]

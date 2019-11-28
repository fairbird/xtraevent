# -*- coding: utf-8 -*-
# by digiteng...10.2019
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from enigma import eConsoleAppContainer, eTimer, getDesktop
import os
import shutil
from Components.config import config, configfile, ConfigSubsection, getConfigListEntry, ConfigSelection
from Components.ConfigList import ConfigListScreen
DESKTOP_WIDTH = getDesktop(0).size().width()

class ipk(Screen):
	if DESKTOP_WIDTH <= 1280:
		skin = """
				<screen position="center,center" size="1000,600" flags="wfBorder" title="CreateIPK v1.0" backgroundColor="#515d67">
					<eLabel name="" position="0,0" size="1000,600" backgroundColor="#515d67" transparent="0" zPosition="-10" />
					<eLabel name="" position="10,11" size="980,580" backgroundColor="#3b444b" transparent="0" zPosition="-1" />
					<eLabel name="" position="10,90" size="980,1" backgroundColor="#515d67" transparent="0" zPosition="1" />
					<eLabel name="" position="10,530" size="980,1" backgroundColor="#515d67" transparent="0" zPosition="1" />
					<eLabel name="" text="( i )" position="928,545" size="60,40" font="Regular;25" foregroundColor="#c5c5c5" backgroundColor="#515d67" transparent="1" zPosition="1" halign="center" />
					<widget name="status" position="25,10" size="950,80" transparent="1" font="Regular;22" foregroundColor="#6be1ff" backgroundColor="#3b444b" halign="left" valign="center" />
					<widget name="info" position="25,100" size="950,400" transparent="1" font="Regular;22" foregroundColor="#c5c5c5" backgroundColor="#3b444b" halign="left" valign="top" />
					<eLabel name="" position="25,545" size="10,30" backgroundColor="red" transparent="0" zPosition="3" />
					<eLabel name="" position="248,545" size="10,30" backgroundColor="#ff00" transparent="0" zPosition="3" />
					<eLabel name="" position="475,545" size="10,30" backgroundColor="#ffff00" transparent="0" zPosition="3" />
					<widget source="key_red" render="Label" font="Regular;25" foregroundColor="#ffffff" backgroundColor="#7f0202" position="25,545" size="200,30" halign="center" transparent="0" zPosition="1" />
					<widget source="key_green" render="Label" font="Regular;25" foregroundColor="#ffffff" backgroundColor="#116b07" position="250,545" size="200,30" halign="center" transparent="0" zPosition="1" />
					<widget source="key_yellow" render="Label" font="Regular;25" foregroundColor="#ffffff" backgroundColor="#a08426" position="475,545" size="200,30" halign="center" transparent="0" zPosition="1" />
				</screen>
		"""
	else:
		skin = """
			<screen position="center,center" size="1500,800" flags="wfBorder" title="CreateIPK v1.0" backgroundColor="#515d67">
				<eLabel name="" position="0,0" size="1000,600" backgroundColor="#515d67" transparent="0" zPosition="-10" />
				<eLabel name="" position="10,11" size="1480,780" backgroundColor="#3b444b" transparent="0" zPosition="-1" />
				<eLabel name="" position="10,90" size="1480,2" backgroundColor="#515d67" transparent="0" zPosition="1" />
				<eLabel name="" position="10,700" size="1480,2" backgroundColor="#515d67" transparent="0" zPosition="1" />
				<eLabel name="" text="( i )" position="1425,742" size="60,40" font="Regular;25" foregroundColor="#c5c5c5" backgroundColor="#515d67" transparent="1" zPosition="1" halign="center" />
				<widget name="status" position="25,10" size="1460,80" transparent="1" font="Regular; 25" foregroundColor="#6be1ff" backgroundColor="#3b444b" halign="left" valign="center" />
				<widget name="info" position="25,105" size="1450,575" transparent="1" font="Regular; 28" foregroundColor="#c5c5c5" backgroundColor="#3b444b" halign="left" valign="top" />
				<eLabel name="" position="60,730" size="10,40" backgroundColor="#ff0000" transparent="0" zPosition="3" />
				<eLabel name="" position="430,730" size="10,40" backgroundColor="#00ff00" transparent="0" zPosition="3" />
				<eLabel name="" position="800,730" size="10,40" backgroundColor="#ffff00" transparent="0" zPosition="3" />
				<widget source="key_red" render="Label" font="Regular;30" foregroundColor="#ffffff" backgroundColor="#7f0202" position="57,730" size="300,40" halign="center" transparent="0" zPosition="1" />
				<widget source="key_green" render="Label" font="Regular;30" foregroundColor="#ffffff" backgroundColor="#116b07" position="430,730" size="300,40" halign="center" transparent="0" zPosition="1" />
				<widget source="key_yellow" render="Label" font="Regular;30" foregroundColor="#ffffff" backgroundColor="#a08426" position="800,730" size="300,40" halign="center" transparent="0" zPosition="1" />
			</screen>
	"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self['key_red'] = Label(_('Close'))
		self['key_green'] = Label(_('Create IPK'))
		self['key_yellow'] = Label(_('Install IPK'))

		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"ok": self.cipk,
			"green": self.cipk,
			"yellow": self.iipk,
			"cancel": self.close,
			#"menu": self.st,
			#"info": self.about
		}, -1)
		
		self.delay = eTimer()
		self.delay.start(100, True)
		self['status'] = Label(_('click OK to create ipk...'))
		with open("/usr/lib/enigma2/python/Plugins/Extensions/CreateIPK/help", "r") as h:
			h = h.read()
		self['info'] = Label(_(h))
		self.onLayoutFinish.append(self.strt)

	def strt(self):
		if os.path.ismount('/media/hdd'):
			if not os.path.isdir('/media/hdd/IPKG/CONTROL'):
				os.makedirs('/media/hdd/IPKG/CONTROL')
			if not os.path.isdir('/media/hdd/IPKG/DATA'):
				os.makedirs('/media/hdd/IPKG/DATA')
			if not os.path.isdir('/media/hdd/IPKG/ipk'):
				os.makedirs('/media/hdd/IPKG/ipk')
			if not os.path.exists("/media/hdd/IPKG/debian-binary"):
				db = "2.0\n"
				open("/media/hdd/IPKG/debian-binary","w").write(db)


	def cipk(self):
		if os.path.exists("/media/hdd/IPKG/CONTROL/control"):
			c = open("/media/hdd/IPKG/CONTROL/control", "r").read()
			self['info'].setText(_(c))
		else:
			self['info'].setText(_("files not found !..."))
		#os.system("rm -rf /media/hdd/IPKG/ipk/*.ipk")
		if os.path.exists("/media/hdd/IPKG/CONTROL/control"):
			os.system("tar -C /media/hdd/IPKG/CONTROL -czvf /media/hdd/IPKG/control.tar.gz .")
			f = open("/media/hdd/IPKG/CONTROL/control", "r")
			m = f.readlines()
			f.close()
			for i in m:
				m = i.split()
				if m[0] == "Package:":
					pckg = m[1]
					pckg = ("%s")%pckg
				if m[0] == "Version:":
					ver = m[1]
					ver = ("_%s_")%ver
				if m[0] == "Architecture:":
					arc = m[1]
					arc = ("%s")%arc
					self.ipk_name = pckg + ver + arc + ".ipk"
		else:
			self['info'].setText(_("files not found !..."))
		if os.path.isdir("/media/hdd/IPKG/DATA/usr"):
			os.system("tar -C /media/hdd/IPKG/DATA -czf /media/hdd/IPKG/data.tar.gz .")
		else:
			self['info'].setText(_("files not found !..."))
		if os.path.exists("/media/hdd/IPKG/control.tar.gz"):
			if os.path.exists("/media/hdd/IPKG/data.tar.gz"):
				if os.path.exists("/media/hdd/IPKG/debian-binary"):
					os.system("mv /media/hdd/IPKG/control.tar.gz /")
					os.system("mv /media/hdd/IPKG/data.tar.gz /")
					os.system("mv /media/hdd/IPKG/debian-binary /")
					self.container = eConsoleAppContainer()
					self.container.appClosed.append(self.finished)
					#self.container.execute("tar -cf /packagetemp.tar /control.tar.gz /data.tar.gz /debian-binary; gzip /packagetemp.tar ./%s; mv /packagetemp.tar.gz /%s"%(self.ipk_name, self.ipk_name))
					self.container.execute("ar -r /%s /control.tar.gz /data.tar.gz /debian-binary"%(self.ipk_name))

	def finished(self, retval):
		self.container.kill()
		self['status'].setText(_('ipk successfully created !.. /media/hdd/IPKG/ipk/ ;\n%s'%self.ipk_name))
		os.system('rm -rf /control.tar.gz; rm -rf /data.tar.gz; rm -rf /debian-binary')
		os.system('mv /%s /media/hdd/IPKG/ipk/%s'%(self.ipk_name, self.ipk_name))

	def iipk(self):
		if os.path.exists("/media/hdd/IPKG/CONTROL/control"):
			f = open("/media/hdd/IPKG/CONTROL/control", "r")
			m = f.readlines()
			f.close()
			for i in m:
				m = i.split()
				if m[0] == "Package:":
					pckg = m[1]
					pckg = ("%s")%pckg
				if m[0] == "Version:":
					ver = m[1]
					ver = ("_%s_")%ver
				if m[0] == "Architecture:":
					arc = m[1]
					arc = ("%s")%arc
					self.ipk_name = pckg + ver + arc + ".ipk"
			if os.path.exists("/media/hdd/IPKG/ipk/%s"%self.ipk_name):
				self['status'].setText(_('ipk installing...wait... \n%s'%self.ipk_name))
				shutil.copy2("/media/hdd/IPKG/ipk/%s"%self.ipk_name, "/tmp/")
				#os.system('mv /media/hdd/IPKG/ipk/%s /tmp/%s '%(self.ipk_name, self.ipk_name))
				os.system("opkg install --force-overwrite --force-depends /tmp/%s" %self.ipk_name)
			else:
				self['status'].setText(_("ipk not found !..."))
			self['status'].setText(_('ipk successfully installed... \n%s'%self.ipk_name))
			os.system('rm -rf /tmp/%s'%self.ipk_name)
		else:
			self['status'].setText(_("control file not found !..."))
		
		
	def about(self):
		with open("/usr/lib/enigma2/python/Plugins/Extensions/CreateIPK/help", "r") as h:
			h = h.read()
			self['info'].setText(_(h))






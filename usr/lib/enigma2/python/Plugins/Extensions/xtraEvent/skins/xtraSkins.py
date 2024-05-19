# -*- coding: utf-8 -*-

from Components.config import config

skinColor = "#3478c1"
try:
	skinColor = config.plugins.xtraEvent.skinSelectColor.value
except:
	pass

xtra_720 = """
<screen name="xtra" position="0,0" size="1280,720" title="xtraEvent..." flags="wfNoBorder" backgroundColor="transparent">
	<widget source="Title" render="Label" position="30,30" size="770,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />
	
	<widget name="config" position="30,100" size="770,510" itemHeight="30" font="xtraRegular;20" 
	foregroundColor="#ffffff" foregroundColorSelected="#ffffff" 
	backgroundColor="#30000000" backgroundColorSelected="{0}"
	scrollbarMode="showOnDemand" scrollbarSliderBorderWidth="0" scrollbarSliderBorderColor="#30000000" scrollbarWidth="7" scrollbarSliderForegroundColor="{0}" 
	transparent="1" />
	
	<widget source="help" position="845,560" size="400,52" render="Label" font="xtraRegular;20" foregroundColor="#f3fc92" backgroundColor="#30000000" halign="left" valign="center" transparent="1" />
	<widget name="status" position="845,100" size="400,30" transparent="1" font="xtraRegular;20" foregroundColor="#92f1fc" backgroundColor="#30000000" />
	<widget name="info" position="845,145" size="400,390" transparent="1" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" halign="left" valign="top" zPosition="5" />
	<widget name="int_statu" position="1230,40" size="30,22" font="xtraRegular; 22" foregroundColor="#1edb76" backgroundColor="#23262e" zPosition="2" transparent="1" />
	<eLabel name="int_statu_off" position="1230,40" size="30,22" font="xtraRegular; 22" foregroundColor="#555555" backgroundColor="#23262e" zPosition="1" transparent="1" />
	<eLabel name="red" position="45,680" size="185,10" backgroundColor="#ef2f2f" zPosition="2" />
	<eLabel name="green" position="230,680" size="185,10" backgroundColor="#2fef53" zPosition="2" />
	<eLabel name="yellow" position="415,680" size="185,10" backgroundColor="#edd02f" zPosition="2" />
	<eLabel name="blue" position="600,680" size="185,10" backgroundColor="#2fc7ed" zPosition="2" />
	<widget source="key_red" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="45,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="230,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="416,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 20" foregroundColor="#ffffff" backgroundColor="#30000000" position="600,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="global.CurrentTime" render="Label" position="825,30" size="440,40" font="xtraRegular; 30" halign="center" valign="center" transparent="0" foregroundColor="#ffffff" backgroundColor="{0}" zPosition="0">
		<convert type="ClockToText">Default</convert>
	</widget>
	<ePixmap position="890,240" size="320,232" zPosition="0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film2.png" transparent="1" alphatest="blend" />
	<eLabel name="menu" text="♪" position="845,647" size="100,30" backgroundColor="#30000000" transparent="1" halign="left" font="xtraRegular; 20" />
	<eLabel name="info" text=" " position="1145,647" size="100,30" backgroundColor="#30000000" transparent="1" halign="right" font="xtraRegular; 20" />
	<eLabel name="new eLabel" position="845,680" size="400,10" backgroundColor="#40484c" zPosition="2" />

	<eLabel name="" position="30,30" size="770,660" backgroundColor="#30000000" zPosition="-1" />
	<eLabel name="" position="825,30" size="440,660" backgroundColor="#30000000" zPosition="-1" />
	<!-- <eLabel name="" position="45,90" size="740,2" backgroundColor="#40484c" zPosition="1" /> -->
	<eLabel name="" position="45,620" size="740,2" backgroundColor="#40484c" zPosition="1" />
	<!-- <eLabel name="" position="845,90" size="400,2" backgroundColor="#40484c" zPosition="1" /> -->
	<eLabel name="" position="845,620" size="400,2" backgroundColor="#40484c" zPosition="1" />
	<eLabel name="" position="845,550" size="400,2" backgroundColor="#40484c" zPosition="1" />

    <eLabel name="" position="1100,640" size="50,50" text="1" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />



</screen>""".format(skinColor)

download_720 = """
<screen name="downloads" position="0,0" size="1280,720" title="downloads..." flags="wfNoBorder" backgroundColor="#ff000000">
	<widget source="Title" render="Label" position="250,30" size="770,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />
	
	<widget name="testver" position="30,30" size="250,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />

	<widget name="progress" position="45,100" size="740,20" foregroundColor="#ffffff" borderColor="#ffffff" borderWidth="1" backgroundColor="#30000000" />
	<widget name="status" position="45,130" size="740,30" transparent="1" font="xtraRegular; 22" foregroundColor="#92f1fc" backgroundColor="#30000000" />
	<widget name="info" position="45,170" size="740,60" transparent="1" font="xtraRegular; 22" foregroundColor="#ffffff" backgroundColor="#30000000" valign="top" />
	<widget name="info2" position="45,240" size="740,370" transparent="1" font="xtraRegular; 24" foregroundColor="#ffffff" backgroundColor="#30000000" />
	<widget name="int_statu" position="1230,40" size="30,22" font="xtraRegular; 22" foregroundColor="#1edb76" backgroundColor="#23262e" zPosition="2" transparent="1" />
	<eLabel name="int_statu_off" position="1230,40" size="30,22" font="xtraRegular; 22" foregroundColor="#555555" backgroundColor="#23262e" zPosition="1" transparent="1" />
	<eLabel name="red" position="45,680" size="185,10" backgroundColor="#ef2f2f" zPosition="2" />
	<eLabel name="green" position="230,680" size="185,10" backgroundColor="#2fef53" zPosition="2" />
	<eLabel name="yellow" position="415,680" size="185,10" backgroundColor="#edd02f" zPosition="2" />
	<eLabel name="blue" position="600,680" size="185,10" backgroundColor="#2fc7ed" zPosition="2" />
	<widget source="key_red" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="45,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="230,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="416,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 20" foregroundColor="#ffffff" backgroundColor="#30000000" position="600,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="global.CurrentTime" render="Label" position="825,30" size="440,40" font="xtraRegular; 30" halign="center" valign="center" transparent="0" foregroundColor="#ffffff" backgroundColor="{0}" zPosition="0">
		<convert type="ClockToText">Default</convert>
	</widget>
	<eLabel name="" position="45,620" size="740,2" backgroundColor="#666666" zPosition="1" />
	<!-- <ePixmap position="890,100" size="320,232" zPosition="0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film2.png" transparent="1" alphatest="blend" /> -->
	<widget name="Picture" position="890,240" size="400,278" zPosition="9" transparent="1" />
	<widget name="Picture2" position="890,240" size="320,232" zPosition="1" transparent="1" alphatest="blend" />
	<eLabel name="" position="30,30" size="770,660" backgroundColor="#30000000" zPosition="-1" />
	<eLabel name="" position="825,30" size="440,660" backgroundColor="#30000000" zPosition="-1" />

     <eLabel name="" position="1100,640" size="50,50" text="2" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />

</screen>""".format(skinColor)

manuel_720 = """
<screen name="manuelSearch" position="center,center" size="1280,720" title="Manuel Search..." backgroundColor="transparent" flags="wfNoBorder">
	<widget source="Title" render="Label" position="250,30" size="770,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />
	
	<widget name="testver" position="30,30" size="250,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />

	
	<widget source="session.CurrentService" render="Label" position="45,100" size="740,40" zPosition="1" font="xtraRegular; 30" transparent="1" backgroundColor="30000000" valign="center">
		<convert type="ServiceName">Name</convert>
	</widget>
	<widget name="config" position="45,145" size="740,391" itemHeight="30" font="xtraRegular;22" foregroundColor="#ffffff" scrollbarMode="showOnDemand" transparent="1" backgroundColor="30000000" backgroundColorSelected="{0}" foregroundColorSelected="#ffffff" />
	<widget name="status" position="45,585" size="740,30" transparent="1" font="xtraRegular;22" foregroundColor="#92f1fc" backgroundColor="30000000" />
	<widget name="info" position="840,640" size="400,30" transparent="1" font="xtraRegular;22" halign="center" foregroundColor="#ffffff" backgroundColor="30000000" />
	<widget name="int_statu" position="1230,40" size="30,22" font="xtraRegular; 22" foregroundColor="#1edb76" backgroundColor="#23262e" zPosition="2" transparent="1" />
	<eLabel name="int_statu_off" position="1230,40" size="30,22" font="xtraRegular; 22" foregroundColor="#555555" backgroundColor="#23262e" zPosition="1" transparent="1" />
	<widget name="progress" position="45,555" size="740,20" foregroundColor="#ffffff" borderColor="#ffffff" borderWidth="1"  backgroundColor="#30000000" />

	<eLabel name="red" position="45,680" size="185,10" backgroundColor="#ef2f2f" zPosition="2" />
	<eLabel name="green" position="230,680" size="185,10" backgroundColor="#2fef53" zPosition="2" />
	<eLabel name="yellow" position="415,680" size="185,10" backgroundColor="#edd02f" zPosition="2" />
	<eLabel name="blue" position="600,680" size="185,10" backgroundColor="#2fc7ed" zPosition="2" />
	<widget source="key_red" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="45,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="230,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="416,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 20" foregroundColor="#ffffff" backgroundColor="#30000000" position="600,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="global.CurrentTime" render="Label" position="825,30" size="440,40" font="xtraRegular; 30" halign="center" valign="center" transparent="0" foregroundColor="#ffffff" backgroundColor="{0}" zPosition="0">
		<convert type="ClockToText">Default</convert>
	</widget>
	<!-- <eLabel name="" position="45,620" size="740,2" backgroundColor="#666666" zPosition="1" /> -->
	<!-- <ePixmap position="890,100" size="320,232" zPosition="0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film2.png" transparent="1" alphatest="blend" /> -->
	<widget name="Picture" position="890,240" size="400,278" zPosition="2" transparent="1" />
	<widget name="Picture2" position="890,240" size="320,232" zPosition="1" transparent="1" alphatest="blend" />
	<eLabel name="" position="30,30" size="770,660" backgroundColor="#30000000" zPosition="-1" />
	<eLabel name="" position="825,30" size="440,660" backgroundColor="#30000000" zPosition="-1" />
	<!-- <eLabel name="" position="45,90" size="740,2" backgroundColor="#666666" zPosition="1" /> -->
	<eLabel name="" position="45,620" size="740,2" backgroundColor="#666666" zPosition="1" />
	<!-- <eLabel name="" position="845,90" size="400,2" backgroundColor="#666666" zPosition="1" /> -->
	<eLabel name="" position="845,620" size="400,2" backgroundColor="#666666" zPosition="1" />

  
	<eLabel name="" position="1100,640" size="50,50" text="3" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />

</screen>""".format(skinColor)

selbuq_720 = """
<screen name="selBouquets" position="0,0" size="1280,720" title="bouquets..." backgroundColor="transparent">
	<widget source="Title" render="Label" position="250,30" size="770,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />
	
	<widget name="testver" position="30,30" size="250,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />

	
	<widget name="list" position="30,100" size="770,510" itemHeight="45" font="xtraRegular;22" foregroundColor="#ffffff" 
	scrollbarMode="showOnDemand" scrollbarSliderBorderWidth="0" scrollbarSliderBorderColor="back_color" 
	scrollbarWidth="10" scrollbarSliderForegroundColor="{0}"  
	transparent="1" backgroundColor="#30000000" backgroundColorSelected="{0}" foregroundColorSelected="#ffffff" />

	<eLabel name="red" position="45,680" size="185,10" backgroundColor="#ef2f2f" zPosition="2" />
	<eLabel name="green" position="230,680" size="185,10" backgroundColor="#2fef53" zPosition="2" />
	<eLabel name="yellow" position="415,680" size="185,10" backgroundColor="#edd02f" zPosition="2" />
	<eLabel name="blue" position="600,680" size="185,10" backgroundColor="#2fc7ed" zPosition="2" />
	<widget source="key_red" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="45,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="230,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;20" foregroundColor="#ffffff" backgroundColor="#30000000" position="416,647" size="185,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 20" foregroundColor="#ffffff" backgroundColor="#30000000" position="600,647" size="185,30" halign="center" transparent="1" zPosition="1" />

	

	<widget source="global.CurrentTime" render="Label" position="825,30" size="440,40" font="xtraRegular; 30" halign="center" valign="center" transparent="0" foregroundColor="#ffffff" backgroundColor="{0}" zPosition="0">
		<convert type="ClockToText">Default</convert>
	</widget>
	<eLabel name="" position="45,620" size="740,2" backgroundColor="#666666" zPosition="1" />
	<ePixmap position="890,240" size="320,232" zPosition="0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film2.png" transparent="1" alphatest="blend" />

	<eLabel name="" position="30,30" size="770,660" backgroundColor="#30000000" zPosition="-1" />
	<eLabel name="" position="825,30" size="440,660" backgroundColor="#30000000" zPosition="-1" />

	<widget name="statussearchold" foregroundColor="#0000ff00" font="Regular; 35" position="300,470" size="400,300" transparent="1" zPosition="3" halign="center" valign="center" backgroundColor="#3a3998"  />
 
	 <eLabel name="" position="1100,640" size="50,50" text="4" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />

</screen>""".format(skinColor)


xtra_720_2 = """
<screen name="xtra" position="0,0" size="1280,720" title="xtraEvent..." flags="wfNoBorder">
	<ePixmap position="0,0" size="1280,720" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_hd3.png" transparent="1" />
	<widget source="Title" render="Label" position="250,35" size="745,40" font="xtraRegular; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
	
	<widget name="testver" position="40,30" size="250,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />
	
	<widget name="config" position="40,95" size="745,510" itemHeight="30" font="xtraRegular;24" 
	foregroundColor="#c5c5c5" foregroundColorSelected="#ffffff" 
	backgroundColor="#23262e" backgroundColorSelected="#565d6d" 
	selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/sel_xtra_hd3.png" 
	scrollbarMode="showOnDemand" scrollbarSliderBorderWidth="0" scrollbarSliderBorderColor="#23262e" 
	scrollbarWidth="7" scrollbarSliderForegroundColor="#565d6d" 
	transparent="1" />
	
	<widget source="help" position="840,600" size="400,26" render="Label" font="xtraRegular;22" foregroundColor="#f3fc92" backgroundColor="#23262e" halign="left" valign="center" transparent="1" />
	<widget name="status" position="840,300" size="400,30" transparent="1" font="xtraRegular;22" foregroundColor="#92f1fc" backgroundColor="#23262e" />
	<widget name="info" position="840,330" size="400,260" transparent="1" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" halign="left" valign="top" />
	<widget name="int_statu" position="1210,40" size="30,22" transparent="1" font="xtraRegular; 22" foregroundColor="#1edb76" backgroundColor="#23262e" zPosition="2" halign="center" />
	<eLabel name="int_statu_off" position="1210,40" size="30,22" font="xtraRegular; 22" foregroundColor="#555555" backgroundColor="#23262e" zPosition="1" transparent="1" /> 
	<widget source="key_red" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="55,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="245,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="435,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 20" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="625,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="global.CurrentTime" render="Label" position="839,40" size="400,30" font="xtraRegular; 25" valign="center" halign="center" transparent="1" foregroundColor="#c5c5c5" backgroundColor="#23262e" zPosition="2">
		<convert type="ClockToText">Default</convert>
	</widget>
	<eLabel name="menu" text="♪" position="785,640" size="150,30" transparent="1" halign="center" font="xtraRegular; 20" />
	<eLabel name="info" text="█" position="1175,640" size="100,30" transparent="1" halign="center" font="xtraRegular; 20" />
  
    <eLabel name="" position="1100,640" size="50,50" text="5" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />

</screen>"""
download_720_2 = """
<screen name="downloads" position="0,0" size="1280,720" title="downloads..." flags="wfNoBorder" backgroundColor="transparent">
	<ePixmap position="0,0" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_hd3.png" zPosition="-1" transparent="1" />
	<widget source="Title" render="Label" position="40,35" size="745,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="#23262e" transparent="1" />
	<widget name="progress" position="40,100" size="740,20" foregroundColor="#ffffff" borderColor="#ffffff" borderWidth="1" backgroundColor="#23262e" />
	<widget name="status" position="40,130" size="740,30" transparent="1" font="xtraRegular; 24" foregroundColor="#92f1fc" backgroundColor="#23262e" />
	<widget name="info" position="40,175" size="740,40" transparent="1" font="xtraRegular; 24" foregroundColor="#ffffff" backgroundColor="#23262e" valign="top" />
	<widget name="info2" position="40,220" size="740,400" transparent="1" font="xtraRegular; 24" foregroundColor="#ffffff" backgroundColor="#23262e" />
	<widget source="key_red" render="Label" font="xtraRegular;22" foregroundColor="#ffffff" backgroundColor="#23262e" position="55,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;22" foregroundColor="#ffffff" backgroundColor="#23262e" position="245,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;22" foregroundColor="#ffffff" backgroundColor="#23262e" position="435,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 20" foregroundColor="#ffffff" backgroundColor="#23262e" position="625,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="global.CurrentTime" render="Label" position="839,40" size="400,30" font="xtraRegular; 25" valign="center" halign="center" transparent="1" foregroundColor="#ffffff" backgroundColor="#23262e" zPosition="2">
		<convert type="ClockToText">Default</convert>
	</widget>
	<widget name="int_statu" position="1210,40" size="30,22" transparent="1" font="xtraRegular; 22" foregroundColor="#1edb76" backgroundColor="#23262e" zPosition="2" halign="center" />
	<eLabel name="int_statu_off" position="1210,40" size="30,22" font="xtraRegular; 22" foregroundColor="#555555" backgroundColor="#23262e" zPosition="1" transparent="1" />
	<widget name="Picture" position="840,324" size="400,278" zPosition="9" transparent="1" />
	<!-- <widget name="Picture2" position="892,343" size="320,232" zPosition="1" transparent="1" alphatest="blend" /> -->
 <widget source="key_1" render="Label" font="xtraRegular; 25" foregroundColor="#ffffff" backgroundColor="#30000000" position="16,678" size="175,30" halign="left" transparent="1" zPosition="1" />	
	
	<widget source="key_2" render="Label" font="xtraRegular; 25" foregroundColor="#ffffff" backgroundColor="#30000000" position="202,678" size="175,30" halign="left" transparent="1" zPosition="1" />	

	<widget source="key_3" render="Label" font="xtraRegular; 25" foregroundColor="#ffffff" backgroundColor="#30000000" position="394,678" size="175,30" halign="left" transparent="1" zPosition="1" />	

	<widget source="key_4" render="Label" font="xtraRegular; 25" foregroundColor="#ffffff" backgroundColor="#30000000" position="583,678" size="175,30" halign="left" transparent="1" zPosition="1" />	

    <widget source="key_5" render="Label" font="xtraRegular; 25" foregroundColor="#ffffff" backgroundColor="#30000000" position="769,678" size="175,30" halign="left" transparent="1" zPosition="1" />	

	<eLabel name="" position="840,100" size="250,30" text="Anzahl" font="Regular; 25" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />

	<eLabel name="" position="840,140" size="250,30" text="Poster :     " font="Regular; 25" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />
	<widget name="infoposter" position="1100,140" size="100,30" transparent="1" font="xtraRegular; 25" foregroundColor="#ffffff" backgroundColor="#30000000" valign="top" />
	
	<eLabel name="" position="840,180" size="250,30" text="Backdrop :     " font="Regular; 25" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />
	<widget name="infobackdrop" position="1100,180" size="100,30" transparent="1" font="xtraRegular; 25" foregroundColor="#ffffff" backgroundColor="#30000000" valign="top" />

	<eLabel name="" position="840,220" size="250,40" text="Banner :     " font="Regular; 25" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />
	<widget name="infobanner" position="1100,220" size="100,30" transparent="1" font="xtraRegular; 25" foregroundColor="#ffffff" backgroundColor="#30000000" valign="top" />

	<eLabel name="" position="840,260" size="250,30" text="Infos :     " font="Regular; 25" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />
	<widget name="infoinfos" position="1100,260" size="100,30" transparent="1" font="xtraRegular; 25" foregroundColor="#ffffff" backgroundColor="#30000000" valign="top" />
	
    
  <eLabel name="" position="1218,658" size="50,50" text="6" font="Regular; 35" halign="left" backgroundColor="3-Buttonshadowfarbe" foregroundColor="lightgreen" />

</screen>"""
manuel_720_2 = """
<screen name="manuelSearch" position="center,center" size="1280,720" title="Manuel Search..." backgroundColor="transparent" flags="wfNoBorder">
	<ePixmap position="0,0" size="1280,720" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_hd3.png" transparent="1" />
	<widget source="Title" render="Label" position="250,40" size="745,40" font="xtraRegular; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
	
	<widget name="testver" position="40,30" size="250,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />

	
	<widget source="session.CurrentService" render="Label" position="40,80" size="745,40" zPosition="1" font="xtraRegular; 30" transparent="1" backgroundColor="#23262e" valign="center">
		<convert type="ServiceName">Name</convert>
	</widget>
	
	<widget name="config" position="40,95" size="745,390" itemHeight="30" font="xtraRegular;24" 
	foregroundColor="#c5c5c5" foregroundColorSelected="#ffffff" 
	backgroundColor="#23262e" backgroundColorSelected="#565d6d" 
	selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/sel_xtra_hd3.png" 
	scrollbarMode="showOnDemand" scrollbarSliderBorderWidth="0" scrollbarSliderBorderColor="#23262e" 
	scrollbarWidth="7" scrollbarSliderForegroundColor="#565d6d" 
	transparent="1" />
	
	<widget name="status" position="40,590" size="745,30" transparent="1" font="xtraRegular;24" foregroundColor="#92f1fc" backgroundColor="#23262e" />
	<widget name="info" position="840,640" size="400,30" transparent="1" font="xtraRegular;22" halign="center" foregroundColor="#c5c5c5" backgroundColor="#23262e" />
	<widget name="Picture" position="840,320" size="185,278" zPosition="5" transparent="1" />
	<widget name="progress" position="40,560" size="745,20" foregroundColor="prgrsbs" borderColor="prgrsbs" borderWidth="1"  backgroundColor="#23262e" />
	<widget source="key_red" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="55,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="245,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="435,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="625,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<eLabel name="" position="40,120" size="745, 1" backgroundColor="#898989" />
	<widget name="int_statu" position="1210,40" size="30,22" transparent="1" font="xtraRegular; 22" foregroundColor="#1edb76" backgroundColor="#23262e" zPosition="2" halign="center" />
	<eLabel name="int_statu_off" position="1210,40" size="30,22" font="xtraRegular; 22" foregroundColor="#555555" backgroundColor="#23262e" zPosition="1" transparent="1" />
    
	<eLabel name="" position="1100,640" size="50,50" text="7" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />

</screen>"""		
selbuq_720_2 = """
<screen name="selBouquets" position="center,center" size="1280,720" title="xtraEvent v1" backgroundColor="#ffffff">
	<ePixmap position="0,0" size="1280,720" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_hd3.png" transparent="1" />
	<widget source="Title" render="Label" position="250,35" size="745,40" font="xtraRegular; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
	
	<widget name="testver" position="40,30" size="250,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />

	<widget name="list" position="40,95" size="745,510" itemHeight="45" font="xtraRegular;24" foregroundColor="#c5c5c5" 
	scrollbarMode="showOnDemand" scrollbarSliderBorderWidth="0" scrollbarSliderBorderColor="#23262e" scrollbarWidth="7" 
	selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/sel_xtra_hd3.png" 
	scrollbarSliderForegroundColor="#0d71aa"  transparent="1" backgroundColor="#23262e" backgroundColorSelected="#0d71aa" foregroundColorSelected="#ffffff" />

	<widget name="status" position="840,300" size="400,30" transparent="1" font="xtraRegular;22" foregroundColor="#92f1fc" backgroundColor="#23262e" />
	<widget name="info" position="840,330" size="400,270" transparent="1" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" halign="left" valign="top" />
	<widget source="key_red" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="55,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="245,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="435,640" size="170,30" halign="left" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular;22" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="625,640" size="170,30" halign="left" transparent="1" zPosition="1" />
   
	<widget name="statussearchold" foregroundColor="#0000ff00" font="Regular; 35" position="300,470" size="400,300" transparent="1" zPosition="3" halign="center" valign="center" backgroundColor="#3a3998"  />

	<eLabel name="" position="1100,640" size="50,50" text="8" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />

</screen>"""


xtra_1080 = """
<screen name="xtra" position="0,0" size="1920,1080" title="xtraEvent..." flags="wfNoBorder" backgroundColor="transparent">
	<widget source="Title" render="Label" position="30,30" size="1165,60" font="xtraRegular; 34" halign="center" valign="center" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" />
	<!-- <ePixmap position="620,30" size="330,70" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_title.png" transparent="1" alphatest="blend" /> -->
	
	<widget name="config" position="30,140" size="1165,800" itemHeight="45" font="xtraRegular;34" foregroundColor="#ffffff" 
	scrollbarMode="showOnDemand" scrollbarSliderBorderWidth="0" scrollbarSliderBorderColor="#ef2f2f" 
	scrollbarWidth="5" scrollbarSliderForegroundColor="{0}"  transparent="1" 
	backgroundColor="#30000000" backgroundColorSelected="{0}" foregroundColorSelected="#ffffff" />

	<widget source="help" position="1255,860" size="600,100" render="Label" font="xtraRegular;28" foregroundColor="#f3fc92" backgroundColor="#30000000" halign="left" valign="center" transparent="1" />
	<widget name="status" position="1255,140" size="600,45" transparent="1" font="xtraRegular;32" foregroundColor="#92f1fc" backgroundColor="#30000000" />
	<widget name="info" position="1255,220" size="600,600" transparent="1" font="xtraRegular;32" foregroundColor="#ffffff" backgroundColor="#30000000" halign="left" valign="top" zPosition="1" />

	<eLabel name="red" position="60,1040" size="275,10" backgroundColor="#ef2f2f" zPosition="2" />
	<eLabel name="green" position="335,1040" size="275,10" backgroundColor="#2fef53" zPosition="2" />
	<eLabel name="yellow" position="610,1040" size="275,10" backgroundColor="#edd02f" zPosition="2" />
	<eLabel name="blue" position="885,1040" size="275,10" backgroundColor="#2fc7ed" zPosition="2" />
	<widget source="key_red" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="70,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="345,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="620,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 26" foregroundColor="#ffffff" backgroundColor="#30000000" position="895,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="global.CurrentTime" render="Label" position="1220,30" size="670,60" font="xtraRegular; 34" valign="center" halign="center" transparent="0" foregroundColor="#ffffff" backgroundColor="{0}" zPosition="2">
		<convert type="ClockToText">Default</convert>
	</widget>
	
	<widget name="int_statu" font="xtraRegular; 30" position="1835,40" size="40,40" foregroundColor="#1edb76" backgroundColor="{0}" zPosition="2" transparent="1" />
	<eLabel name="int_statu_off" font="xtraRegular; 30" position="1840,35" size="40,40" foregroundColor="#555555" backgroundColor="{0}" zPosition="1" transparent="1" />	
	<eLabel name="menu" text="♪" position="1255,1000" size="40,40" backgroundColor="#30000000" transparent="1" halign="left" font="xtraRegular; 40" />
	<eLabel name="info" text="█" position="1815,1000" size="40,40" backgroundColor="#30000000" transparent="1" halign="right" font="xtraRegular; 40" />

	<eLabel name="new eLabel" position="1255,1040" size="600,10" backgroundColor="#40484c" zPosition="2" />
	<eLabel name="" position="30,30" size="1165,1020" backgroundColor="#30000000" zPosition="-1" />
	<eLabel name="" position="1220,30" size="670,1020" backgroundColor="#30000000" zPosition="-1" />
	<!-- <eLabel name="" position="30,30" size="1165,60" backgroundColor="{0}" zPosition="1" /> -->
	<eLabel name="" position="60,970" size="1100,2" backgroundColor="#666666" zPosition="1" />
	<!-- <eLabel name="" position="1260,130" size="600,2" backgroundColor="#666666" zPosition="1" /> -->
	<eLabel name="" position="1255,845" size="600,2" backgroundColor="#666666" zPosition="1" />
	<eLabel name="" position="1255,970" size="600,2" backgroundColor="#666666" zPosition="1" />
	<ePixmap position="1410,413" size="320,232" zPosition="0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film2.png" transparent="1" alphatest="blend" />

    <eLabel name="" position="1800,1000" size="50,50" text="9" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />

</screen>""".format(skinColor)
# --------------------------------------------------------------------------------------------------------------------------------------
download_1080 = """	
<screen name="downloads" position="0,0" size="1920,1080" title="downloads..." flags="wfNoBorder" backgroundColor="transparent">
	<widget source="Title" render="Label" position="250,30" size="1165,60" font="xtraRegular; 45" halign="center" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" />
	
	<widget name="testver" position="30,30" size="250,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />

	<widget name="progress" position="60,148" size="1100,20" foregroundColor="#ffffff" borderColor="#ffffff" borderWidth="1" backgroundColor="#30000000" />
	<widget name="status" position="60,190" size="1100,144" transparent="1" font="xtraRegular;30" foregroundColor="#92f1fc" backgroundColor="#30000000" />

	<eLabel name="red" position="60,1040" size="275,10" backgroundColor="#ef2f2f" zPosition="2" />
	<eLabel name="green" position="335,1040" size="275,10" backgroundColor="#2fef53" zPosition="2" />
	<eLabel name="yellow" position="610,1040" size="275,10" backgroundColor="#edd02f" zPosition="2" />
	<eLabel name="blue" position="885,1040" size="275,10" backgroundColor="#2fc7ed" zPosition="2" />
	<widget source="key_red" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="70,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="345,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="620,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 26" foregroundColor="#ffffff" backgroundColor="#30000000" position="895,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	
	<widget source="global.CurrentTime" render="Label" position="1220,30" size="670,60" font="xtraRegular; 34" valign="center" halign="center" transparent="0" foregroundColor="#ffffff" backgroundColor="{0}" zPosition="2">
		<convert type="ClockToText">Default</convert>
	</widget>
	<widget name="Picture" position="1258,400" size="596,278" zPosition="2" transparent="1" />
	<widget name="Picture2" position="1410,400" size="320,232" zPosition="1" transparent="1" alphatest="blend" />
	
	<eLabel name="" position="30,30" size="1165,1020" backgroundColor="#30000000" zPosition="-1" />
	<eLabel name="" position="1220,30" size="670,1020" backgroundColor="#30000000" zPosition="-1" />
	<!-- <eLabel name="" position="60,130" size="1100,2" backgroundColor="#666666" zPosition="1" /> -->
	<eLabel name="" position="60,950" size="1100,2" backgroundColor="#666666" zPosition="1" />
	<!-- <eLabel name="" position="1260,130" size="600,2" backgroundColor="#666666" zPosition="1" /> -->
	<eLabel name="" position="1260,950" size="600,2" backgroundColor="#666666" zPosition="1" />
	<!-- <ePixmap position="1410,120" size="320,232" zPosition="0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film2.png" transparent="1" alphatest="blend" /> -->

	<widget name="info" position="60,270" size="1100,94" transparent="1" font="xtraRegular;30" foregroundColor="#ffffff" backgroundColor="#30000000" valign="top" />
	<widget name="info2" position="60,385" size="1100,550" transparent="1" font="xtraRegular; 33" foregroundColor="#ffffff" backgroundColor="#30000000" />
	<widget name="int_statu" font="xtraRegular; 30" position="1835,40" size="40,40" foregroundColor="#1edb76" backgroundColor="{0}" zPosition="2" transparent="1" />
	<eLabel name="int_statu_off" font="xtraRegular; 30" position="1840,35" size="40,40" foregroundColor="#555555" backgroundColor="{0}" zPosition="1" transparent="1" />
	
	<widget source="key_1" render="Label" font="xtraRegular;35" foregroundColor="#ffffff" backgroundColor="#30000000" position="1300,700" size="375,50" halign="left" transparent="1" zPosition="1" />	
	
	<widget source="key_2" render="Label" font="xtraRegular;35" foregroundColor="#ffffff" backgroundColor="#30000000" position="1300,750" size="375,50" halign="left" transparent="1" zPosition="1" />	

	<widget source="key_3" render="Label" font="xtraRegular;35" foregroundColor="#ffffff" backgroundColor="#30000000" position="1300,800" size="375,50" halign="left" transparent="1" zPosition="1" />	

	<widget source="key_4" render="Label" font="xtraRegular;35" foregroundColor="#ffffff" backgroundColor="#30000000" position="1300,850" size="375,50" halign="left" transparent="1" zPosition="1" />	

    <widget source="key_5" render="Label" font="xtraRegular;35" foregroundColor="#ffffff" backgroundColor="#30000000" position="1300,900" size="375,50" halign="left" transparent="1" zPosition="1" />	

	<eLabel name="" position="1300,100" size="250,50" text="Anzahl" font="Regular; 35" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />

	<eLabel name="" position="1300,150" size="250,50" text="Poster :     " font="Regular; 35" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />
	<widget name="infoposter" position="1600,150" size="100,50" transparent="1" font="xtraRegular;35" foregroundColor="#ffffff" backgroundColor="#30000000" valign="top" />
	
	<eLabel name="" position="1300,200" size="250,50" text="Backdrop :     " font="Regular; 35" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />
	<widget name="infobackdrop" position="1600,200" size="100,50" transparent="1" font="xtraRegular;35" foregroundColor="#ffffff" backgroundColor="#30000000" valign="top" />

	<eLabel name="" position="1300,250" size="250,50" text="Banner :     " font="Regular; 35" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />
	<widget name="infobanner" position="1600,250" size="100,50" transparent="1" font="xtraRegular;35" foregroundColor="#ffffff" backgroundColor="#30000000" valign="top" />

	<eLabel name="" position="1300,300" size="250,50" text="Infos :     " font="Regular; 35" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />
	<widget name="infoinfos" position="1600,300" size="100,50" transparent="1" font="xtraRegular;35" foregroundColor="#ffffff" backgroundColor="#30000000" valign="top" />
	
    <eLabel name="" position="1800,1000" size="50,50" text="10" font="Regular; 35" halign="left" backgroundColor="#30000000" foregroundColor="#0000ff00" />

</screen>""".format(skinColor)






manuel_1080 = """
<screen name="manuelSearch" position="center,center" size="1920,1080" title="Manuel Search..." backgroundColor="transparent" flags="wfNoBorder">

	<widget source="Title" render="Label" position="250,30" size="1165,60" font="xtraRegular; 45" halign="center"  foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" />

	<widget name="testver" position="30,30" size="250,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />

<widget source="session.CurrentService" render="Label" position="60,145" size="1100,60" zPosition="2" font="xtraRegular; 45" transparent="1" backgroundColor="#30000000" valign="center">
		<convert type="ServiceName">Name</convert>
	</widget>
	
<widget name="config" position="60,225" size="1100,588" itemHeight="45" font="xtraRegular;36" foregroundColor="#ffffff" scrollbarMode="showOnDemand" transparent="1" backgroundColor="#30000000" backgroundColorSelected="{0}" foregroundColorSelected="#ffffff" />

	<widget name="status" position="60,885" size="1100,40" transparent="1" font="xtraRegular;36" foregroundColor="#92f1fc" backgroundColor="#30000000" />

	<widget name="info" position="1260,965" size="600,45" transparent="1" font="xtraRegular;30" halign="center" foregroundColor="#ffffff" backgroundColor="#30000000" />
	
	<widget name="Picture2" position="1510,300" size="320,232" zPosition="1" transparent="1" alphatest="blend" />

	<widget name="Picture" position="1060,720" size="133,200" zPosition="5" transparent="1" alphatest="blend" />
	
	<widget name="progress" position="60,840" size="1100,20" foregroundColor="#ffffff" borderColor="#ffffff" borderWidth="1"  backgroundColor="#30000000" />

	<widget name="int_statu" font="xtraRegular; 30" position="1835,40" size="40,40" foregroundColor="#1edb76" backgroundColor="{0}" zPosition="2" transparent="1" />
	<eLabel name="int_statu_off" font="xtraRegular; 30" position="1840,35" size="40,40" foregroundColor="#555555" backgroundColor="{0}" zPosition="1" transparent="1" />

	<eLabel name="red" position="60,1040" size="275,10" backgroundColor="#ef2f2f" zPosition="2" />
	<eLabel name="green" position="336,1040" size="275,10" backgroundColor="#2fef53" zPosition="2" />
	<eLabel name="yellow" position="610,1040" size="275,10" backgroundColor="#edd02f" zPosition="2" />
	<eLabel name="blue" position="885,1040" size="275,10" backgroundColor="#2fc7ed" zPosition="2" />

	<widget source="key_red" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="70,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="345,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="620,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 26" foregroundColor="#ffffff" backgroundColor="#30000000" position="895,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	
    <widget source="global.CurrentTime" render="Label" position="1220,30" size="670,60" font="xtraRegular; 34" valign="center" halign="center" transparent="0" foregroundColor="#ffffff" backgroundColor="{0}" zPosition="2">
		<convert type="ClockToText">Default</convert>
	</widget>

	<eLabel name="" position="30,30" size="1165,1020" backgroundColor="#30000000" zPosition="-1" />
	<eLabel name="" position="1220,30" size="670,1020" backgroundColor="#30000000" zPosition="-1" />
	<!-- <eLabel name="" position="60,130" size="1100,2" backgroundColor="#666666" zPosition="1" /> -->
	<eLabel name="" position="60,950" size="1100,2" backgroundColor="#666666" zPosition="1" />
	<!-- <eLabel name="" position="1260,130" size="600,2" backgroundColor="#666666" zPosition="1" /> -->
	<eLabel name="" position="1260,950" size="600,2" backgroundColor="#666666" zPosition="1" />
	
    <eLabel name="" position="1256,130" size="600,50" text="For EMC Movie search " font="Regular; 30" halign="left" backgroundColor="3-Buttonshadowfarbe" foregroundColor="lightgreen" transparent="1" />
    <eLabel name="" position="1256,230" size="600,50" text="Movie search " font="Regular; 30" halign="left" backgroundColor="3-Buttonshadowfarbe" foregroundColor="lightgreen" transparent="1" />
	<eLabel name="" position="1256,270" size="600,50" text="left - right Title" font="Regular; 30" halign="left" backgroundColor="3-Buttonshadowfarbe" foregroundColor="lightgreen" transparent="1" />
	<eLabel name="" position="1256,320" size="600,50" text="path Movies " font="Regular; 30" halign="left" backgroundColor="3-Buttonshadowfarbe" foregroundColor="lightgreen" transparent="1" />
	<eLabel name="" position="1256,540" size="600,50" text="search Movie " font="Regular; 30" halign="left" backgroundColor="3-Buttonshadowfarbe" foregroundColor="lightgreen" transparent="1" />
	<eLabel name="" position="1256,670" size="600,50" text="left-right Poster/Backdrop search " font="Regular; 30" halign="left" backgroundColor="3-Buttonshadowfarbe" foregroundColor="lightgreen" transparent="1" />
	<eLabel name="" position="1256,1000" size="540,50" text="yellow Poster/Backdrop save " font="Regular; 30" halign="left" backgroundColor="3-Buttonshadowfarbe" foregroundColor="lightgreen" transparent="1" />
    <eLabel name="" position="1800,1000" size="50,50" text="11" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />


</screen>""".format(skinColor)

selbuq_1080 = """
<screen name="selBouquets" position="center,center" size="1920,1080" title="xtraEvent" backgroundColor="transparent">
	<widget source="Title" render="Label" position="250,30" size="1165,60" font="xtraRegular; 45" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />
	
	<widget name="testver" position="30,30" size="250,40" font="xtraRegular; 30" foregroundColor="#ffffff" backgroundColor="{0}" transparent="0" halign="center" valign="center" />

	<widget name="list" position="30,140" size="1165,765" itemHeight="45" font="xtraRegular;36" foregroundColor="#ffffff" 
		scrollbarMode="showOnDemand" scrollbarSliderBorderWidth="0" scrollbarSliderBorderColor="#30000000" 
		scrollbarWidth="5" scrollbarSliderForegroundColor="{0}"  transparent="1" 
		backgroundColor="#30000000" backgroundColorSelected="{0}" foregroundColorSelected="#ffffff" />
	<widget name="status" position="1260,450" size="600,45" transparent="1" font="xtraRegular;30" foregroundColor="#92f1fc" backgroundColor="#30000000" />
	<widget name="info" position="1260,495" size="600,405" transparent="1" font="xtraRegular;30" foregroundColor="#ffffff" backgroundColor="#30000000" halign="left" valign="top" />
	<eLabel name="red" position="60,1040" size="275,10" backgroundColor="#ef2f2f" zPosition="2" />
	<eLabel name="green" position="335,1040" size="275,10" backgroundColor="#2fef53" zPosition="2" />
	<eLabel name="yellow" position="610,1040" size="275,10" backgroundColor="#edd02f" zPosition="2" />
	<eLabel name="blue" position="885,1040" size="275,10" backgroundColor="#2fc7ed" zPosition="2" />
	<widget source="key_red" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="70,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="345,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;26" foregroundColor="#ffffff" backgroundColor="#30000000" position="620,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 26" foregroundColor="#ffffff" backgroundColor="#30000000" position="895,1010" size="275,30" halign="center" transparent="1" zPosition="1" />
	<widget source="global.CurrentTime" render="Label" position="1220,30" size="670,60" font="xtraRegular; 34" valign="center" halign="center" transparent="0" foregroundColor="#ffffff" backgroundColor="{0}" zPosition="2">
		<convert type="ClockToText">Default</convert>
	</widget>
	<eLabel name="" position="30,30" size="1165,1020" backgroundColor="#30000000" zPosition="-1" />
	<eLabel name="" position="1220,30" size="670,1020" backgroundColor="#30000000" zPosition="-1" />
	<!-- <eLabel name="" position="60,130" size="1100,2" backgroundColor="#666666" zPosition="1" /> -->
	<eLabel name="" position="60,950" size="1100,2" backgroundColor="#666666" zPosition="1" />
	<!-- <eLabel name="" position="1260,130" size="600,2" backgroundColor="#666666" zPosition="1" /> -->
	<!-- <eLabel name="" position="1260,840" size="600,2" backgroundColor="#666666" zPosition="1" /> -->
	<eLabel name="" position="1260,950" size="600,2" backgroundColor="#666666" zPosition="1" />
	<ePixmap position="1410,750" size="320,232" zPosition="0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film2.png" transparent="1" alphatest="blend" />

	<widget name="statussearchold" foregroundColor="#0000ff00" font="Regular; 35" position="520,470" size="400,300" transparent="1" zPosition="3" halign="center" valign="center" 		backgroundColor="#3a3998"  />


    <eLabel name="" position="1800,1000" size="80,50" text="12" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" transparent="0" />

</screen>""".format(skinColor)


xtra_1080_2 = """
<screen name="xtra" position="0,0" size="1920,1080" title="xtraEvent..." flags="wfNoBorder">
	<ePixmap position="0,0" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_fhd3.png" transparent="1" />
	<widget source="Title" render="Label" position="60,53" size="1118,60" font="xtraRegular; 45" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
	
	<widget name="config" position="60,143" size="1118,765" itemHeight="45" font="xtraRegular;34" 
	foregroundColor="#c5c5c5" foregroundColorSelected="#ffffff" 
	backgroundColor="#23262e" backgroundColorSelected="#0d71aa" 
	selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/sel_xtra_fhd3.png" 
	  
	transparent="1" />
	
	<widget source="help" position="1260,850" size="600,60" render="Label" font="xtraRegular;28" foregroundColor="#f3fc92" backgroundColor="#23262e" halign="left" valign="center" transparent="1" />
	<widget name="status" position="1260,450" size="600,45" transparent="1" font="xtraRegular;30" foregroundColor="#92f1fc" backgroundColor="#23262e" />
	<widget name="info" position="1260,495" size="600,390" transparent="1" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" halign="left" valign="top" />
	<widget name="int_statu" position="1819,55" size="40,40" transparent="1" text="●" font="xtraRegular; 36" foregroundColor="#1edb76" backgroundColor="#23262e" zPosition="2" halign="center" />
	<widget source="key_red" render="Label" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="68,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="353,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="638,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="923,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="global.CurrentTime" render="Label" position="1259,60" size="600,45" font="xtraRegular; 38" valign="center" halign="center" transparent="1" foregroundColor="#c5c5c5" backgroundColor="#23262e" zPosition="1">
		<convert type="ClockToText">Default</convert>
	</widget>
	<eLabel name="" text=" MENU" position="1235,960" size="150,45" transparent="1" halign="center" font="xtraRegular; 30" />
	<eLabel name="" text=" INFO" position="1735,960" size="150,45" transparent="1" halign="center" font="xtraRegular; 30" />
   
    <eLabel name="" position="1800,1000" size="50,50" text="13" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />


</screen>"""

download_1080_2 = """
<screen name="downloads" position="0,0" size="1920,1080" title="downloads..." flags="wfNoBorder" backgroundColor="transparent">
	<ePixmap position="0,0" size="1920,1080" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_fhd3.png" zPosition="-1" transparent="1" />
	<widget source="Title" render="Label" position="60,53" size="1118,60" font="xtraRegular; 45" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
	<widget name="progress" position="60,148" size="1100,20" foregroundColor="#ffffff" borderColor="#ffffff" borderWidth="1" backgroundColor="#23262e" />
	<widget name="status" position="60,190" size="1100,44" transparent="1" font="xtraRegular;30" foregroundColor="#92f1fc" backgroundColor="#23262e" />
	<widget name="info" position="60,270" size="1100,44" transparent="1" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" valign="top" />
	<widget name="info2" position="60,350" size="1100,600" transparent="1" font="xtraRegular; 33" foregroundColor="#ffffff" backgroundColor="#23262e" />
	<widget source="key_red" render="Label" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="68,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="353,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="638,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular; 30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="923,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="global.CurrentTime" render="Label" position="1259,60" size="600,45" font="xtraRegular; 38" transparent="1" foregroundColor="#c5c5c5" backgroundColor="#23262e" zPosition="2">
		<convert type="ClockToText">Default</convert>
	</widget>
   
    <eLabel name="" position="1800,1000" size="50,50" text="14" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />


</screen>"""

manuel_1080_2 = """
<screen name="manuelSearch" position="center,center" size="1920,1080" title="Manuel Search..." backgroundColor="#000000" flags="wfNoBorder">
	<ePixmap position="0,0" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_fhd3.png" transparent="1" />
	<widget source="Title" render="Label" position="60,60" size="1118,60" font="xtraRegular; 45" foregroundColor="#ffffff" backgroundColor="#23262e" transparent="1" />
	<widget source="session.CurrentService" render="Label" position="60,120" size="957,60" zPosition="2" font="xtraRegular; 45" transparent="1" backgroundColor="#23262e" valign="center">
		<convert type="ServiceName">Name</convert>
	</widget>
	
	<widget name="config" position="60,225" size="1118,588" itemHeight="45" font="xtraRegular;34"
	foregroundColor="#c5c5c5" foregroundColorSelected="#ffffff" 
	backgroundColor="#23262e" backgroundColorSelected="#0d71aa" 
	selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/sel_xtra_fhd3.png" 
	scrollbarMode="showOnDemand" scrollbarSliderBorderWidth="0" scrollbarWidth="3" scrollbarSliderForegroundColor="#0d71aa"  
	transparent="1" />
	
	<widget name="status" position="60,885" size="1118,40" transparent="1" font="xtraRegular;36" foregroundColor="#92f1fc" backgroundColor="#23262e" />
	<widget name="info" position="1270,960" size="600,45" transparent="1" font="xtraRegular;30" halign="center" foregroundColor="#ffffff" backgroundColor="#23262e" />
	<widget name="Picture" position="1260,480" size="278,417" zPosition="5" transparent="1" />
	<widget name="progress" position="60,840" size="1118,20" foregroundColor="#ffffff" borderColor="#ffffff" borderWidth="1"  backgroundColor="#23262e" />
	<widget source="key_red" render="Label" font="xtraRegular;30" foregroundColor="#ffffff" backgroundColor="#23262e" position="70,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;30" foregroundColor="#ffffff" backgroundColor="#23262e" position="355,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;30" foregroundColor="#ffffff" backgroundColor="#23262e" position="640,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular;30" foregroundColor="#ffffff" backgroundColor="#23262e" position="925,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<eLabel name="" position="60,180" size="1118, 2" backgroundColor="#898989" />
   
    <eLabel name="" position="1800,1000" size="50,50" text="15" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />


</screen>"""

selbuq_1080_2 = """
<screen name="selBouquets" position="center,center" size="1920,1080" title="xtraEvent v1" backgroundColor="#ffffff">
	<ePixmap position="0,0" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/xtra_fhd3.png" transparent="1" />
	<widget source="Title" render="Label" position="60,53" size="1118,60" font="xtraRegular; 45" foregroundColor="#c5c5c5" backgroundColor="#23262e" transparent="1" />
	
	<widget name="list" position="60,143" size="1118,765" itemHeight="45" font="xtraRegular;36" 
	foregroundColor="#c5c5c5" foregroundColorSelected="#ffffff" 
	backgroundColor="#23262e" backgroundColorSelected="#0d71aa" 
	scrollbarMode="showOnDemand" scrollbarSliderBorderWidth="0" scrollbarWidth="3" scrollbarSliderForegroundColor="#0d71aa" 
	selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/sel_xtra_fhd3.png" 
	transparent="1" />
	
	<widget name="status" position="1260,450" size="600,45" transparent="1" font="xtraRegular;30" foregroundColor="#92f1fc" backgroundColor="#23262e" />
	<widget name="info" position="1260,495" size="600,405" transparent="1" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" halign="left" valign="top" />
	<widget source="key_red" render="Label" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="70,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_green" render="Label" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="355,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_yellow" render="Label" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="640,960" size="255,45" halign="left" transparent="1" zPosition="1" />
	<widget source="key_blue" render="Label" font="xtraRegular;30" foregroundColor="#c5c5c5" backgroundColor="#23262e" position="925,960" size="255,45" halign="left" transparent="1" zPosition="1" />
  
    <eLabel name="" position="1800,1000" size="50,50" text="16" font="Regular; 35" halign="left" backgroundColor="#00000000" foregroundColor="#0000ff00" />


</screen>"""




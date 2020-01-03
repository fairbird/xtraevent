*********************************
POSTER
*********************************

v1.1 : poster folder(/media/hdd/poster) is deleted when it reaches 10mb
you can change this value as you like...

v1.1a : poster folder(/tmp/poster/poster.jpg) in tmp...just one poster...


for,
infobar, SecondInfoBar : source="session.Event_Now"
						 source="session.Event_Next"	
ChannelSelection       : source="ServiceEvent"

<widget render="pstrRndr" source="session.Event_Now" path="poster" position="5,60" size="185,278" backgroundColor="tb" zPosition="1" transparent="0">
	<convert type="pstrCnvrt">POSTER</convert>
</widget>

pstrCnvrt.py 
/usr/lib/enigma2/python/Components/Converter

pstrRndr.py 
/usr/lib/enigma2/python/Components/Renderer

##################

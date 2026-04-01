import gettext
# Set up translation function
_ = gettext.gettext

maintype = [
	_('Reserved'),
	_('Movie/Drama'),
	_('News/Current Affairs'),
	_('Show/Game Show'),
	_('Sports'),
	_('Children/Youth Programs'),
	_('Music/Ballet/Dance'),
	_('Arts/Culture'),
	_('Social/Political/Economics'),
	_('Education/Science/Factual Topics'),
	_('Leisure/Hobbies'),
	_('Other')
]

subtype = {}
subtype[1] = [
	_('Movie'), _('Detective/Thriller'), _('Adventure/Western/War'),
	_('Science Fiction/Fantasy/Horror'), _('Comedy'), _('Soap/Melodrama/Folkloric'),
	_('Romance'), _('Serious/Classical/Religious/Historical Drama'), _('Adult')
]
subtype[2] = [
	_('General News'), _('Weather Report'), _('Magazine'), _('Documentary'),
	_('Discussion/Interview/Debate')
]
subtype[3] = [
	_('Game Show/Quiz/Contest'), _('Variety Show'), _('Talk Show')
]
subtype[4] = [
	_('Sports News'), _('Special Event'), _('Sports Magazine'),
	_('Football/Soccer'), _('Tennis/Squash'), _('Team Sports'),
	_('Athletics'), _('Motor Sports'), _('Water Sports'),
	_('Winter Sports'), _('Equestrian'), _('Martial Sports')
]
subtype[5] = [
	_('Pre-School Children'), _('Older Children (6-14)'), _('Youth (10-16)'),
	_('Children\'s Entertainment'), _('Cartoons/Animations')
]
subtype[6] = [
	_('Rock/Pop'), _('Classical Music'), _('Folk/Traditional Music'),
	_('Jazz'), _('Musical/Opera'), _('Ballet')
]
subtype[7] = [
	_('Performing Arts'), _('Fine Arts'), _('Religion'),
	_('Popular Culture/Tradition'), _('Literature'), _('Cinema/Film'),
	_('Experimental Film/Video'), _('Press'), _('New Media'),
	_('Cultural Magazines'), _('Fashion')
]
subtype[8] = [
	_('Politics'), _('Business/Financial'), _('People/Society')
]
subtype[9] = [
	_('Nature/Animals/Environment'), _('Technology'), _('Medicine/Physiology/Psychology'),
	_('Expeditions/Adventure'), _('Social Sciences'), _('Further Education'),
	_('Languages')
]
subtype[10] = [
	_('Tourism/Travel'), _('Handicraft'), _('Motoring'),
	_('Fitness/Health'), _('Cooking'), _('Shopping'), _('Gardening')
]
subtype[11] = [
	_('Original Language'), _('Black & White'), _('Unpublished'),
	_('Live Broadcast'), _('Reality TV'), _('Esports'),
	_('True Crime'), _('Anime')
]


def getGenreStringMain(hn, ln):
	if hn == 15:
		return _('User defined')
	if 0 < hn < len(maintype):
		return maintype[hn]
	return ''


def getGenreStringSub(hn, ln):
	if 0 < hn < len(maintype):
		if ln < len(subtype.get(hn, [])):
			return subtype[hn][ln]
	return ''

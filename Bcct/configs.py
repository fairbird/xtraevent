# -*- coding: utf-8 -*-
# by digiteng...01.2020

from Components.config import config, ConfigSubsection, ConfigSlider
from Components.ConfigList import ConfigListScreen



config.vset = ConfigSubsection()

config.vset.bright = ConfigSlider(default=128, increment=4, limits=(0,255))
config.vset.contrast = ConfigSlider(default=128, increment=4, limits=(0,255))
config.vset.color = ConfigSlider(default=128, increment=4, limits=(0,255))
config.vset.tint = ConfigSlider(default=128, increment=4, limits=(0,255))

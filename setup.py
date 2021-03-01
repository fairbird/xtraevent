#!/usr/bin/python
# -*- coding: utf-8 -*-
from distutils.core import setup

pkg = 'Extensions.xtraEvent'
setup(name='enigma2-plugin-extensions-xtraevent',
       version='1.3',
       description='Plugin to show extra events for enigma2 skins.',
       packages=[pkg],
       package_dir={pkg: 'usr'},
       package_data={pkg: ['plugin.png', '*/*.png']},
      )

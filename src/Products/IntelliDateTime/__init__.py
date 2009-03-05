# -*- coding: utf-8 -*-
#
# Copyright 2008, BDA - Blue Dynamics Alliance, Austria - www.bluedynamics.com
#
# GNU General Public Licence Version 2 or later - see LICENCE.GPL

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

import logging
logger = logging.getLogger('IntelliDateTime')
logger.info('Installing Product')

from widget import IntelliDateTimeWidget
from field import IntelliDateTimeField

from Products.CMFCore.DirectoryView import registerDirectory
from config import GLOBALS
registerDirectory('skins', GLOBALS)
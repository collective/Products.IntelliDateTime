# -*- coding: utf-8 -*-
#
# Copyright 2008, BDA - Blue Dynamics Alliance, Austria - www.bluedynamics.com
#
# GNU General Public Licence Version 2 or later - see LICENCE.GPL

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo

from Products.Archetypes.Widget import CalendarWidget

class IntelliDateTimeWidget(CalendarWidget):
    """Widget for IntelliDateTime input.
    """
    
    _properties = CalendarWidget._properties.copy()
    _properties.update({
        'macro' : "intellidatetime",
    })

    security = ClassSecurityInfo()
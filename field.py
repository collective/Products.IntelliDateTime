#
# Copyright 2008, BlueDynamics Alliance, Austria - http://bluedynamics.com
#
# GNU General Public Licence Version 2 or later

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from datetime import datetime
from DateTime import DateTime
from AccessControl import ClassSecurityInfo

from Products.Archetypes.Field import ObjectField
from Products.Archetypes.Field import DateTimeField

from widget import IntelliDateTimeWidget

class IntelliDateTimeField(DateTimeField):
    
    _properties = DateTimeField._properties.copy()
    _properties.update({
        'type': 'intellidatetime',
        'widget': IntelliDateTimeWidget,
    })

    security  = ClassSecurityInfo()
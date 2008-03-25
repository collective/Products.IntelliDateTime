# -*- coding: utf-8 -*-
#
# Copyright 2008, BDA - Blue Dynamics Alliance, Austria - www.bluedynamics.com
#
# GNU General Public Licence Version 2 or later - see LICENCE.GPL

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
    
    security.declarePrivate('validate_required')
    def validate_required(self, instance, value, errors):
        try:
            DateTime(value.isoformat())
        except Exception:
            result = False
        else:
            result = value is not None
        return ObjectField.validate_required(self, instance, result, errors)

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        if not value:
            value = None
        elif not isinstance(value, DateTime):
            try:
                value = DateTime(value.isoformat())
            except DateTime.DateTimeError:
                value = None

        ObjectField.set(self, instance, value, **kwargs)
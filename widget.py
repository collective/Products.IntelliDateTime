# -*- coding: utf-8 -*-
#
# Copyright 2008, BDA - Blue Dynamics Alliance, Austria - www.bluedynamics.com
#
# GNU General Public Licence Version 2 or later - see LICENCE.GPL

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from DateTime import DateTime
from AccessControl import ClassSecurityInfo

from Products.Archetypes.Widget import CalendarWidget

from bda.calendar.base.interfaces import ITimezoneFactory
from bda.intellidatetime import IIntelliDateTime
from bda.intellidatetime import DateTimeConversionError

class IntelliDateTimeWidget(CalendarWidget):
    """Widget for IntelliDateTime input.
    """
    
    _properties = CalendarWidget._properties.copy()
    _properties.update({
        'macro' : 'intellidatetime',
        'starting_year': 1900,
        'ending_year': 2100,
        'format': 'dd/mm/y', # TODO: strformat compatibility for the js
    })

    security = ClassSecurityInfo()
    
    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False):
        
        fieldname = field.getName()
        value = self._readDateTimeFromForm(instance, form, fieldname)
        
        if value is None and emptyReturnsMarker:
            value = empty_marker
        
        return value, {}
    
    def dateInputValue(self, instance, value, fieldname=None):
        value = self._readValue(instance, value, fieldname)
        if not value:
            return ''
        
        date = ''
        lastchar = None
        for char in self.format:
            if char != lastchar:
                if char == 'd':
                    lastchar = char
                    date += str(value.day()) + '.'
                    continue
                if char == 'm':
                    lastchar = char
                    date += str(value.month()) + '.'
                    continue
                if char == 'y':
                    lastchar = char
                    date += str(value.year()) + '.'
                    continue
        return date.strip('.')
    
    def timeInputValue(self, instance, value, fieldname=None):
        value = self._readValue(instance, value, fieldname)
        if not value:
            return ''
        
        if not value.hour and not value.minute:
            return ''
        
        formatted = '%02d:%02d' % (value.hour(), value.minute())
        return formatted
    
    def _readValue(self, instance, value, fieldname):
        if not value:
            if fieldname is not None:
                value = self._readDateTimeFromForm(instance, self.REQUEST.form, 
                                                   fieldname)
        return value
    
    def _readDateTimeFromForm(self, instance, form, fieldname):
        date = form.get('%s_date' % fieldname)
        time = form.get('%s_time' % fieldname)
        tzinfo = ITimezoneFactory(instance)
        try:
            value = IIntelliDateTime(self).convert(date, time=time, locale='de',
                                                   tzinfo=tzinfo)
            try:
                value = DateTime(value.isoformat())
            except DateTime.DateTimeError:
                value = None
        except DateTimeConversionError, e:
            value = None
        return value

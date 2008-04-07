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
        value = self._readDateTimeFromForm(form, fieldname)
        
        if value is None and emptyReturnsMarker:
            value = empty_marker
        
        return value, {}
    
    def dateInputValue(self, value, fieldname=None):
        value = self._readValue(value, fieldname)
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
    
    def timeInputValue(self, value, fieldname=None):
        value = self._readValue(value, fieldname)
        if not value:
            return ''
        
        hour = str(value.hour())
        minute = str(value.minute())
        if hour == '0' and minute == '0':
            return ''
        
        if len(hour) == 1:
            hour = '0%s' % hour
        if len(minute) == 1:
            minute = '0%s' % minute
        
        return '%s:%s' % (hour, minute)
    
    def _readValue(self, value, fieldname):
        if not value:
            if fieldname is not None:
                value = self._readDateTimeFromForm(self.REQUEST.form, fieldname)
        return value
    
    def _readDateTimeFromForm(self, form, fieldname):
        date = form.get('%s_date' % fieldname)
        time = form.get('%s_time' % fieldname)
        try:
            value = IIntelliDateTime(self).convert(date,
                                                   time=time,
                                                   locale='de')
            try:
                value = DateTime(value.isoformat())
            except DateTime.DateTimeError:
                value = None
        except DateTimeConversionError, e:
            value = None
        return value

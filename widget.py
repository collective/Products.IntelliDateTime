# -*- coding: utf-8 -*-
#
# Copyright 2008, BDA - Blue Dynamics Alliance, Austria - www.bluedynamics.com
#
# GNU General Public Licence Version 2 or later - see LICENCE.GPL

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

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
        date = form.get('%s_date' % fieldname)
        time = form.get('%s_time' % fieldname)
        
        try:
            value = IIntelliDateTime(self).convert(date,
                                                   time=time,
                                                   locale='de')
        except DateTimeConversionError, e:
            print e
            if emptyReturnsMarker and not date:
                value = empty_marker
            else:
                value = None
        
        return value, {}
    
    def dateInputValue(self, value):
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
    
    def timeInputValue(self, value):
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

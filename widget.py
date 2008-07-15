#
# Copyright 2008, BlueDynamics Alliance, Austria - http://bluedynamics.com
#
# GNU General Public Licence Version 2 or later

__author__ = """Robert Niederreiter <rnix@squarewave.at>
                Jens Klein <jens@bluedynamics.com>"""
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
    del _properties['helper_js']

    security = ClassSecurityInfo()
    
    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        
        fieldname = field.getName()        
        
        # check if field is there!
        testvalue = form.get('%s_date' % fieldname, empty_marker)
        if testvalue is empty_marker:
            return empty_marker
        
        # if its there we can read
        value = self._readDateTimeFromForm(instance, form, fieldname)
        if value is None and empty_marker:
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
        submitted = self.REQUEST.form.get('submitted')
        if fieldname is None:
            return value
        formvalue = self._readDateTimeFromForm(instance, self.REQUEST.form, 
                                               fieldname)
        if formvalue or (not formvalue and value and submitted):
            return formvalue
        return value
    
    def _readDateTimeFromForm(self, instance, form, fieldname):
        date = form.get('%s_date' % fieldname)
        time = form.get('%s_time' % fieldname)
        tzinfo = ITimezoneFactory(instance)
        try:
            value = IIntelliDateTime(self).convert(date, time=time, locale='de',
                                                   tzinfo=tzinfo)
        except DateTimeConversionError, e:
            return None
        # correct DST, dont add one hour!
        value = value.replace(tzinfo=tzinfo.normalize(value).tzinfo)
        try:
            value = DateTime(value.isoformat())
        except DateTime.DateTimeError:
            return None
        return value

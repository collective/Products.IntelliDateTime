Changes for IntelliDateTime
===========================

dev (unreleased)
----------------

- Plone4.3 compatibility by adding popup_calendar.gif to skin directory of this
  product [2014-12-05 fRiSi]


1.3.2 (2010/01/26)
------------------

- adjust the output datetime for the widget to the users timezone using
  ITimeZone
  [2009-04-27 jensens]

- removed the additional calendar javascripts added in
  http://dev.plone.org/archetypes/changeset/10556 since they broke the
  popup

  at least in plone4 loading calendar.js in addition to calendar_stripped.js
  (which is loaded as helper.js by the calendarwidget) results in
  recursion errors and the date picked in the popup is not written to the input fields.

  [2010-01-26 fRiSi]

1.3.1
-----

- correct show_hm condition for datetime.datetime rendering
  [2009-04-15 rnix]

1.3
---

- view macro - render datetime.datetime properly
  [2009-04-15 rnix]

- remove view_later macro
  [2009-04-15 rnix]

1.2
---

- overwrite validate_required in field.py
  [2009-03-01 jensens]

- remove wrong condition in widget.py
  [2009-03-01 jensens]

1.1
---

- eggified
  [2009-03-05 rnix]

1.0
---

- widget now can return zope DateTime or python datetime
  [Jensens]

- widget now displays time input only if ``show_hm`` is set to ``True``
  (as does CalendarWidget)
  [2008-07-28 fRiSi]

- locale for parsing the date in bda.indellidatetime.converter is obtained
  from the site_property `default_language`
  (widged was simply using 'de' before)
  this might break your testcases since for a default plone site the english dateformat is
  expected. you need to set the default language in your testsuite's `setUp` method to fix this.
  [2008-09-12 fRiSi]
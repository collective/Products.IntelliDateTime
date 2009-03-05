from zope import interface

class ILocaleFactory(interface.Interface):
    """callable that returns the locale that shall be used for date parsing.
    it must be one if the locales defined in bda.indellidatetime.converter.
    """
    
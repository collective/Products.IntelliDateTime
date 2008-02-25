# -*- coding: utf-8 -*-
#
# Copyright 2008, BDA - Blue Dynamics Alliance, Austria - www.bluedynamics.com
#
# GNU General Public Licence Version 2 or later - see LICENCE.GPL

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from StringIO import StringIO
from Products.Archetypes.Extensions.utils import install_subskin
from Products.UserAndGroupSelectionWidget.config import PROJECTNAME, GLOBALS
        
def install(self):
    out = StringIO()
    install_subskin(self, out, GLOBALS)
    out.write("Successfully installed %s." % PROJECTNAME)
    return out.getvalue()

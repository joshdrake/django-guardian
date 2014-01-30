"""
Implementation of per object permissions for Django 1.2 or later.
"""
from __future__ import unicode_literals

VERSION = (1, 2, 0)

__version__ = '.'.join((str(each) for each in VERSION[:4]))
default_app_config = 'guardian.apps.GuardianConfig'

def get_version():
    """
    Returns shorter version (digit parts only) as string.
    """
    return '.'.join((str(each) for each in VERSION[:4]))

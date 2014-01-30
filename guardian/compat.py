from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AnonymousUser
from django.db.models import get_model


try:
    from django.conf.urls import url, patterns, include, handler404, handler500
except ImportError:
    from django.conf.urls.defaults import url, patterns, include, handler404, handler500 # pyflakes:ignore

__all__ = [
    'User',
    'Group',
    'Permission',
    'AnonymousUser',
    'get_user_model',
    'user_model_label',
    'url',
    'patterns',
    'include',
    'handler404',
    'handler500',
    'mock',
    'unittest',
]

try:
    import unittest2 as unittest
except ImportError:
    import unittest  # pyflakes:ignore
try:
    from unittest import mock  # Since Python 3.3 mock is is in stdlib
except ImportError:
    import mock # pyflakes:ignore

# Django 1.5 compatibility utilities, providing support for custom User models.
# Since get_user_model() causes a circular import if called when app models are
# being loaded, the user_model_label should be used when possible, with calls
# to get_user_model deferred to execution time

user_model_label = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User

def get_user_model_path():
    """
    Returns 'app_label.ModelName' for User model. Basically if
    ``AUTH_USER_MODEL`` is set at settings it would be returned, otherwise
    ``auth.User`` is returned.
    """
    return getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

def get_user_permission_full_codename(perm):
    """
    Returns 'app_label.<perm>_<usermodulename>'. If standard ``auth.User`` is
    used, for 'change' perm this would return ``auth.change_user`` and if
    ``myapp.CustomUser`` is used it would return ``myapp.change_customuser``.
    """
    User = get_user_model()
    return '%s.%s_%s' % (User._meta.app_label, perm, User._meta.module_name)

def get_user_permission_codename(perm):
    """
    Returns '<perm>_<usermodulename>'. If standard ``auth.User`` is
    used, for 'change' perm this would return ``change_user`` and if
    ``myapp.CustomUser`` is used it would return ``change_customuser``.
    """
    return get_user_permission_full_codename(perm).split('.')[1]

# Django 1.7 compatibility utilities
# initialization code that accesses models at import-time should be moved in to the ``ready`` method of an ``django.apps.AppConfig`` instance

def setup_prototype_methods(app_config=None):
    """
    Sets up prototype methods on ``auth.User`` and ``auth.Group``.
    Optionally takes an ``django.apps.AppConfig`` instance for 1.7+ compatibility; otherwise
    falls back to ``get_model``. This function should be invoked in the ``ready`` method of a
    ``django.apps.AppConfig`` instance in Django 1.7+, and cautiously at import-time otherwise.
    """
    from guardian.utils import get_anonymous_user # avoid circular import
    User = get_user_model()

    if app_config is None:
        UserObjectPermission = get_model('guardian', 'UserObjectPermission')
        GroupObjectPermission = get_model('guardian', 'GroupObjectPermission')
    else:
        UserObjectPermission = app_config.get_model('UserObjectPermission')
        GroupObjectPermission = app_config.get_model('GroupObjectPermission')

    # Prototype User and Group methods
    setattr(User, 'get_anonymous', staticmethod(lambda: get_anonymous_user()))
    setattr(User, 'add_obj_perm',
        lambda self, perm, obj: UserObjectPermission.objects.assign_perm(perm, self, obj))
    setattr(User, 'del_obj_perm',
        lambda self, perm, obj: UserObjectPermission.objects.remove_perm(perm, self, obj))

    setattr(Group, 'add_obj_perm',
        lambda self, perm, obj: GroupObjectPermission.objects.assign_perm(perm, self, obj))
    setattr(Group, 'del_obj_perm',
        lambda self, perm, obj: GroupObjectPermission.objects.remove_perm(perm, self, obj))

# Python 3
try:
    unicode = unicode # pyflakes:ignore
    basestring = basestring # pyflakes:ignore
    str = str # pyflakes:ignore
except NameError:
    basestring = unicode = str = str

__all__ = ['User', 'Group', 'Permission', 'AnonymousUser']

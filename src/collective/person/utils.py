# -*- coding:utf-8 -*-
from datetime import datetime
from DateTime import DateTime

from zope.interface import Invalid

from collective.person import MessageFactory as _


def check_birthday(value):
    ''' Validate that a birthday must be a datetime or a DateTime in
        the past

        >>> check_birthday(DateTime('1969/7/21'))
        True

        >>> check_birthday(datetime(1969,7,21))
        True

        >>> try:
        ...     check_birthday(DateTime('2063/4/5'))
        ... except Invalid:
        ...     print 'Invalid Date'
        Invalid Date

        >>> try:
        ...     check_birthday(datetime(2063,4,5))
        ... except Invalid:
        ...     print 'Invalid Date'
        Invalid Date

        >>> try:
        ...     check_birthday('1999/12/31')
        ... except ValueError:
        ...     print 'Invalid Date'
        Invalid Date

    '''
    now = datetime.now()
    if isinstance(value, DateTime):
        value = value.asdatetime()

    if not isinstance(value, datetime):
        raise ValueError

    # Is in the past?
    delta = (now - value)
    delta_seconds = (delta.days * 86400) + delta.seconds
    if not delta_seconds > 0:
        raise Invalid(_(u"Birthday must be a date in the past."))
    else:
        return True

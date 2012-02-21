# -*- coding:utf-8 -*-
from datetime import date
from datetime import datetime
from DateTime import DateTime

from zope.interface import Invalid

from collective.person import MessageFactory as _


def check_birthday(value):
    ''' Validate that a birthday must be a date,
        datetime or a DateTime in the past

        >>> check_birthday(DateTime('1969/7/21'))
        True

        >>> check_birthday(datetime(1969,7,21))
        True

        >>> check_birthday(date(1969,7,21))
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
        ...     check_birthday(date(2063,4,5))
        ... except Invalid:
        ...     print 'Invalid Date'
        Invalid Date

        >>> try:
        ...     check_birthday('1999/12/31')
        ... except ValueError:
        ...     print 'Invalid Date'
        Invalid Date

    '''
    now = datetime.now().date()
    if isinstance(value, DateTime):
        value = value.asdatetime()

    if isinstance(value, datetime):
        value = value.date()

    if not isinstance(value, date):
        raise ValueError

    # Is in the past?
    delta = (now - value)
    if not delta > 0:
        raise Invalid(_(u"Birthday must be a date in the past."))
    else:
        return True

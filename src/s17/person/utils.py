# -*- coding:utf-8 -*-
import re
from string import digits
from datetime import date
from datetime import datetime
from DateTime import DateTime

from zope.interface import Invalid

from Products.validation import validation

from s17.person import MessageFactory as _


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
    if not delta.days > 0:
        raise Invalid(_(u"Birthday must be a date in the past."))
    else:
        return True


def validate_email(value):
    ''' Validate email using Products.validation

        >>> validate_email('foo@bar.org') == 1
        True

        >>> validate_email('foo@bar.com') == 1
        True

        >>> validate_email('+@bar.com') == 1
        True

        >>> validate_email('1@ee.br') == 1
        True

        >>> try:
        ...     validate_email('@bar.com')
        ... except Invalid:
        ...     print 'Invalid email'
        Invalid email

    '''
    v = validation.validatorFor('isEmail')
    if v(str(value)) == 1:
        return True
    else:
        raise Invalid(_(u"The informed email is invalid."))


def validate_telephone(value):
    ''' Validate a phone number

        >>> validate_telephone('+551138982121')
        True

        >>> validate_telephone('+55(11)3898.2121')
        True

        >>> validate_telephone('+55-11-3898-2121')
        True

        >>> try:
        ...     validate_telephone('+55-11-3898-SIMP')
        ... except Invalid:
        ...     print 'Invalid phone'
        Invalid phone

        >>> try:
        ...     validate_telephone('11-3898-2121')
        ... except Invalid:
        ...     print 'Invalid phone'
        Invalid phone

    '''
    valid = digits + '+'
    value = ''.join([c for c in value if c in valid])
    pattern = re.compile('\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[854321]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{7,14}$')

    if re.match(pattern, value):
        return True
    else:
        raise Invalid(_(u"The informed phone number is invalid."))

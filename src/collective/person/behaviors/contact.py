# -*- coding:utf-8 -*-
from zope import schema

from zope.annotation.interfaces import IAnnotations

from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
from zope.interface import invariant
from zope.interface import Invalid

from plone.directives import form

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow

from collective.person.content.person import IPerson

from collective.person.utils import validate_email
from collective.person.utils import validate_telephone

from collective.person import MessageFactory as _


item_options = SimpleVocabulary(
    [SimpleTerm(value=u'work', title=_(u'Work')),
     SimpleTerm(value=u'home', title=_(u'Home'))])


im_options = SimpleVocabulary(
    [SimpleTerm(value=u'aim', title=_(u'AIM')),
     SimpleTerm(value=u'facebook', title=_(u'Facebook')),
     SimpleTerm(value=u'gadu-gadu', title=_(u'Gadu-Gadu')),
     SimpleTerm(value=u'gtalk', title=_(u'Google Talk')),
     SimpleTerm(value=u'icq', title=_(u'ICQ')),
     SimpleTerm(value=u'jabber', title=_(u'Jabber')),
     SimpleTerm(value=u'msn', title=_(u'MSN')),
     SimpleTerm(value=u'skype', title=_(u'Skype')),
     SimpleTerm(value=u'yahoo', title=_(u'Yahoo'))])


class InvalidInformation(Invalid):
    __doc__ = _(u"Please fix the provided information.")


class IContactItem(Interface):
    ''' An item in a list of contact information '''

    category = schema.Choice(
        title=u"Category",
        source=item_options,
        required=True)

    data = schema.TextLine(
        title=_(u"Value"),
        required=True)


class IIMItem(Interface):
    ''' An item in a list of instant messengers '''

    category = schema.Choice(
        title=u"Category",
        source=im_options,
        required=True)


class IContactInfo(form.Schema):
    '''Behavior providing contact info for an IPerson
    '''

    form.widget(emails=DataGridFieldFactory)
    emails = schema.List(
            title=_(u'E-mails'),
            description=_(u'Please inform emails for this person.'),
            required=False,
            value_type=DictRow(title=_(u'E-mails'),
                               schema=IContactItem),
            default=[],
        )

    form.widget(instant_messengers=DataGridFieldFactory)
    instant_messengers = schema.List(
            title=_(u'Instant Messengers'),
            description=_(u'Instant messangers for this person.'),
            value_type=DictRow(title=_(u'Instant Messengers'),
                               schema=IIMItem),
            required=False,
        )

    form.widget(telephones=DataGridFieldFactory)
    telephones = schema.List(
            title=_(u'Telephones'),
            description=_(u'Please inform telephones for this person.'),
            required=False,
            value_type=DictRow(title=_(u'Telephones'),
                               schema=IContactItem),
            default=[],
        )

    @invariant
    def validate_emails(data):
        ''' Validate provided emails '''
        emails = data.emails
        if emails:
            for line in emails:
                email = line.get('data', '')
                if email and not validate_email(email):
                    return InvalidInformation(_(u'Invalid E-mail'))

    @invariant
    def validate_instant_messengers(data):
        ''' Validate provided instant messengers '''
        pass

    @invariant
    def validate_telephones(data):
        ''' Validate provided telephones '''
        telephones = data.telephones
        if telephones:
            for line in telephones:
                phone = line.get('data', '')
                if phone and not validate_telephone(phone):
                    return InvalidInformation(_(u'Invalid Phone Number'))


alsoProvides(IContactInfo, form.IFormFieldProvider)


class ContactInfo(object):
    ''' adapter for IContactInfo '''

    implements(IContactInfo)
    adapts(IPerson)

    def __init__(self, context):
        self.context = context
        self.annotation = IAnnotations(self.context)

    @property
    def emails(self):
        return self.annotation.get('collective.person.emails', [])

    @emails.setter
    def emails(self, value):
        self.annotation['collective.person.emails'] = value

    @property
    def instant_messengers(self):
        return self.annotation.get('collective.person.instant_messengers', [])

    @instant_messengers.setter
    def instant_messengers(self, value):
        self.annotation['collective.person.instant_messengers'] = value

    @property
    def telephones(self):
        return self.annotation.get('collective.person.telephones', [])

    @telephones.setter
    def telephones(self, value):
        self.annotation['collective.person.telephones'] = value

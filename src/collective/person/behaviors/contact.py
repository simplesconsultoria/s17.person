# -*- coding:utf-8 -*-
from zope import schema

from zope.annotation.interfaces import IAnnotations

from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements

from plone.directives import form

from collective.person.content.person import IPerson

from collective.person import MessageFactory as _


class IContactInfo(form.Schema):
    '''Behavior providing contact info for an IPerson
    '''

    emails = schema.List(
            title=_(u'E-mails'),
            description=_(u'Please inform emails for this person.'),
            required=False,
        )

    instant_messengers = schema.List(
            title=_(u'Instant Messengers'),
            description=_(u'Instant messangers for this person.'),
            required=False,
        )

    telephones = schema.List(
            title=_(u'Telephones'),
            description=_(u'Please inform telephones for this person.'),
            required=False,
        )


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
